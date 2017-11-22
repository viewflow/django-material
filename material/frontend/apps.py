import warnings
from importlib import import_module

from django.apps import AppConfig, apps
from django.db.models.signals import post_migrate
from django.template import Template, TemplateDoesNotExist
from django.template.loader import get_template, select_template
from django.urls import reverse
from django.utils.module_loading import module_has_submodule
from django.utils.six.moves import input
from django.utils.translation import ugettext_lazy as _

from .registry import modules as modules_registry
from .urlconf import ModuleURLResolver


class ModuleMixin(object):
    """Extension for the django AppConfig. Makes django app pluggable at runtime.

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

    :keyword order: The relative module order priority. Modules in the
                    site menu would be listed according its priorities.

    :keyword icon: The module icon.

    Example::

        class Sales(ModuleMixin, AppConfig):
            name = 'sales'
            icon = '<i class="material-icons">call</i>'

    """

    order = 10
    icon = '<i class="material-icons">receipt</i>'

    @property
    def verbose_name(self):
        """Module name."""
        return self.label.title()

    @property
    def installed(self):
        """Check the module installation state.

        Default implementation store installed state in the database
        `frontend_dbmodule` table.
        """
        from .models import Module as DbModule
        return DbModule.objects.installed(self.label)

    def description(self):
        """Module description.

        By default taken from the module docstring.
        """
        return (self.__doc__ or "").strip()

    def has_perm(self, user):
        """Check is user have permission to access to the module."""
        return True

    def get_urls(self):  # noqa D102
        if module_has_submodule(self.module, 'urls'):
            urls_module_name = '%s.%s' % (self.name, 'urls')
            urls_module = import_module(urls_module_name)
            if hasattr(urls_module, 'urlpatterns'):
                return urls_module.urlpatterns

        warnings.warn('Module {} have not urls.py submodule or `urlpatterns` in it'.format(self.label))
        return []

    @property
    def urls(self):
        """Module url config.

        By default it would be loaded from '<app>/urls.py'
        """
        base_url = r'^{}/'.format(self.label)
        return ModuleURLResolver(base_url, self.get_urls(), module=self, app_name=self.label, namespace=self.label)

    def index_url(self):
        """Entry url for a module."""
        return reverse('{}:index'.format(self.label))

    def menu(self):
        """Load module menu template.

        Template should be located in `<app_label>/menu.html`

        If no template exists, no exception raised.

        Intended to use with {% include %} template tag::

            {% include module.menu %}
        """
        try:
            return get_template('{}/menu.html'.format(self.label))
        except TemplateDoesNotExist:
            return Template('')

    def base_template(self):
        """Base template for a module.

        If  <app_label>/base_module.html exists it would be used.
        The default is 'material/frontend/base_module.html'

        Intended to use in modules generic templates. Ex::

            {% extends current_module.base_template %}
        """
        return select_template([
            '{}/base_module.html'.format(self.label),
            'material/frontend/base_module.html'
        ])


class MaterialFrontendConfig(AppConfig):
    """Default config for Material Frontend."""

    name = 'material.frontend'
    verbose_name = _('Frontend')
    icon = '<i class="material-icons">view_module</i>'

    def ready(self):
        """Register all available modules."""
        for app_config in apps.get_app_configs():
            if isinstance(app_config, ModuleMixin):
                modules_registry.register(app_config)
        post_migrate.connect(update_modules, sender=self)


def update_modules(app_config, verbosity=2, interactive=True, **kwargs):
    """Sync installed modules and database records."""
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
                "Are you sure you want to delete these modules entries?\n\n"
                "Type 'yes' to continue, or 'no' to cancel: ".format(
                    '    %s'.join(module.label for module in stale_modules)
                ))
        else:
            ok_to_delete = 'yes'

        if ok_to_delete == 'yes':
            stale_modules.delete()
            print("Stale modules deleted.")
        else:
            if verbosity >= 2 or interactive:
                print("Stale modules remain.")
