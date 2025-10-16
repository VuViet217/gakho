from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

# Decorator để thêm vào các view
def no_cache_view(view_func):
    return never_cache(view_func)

# Decorator để thêm vào các class-based view
def no_cache_class_view(cls):
    return method_decorator(never_cache, name='dispatch')(cls)