from django.db import models
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save


class ModuleManager(models.Manager):
    def installed(self, module):
        installed_cache = cache.get('material.modules.installed')
        if not installed_cache:
            installed_cache = [mod.slug for mod in self.get_queryset().filter(installed=True)]
            cache.set('material.modules.installed', installed_cache, 60*60*24)
        return module in installed_cache


class Module(models.Model):
    slug = models.SlugField()
    installed = models.BooleanField(default=False)

    objects = ModuleManager()

    class Meta:
        permissions = (
            ('can_configure', 'Can install/uninstall modules'),
        )


@receiver(post_save, sender=Module)
def clean_installed_cache(sender, **kwargs):
    cache.delete('material.modules.installed')
