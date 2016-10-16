class Registry(object):
    """Frontend module registry."""

    def __init__(self):  # noqa D102
        self._registry = {}

    def modules(self):
        """List of modules in the forntend according to it's order."""
        return sorted([module for module in self._registry.values()],
                      key=lambda module: (module.order, module.label))

    def installed_modules(self):
        """List of installed modules.

        A frontend module itself determines if it installed or not.
        If the module instance have no `installed` attribute, the
        module considered installed.
        """
        return [module for module in self.modules()
                if getattr(module, 'installed', True)]

    def available_modules(self, user):
        """List of modules permitted for the user."""
        return [module for module in self.installed_modules()
                if module.has_perm(user)]

    def get_module(self, module_label):
        """Get module by label."""
        return self._registry.get(module_label, None)

    def register(self, module):
        """Register a module.

        Can be called on the package level.
        """
        self._registry[module.label] = module

    @property
    def urls(self):
        """Collected list of all modules url.

        Even uninstalled modules urls returned here. The module url
        config have the responsibility to check the module installed
        state.
        """
        patterns = []
        for module in self.modules():
            patterns.append(module.urls)
        return patterns


modules = Registry()
