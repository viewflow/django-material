from django.views import generic

from .mixins import ModelViewMixin


class CreateModelView(ModelViewMixin, generic.CreateView):
    template_name_suffix = '_create'

    def has_object_permission(self, request, obj):
        if self.viewset is not None:
            return self.viewset.has_add_permission(request, obj)
        raise NotImplementedError('Viewset is not provided')
