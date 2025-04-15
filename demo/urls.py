from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="demo/index.html"), name="index"),
    path(
        "buttons/",
        TemplateView.as_view(template_name="demo/buttons.html"),
        name="buttons",
    ),
    path(
        "navigation/",
        TemplateView.as_view(template_name="demo/navigation.html"),
        name="navigation",
    ),
    path("tables/", TemplateView.as_view(template_name="demo/tables.html"), name="tables"),
    path(
        "templates/",
        TemplateView.as_view(template_name="demo/templates.html"),
        name="templates",
    ),
    path(
        "breadcrumbs/",
        TemplateView.as_view(template_name="demo/breadcrumbs.html"),
        name="breadcrumbs",
    ),
    path("colors/", TemplateView.as_view(template_name="demo/colors.html"), name="colors"),
    path(
        "checkboxes/",
        TemplateView.as_view(template_name="demo/checkboxes.html"),
        name="checkboxes",
    ),
    path(
        "textfields/",
        TemplateView.as_view(template_name="demo/textfields.html"),
        name="textfields",
    ),
    path(
        "textareas/",
        TemplateView.as_view(template_name="demo/textareas.html"),
        name="textareas",
    ),
    path("cards/", TemplateView.as_view(template_name="demo/cards.html"), name="cards"),
    path("lists/", TemplateView.as_view(template_name="demo/lists.html"), name="lists"),
    path("widgets/", include("demo.forms.widgets.urls")),
    path("showcases/", include("demo.forms.showcases.urls")),
    # API Documentation
    path(
        "api/",
        TemplateView.as_view(template_name="demo/api/index.html"),
        name="api_index",
    ),
    path(
        "api/urls/",
        TemplateView.as_view(template_name="demo/api/urls.html"),
        name="api_urls",
    ),
    path(
        "api/forms/",
        TemplateView.as_view(template_name="demo/api/forms.html"),
        name="api_forms",
    ),
    path(
        "api/layout/",
        TemplateView.as_view(template_name="demo/api/layout.html"),
        name="api_layout",
    ),
    path(
        "api/utils/",
        TemplateView.as_view(template_name="demo/api/utils.html"),
        name="api_utils",
    ),
    path(
        "api/views/",
        TemplateView.as_view(template_name="demo/api/views.html"),
        name="api_views",
    ),
    path(
        "api/templatetags/",
        TemplateView.as_view(template_name="demo/api/templatetags.html"),
        name="api_templatetags",
    ),
]
