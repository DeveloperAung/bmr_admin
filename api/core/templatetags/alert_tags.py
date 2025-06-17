from django import template

register = template.Library()


@register.filter
def get_field_label(form, field_name):
    """Get the label for a form field"""
    try:
        return form.fields[field_name].label or field_name.replace('_', ' ').title()
    except KeyError:
        return field_name.replace('_', ' ').title()
