from django import forms
from django.utils.translation import gettext_lazy as _
from system_settings.models import EmailTemplate
from system_settings.utils import extract_variables_from_template
from django_summernote.widgets import SummernoteWidget

class EmailTemplateForm(forms.ModelForm):
    """
    Form để tạo và chỉnh sửa mẫu email.
    """
    class Meta:
        model = EmailTemplate
        fields = ['code', 'type', 'name', 'subject', 'content', 'description', 'is_html', 'is_active', 'default_recipients', 'default_cc']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': SummernoteWidget(attrs={'summernote': {'height': '300px', 'toolbar': [
                ['style', ['style', 'bold', 'italic', 'underline', 'clear']],
                ['font', ['strikethrough', 'superscript', 'subscript']],
                ['para', ['ul', 'ol', 'paragraph']],
                ['insert', ['table', 'link', 'picture']],
                ['color', ['color']],
                ['view', ['fullscreen', 'codeview']],
            ]}}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'default_recipients': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'a@x.com,b@y.com'}),
            'default_cc': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'cc1@x.com,cc2@y.com'}),
            'is_html': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Tự động trích xuất các biến từ nội dung và tiêu đề
        subject = cleaned_data.get('subject', '')
        content = cleaned_data.get('content', '')
        
        subject_vars = extract_variables_from_template(subject)
        content_vars = extract_variables_from_template(content)
        all_vars = list(set(subject_vars + content_vars))
        
        # Lưu danh sách biến vào trường variables
        variables_dict = {}
        for var in all_vars:
            variables_dict[var] = ""
            
        cleaned_data['variables'] = variables_dict
        
        return cleaned_data


class EmailTemplateTestForm(forms.Form):
    """
    Form để test một mẫu email với dữ liệu mẫu.
    """
    recipient = forms.EmailField(
        label=_('Email nhận'),
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    
    test_data = forms.CharField(
        label=_('Dữ liệu test (JSON)'),
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        required=False,
        help_text=_('Dữ liệu JSON để test mẫu email, định dạng: {"key": "value"}')
    )