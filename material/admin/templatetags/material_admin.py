import re
import datetime
from importlib import import_module

from django.apps import apps
from django.contrib.admin.views.main import PAGE_VAR
from django.contrib.admin.utils import get_fields_from_path
from django.core.urlresolvers import reverse, NoReverseMatch
from django.conf import settings
from django.db import models
from django.utils import formats, six
from django.utils.dates import MONTHS
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.template import Library

from material import Layout, Fieldset, Row
from material.compat import simple_tag
from ..base import AdminReadonlyField, Inline


register = Library()


CL_VALUE_RE = re.compile('value="(.*)\"')


def get_admin_site():
    """TODO: Remove."""
    site_module = getattr(
        settings,
        'MATERIAL_ADMIN_SITE',
        'django.contrib.admin.site'
    )
    mod, inst = site_module.rsplit('.', 1)
    mod = import_module(mod)
    return getattr(mod, inst)


site = get_admin_site()


@register.assignment_tag
def get_app_list(request):
    """Django 1.8 way to get application registred at default Admin Site."""
    app_dict = {}
    user = request.user

    for model, model_admin in site._registry.items():
        app_label = model._meta.app_label
        has_module_perms = user.has_module_perms(app_label)

        if has_module_perms:
            perms = model_admin.get_model_perms(request)

            # Check whether user has any perm for this module.
            # If so, add the module to the model_list.
            if True in perms.values():
                info = (app_label, model._meta.model_name)
                model_icon = '<i class="material-icons admin-modelicon admin-modelicon-{}-{}"></i>'.format(
                    app_label, model._meta.model_name)
                if hasattr(model_admin, 'icon'):
                    model_icon = model_admin.icon
                model_dict = {
                    'name': capfirst(model._meta.verbose_name_plural),
                    'object_name': model._meta.object_name,
                    'perms': perms,
                    'icon': mark_safe(model_icon)
                }
                if perms.get('change', False):
                    try:
                        model_dict['admin_url'] = reverse('admin:%s_%s_changelist' % info, current_app=site.name)
                        if request.path.startswith(model_dict['admin_url']):
                            model_dict['active'] = True
                    except NoReverseMatch:
                        pass
                if app_label in app_dict:
                    app_dict[app_label]['models'].append(model_dict)
                else:
                    app_config = apps.get_app_config(app_label)

                    app_name = app_config.verbose_name
                    if len(app_name) > 23:
                        app_name = app_label.title()
                    app_name = app_name.replace('_', ' ')

                    app_icon = '<i class="material-icons admin-appicon admin-appicon-{}"></i>'.format(app_label)
                    if hasattr(app_config, 'icon'):
                        app_icon = app_config.icon

                    app_dict[app_label] = {
                        'name': app_name,
                        'app_label': app_label,
                        'app_icon': mark_safe(app_icon),
                        'app_url': reverse('admin:app_list', kwargs={'app_label': app_label}, current_app=site.name),
                        'has_module_perms': has_module_perms,
                        'models': [model_dict],
                    }

                    if request.path.startswith(app_dict[app_label]['app_url']):
                        app_dict[app_label]['active'] = True

    # Sort the apps alphabetically.
    app_list = list(six.itervalues(app_dict))
    app_list.sort(key=lambda x: x['name'].lower())

    # Sort the models alphabetically within each app.
    for app in app_list:
        app['models'].sort(key=lambda x: x['name'])

    return app_list


@register.assignment_tag
def fieldset_layout(adminform, inline_admin_formsets):
    """Generate materila layout for admin inlines."""
    layout = getattr(adminform.model_admin, 'layout', None)
    if layout is not None:
        for element in layout.elements:
            # TODO Ugly hack to substitute inline classes to instances
            if isinstance(element, Inline) and isinstance(element.inline, type):
                for inline in inline_admin_formsets:
                    if inline.formset.model == element.inline.model:
                        element.inline = inline
        return layout

    sets = []

    for fieldset in adminform:
        fields = []

        for line in fieldset:
            line_fields = []

            for fieldset_field in line:
                field = None

                if getattr(fieldset_field, 'is_readonly', False):
                    field = AdminReadonlyField(fieldset_field)
                else:
                    field = fieldset_field.field.name

                line_fields.append(field)

            if len(line_fields) == 1:
                fields.append(line_fields[0])
            else:
                fields.append(Row(*line_fields))

        if fieldset.name:
            sets.append(Fieldset(fieldset.name, *fields))
        else:
            sets += fields

    for inline in inline_admin_formsets:
        sets.append(Inline(inline))

    return Layout(*sets)


