from django import template

register = template.Library()


@register.filter(name='multiply')
def multiply(value,
             arg):
    return str(value) * arg


@register.filter(name='censor')
def censor(value):

    CENSORED_WORDS = ['bad'] # List of censored words

    words = set(str(value).replace('_', ' ').split())
    for i in words:
        if i in CENSORED_WORDS:
            raise Exception(f'Word "{i}" is not allowed!')
    return str(value)
