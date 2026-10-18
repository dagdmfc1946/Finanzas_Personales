from decimal import Decimal
from django import template

register = template.Library()


@register.filter
def pesos(cents):
    formatted = format(Decimal(cents) / 100, ",.2f")
    return "$ " + formatted.replace(",", "_").replace(".", ",").replace("_", ".")
