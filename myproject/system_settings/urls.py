from django.urls import path
from system_settings import views

urlpatterns = [
    # Email configuration
    path('email/', views.email_settings, name='email_settings'),
    
    # Email templates
    path('email/templates/', views.email_template_list, name='email_template_list'),
    path('email/templates/create/', views.email_template_create, name='email_template_create'),
    path('email/templates/<int:template_id>/edit/', views.email_template_edit, name='email_template_edit'),
    path('email/templates/<int:template_id>/delete/', views.email_template_delete, name='email_template_delete'),
    path('email/templates/<int:template_id>/test/', views.email_template_test, name='email_template_test'),
    path('email/templates/variables/', views.get_template_variables, name='get_template_variables'),
    
    # Backup
    path('backup/', views.backup_settings, name='backup_settings'),
    path('backup/create/', views.create_backup, name='create_backup'),
    path('backup/<int:backup_id>/download/', views.download_backup, name='download_backup'),
    path('backup/<int:backup_id>/restore/', views.restore_backup, name='restore_backup'),
    path('backup/<int:backup_id>/delete/', views.delete_backup, name='delete_backup'),
]