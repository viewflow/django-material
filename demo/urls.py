from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from material.urls import Site, Application, menu_path


cotton = Application(
    title="Compoments",
    app_name="html",
    icon="layers",
    urlpatterns=[
        menu_path(
            "breadcrumbs/",
            TemplateView.as_view(template_name="demo/html/breadcrumbs.html"),
            name="breadcrumbs",
            title="Breadcrumbs",
        ),
        menu_path(
            "buttons/",
            TemplateView.as_view(template_name="demo/html/buttons.html"),
            name="buttons",
            icon="touch_app",
            title="Buttons",
        ),
        menu_path(
            "cards/",
            TemplateView.as_view(template_name="demo/html/cards.html"),
            name="cards",
            icon="style",
            title="Cards",
        ),
        menu_path(
            "checkboxes/",
            TemplateView.as_view(template_name="demo/html/checkboxes.html"),
            name="checkboxes",
            icon="check_box",
            title="Checkboxes",
        ),
        menu_path(
            "colors/",
            TemplateView.as_view(template_name="demo/html/colors.html"),
            name="colors",
            icon="palette",
            title="Color System",
        ),
        menu_path(
            "lists/",
            TemplateView.as_view(template_name="demo/html/lists.html"),
            name="lists",
            icon="format_list_bulleted",
            title="Lists",
        ),
        menu_path(
            "navigation/",
            TemplateView.as_view(template_name="demo/html/navigation.html"),
            name="navigation",
            icon="menu",
            title="Navigation",
        ),
        menu_path(
            "tables/",
            TemplateView.as_view(template_name="demo/html/tables.html"),
            name="tables",
            icon="table_chart",
            title="Tables",
        ),
        menu_path(
            "templates/",
            TemplateView.as_view(template_name="demo/html/templates.html"),
            name="templates",
            icon="layers",
            title="Templates",
        ),
        menu_path(
            "textareas/",
            TemplateView.as_view(template_name="demo/html/textareas.html"),
            name="textareas",
            icon="text_fields",
            title="Text Areas",
        ),
        menu_path(
            "textfields/",
            TemplateView.as_view(template_name="demo/html/textfields.html"),
            name="textfields",
            icon="input",
            title="Text Fields",
        ),
    ],
)

api = Application(
    title="Documentation",
    app_name="api",
    icon="code",
    urlpatterns=[
        menu_path(
            "",
            TemplateView.as_view(template_name="demo/api/index.html"),
            name="index",
            icon="home",
            title="Overview",
        ),
        menu_path(
            "urls/",
            TemplateView.as_view(template_name="demo/api/urls.html"),
            name="urls",
            icon="link",
            title="URL Configuration",
        ),
        menu_path(
            "forms/",
            TemplateView.as_view(template_name="demo/api/forms.html"),
            name="forms",
            icon="description",
            title="Forms API",
        ),
        menu_path(
            "layout/",
            TemplateView.as_view(template_name="demo/api/layout.html"),
            name="layout",
            icon="grid_view",
            title="Layout System",
        ),
        menu_path(
            "middleware/",
            TemplateView.as_view(template_name="demo/api/middleware.html"),
            name="middleware",
            icon="swap_horiz",
            title="Middleware System",
        ),
        menu_path(
            "utils/",
            TemplateView.as_view(template_name="demo/api/utils.html"),
            name="utils",
            icon="build",
            title="Utility Functions",
        ),
        menu_path(
            "views/",
            TemplateView.as_view(template_name="demo/api/views.html"),
            name="views",
            icon="visibility",
            title="Views Framework",
        ),
        menu_path(
            "templatetags/",
            TemplateView.as_view(template_name="demo/api/templatetags.html"),
            name="templatetags",
            icon="code",
            title="Template Tags",
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
        menu_path("", TemplateView.as_view(template_name="demo/index.html"), name="index", icon="home", title="Home"),
    ],
)

urlpatterns = [
    path("", site.urls),
    path("admin/", admin.site.urls),
    path("widgets/", include("demo.forms.widgets.urls")),
    path("showcases/", include("demo.forms.showcases.urls")),
]
