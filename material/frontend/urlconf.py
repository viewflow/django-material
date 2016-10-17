from django.core.urlresolvers import RegexURLResolver, Resolver404


class ModuleMatchName(str):
    """Dump str wrapper.

    Just to keep module reference over django url resolve calling
    hierarhy.
    """


class ModuleURLResolver(RegexURLResolver):
    """Module URL Resolver.

    A wrapper around RegexURLResolver that check the module installed
    state. And allows access to the resolved current module at runtime.

    Django reads url config once at the start. Installation and
    deisntallation the module at runtime don't produce change in the
    django url-conf.

    Url access check happens at the resolve time.
    """

    def __init__(self, *args, **kwargs):  # noqa D102
        self._module = kwargs.pop('module')
        super(ModuleURLResolver, self).__init__(*args, **kwargs)

    def resolve(self, *args, **kwargs):  # noqa D102
        result = super(ModuleURLResolver, self).resolve(*args, **kwargs)

        if result and not getattr(self._module, 'installed', True):
            raise Resolver404({'message': 'Module not installed'})

        result.url_name = ModuleMatchName(result.url_name)
        result.url_name.module = self._module

        return result
