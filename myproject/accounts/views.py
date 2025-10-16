from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import CustomAuthenticationForm, UserRegistrationForm, UserUpdateForm
from django.contrib.auth import get_user_model

User = get_user_model()

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

class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Đăng ký tài khoản'
        return context

@login_required
def dashboard(request):
    # Redirect to the main dashboard instead
    return redirect('main_dashboard')

class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('main_dashboard')
    
    def get_object(self):
        return self.request.user
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cập nhật thông tin cá nhân'
        return context