@register.simple_tag
def paginator_number(cl, i):
    """Generate an individual page index link in a paginated list."""
    current_page = cl.paginator.page(cl.page_num+1)
    if i == 'prev':
        if current_page.has_previous():
            return format_html('<li class="disabled"><a href="{}"><i class="material-icons">chevron_left</i></a></li>',
                               cl.get_query_string({PAGE_VAR: current_page.previous_page_number()}))
        else:
            return format_html('<li class="disabled"><a href="#!"><i class="material-icons">chevron_left</i></a></li>')
    elif i == 'next':
        if current_page.has_next():
            return format_html(
                '<li class="disabled"><a href="{}"><i class="material-icons">chevron_right</i></i></a></li>',
                cl.get_query_string({PAGE_VAR: current_page.next_page_number()}))
        else:
            return format_html(
                '<li class="disabled"><a href="#!"><i class="material-icons">chevron_right</i></a></li>')
    elif i == '.':
        return mark_safe('<li class="disabled"><a href="#" onclick="return false;">...</a></li>')
    elif i == cl.page_num:
        return format_html('<li class="active"><a href="#!">{0}</a></li> ',
                           i+1,
                           cl.get_query_string({PAGE_VAR: i}))
    else:
        return format_html('<li><a href="{0}"{1}>{2}</a></li>',
                           cl.get_query_string({PAGE_VAR: i}),
                           mark_safe(' class="end"' if i == cl.paginator.num_pages - 1 else ''),
                           i + 1)


@register.inclusion_tag('admin/date_hierarchy.html')
def date_hierarchy(cl):
    """Display the date hierarchy for date drill-down functionality."""
    if cl.date_hierarchy:
        field_name = cl.date_hierarchy
        field = get_fields_from_path(cl.model, field_name)[-1]
        dates_or_datetimes = 'datetimes' if isinstance(field, models.DateTimeField) else 'dates'
        year_field = '%s__year' % field_name
        month_field = '%s__month' % field_name
        day_field = '%s__day' % field_name
        field_generic = '%s__' % field_name
        year_lookup = cl.params.get(year_field)
        month_lookup = cl.params.get(month_field)
        day_lookup = cl.params.get(day_field)

        def link(filters):
            return cl.get_query_string(filters, [field_generic])

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


def admin_related_field_urls(bound_field):
    """
    Construct add/remove/change links for admin related field.

    Usage:

        {% admin_related_field_urls bound_field as bound_field_urls %}
    """
    from django.contrib.admin.views.main import IS_POPUP_VAR, TO_FIELD_VAR

    rel_widget = bound_field.field.widget
    rel_opts = rel_widget.rel.model._meta
    info = (rel_opts.app_label, rel_opts.model_name)
    rel_widget.widget.choices = rel_widget.choices
    url_params = '&'.join("%s=%s" % param for param in [
        (TO_FIELD_VAR, rel_widget.rel.get_related_field().name),
        (IS_POPUP_VAR, 1),
    ])

    context = {
        'widget': rel_widget.widget.render(bound_field.name, bound_field.value()),
        'name': bound_field.name,
        'url_params': url_params,
        'model': rel_opts.verbose_name,
    }
    if rel_widget.can_change_related:
        change_related_template_url = rel_widget.get_related_url(info, 'change', '__fk__')
        context.update(
            can_change_related=True,
            change_related_template_url=change_related_template_url,
        )
    if rel_widget.can_add_related:
        add_related_url = rel_widget.get_related_url(info, 'add')
        context.update(
            can_add_related=True,
            add_related_url=add_related_url,
        )
    if rel_widget.can_delete_related:
        delete_related_template_url = rel_widget.get_related_url(info, 'delete', '__fk__')
        context.update(
            can_delete_related=True,
            delete_related_template_url=delete_related_template_url,
        )

    return context


simple_tag(register, admin_related_field_urls)


@register.filter
def admin_change_list_value(result_checkbox_html):
    """Extract value from rendered admin list action checkbox."""
    value = CL_VALUE_RE.findall(result_checkbox_html)
    return value[0] if value else None


def admin_select_related_link(bound_field):
    """
    Helper for admin RelatedWidgetWrapper.

    {% admin_select_related_link bound_field as rel_field_urls %}
    """
    rel_widget = bound_field.field.widget
    rel_to = rel_widget.rel.model
    if rel_to in rel_widget.admin_site._registry:
        related_url = reverse(
            'admin:%s_%s_changelist' % (
                rel_to._meta.app_label,
                rel_to._meta.model_name,
            ),
            current_app=rel_widget.admin_site.name,
        )
        params = rel_widget.url_parameters()
        if params:
            related_url += '?' + '&amp;'.join('%s=%s' % (k, v) for k, v in params.items())
        return {'related_url': related_url}
    return {}


simple_tag(register, admin_select_related_link)
