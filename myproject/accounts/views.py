from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import (
    CustomAuthenticationForm, 
    UserRegistrationForm, 
    UserUpdateForm,
    UserProfileForm,
    CustomPasswordChangeForm
)
from django.contrib.auth import get_user_model

User = get_user_model()


# === Views đăng nhập/đăng xuất ===

class CustomLoginView(LoginView):
    template_name = 'accounts/login_new.html'
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Đăng nhập'
        return context


class CustomLogoutView(LogoutView):
    next_page = 'login'
    
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


# === Views quản lý người dùng (Admin) ===

def is_admin_or_sm(user):
    """Kiểm tra user có phải admin hoặc SM"""
    return user.is_authenticated and (user.is_superuser or user.role in ['sm', 'admin'])


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Danh sách người dùng"""
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def test_func(self):
        return is_admin_or_sm(self.request.user)
    
    def get_queryset(self):
        queryset = User.objects.all().select_related('manager').order_by('-date_joined')
        
        # Tìm kiếm
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(department__icontains=search)
            )
        
        # Lọc theo vai trò
        role = self.request.GET.get('role', '')
        if role:
            queryset = queryset.filter(role=role)
        
        # Lọc theo trạng thái
        status = self.request.GET.get('status', '')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Danh sách người dùng'
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_role'] = self.request.GET.get('role', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['role_choices'] = User.ROLE_CHOICES
        return context


class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Tạo người dùng mới"""
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user_list')
    
    def test_func(self):
        return is_admin_or_sm(self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, f'Đã tạo tài khoản {form.instance.username} thành công!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tạo người dùng mới'
        context['button_text'] = 'Tạo tài khoản'
        return context


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Cập nhật thông tin người dùng (Admin)"""
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user_list')
    
    def test_func(self):
        return is_admin_or_sm(self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, f'Đã cập nhật thông tin {form.instance.username} thành công!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Cập nhật: {self.object.get_full_name() or self.object.username}'
        context['button_text'] = 'Cập nhật'
        return context


class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Chi tiết người dùng"""
    model = User
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user_detail'
    
    def test_func(self):
        return is_admin_or_sm(self.request.user) or self.request.user == self.get_object()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Thông tin: {self.object.get_full_name() or self.object.username}'
        
        # Lấy danh sách nhân viên cấp dưới
        context['subordinates'] = User.objects.filter(manager=self.object).order_by('first_name', 'last_name')
        
        return context


@login_required
@user_passes_test(is_admin_or_sm)
def user_delete(request, pk):
    """Xóa người dùng"""
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'Đã xóa người dùng {username}!')
        return redirect('user_list')
    
    return render(request, 'accounts/user_confirm_delete.html', {
        'user_detail': user,
        'title': f'Xóa người dùng: {user.username}'
    })


# === Views profile cá nhân ===

@login_required
def profile_view(request):
    """Xem và chỉnh sửa thông tin cá nhân"""
    user = request.user
    form_type = request.POST.get('form_type')
    
    # Form chỉnh sửa thông tin
    if request.method == 'POST' and form_type == 'profile':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        password_form = CustomPasswordChangeForm(user=user)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã cập nhật thông tin cá nhân thành công!')
            return redirect('profile_view')
    
    # Form đổi mật khẩu
    elif request.method == 'POST' and form_type == 'password':
        form = UserProfileForm(instance=user)
        password_form = CustomPasswordChangeForm(user=user, data=request.POST)
        
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Giữ session sau khi đổi mật khẩu
            messages.success(request, 'Đã đổi mật khẩu thành công!')
            return redirect('profile_view')
    else:
        form = UserProfileForm(instance=user)
        password_form = CustomPasswordChangeForm(user=user)
    
    # Lấy danh sách tất cả users có vai trò quản lý
    potential_managers = User.objects.filter(
        role__in=['sm', 'admin', 'manager']
    ).exclude(pk=user.pk).order_by('first_name', 'last_name')
    
    return render(request, 'accounts/profile.html', {
        'form': form,
        'password_form': password_form,
        'title': 'Thông tin cá nhân',
        'user': user,
        'potential_managers': potential_managers
    })


@login_required
def dashboard(request):
    """Redirect to the main dashboard"""
    return redirect('main_dashboard')
