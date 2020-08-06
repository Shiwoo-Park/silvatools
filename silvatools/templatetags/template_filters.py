from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def div(value, arg):
    """
    Divides the value; argument is the divisor.
    Returns empty string on any error.
    """
    try:
        value = int(value)
        arg = int(arg)
        if arg:
            return value / arg
    except:
        pass
    return ""
