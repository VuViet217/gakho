from django.urls import path
from . import views

urlpatterns = [
    # Department URLs
    path('departments/', views.department_list, name='department_list'),
    path('departments/create/', views.department_create, name='department_create'),
    path('departments/<int:pk>/update/', views.department_update, name='department_update'),
    path('departments/<int:pk>/delete/', views.department_delete, name='department_delete'),
    
    # Employee URLs
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/<int:pk>/update/', views.employee_update, name='employee_update'),
    path('employees/<int:pk>/detail/', views.employee_detail, name='employee_detail'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    
    # Import/Export URLs
    path('employees/import/', views.import_employees, name='import_employees'),
    path('employees/export/', views.export_employees, name='export_employees'),
    path('departments/import/', views.import_departments, name='import_departments'),
    path('departments/export/', views.export_departments, name='export_departments'),
]