def user_permissions(request):
    """
    Context processor to make user permissions available in templates
    """
    if request.user.is_authenticated:
        return {
            'user_permissions': {
                'has_permission': request.user.has_permission,
                'has_permission_type': request.user.has_permission_type,
                'has_any_permission': request.user.has_any_permission,
                'has_all_permissions': request.user.has_all_permissions,
            }
        }
    return {
        'user_permissions': {
            'has_permission': lambda x: False,
            'has_permission_type': lambda x: False,
            'has_any_permission': lambda x: False,
            'has_all_permissions': lambda x: False,
        }
    } 