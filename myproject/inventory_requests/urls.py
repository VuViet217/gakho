from django.urls import path
from . import views

app_name = 'inventory_requests'

urlpatterns = [
    # Quản lý yêu cầu cấp phát
    path('', views.inventory_request_list, name='inventory_request_list'),
    path('my-requests/', views.my_requests_list, name='my_requests'),
    path('my-approvals/', views.my_approvals_list, name='my_approval_requests'),
    path('create/', views.inventory_request_create, name='inventory_request_create'),
    path('<int:request_id>/', views.inventory_request_detail, name='inventory_request_detail'),
    path('<int:request_id>/edit/', views.inventory_request_edit, name='inventory_request_edit'),
    path('<int:request_id>/delete/', views.inventory_request_delete, name='inventory_request_delete'),
    path('<int:request_id>/submit/', views.inventory_request_submit, name='inventory_request_submit'),
    
    # Phê duyệt yêu cầu
    path('<int:request_id>/approve/', views.inventory_request_approve, name='inventory_request_approve'),
    path('<int:request_id>/reject/', views.inventory_request_reject, name='request_reject'),
    
    # Quản lý kho lên lịch và hoàn thành yêu cầu
    path('warehouse-requests/', views.warehouse_requests_list, name='warehouse_requests_list'),
    path('<int:request_id>/schedule/', views.inventory_request_schedule, name='inventory_request_schedule'),
    path('<int:request_id>/complete/', views.inventory_request_complete, name='inventory_request_complete'),
    path('<int:request_id>/print-delivery-note/', views.print_delivery_note, name='print_delivery_note'),
]