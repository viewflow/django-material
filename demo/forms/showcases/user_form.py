from django.contrib.auth.models import User, Group
from django.forms.models import inlineformset_factory
from viewflow.forms import ModelForm, InlineFormSetField, AjaxModelSelect


GroupFormSet = inlineformset_factory(
    User,
    Group.user_set.through,
    fields=("group",),
    can_delete=False,
    extra=1,
    widgets={"group": AjaxModelSelect(lookups=["name__istartswith"])},
)


class UserForm(ModelForm):
    groups = InlineFormSetField(formset_class=GroupFormSet)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]
