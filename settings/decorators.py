from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if not request.user.groups.filter(name__in=allowed_roles).exists():
                messages.error(request, "Você não tem permissão para acessar esta página.")
                return redirect('index')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator