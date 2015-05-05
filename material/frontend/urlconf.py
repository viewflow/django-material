from django.core.urlresolvers import RegexURLResolver, Resolver404


class ModuleURLResolver(RegexURLResolver):
    def __init__(self, *args, **kwargs):
        self._module = kwargs.pop('module')
        super(ModuleURLResolver, self).__init__(*args, **kwargs)

    def resolve(self, *args, **kwargs):
        result = super(ModuleURLResolver, self).resolve(*args, **kwargs)

        if result and not getattr(self._module, 'installed', True):
            raise Resolver404({'message': 'Module not installed'})

        result.kwargs['module'] = self._module

        return result
