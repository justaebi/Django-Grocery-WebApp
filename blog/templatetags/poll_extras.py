from django import template
from django.template.defaulttags import register

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def in_category(things, category):
    return things.filter(details=category)

@register.filter
def multiply(value, arg):
    return int(value) * int(arg)

@register.filter
def get(value,arg):
    return value.arg