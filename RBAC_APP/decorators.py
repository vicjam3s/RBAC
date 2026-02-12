from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def login_required(view_func):
    """Decorator to ensure user is logged in"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'You must be logged in to access this page.')
            return redirect('rbac_app:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(role_name):
    """
    Decorator to check if user has a specific role or higher
    Usage: @role_required('reader') or @role_required('editor') or @role_required('author')
    """
    ROLE_HIERARCHY = {
        'reader': 0,
        'editor': 1,
        'author': 2,
    }
    
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'You must be logged in.')
                return redirect('rbac_app:login')
            
            # Superusers have all permissions
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            try:
                user_role = request.user.user_role
                user_role_level = ROLE_HIERARCHY.get(user_role.role.name, -1)
                required_role_level = ROLE_HIERARCHY.get(role_name, -1)
                
                if user_role_level >= required_role_level:
                    return view_func(request, *args, **kwargs)
                else:
                    messages.error(request, f'You need {role_name} role or higher to access this page.')
                    return redirect('rbac_app:blog')
            except:
                messages.error(request, 'You do not have a role assigned.')
                return redirect('rbac_app:blog')
        return wrapper
    return decorator

