from django.urls import path
from .views import MainDashboardView, TestDashboardView

urlpatterns = [
    path('', MainDashboardView.as_view(), name='main_dashboard'),
    path('test/', TestDashboardView.as_view(), name='test_dashboard'),
]