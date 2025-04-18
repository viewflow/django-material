from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from material.urls import Site, Application


cotton = Application(
    title="Compoments",
    app_name="html",
    urlpatterns=[
        path(
            "breadcrumbs/",
            TemplateView.as_view(template_name="demo/html/breadcrumbs.html"),
            name="breadcrumbs",
        ),
        path(
            "buttons/",
            TemplateView.as_view(template_name="demo/html/buttons.html"),
            name="buttons",
        ),
        path(
            "cards/",
            TemplateView.as_view(template_name="demo/html/cards.html"),
            name="cards",
        ),
        path(
            "checkboxes/",
            TemplateView.as_view(template_name="demo/html/checkboxes.html"),
            name="checkboxes",
        ),
        path(
            "colors/",
            TemplateView.as_view(template_name="demo/html/colors.html"),
            name="colors",
        ),
        path(
            "lists/",
            TemplateView.as_view(template_name="demo/html/lists.html"),
            name="lists",
        ),
        path(
            "navigation/",
            TemplateView.as_view(template_name="demo/html/navigation.html"),
            name="navigation",
        ),
        path(
            "tables/",
            TemplateView.as_view(template_name="demo/html/tables.html"),
            name="tables",
        ),
        path(
            "templates/",
            TemplateView.as_view(template_name="demo/html/templates.html"),
            name="templates",
        ),
        path(
            "textareas/",
            TemplateView.as_view(template_name="demo/html/textareas.html"),
            name="textareas",
        ),
        path(
            "textfields/",
            TemplateView.as_view(template_name="demo/html/textfields.html"),
            name="textfields",
        ),
    ],
)

api = Application(
    title="Documentation",
    app_name="api",
    urlpatterns=[
        path(
            "",
            TemplateView.as_view(template_name="demo/api/index.html"),
            name="index",
        ),
        path(
            "urls/",
            TemplateView.as_view(template_name="demo/api/urls.html"),
            name="urls",
        ),
        path(
            "forms/",
            TemplateView.as_view(template_name="demo/api/forms.html"),
            name="forms",
        ),
        path(
            "layout/",
            TemplateView.as_view(template_name="demo/api/layout.html"),
            name="layout",
        ),
        path(
            "utils/",
            TemplateView.as_view(template_name="demo/api/utils.html"),
            name="utils",
        ),
        path(
            "views/",
            TemplateView.as_view(template_name="demo/api/views.html"),
            name="views",
        ),
        path(
            "templatetags/",
            TemplateView.as_view(template_name="demo/api/templatetags.html"),
            name="templatetags",
        ),
    ],
)

site = Site(
    title="Django Vibe Components",
    viewsets=[
        cotton,
        api,
    ],
    urlpatterns=[
        path("", TemplateView.as_view(template_name="demo/index.html"), name="index"),
    ],
)

urlpatterns = [
    path("", site.urls),
    path("admin/", admin.site.urls),
    path("widgets/", include("demo.forms.widgets.urls")),
    path("showcases/", include("demo.forms.showcases.urls")),
]
