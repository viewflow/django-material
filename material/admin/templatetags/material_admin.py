from django.contrib.admin.views.main import PAGE_VAR
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.template import Library

register = Library()


@register.simple_tag
def paginator_number(cl, i):
    """
    Generates an individual page index link in a paginated list.
    """
    if i == '.':
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

