from django.urls import path
from .views import MainDashboardView

urlpatterns = [
    path('', MainDashboardView.as_view(), name='main_dashboard'),
]