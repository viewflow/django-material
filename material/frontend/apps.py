import warnings
from importlib import import_module

from django.apps import AppConfig, apps
from django.core.urlresolvers import reverse
from django.db.models.signals import post_migrate
from django.template import Template, TemplateDoesNotExist
from django.template.loader import get_template
from django.utils.module_loading import module_has_submodule

from .registry import modules as modules_registry
from .urlconf import ModuleURLResolver


class ModuleMixin(object):
    """
    Extension for the django AppConfig. Makes django app pluggable at runtime.

    - Application level user permission access
    - Runtime app installation/deinstallation
    - Autodiscovery for <app_module>/urls.py
    - Collect common website menu from `<app_label>/menu.html`

    Example::

        class Sales(ModuleMixin, AppConfig):
            name = 'sales'
            icon = '<i class="material-icons">call</i>'

    The application have to have <app_module>/urls.py file, with
    a single no-parametrized url with name='index', ex::

        urlpatterns = [
            url('^$', generic.TemplateView.as_view(template_name="sales/index.html"), name="index"),
        ]

    All AppConfigs urls will be included into material.frontend.urls automatically under /<app_label>/ prefix
    The AppConfig.label, used for the urls namespace.

    The menu.html sample::

        <ul>
            <li><a href="{% url 'sales:index' %}">Dashboard</a></li>
            <li><a href="{% url 'sales:customers' %}">Customers</a></li>
            {% if perms.sales.can_add_lead %}<li><a href="{% url 'sales:leads' %}">Leads</a></li>{% endif %}
        </ul>

    In all application templates, the current application config
    instance would be available as `current_module` template variable

    """
    order = 10
    icon = '<i class="material-icons">receipt</i>'

    @property
    def verbose_name(self):
        return self.label.title()

    @property
    def installed(self):
        from .models import Module as DbModule
        return DbModule.objects.installed(self.label)

    def description(self):
        return (self.__doc__ or "").strip()

    def has_perm(self, user):
        return True

    def get_urls(self):
        if module_has_submodule(self.module, 'urls'):
            urls_module_name = '%s.%s' % (self.name, 'urls')
            urls_module = import_module(urls_module_name)
            if hasattr(urls_module, 'urlpatterns'):
                return urls_module.urlpatterns

        warnings.warn('Module {} have not urls.py submodule or `urlpatterns` in it'.format(self.label))
        return []

    @property
    def urls(self):
        base_url = r'^{}/'.format(self.label)
        return ModuleURLResolver(base_url, self.get_urls(), module=self, app_name=self.label, namespace=self.label)

    def index_url(self):
        return reverse('{}:index'.format(self.label))

    def menu(self):
        try:
            return get_template('{}/menu.html'.format(self.label))
        except TemplateDoesNotExist:
            return Template('')


class MaterialFrontendConfig(AppConfig):
    name = 'material.frontend'
    verbose_name = 'Site Modules'
    icon = '<i class="material-icons">view_module</i>'

    def ready(self):
        for app_config in apps.get_app_configs():
            if isinstance(app_config, ModuleMixin):
                modules_registry.register(app_config)
        post_migrate.connect(update_modules, sender=self)


def update_modules(app_config, verbosity=2, interactive=True, **kwargs):
    from .models import Module as DbModule

    for module in modules_registry.modules():
        _, created = DbModule.objects.get_or_create(label=module.label)
        if created and verbosity >= 2:
            print('Adding module {}'.format(module.label))

    stale_modules = DbModule.objects.exclude(
        label__in=[module.label for module in modules_registry.modules()])

    if stale_modules.exists():
        if interactive:
            ok_to_delete = input(
                "The following modules are stale and need to be deleted:\n {}\n"
                "Are you sure you want to delete these content types?".format(
                    '    %s'.join(module.label for module in stale_modules)
                ))
        else:
            ok_to_delete = True

        if ok_to_delete == 'yes':
            stale_modules.delete()
            print("Stale modules deleted.")
