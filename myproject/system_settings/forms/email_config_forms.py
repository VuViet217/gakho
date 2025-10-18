from django import forms
from system_settings.models import EmailConfiguration

class EmailConfigurationForm(forms.ModelForm):
    """
    Form để cấu hình SMTP Email
    """
    smtp_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
        required=False,
        label='SMTP Password'
    )
    
    class Meta:
        model = EmailConfiguration
        fields = [
            'smtp_host', 'smtp_port', 'auth_method', 'smtp_username', 'smtp_password', 
            'from_email', 'use_tls', 'use_ssl', 'smtp_conn_timeout', 'smtp_timeout', 'is_active'
        ]
        widgets = {
            'smtp_host': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: smtp.gmail.com'}),
            'smtp_port': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'VD: 587 cho TLS, 465 cho SSL'}),
            'auth_method': forms.Select(attrs={'class': 'form-control'}),
            'smtp_username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên đăng nhập SMTP'}),
            'from_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email hiển thị khi gửi'}),
            'smtp_conn_timeout': forms.NumberInput(attrs={'class': 'form-control'}),
            'smtp_timeout': forms.NumberInput(attrs={'class': 'form-control'}),
            'use_tls': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'use_ssl': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class TestEmailForm(forms.Form):
    """
    Form để test gửi email
    """
    recipient = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Nhập email nhận thử nghiệm'}),
        required=True,
        label='Email nhận'
    )
    subject = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tiêu đề email'}),
        required=True,
        initial='Test Email từ OVNC Inventory',
        label='Tiêu đề'
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Nội dung email'}),
        required=True,
        initial='Đây là email test từ hệ thống OVNC Inventory. Nếu bạn nhận được email này, cấu hình SMTP đã hoạt động.',
        label='Nội dung'
    )