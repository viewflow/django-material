from django.db import models
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save
from ..compat import _

try:
    from django.utils.encoding import python_2_unicode_compatible
except ImportError:
    # django 3.0+
    python_2_unicode_compatible = lambda cls: cls  # NOQA


class ModuleManager(models.Manager):
    """Base module state manager."""

    def installed(self, module):
        """By default, all modules considered installed."""
        installed_cache = cache.get('material.modules.installed')
        if not installed_cache:
            installed_cache = [mod.label for mod in self.get_queryset().filter(installed=True)]
            cache.set('material.modules.installed', installed_cache, 60 * 60 * 24)
        return module in installed_cache


@python_2_unicode_compatible
class Module(models.Model):
    """Keep module installed state in the database."""

    label = models.SlugField(_('label'))
    installed = models.BooleanField(_('installed'), default=True)

    objects = ModuleManager()

    class Meta:
        verbose_name = _('module')
        verbose_name_plural = _('modules')

    def __str__(self):
        return self.label


@receiver(post_save, sender=Module)
def _clean_installed_cache(sender, **kwargs):
    cache.delete('material.modules.installed')
