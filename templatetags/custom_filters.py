from django import template

register = template.Library()

@register.filter
def currency(value, currency_code):
    if currency_code == 'KZT':
        return f'{value} ₸'
    return value