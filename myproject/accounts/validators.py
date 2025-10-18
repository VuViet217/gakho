from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

def validate_minimum_length(password):
    """
    Xác thực mật khẩu có độ dài tối thiểu 6 ký tự.
    """
    if len(password) < 6:
        raise ValidationError(
            _("Mật khẩu phải có ít nhất 6 ký tự."),
            code='password_too_short',
        )