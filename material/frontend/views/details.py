from django.views.generic import View


class DetailsModelView(View):
    model = None
    viewset = None

    @classmethod
    def has_perm(cls, user, obj):
        return True