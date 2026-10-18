from django import template

register = template.Library()


@register.filter
def cop(value):
    """La demo usa pesos enteros; el formato no modifica el valor."""
    return "$ " + format(value, ",").replace(",", ".")
