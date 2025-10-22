from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Nhân hai số"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def div(value, arg):
    """Chia hai số"""
    try:
        if int(arg) == 0:
            return 0
        return int(value) // int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def percentage(value, total):
    """Tính phần trăm"""
    try:
        if int(total) == 0:
            return 0
        return int((int(value) / int(total)) * 100)
    except (ValueError, TypeError):
        return 0
