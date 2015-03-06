import datetime

from django.contrib.admin.views.main import PAGE_VAR
from django.db import models
from django.utils import formats
from django.utils.dates import MONTHS
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.template import Library

from material import Layout, Fieldset, Row


register = Library()


@register.assignment_tag
def fieldset_layout(adminform):
    sets = []
    for fieldset in adminform:
        fields = []
        for field in fieldset.fields:
            if isinstance(field, (list, tuple)):
                fields.append(Row(*field))
            else:
                fields.append(field)

        sets.append(Fieldset(fieldset.name, *fields))

    return Layout(*sets)


@register.simple_tag
def paginator_number(cl, i):
    """
    Generates an individual page index link in a paginated list.
    """
    current_page = cl.paginator.page(cl.page_num+1)
    if i == 'prev':
        if current_page.has_previous():
            return format_html('<li class="disabled"><a href="{}"><i class="mdi-navigation-chevron-left"></i></a></li>',
                               cl.get_query_string({PAGE_VAR: current_page.previous_page_number()}))
        else:
            return format_html('<li class="disabled"><a href="#!"><i class="mdi-navigation-chevron-left"></i></a></li>')
    elif i == 'next':
        if current_page.has_next():
            return format_html('<li class="disabled"><a href="{}"><i class="mdi-navigation-chevron-right"></i></a></li>',
                               cl.get_query_string({PAGE_VAR: current_page.next_page_number()}))
        else:
            return format_html('<li class="disabled"><a href="#!"><i class="mdi-navigation-chevron-right"></i></a></li>')
    elif i == '.':
        return '<li class="disabled"><a href="#" onclick="return false;">...</a></li>'
    elif i == cl.page_num:
        return format_html('<li class="active"><a href="{0}">{0}</a></li> ',
                           i+1,
                           cl.get_query_string({PAGE_VAR: i}))
    else:
        return format_html('<li><a href="{0}"{1}>{2}</a></li>',
                           cl.get_query_string({PAGE_VAR: i}),
                           mark_safe(' class="end"' if i == cl.paginator.num_pages - 1 else ''),
                           i + 1)


@register.inclusion_tag('admin/date_hierarchy.html')
def date_hierarchy(cl):
    """
    Displays the date hierarchy for date drill-down functionality.
    """
    if cl.date_hierarchy:
        field_name = cl.date_hierarchy
        field = cl.opts.get_field_by_name(field_name)[0]
        dates_or_datetimes = 'datetimes' if isinstance(field, models.DateTimeField) else 'dates'
        year_field = '%s__year' % field_name
        month_field = '%s__month' % field_name
        day_field = '%s__day' % field_name
        field_generic = '%s__' % field_name
        year_lookup = cl.params.get(year_field)
        month_lookup = cl.params.get(month_field)
        day_lookup = cl.params.get(day_field)

        link = lambda filters: cl.get_query_string(filters, [field_generic])

        if not (year_lookup or month_lookup or day_lookup):
            # select appropriate start level
            date_range = cl.queryset.aggregate(first=models.Min(field_name),
                                               last=models.Max(field_name))
            if date_range['first'] and date_range['last']:
                if date_range['first'].year == date_range['last'].year:
                    year_lookup = date_range['first'].year
                    if date_range['first'].month == date_range['last'].month:
                        month_lookup = date_range['first'].month
        if year_lookup and month_lookup and day_lookup:
            day = datetime.date(int(year_lookup), int(month_lookup), int(day_lookup))
            return {
                'field_name': field.verbose_name,
                'show': True,
                'back': {
                    'link': link({year_field: year_lookup, month_field: month_lookup}),
                    'title': capfirst(formats.date_format(day, 'YEAR_MONTH_FORMAT'))
                },
                'choices': [{'title': capfirst(formats.date_format(day, 'MONTH_DAY_FORMAT'))}]
            }
        elif year_lookup and month_lookup:
            days = cl.queryset.filter(**{year_field: year_lookup, month_field: month_lookup})
            days = getattr(days, dates_or_datetimes)(field_name, 'day')
            return {
                'show': True,
                'field_name': field.verbose_name,
                'current_filter': capfirst(MONTHS.get(int(month_lookup), 'UNKNOWN')),
                'back': {
                    'link': link({year_field: year_lookup}),
                    'title': str(year_lookup)
                },
                'choices': [{
                    'link': link({year_field: year_lookup, month_field: month_lookup, day_field: day.day}),
                    'title': capfirst(formats.date_format(day, 'MONTH_DAY_FORMAT'))
                } for day in days]
            }
        elif year_lookup:
            months = cl.queryset.filter(**{year_field: year_lookup})
            months = getattr(months, dates_or_datetimes)(field_name, 'month')
            return {
                'show': True,
                'field_name': field.verbose_name,
                'current_filter': year_lookup,
                'back': {
                    'link': link({}),
                    'title': _('All dates')
                },
                'choices': [{
                    'link': link({year_field: year_lookup, month_field: month.month}),
                    'title': capfirst(formats.date_format(month, 'YEAR_MONTH_FORMAT'))
                } for month in months]
            }
        else:
            years = getattr(cl.queryset, dates_or_datetimes)(field_name, 'year')
            return {
                'show': True,
                'current_filter': _('All'),
                'field_name': field.verbose_name,
                'choices': [{
                    'link': link({year_field: str(year.year)}),
                    'title': str(year.year),
                } for year in years]
            }
