from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Dashboard báo cáo tổng quan
    path('', views.reports_dashboard, name='dashboard'),
    
    # Báo cáo tháng
    path('monthly/', views.monthly_report, name='monthly_report'),
    path('monthly/<int:year>/<int:month>/', views.monthly_report_detail, name='monthly_report_detail'),
    path('monthly/<int:year>/<int:month>/close/', views.close_month, name='close_month'),
    path('monthly/<int:year>/<int:month>/pdf/', views.monthly_report_pdf, name='monthly_report_pdf'),
    
    # Báo cáo sản phẩm sắp hết
    path('low-stock/', views.low_stock_report, name='low_stock_report'),
    path('low-stock/pdf/', views.low_stock_report_pdf, name='low_stock_report_pdf'),
    
    # Kiểm kê
    path('audits/', views.audit_list, name='audit_list'),
    path('audits/create/', views.audit_create, name='audit_create'),
    path('audits/<int:audit_id>/', views.audit_detail, name='audit_detail'),
    path('audits/<int:audit_id>/edit/', views.audit_edit, name='audit_edit'),
    path('audits/<int:audit_id>/pdf/', views.audit_pdf, name='audit_pdf'),
    path('audits/<int:audit_id>/complete/', views.audit_complete, name='audit_complete'),
]
