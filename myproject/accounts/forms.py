from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Tên đăng nhập',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Tên đăng nhập', 
                'autocomplete': 'username',
                'autofocus': True
            }
        )
    )
    password = forms.CharField(
        label='Mật khẩu',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Mật khẩu', 
                'autocomplete': 'current-password'
            }
        )
    )


class UserRegistrationForm(UserCreationForm):
    """Form đăng ký tài khoản mới"""
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'role', 'department', 'phone', 'manager', 'auto_approve', 'profile_image', 'is_staff', 'is_superuser', 'is_active')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên đăng nhập'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Họ'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bộ phận'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Số điện thoại'}),
            'manager': forms.Select(attrs={'class': 'form-control select2'}),
            'auto_approve': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
        }
        labels = {
            'username': 'Tên đăng nhập',
            'first_name': 'Tên',
            'last_name': 'Họ',
            'email': 'Email',
            'role': 'Vai trò',
            'department': 'Bộ phận',
            'phone': 'Số điện thoại',
            'manager': 'Người quản lý',
            'auto_approve': 'Tự động phê duyệt',
            'profile_image': 'Ảnh đại diện',
            'is_staff': 'Quyền truy cập trang quản trị',
            'is_superuser': 'Quyền superuser',
            'is_active': 'Kích hoạt tài khoản',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Mật khẩu'}
        )
        self.fields['password1'].label = 'Mật khẩu'
        
        # Xóa các trường help_text mặc định của Django về quy định mật khẩu
        self.fields['password1'].help_text = ''
        
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Nhập lại mật khẩu'}
        )
        self.fields['password2'].label = 'Xác nhận mật khẩu'
        
        # Chỉ hiển thị SM, admin, manager trong danh sách người quản lý
        self.fields['manager'].queryset = User.objects.filter(
            role__in=['sm', 'admin', 'manager']
        ).order_by('first_name', 'last_name', 'username')
        
        # Các trường required
        self.fields['manager'].required = False
        self.fields['manager'].help_text = ''  # Xóa help text
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        
        # Mặc định là user thường, không phải admin/superuser
        self.fields['is_staff'].initial = False
        self.fields['is_superuser'].initial = False
        self.fields['is_active'].initial = True
    
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        manager = cleaned_data.get('manager')
        
        # SM không được có người quản lý
        if role == 'sm' and manager:
            raise ValidationError({
                'manager': 'SM (Senior Manager) không được có người quản lý.'
            })
        
        # Manager không còn bắt buộc cho các vai trò khác
        
        return cleaned_data
        
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Nếu người dùng cung cấp manager_email, lưu vào model
        if self.cleaned_data.get('manager_email'):
            user.manager_email = self.cleaned_data.get('manager_email')
        
        if commit:
            user.save()
            
        return user


class UserUpdateForm(UserChangeForm):
    """Form cập nhật thông tin người dùng (dành cho admin)"""
    password = None
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'role', 'department', 'phone', 'manager', 'auto_approve', 'profile_image', 'is_staff', 'is_superuser', 'is_active')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control select2'}),
            'auto_approve': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
        }
        labels = {
            'username': 'Tên đăng nhập',
            'first_name': 'Tên',
            'last_name': 'Họ',
            'email': 'Email',
            'role': 'Vai trò',
            'department': 'Bộ phận',
            'phone': 'Số điện thoại',
            'manager': 'Người quản lý',
            'auto_approve': 'Tự động phê duyệt',
            'profile_image': 'Ảnh đại diện',
            'is_staff': 'Quyền truy cập trang quản trị',
            'is_superuser': 'Quyền superuser',
            'is_active': 'Kích hoạt tài khoản',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Chỉ hiển thị SM, admin, manager trong danh sách người quản lý
        # Loại trừ chính user hiện tại
        manager_queryset = User.objects.filter(
            role__in=['sm', 'admin', 'manager']
        ).order_by('first_name', 'last_name', 'username')
        
        if self.instance and self.instance.pk:
            manager_queryset = manager_queryset.exclude(pk=self.instance.pk)
        
        self.fields['manager'].queryset = manager_queryset
        self.fields['manager'].required = False
        self.fields['manager'].help_text = ''  # Xóa help text
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
    
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        manager = cleaned_data.get('manager')
        
        # SM không được có người quản lý
        if role == 'sm' and manager:
            raise ValidationError({
                'manager': 'SM (Senior Manager) không được có người quản lý.'
            })
        
        # Manager không còn bắt buộc cho các vai trò khác
        
        return cleaned_data
        
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Nếu người dùng cung cấp manager_email, lưu vào model
        if self.cleaned_data.get('manager_email'):
            user.manager_email = self.cleaned_data.get('manager_email')
        
        if commit:
            user.save()
            
        return user


class UserProfileForm(forms.ModelForm):
    """Form chỉnh sửa thông tin cá nhân (dành cho user tự chỉnh sửa)"""
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'department', 'phone', 'manager', 'profile_image')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control select2', 'data-placeholder': 'Chọn người quản lý'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Tên',
            'last_name': 'Họ',
            'email': 'Email',
            'department': 'Bộ phận',
            'phone': 'Số điện thoại',
            'manager': 'Người quản lý',
            'profile_image': 'Ảnh đại diện',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        
        # Thiết lập queryset cho manager (tất cả users trừ chính mình)
        # Hiển thị tất cả người dùng đang hoạt động
        if self.instance and self.instance.pk:
            self.fields['manager'].queryset = User.objects.filter(
                is_active=True
            ).exclude(pk=self.instance.pk).order_by('first_name', 'last_name', 'username')
            self.fields['manager'].required = False
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Tự động cập nhật manager_name và manager_email từ manager
        if user.manager:
            user.manager_name = user.manager.get_full_name() or user.manager.username
            user.manager_email = user.manager.email
        
        if commit:
            user.save()
            
        return user
                
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Lưu thông tin người quản lý nếu được cung cấp
        if self.cleaned_data.get('manager_name'):
            user.manager_name = self.cleaned_data.get('manager_name')
            
        if self.cleaned_data.get('manager_email'):
            user.manager_email = self.cleaned_data.get('manager_email')
        
        if commit:
            user.save()
            
        return user


class CustomPasswordChangeForm(PasswordChangeForm):
    """Form đổi mật khẩu"""
    
    old_password = forms.CharField(
        label='Mật khẩu hiện tại',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nhập mật khẩu hiện tại'})
    )
    new_password1 = forms.CharField(
        label='Mật khẩu mới',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nhập mật khẩu mới'})
    )
    new_password2 = forms.CharField(
        label='Xác nhận mật khẩu mới',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nhập lại mật khẩu mới'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Xóa các trường help_text mặc định của Django về quy định mật khẩu
        self.fields['new_password1'].help_text = 'Mật khẩu cần có ít nhất 6 ký tự.'