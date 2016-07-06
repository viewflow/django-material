from django.core.urlresolvers import reverse
from django.db import router
from django.db.models.deletion import Collector
from django.core.exceptions import PermissionDenied
from django.views import generic


class DeleteModelView(generic.DeleteView):
    viewset = None

    def has_object_permission(self, request, obj):
        if self.viewset is not None:
            return self.viewset.has_delete_permission(request, obj)
        raise NotImplementedError('Viewset is not provided')

    def get_deleted_objects(self):
        collector = Collector(using=router.db_for_write(self.object))
        collector.collect([self.object])
        return collector.data

    def get_context_data(self, **kwargs):
        kwargs['deleted_objects'] = self.get_deleted_objects()
        return super(DeleteModelView, self).get_context_data(**kwargs)

    def get_object(self):
        obj = super(DeleteModelView, self).get_object()
        if not self.has_object_permission(self.request, obj):
            raise PermissionDenied
        return obj

    def get_success_url(self):
        if self.success_url is None:
            opts = self.model._meta
            return reverse('{}:{}_list'.format(opts.app_label, opts.model_name))
        return super(DeleteModelView, self).get_success_url()

    def get_template_names(self):
        if self.template_name is None:
            opts = self.model._meta
            return [
                '{}/{}{}.html'.format(opts.app_label, opts.model_name, self.template_name_suffix),
                'material/frontend/views/confirm_delete.html',
            ]

        return [self.template_name]
