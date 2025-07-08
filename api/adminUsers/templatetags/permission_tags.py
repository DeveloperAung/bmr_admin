from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def has_permission(user, permission_name):
    """
    Check if user has specific permission
    Usage: {% if user|has_permission:"user_create" %}
    """
    if not user.is_authenticated:
        return False
    return user.has_permission(permission_name)


@register.filter
def has_permission_type(user, permission_type):
    """
    Check if user has specific permission type
    Usage: {% if user|has_permission_type:"create" %}
    """
    if not user.is_authenticated:
        return False
    return user.has_permission_type(permission_type)


@register.filter
def has_any_permission(user, permission_names):
    """
    Check if user has any of the specified permissions
    Usage: {% if user|has_any_permission:"user_create,user_update" %}
    """
    if not user.is_authenticated:
        return False
    permission_list = [perm.strip() for perm in permission_names.split(',')]
    return user.has_any_permission(permission_list)


@register.filter
def has_all_permissions(user, permission_names):
    """
    Check if user has all of the specified permissions
    Usage: {% if user|has_all_permissions:"user_create,user_update" %}
    """
    if not user.is_authenticated:
        return False
    permission_list = [perm.strip() for perm in permission_names.split(',')]
    return user.has_all_permissions(permission_list)


@register.filter
def has_role(user, role_title):
    """
    Check if user has specific role
    Usage: {% if user|has_role:"Admin" %}
    """
    if not user.is_authenticated:
        return False
    return user.admin_user_role and user.admin_user_role.title == role_title


@register.simple_tag
def show_if_permission(user, permission_name, content):
    """
    Show content only if user has permission
    Usage: {% show_if_permission user "user_create" "Create User" %}
    """
    if not user.is_authenticated:
        return ""
    if user.has_permission(permission_name):
        return content
    return ""


@register.simple_tag
def show_if_permission_type(user, permission_type, content):
    """
    Show content only if user has permission type
    Usage: {% show_if_permission_type user "create" "Create" %}
    """
    if not user.is_authenticated:
        return ""
    if user.has_permission_type(permission_type):
        return content
    return ""


@register.simple_tag
def show_if_any_permission(user, permission_names, content):
    """
    Show content only if user has any of the specified permissions
    Usage: {% show_if_any_permission user "user_create,user_update" "Manage Users" %}
    """
    if not user.is_authenticated:
        return ""
    permission_list = [perm.strip() for perm in permission_names.split(',')]
    if user.has_any_permission(permission_list):
        return content
    return ""


@register.simple_tag
def show_if_all_permissions(user, permission_names, content):
    """
    Show content only if user has all of the specified permissions
    Usage: {% show_if_all_permissions user "user_create,user_update" "Full User Management" %}
    """
    if not user.is_authenticated:
        return ""
    permission_list = [perm.strip() for perm in permission_names.split(',')]
    if user.has_all_permissions(permission_list):
        return content
    return ""


@register.simple_tag
def show_if_role(user, role_title, content):
    """
    Show content only if user has specific role
    Usage: {% show_if_role user "Admin" "Admin Panel" %}
    """
    if not user.is_authenticated:
        return ""
    if user.admin_user_role and user.admin_user_role.title == role_title:
        return content
    return ""


@register.simple_tag
def show_if_staff(user, content):
    """
    Show content only if user is staff
    Usage: {% show_if_staff user "Staff Panel" %}
    """
    if not user.is_authenticated:
        return ""
    if user.is_staff:
        return content
    return ""


@register.simple_tag
def show_if_superuser(user, content):
    """
    Show content only if user is superuser
    Usage: {% show_if_superuser user "Superuser Panel" %}
    """
    if not user.is_authenticated:
        return ""
    if user.is_superuser:
        return content
    return "" 