from django_filters import FilterSet, ModelChoiceFilter
from .models import Ocean, Sea


class SeaFilterSet(FilterSet):
    parent = ModelChoiceFilter(
        queryset=Sea.objects.filter(pk__in=Sea.objects.filter(parent__isnull=False).values('parent')))
    ocean = ModelChoiceFilter(queryset=Ocean.objects.all(), help_text='')
