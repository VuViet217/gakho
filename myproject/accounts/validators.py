from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class MinimumLengthValidator:
    """
    Xác thực mật khẩu có độ dài tối thiểu.
    """
    def __init__(self, min_length=6):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("Mật khẩu phải có ít nhất %(min_length)d ký tự."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return _(
            "Mật khẩu của bạn phải chứa ít nhất %(min_length)d ký tự."
            % {'min_length': self.min_length}
        )