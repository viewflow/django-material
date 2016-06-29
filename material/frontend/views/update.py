from django.views.generic import View


class UpdateModelView(View):
    model = None
    viewset = None

    def has_perm(self, user, obj):
        return True
