from django import template

register = template.Library()

@register.simple_tag
def url_replace(request, field, value):
    """
    Replace or add a query parameter to the URL.
    """
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()
