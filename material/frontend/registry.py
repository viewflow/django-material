class Registry(object):
    def __init__(self):
        self._registry = {}

    def modules(self):
        return sorted([module for module in self._registry.values()],
                      key=lambda module: (module.order, module.label))

    def installed_modules(self):
        return [module for module in self.modules()
                if getattr(module, 'installed', True)]

    def available_modules(self, user):
        return [module for module in self.installed_modules()
                if module.has_perm(user)]

    def get_module(self, module_label):
        return self._registry.get(module_label, None)

    def register(self, module):
        self._registry[module.label] = module

    @property
    def urls(self):
        patterns = []
        for module in self.modules():
            patterns.append(module.urls)
        return patterns


modules = Registry()
