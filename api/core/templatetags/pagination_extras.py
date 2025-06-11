# core/templatetags/pagination_extras.py

from django import template

register = template.Library()


@register.filter
def make_list(value):
    try:
        return range(1, int(value) + 1)
    except:
        return []


@register.filter
def cut_if_gt(value, limit):
    return min(int(value), int(limit))


@register.simple_tag
def calculate_start(current_page, page_size):
    return (current_page - 1) * page_size + 1


@register.simple_tag
def calculate_end(current_page, page_size, total_records):
    return min(current_page * page_size, total_records)


@register.filter
def to(value, arg):
    return range(int(value), int(arg)+1)


@register.simple_tag(takes_context=True)
def querystring_replace(context, key, value):
    query = context['request'].GET.copy()
    query[key] = value
    return '?' + query.urlencode()
