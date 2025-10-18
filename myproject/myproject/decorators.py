from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps

# Decorator để thêm vào các view
def no_cache_view(view_func):
    return never_cache(view_func)

# Decorator để thêm vào các class-based view
def no_cache_class_view(cls):
    return method_decorator(never_cache, name='dispatch')(cls)

# Decorator yêu cầu đăng nhập và kiểm tra quyền theo vai trò
def role_required(allowed_roles=None):
    """
    Decorator để kiểm tra vai trò của người dùng
    allowed_roles: list các vai trò được phép truy cập (sm, admin, manager, staff)
                  hoặc 'all' để cho phép tất cả người dùng đã đăng nhập
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(reverse('accounts:login') + f'?next={request.path}')
                
            if allowed_roles == 'all':
                return view_func(request, *args, **kwargs)
                
            if allowed_roles is None or request.user.role in allowed_roles or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
                
            return HttpResponseForbidden("Bạn không có quyền truy cập chức năng này")
        return _wrapped_view
    return decorator