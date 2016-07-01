from django.views import generic

from .mixins import ModelViewMixin


class UpdateModelView(ModelViewMixin, generic.UpdateView):
    template_name_suffix = '_update'
