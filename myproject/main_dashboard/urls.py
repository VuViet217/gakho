from django.urls import path
from .views import MainDashboardView, TestDashboardView
from .admin_views import fix_issued_quantity

urlpatterns = [
    path('', MainDashboardView.as_view(), name='main_dashboard'),
    path('test/', TestDashboardView.as_view(), name='test_dashboard'),
    path('admin/fix-issued/', fix_issued_quantity, name='fix_issued_quantity'),
]