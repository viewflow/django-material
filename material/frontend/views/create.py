from django.views import generic

from .mixins import ModelViewMixin


class CreateModelView(ModelViewMixin, generic.CreateView):
    template_name_suffix = '_create'
