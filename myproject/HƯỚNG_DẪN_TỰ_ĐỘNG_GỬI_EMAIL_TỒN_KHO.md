# 📧 Hướng dẫn Thiết lập Tự động Gửi Email Cảnh báo Tồn kho

## 🎯 Tổng quan

Hệ thống đã có sẵn **management command** để quét sản phẩm sắp hết hàng và tự động gửi email cảnh báo. Bạn cần thiết lập **scheduled task** (Windows) hoặc **cron job** (Linux) để chạy định kỳ.

## ✅ Command đã có sẵn

```bash
python manage.py send_low_stock_notifications
```

### Tính năng:
- ✅ Tự động quét tất cả sản phẩm có `current_quantity <= minimum_quantity`
- ✅ Gửi email theo mẫu `low_stock_alert` đã được cấu hình
- ✅ Tự động lấy danh sách người nhận từ trường **"Người nhận mặc định"** và **"CC mặc định"** trong mẫu email
- ✅ Hiển thị log chi tiết về số lượng sản phẩm và trạng thái gửi email

### Tham số command:

| Tham số | Mô tả | Mặc định |
|---------|-------|----------|
| `--template` | Mã mẫu email sử dụng | `low_stock_alert` |
| `--force` | Bắt buộc gửi ngay cả khi không có người nhận | False |

### Ví dụ sử dụng:

```bash
# Gửi email cảnh báo bình thường
python manage.py send_low_stock_notifications

# Gửi email test (bỏ qua kiểm tra người nhận)
python manage.py send_low_stock_notifications --force

# Sử dụng mẫu email khác
python manage.py send_low_stock_notifications --template custom_template
```

---

## 🪟 Thiết lập trên Windows (Task Scheduler)

### Bước 1: Tạo file batch script

Tạo file `send_low_stock_alert.bat` trong thư mục `myproject`:

```batch
@echo off
cd /d "C:\Code\khoga\myproject"
"C:\Code\khoga\venv\Scripts\python.exe" manage.py send_low_stock_notifications >> logs\low_stock_email.log 2>&1
echo ========================== >> logs\low_stock_email.log
```

**Lưu ý**: Thay đổi đường dẫn cho phù hợp với máy của bạn.

### Bước 2: Tạo thư mục logs

```powershell
cd C:\Code\khoga\myproject
mkdir logs
```

### Bước 3: Mở Task Scheduler

1. Nhấn `Win + R`, gõ `taskschd.msc` và Enter
2. Click **"Create Basic Task..."** ở panel bên phải

### Bước 4: Cấu hình Task

#### General Tab:
- **Name**: `Low Stock Email Alert`
- **Description**: `Tự động gửi email cảnh báo khi sản phẩm sắp hết hàng`
- ☑️ **Run whether user is logged on or not**
- ☑️ **Run with highest privileges**

#### Triggers Tab:
Click **"New..."** để thêm trigger:

**Tùy chọn 1: Chạy hàng ngày**
- **Begin the task**: On a schedule
- **Settings**: Daily
- **Start**: 08:00:00 AM (hoặc giờ bạn muốn)
- **Recur every**: 1 days
- ☑️ **Enabled**

**Tùy chọn 2: Chạy mỗi giờ**
- **Begin the task**: On a schedule
- **Settings**: Daily
- **Repeat task every**: 1 hour
- **For a duration of**: 1 day
- ☑️ **Enabled**

#### Actions Tab:
Click **"New..."**:
- **Action**: Start a program
- **Program/script**: Browse đến file `send_low_stock_alert.bat`
- **Start in**: `C:\Code\khoga\myproject`

#### Conditions Tab:
- ☐ Bỏ chọn **"Start the task only if the computer is on AC power"**
- ☑️ Chọn **"Wake the computer to run this task"** (nếu cần)

#### Settings Tab:
- ☑️ **Allow task to be run on demand**
- ☑️ **Run task as soon as possible after a scheduled start is missed**
- **If the task fails, restart every**: 1 minute
- **Attempt to restart up to**: 3 times

### Bước 5: Lưu và Test

1. Click **OK** để lưu task
2. Tìm task vừa tạo trong danh sách
3. Click chuột phải → **"Run"** để test ngay

### Bước 6: Kiểm tra log

Xem file log để kiểm tra kết quả:

```powershell
cat C:\Code\khoga\myproject\logs\low_stock_email.log
```

---

## 🐧 Thiết lập trên Linux (Cron Job)

### Bước 1: Tạo shell script

Tạo file `send_low_stock_alert.sh`:

```bash
#!/bin/bash
cd /path/to/khoga/myproject
/path/to/venv/bin/python manage.py send_low_stock_notifications >> logs/low_stock_email.log 2>&1
echo "==========================" >> logs/low_stock_email.log
```

Cấp quyền thực thi:

```bash
chmod +x send_low_stock_alert.sh
```

### Bước 2: Mở crontab

```bash
crontab -e
```

### Bước 3: Thêm cron job

**Chạy hàng ngày lúc 8:00 AM:**
```cron
0 8 * * * /path/to/khoga/myproject/send_low_stock_alert.sh
```

