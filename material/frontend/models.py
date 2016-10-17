from django.db import models
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save


class ModuleManager(models.Manager):
    """Base module state maanger."""

    def installed(self, module):
        """By default, all modules considered installed."""
        installed_cache = cache.get('material.modules.installed')
        if not installed_cache:
            installed_cache = [mod.label for mod in self.get_queryset().filter(installed=True)]
            cache.set('material.modules.installed', installed_cache, 60*60*24)
        return module in installed_cache


class Module(models.Model):
    """Keep module installed state in the database."""

    label = models.SlugField()
    installed = models.BooleanField(default=True)

    objects = ModuleManager()

    def __str__(self):
        return self.label


@receiver(post_save, sender=Module)
def _clean_installed_cache(sender, **kwargs):
    cache.delete('material.modules.installed')
