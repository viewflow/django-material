from django.views.generic import FormView as BaseFormView

class FormView(BaseFormView):
    template_name = "demo/widgets.html"

    def form_valid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
