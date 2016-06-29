from django.template import Library


register = Library()


@register.filter
def frontend_urlname(model, url_type):
    return '{}:{}_{}'.format(model._meta.app_label, model._meta.model_name, url_type)
