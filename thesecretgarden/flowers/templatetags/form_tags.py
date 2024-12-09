from django import template

register = template.Library()

@register.filter
def placeholder(field, text):
    """Adds a placeholder to a form field widget."""
    field.field.widget.attrs['placeholder'] = text
    return field
