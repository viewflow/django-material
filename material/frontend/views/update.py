from django.views import generic

from .mixins import ModelViewMixin


class UpdateModelView(ModelViewMixin, generic.UpdateView):
    template_name_suffix = '_update'

    def has_object_permission(self, request, obj):
        if self.viewset is not None:
            return self.viewset.has_change_permission(request, obj)
        raise NotImplementedError('Viewset is not provided')
