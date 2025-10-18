"""
Views package initialization
"""
# Import views so they're available directly from system_settings.views
from .email_config_views import email_settings
from .email_template_views import (
    email_template_list,
    email_template_create,
    email_template_edit,
    email_template_delete,
    email_template_test,
    get_template_variables
)