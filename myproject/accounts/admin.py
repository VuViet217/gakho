from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import UserRegistrationForm, UserUpdateForm

class CustomUserAdmin(UserAdmin):
    add_form = UserRegistrationForm
    form = UserUpdateForm
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'department', 'manager', 'is_active']
    list_filter = ['role', 'is_active', 'department', 'is_staff', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Thông tin cá nhân', {'fields': ('first_name', 'last_name', 'email', 'phone', 'profile_image')}),
        ('Quyền hạn', {'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'groups', 'user_permissions')}),
        ('Phòng ban & Quản lý', {'fields': ('department', 'manager', 'manager_name', 'manager_email')}),
        ('Ngày quan trọng', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'department', 'manager', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)
