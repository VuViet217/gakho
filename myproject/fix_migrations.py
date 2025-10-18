"""
Script để sửa lỗi migration history
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.db import connection

# Xóa migration suppliers.0002 tạm thời
with connection.cursor() as cursor:
    try:
        cursor.execute(
            "DELETE FROM django_migrations WHERE app='suppliers' AND name='0002_purchaseorderitem'"
        )
        print("✓ Đã xóa migration suppliers.0002 khỏi database")
    except Exception as e:
        print(f"Lỗi: {e}")

print("\nHoàn tất! Bây giờ bạn có thể chạy:")
print("1. python manage.py migrate inventory")
print("2. python manage.py migrate suppliers")
print("3. python manage.py makemigrations accounts")
print("4. python manage.py migrate accounts")