**Chạy mỗi giờ:**
```cron
0 * * * * /path/to/khoga/myproject/send_low_stock_alert.sh
```

**Chạy mỗi 30 phút:**
```cron
*/30 * * * * /path/to/khoga/myproject/send_low_stock_alert.sh
```

**Chạy mỗi ngày lúc 8:00 AM và 5:00 PM:**
```cron
0 8,17 * * * /path/to/khoga/myproject/send_low_stock_alert.sh
```

### Bước 4: Kiểm tra cron job

```bash
crontab -l
```

---

## 🔧 Thiết lập nâng cao với Django-Crontab (khuyến nghị)

### Cài đặt:

```bash
pip install django-crontab
```

### Thêm vào `settings.py`:

```python
INSTALLED_APPS = [
    # ... các app khác
    'django_crontab',
]

CRONJOBS = [
    # Chạy mỗi ngày lúc 8:00 AM
    ('0 8 * * *', 'django.core.management.call_command', ['send_low_stock_notifications']),
    
    # Hoặc chạy mỗi giờ
    # ('0 * * * *', 'django.core.management.call_command', ['send_low_stock_notifications']),
]
```

### Kích hoạt cron jobs:

```bash
python manage.py crontab add
```

### Quản lý cron jobs:

```bash
# Xem danh sách
python manage.py crontab show

# Xóa tất cả
python manage.py crontab remove
```

---

## 🎨 Thiết lập với Celery Beat (khuyến nghị cho production)

### Cài đặt:

```bash
pip install celery redis django-celery-beat
```

### Tạo file `myproject/celery.py`:

```python
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-low-stock-alerts-daily': {
        'task': 'inventory.tasks.send_low_stock_alerts',
        'schedule': crontab(hour=8, minute=0),  # 8:00 AM mỗi ngày
    },
}
```

### Tạo file `inventory/tasks.py`:

```python
from celery import shared_task
from django.core.management import call_command

@shared_task
def send_low_stock_alerts():
    call_command('send_low_stock_notifications')
```

### Chạy Celery:

```bash
# Worker
celery -A myproject worker -l info

# Beat scheduler (cửa sổ terminal riêng)
celery -A myproject beat -l info
```

---

## 📊 Giám sát và Logging

### Xem log gần đây:

**Windows:**
```powershell
Get-Content -Tail 50 C:\Code\khoga\myproject\logs\low_stock_email.log
```

**Linux:**
```bash
tail -f /path/to/logs/low_stock_email.log
```

### Log format mẫu:

```
Tìm thấy 3 sản phẩm dưới ngưỡng tối thiểu.
Đã gửi thông báo tới: ['kho@company.com', 'quanly@company.com']
==========================
Không có sản phẩm dưới ngưỡng.
==========================
```

---

## ⚠️ Troubleshooting

### Lỗi: "Không có người nhận mặc định trong mẫu"

**Nguyên nhân**: Chưa cấu hình người nhận trong mẫu email.

**Giải pháp**:
1. Truy cập: http://127.0.0.1:8000/system/email/templates/
2. Chỉnh sửa mẫu "Cảnh báo tồn kho thấp"
3. Điền vào trường **"Người nhận mặc định"**: `kho@company.com,quanly@company.com`
4. Lưu lại

### Lỗi: "Không tìm thấy mẫu email"

**Nguyên nhân**: Chưa chạy command tạo mẫu.

**Giải pháp**:
```bash
python manage.py create_low_stock_template
```

### Lỗi: SMTP connection timeout

**Nguyên nhân**: Cấu hình SMTP chưa đúng.

**Giải pháp**: Kiểm tra `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Hoặc SMTP server của bạn
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Task Scheduler không chạy

**Giải pháp**:
1. Kiểm tra **Task Scheduler Library** → **History** tab
2. Enable history nếu chưa bật: Actions → **Enable All Tasks History**
3. Kiểm tra log file
4. Đảm bảo user có quyền thực thi

---

## 📝 Checklist Triển khai

- [ ] Đã cấu hình người nhận mặc định trong mẫu email
- [ ] Đã test command thủ công: `python manage.py send_low_stock_notifications --force`
- [ ] Đã tạo file batch/shell script
- [ ] Đã tạo thư mục logs
- [ ] Đã thiết lập Task Scheduler / Cron Job
- [ ] Đã test chạy task/cron job
- [ ] Đã kiểm tra log file
- [ ] Đã verify email đã được gửi thành công

---

## 🚀 Khuyến nghị

### Cho môi trường Development/Testing:
- Sử dụng **Windows Task Scheduler** hoặc **Cron Job**
- Chạy mỗi ngày 1 lần vào buổi sáng (8:00 AM)

### Cho môi trường Production:
- Sử dụng **Celery Beat** với Redis
- Giám sát logs qua hệ thống logging tập trung (ELK Stack, Sentry)
- Thiết lập alert khi gửi email thất bại
- Backup logs định kỳ

---

**Cập nhật lần cuối**: 21/10/2025
**Phiên bản**: 1.0
