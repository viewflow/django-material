from karenina import modules


class Admin(modules.Module):
    icon = "mdi-action-settings-applications"
    order = 1000

    @property
    def label(self):
        return 'Administration'

    def has_perm(self, user):
        return user.is_staff