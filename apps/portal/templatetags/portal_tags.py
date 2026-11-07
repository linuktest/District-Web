from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Allow dict[key] access in templates: {{ my_dict|get_item:key }}"""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None


@register.filter
def split(value, delimiter=','):
    """Split a string by delimiter: {{ "a,b,c"|split:"," }}"""
    return value.split(delimiter)
