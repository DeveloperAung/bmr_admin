from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied


def require_permission(permission_name):
    """
    Decorator to check if user has specific permission
    Usage: @require_permission('user_create')
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                if request.is_ajax():
                    return JsonResponse({'error': 'Authentication required'}, status=401)
                return redirect('login')
            
            if not request.user.has_permission(permission_name):
                if request.is_ajax():
                    return JsonResponse({'error': 'Permission denied'}, status=403)
                messages.error(request, f'You do not have permission to perform this action.')
                raise PermissionDenied("Permission denied")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def require_permission_type(permission_type):
    """
    Decorator to check if user has specific permission type
    Usage: @require_permission_type('create')
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                if request.is_ajax():
                    return JsonResponse({'error': 'Authentication required'}, status=401)
                return redirect('login')
            
            if not request.user.has_permission_type(permission_type):
                if request.is_ajax():
                    return JsonResponse({'error': 'Permission denied'}, status=403)
                messages.error(request, f'You do not have {permission_type} permission.')
                raise PermissionDenied("Permission denied")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def require_any_permission(permission_names):
    """
    Decorator to check if user has any of the specified permissions
    Usage: @require_any_permission(['user_create', 'user_update'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                if request.is_ajax():
                    return JsonResponse({'error': 'Authentication required'}, status=401)
                return redirect('login')
            
            if not request.user.has_any_permission(permission_names):
                if request.is_ajax():
                    return JsonResponse({'error': 'Permission denied'}, status=403)
                messages.error(request, 'You do not have sufficient permissions to perform this action.')
                raise PermissionDenied("Permission denied")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def require_all_permissions(permission_names):
    """
    Decorator to check if user has all of the specified permissions
    Usage: @require_all_permissions(['user_create', 'user_update'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                if request.is_ajax():
                    return JsonResponse({'error': 'Authentication required'}, status=401)
                return redirect('login')
            
            if not request.user.has_all_permissions(permission_names):
                if request.is_ajax():
                    return JsonResponse({'error': 'Permission denied'}, status=403)
                messages.error(request, 'You do not have all required permissions to perform this action.')
                raise PermissionDenied("Permission denied")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def require_role(role_title):
    """
    Decorator to check if user has specific role
    Usage: @require_role('Admin')
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                if request.is_ajax():
                    return JsonResponse({'error': 'Authentication required'}, status=401)
                return redirect('login')
            
            if not request.user.admin_user_role or request.user.admin_user_role.title != role_title:
                if request.is_ajax():
                    return JsonResponse({'error': 'Role required'}, status=403)
                messages.error(request, f'You must have {role_title} role to perform this action.')
                raise PermissionDenied("Role required")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def require_staff():
    """
    Decorator to check if user is staff
    Usage: @require_staff
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                if request.is_ajax():
                    return JsonResponse({'error': 'Authentication required'}, status=401)
                return redirect('login')
            
            if not request.user.is_staff:
                if request.is_ajax():
                    return JsonResponse({'error': 'Staff access required'}, status=403)
                messages.error(request, 'Staff access is required to perform this action.')
                raise PermissionDenied("Staff access required")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def require_superuser():
    """
    Decorator to check if user is superuser
    Usage: @require_superuser
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                if request.is_ajax():
                    return JsonResponse({'error': 'Authentication required'}, status=401)
                return redirect('login')
            
            if not request.user.is_superuser:
                if request.is_ajax():
                    return JsonResponse({'error': 'Superuser access required'}, status=403)
                messages.error(request, 'Superuser access is required to perform this action.')
                raise PermissionDenied("Superuser access required")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator 