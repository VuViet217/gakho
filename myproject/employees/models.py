from django.db import models
from django.utils import timezone

class Department(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name="Mã bộ phận")
    name = models.CharField(max_length=100, verbose_name="Tên bộ phận")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Bộ phận"
        verbose_name_plural = "Bộ phận"
        ordering = ['name']

    def __str__(self):
        return f"{self.code} - {self.name}"


class Employee(models.Model):
    GENDER_CHOICES = (
        ('M', 'Nam'),
        ('F', 'Nữ'),
        ('O', 'Khác'),
    )

    employee_id = models.CharField(max_length=20, unique=True, verbose_name="Mã nhân viên")
    first_name = models.CharField(max_length=50, verbose_name="Tên")
    last_name = models.CharField(max_length=50, verbose_name="Họ")
    full_name = models.CharField(max_length=100, verbose_name="Họ và tên", blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="employees", verbose_name="Bộ phận")
    
    # Thông tin cá nhân - tất cả đều optional
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Ngày sinh")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', null=True, blank=True, verbose_name="Giới tính")
    id_card = models.CharField(max_length=20, blank=True, null=True, verbose_name="Số CMND/CCCD")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Số điện thoại")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    address = models.TextField(blank=True, null=True, verbose_name="Địa chỉ")
    
    # Thông tin công việc - tất cả đều optional
    position = models.CharField(max_length=100, blank=True, null=True, verbose_name="Chức vụ")
    join_date = models.DateField(null=True, blank=True, verbose_name="Ngày vào làm")
    status = models.BooleanField(default=True, verbose_name="Đang làm việc")
    
    # Thông tin hệ thống
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Nhân viên"
        verbose_name_plural = "Nhân viên"
        ordering = ['employee_id', 'last_name', 'first_name']

    def save(self, *args, **kwargs):
        # Tự động tạo full_name từ first_name và last_name
        self.full_name = f"{self.last_name} {self.first_name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_id} - {self.full_name}"
