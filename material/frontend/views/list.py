import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic.base import ContextMixin, TemplateResponseMixin


from ..datalist import DataList
from .. import forms


class ListModelView(ContextMixin, TemplateResponseMixin, View):
    """List view sutable to work with jQuery Datatables.

    The view responsive for handling GET/POST requests from the browser
    and AJAX from the datatable.

    :keyword model: Model class views

    :keyword queryset: Base views queryset

    :keyword paginate_by: Page size

    :keyword datatable_config: Datatable default config overrides

    :keyword datalist_class: Queryset to data adapter implementation

    :keyword list_display: List of fields to display

    :keyword list_display_links: List of fields form `list_display`
                                 linked to change view

    """

    model = None
    viewset = None
    queryset = None
    paginate_by = 15
    datatable_config = None
    template_name_suffix = '_list'

    datalist_class = DataList
    list_display = ('__str__', )
    list_display_links = ()

    datatable_default_config = {
        'processing': False,
        'serverSide': True,
        'ajax': '.',
        'ordering': False,
        'info': False,
        'bFilter': False,
        'bAutoWidth': False,
        'bLengthChange': False,
        'oLanguage': {
            'oPaginate': {
                'sFirst': "",
                'sLast': "",
                'sNext': "&rang;",
                'sPrevious': "&lang;",
            }
        },
        'responsive': {
            'details': False
        }
    }

    def has_view_permission(self, request, obj=None):
        """Object view permission check.

        If view had a `viewset`, the `viewset.has_view_permission` used.
        """
        if self.viewset is not None:
            return self.viewset.has_view_permission(request, obj)
        raise NotImplementedError('Viewset is not provided')

    def has_change_permission(self, request, obj=None):
        """Object change permission check.

        If view had a `viewset`, the `viewset.has_change_permission` used.
        """
        if self.viewset is not None:
            return self.viewset.has_change_permission(request, obj)
        raise NotImplementedError('Viewset is not provided')

    def get_template_names(self):
        """
        List of templates for the view.

        If no `self.template_name` defined, uses::

             [<app_label>/<model_label>_list.html,
              'material/frontend/views/list.html']
        """
        if self.template_name is None:
            opts = self.object_list.model._meta
            return [
                '{}/{}{}.html'.format(
                    opts.app_label,
                    opts.model_name,
                    self.template_name_suffix),
                'material/frontend/views/list.html',
            ]
        return [self.template_name]

    def get_list_display(self):
        """Return list of coluns to display."""
        return self.list_display

    def get_list_display_links(self, list_display):
        """Return columns list that would be linked to the object details.

        If `self.list_display_links` is not set, the first column would be used.
        """
        if (self.list_display_links or
                self.list_display_links is None or
                not list_display):
            return list(self.list_display_links)
        else:
            # Use only the first item in list_display as link
            return list(list_display)[:1]

    def create_datalist(self):
        """Create data adapter instance."""
        list_display = self.get_list_display()
        list_display_links = self.get_list_display_links(list_display)
        return self.datalist_class(
            self.model,
            self.object_list,
            data_sources=[self, self.viewset] if self.viewset else [self],
            list_display=list_display,
            list_display_links=list_display_links
        )

    def get_queryset(self):
        """Retrive the view queryset."""
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                })
        return queryset

    def get_datatable_config(self):
        """Prepare datatable config."""
        config = self.datatable_default_config.copy()
        config['iDisplayLength'] = self.paginate_by
        config['columns'] = [
            {'data': field_name}
            for field_name in self.datalist.list_display
        ]
        if self.datatable_config is not None:
            config.update(self.datatable_config)
        return config

    def get_context_data(self, **kwargs):
        """Update view context.

        Include `datatable_config`, 'headers' and initial `data` to
        first page render.
        """
        context = super(ListModelView, self).get_context_data(**kwargs)
        context.update({
            'datatable_config': json.dumps(self.get_datatable_config()),
            'headers': self.datalist.get_headers_data(),
            'data': self.datalist.get_data(0, self.paginate_by),
        })

        return context

    def get(self, request, *args, **kwargs):
        """Response with rendered html template."""
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_item_data(self, item):
        """Row data post-processing.

        Include link to object detail to `list_display_links` columns.
        """
        opts = self.model._meta

        result = {}
        if self.has_view_permission(self.request, item):
            result['view_url'] = reverse(
                '{}:{}_detail'.format(opts.app_label, opts.model_name),
                args=[item.pk])
        return result

    def get_json_data(self, request, *args, **kwargs):
        """Return `JSONResponse` with data for datatable."""
        form = forms.DatatableRequestForm(request.GET)
        if not form.is_valid():
            return {'error': form.errors}

        draw = form.cleaned_data['draw']
        start = form.cleaned_data['start']
        length = form.cleaned_data['length']

        result = []
        for item, columns_data in self.datalist.get_data(start, length):
            columns_data.update(self.get_item_data(item))
            result.append(columns_data)

        data = {
            "draw": draw,
            "recordsTotal": self.datalist.total(),
            "recordsFiltered": self.datalist.total_filtered(),
            "data": result
        }

        return JsonResponse(data)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """Handle for browser HTTP and AJAX requests from datatables."""
        if not self.has_view_permission(self.request):
            raise PermissionDenied

        self.object_list = self.get_queryset()
        self.datalist = self.create_datalist()

        if request.is_ajax() and not request.META.get("PJAX", False):
            handler = self.get_json_data
        elif request.method.lower() in self.http_method_names:
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)
