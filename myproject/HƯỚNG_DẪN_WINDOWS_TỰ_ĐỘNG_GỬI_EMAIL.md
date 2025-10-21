# 📧 Hướng dẫn Thiết lập Tự động Gửi Email Cảnh báo Tồn kho (Windows)

## 🎯 Tổng quan

Hệ thống sẽ tự động quét sản phẩm sắp hết hàng và gửi email cảnh báo theo lịch trình bạn thiết lập.

## ✅ Bước 1: Cấu hình Email nhận cảnh báo

1. Truy cập: http://127.0.0.1:8000/system/email/templates/
2. Tìm và click vào mẫu **"Cảnh báo tồn kho thấp"**
3. Điền thông tin:
   - **Người nhận mặc định**: `kho@company.com,quanly@company.com` (các email cách nhau bằng dấu phẩy)
   - **CC mặc định**: `giamdoc@company.com` (nếu cần)
4. Click **Lưu**

## 🧪 Bước 2: Test thử Command

Mở PowerShell và chạy:

```powershell
cd C:\Code\khoga\myproject
C:\Code\khoga\venv\Scripts\python.exe manage.py send_low_stock_notifications --force
```

Nếu thành công, bạn sẽ thấy:
```
Tìm thấy X sản phẩm dưới ngưỡng tối thiểu.
Đã gửi thông báo tới: ['email1@company.com', 'email2@company.com']
```

## ⏰ Bước 3: Thiết lập Windows Task Scheduler

### Cách 1: Tự động (Khuyến nghị)

1. Mở PowerShell **với quyền Administrator** (chuột phải → Run as Administrator)

2. Chạy lệnh sau để tạo scheduled task tự động:

```powershell
# Tạo task chạy mỗi ngày lúc 8:00 sáng
$action = New-ScheduledTaskAction -Execute "C:\Code\khoga\myproject\send_low_stock_alert.bat"
$trigger = New-ScheduledTaskTrigger -Daily -At 8:00AM
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType S4U -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName "Low Stock Email Alert" -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description "Tự động gửi email cảnh báo khi sản phẩm sắp hết hàng"
```

3. Xong! Task đã được tạo và sẽ chạy mỗi ngày lúc 8:00 sáng.

### Cách 2: Thủ công (Qua giao diện)

#### Bước 3.1: Mở Task Scheduler

1. Nhấn `Win + R`
2. Gõ: `taskschd.msc`
3. Nhấn Enter

#### Bước 3.2: Tạo Task mới

1. Ở panel bên phải, click **"Create Basic Task..."**
2. Điền thông tin:
   - **Name**: `Low Stock Email Alert`
   - **Description**: `Tự động gửi email cảnh báo khi sản phẩm sắp hết hàng`
3. Click **Next**

#### Bước 3.3: Chọn lịch chạy (Trigger)

**Chọn Daily** (Mỗi ngày)
- Click **Next**
- Chọn thời gian: **8:00:00 AM** (hoặc giờ bạn muốn)
- **Recur every**: 1 days
- Click **Next**

#### Bước 3.4: Chọn Action

1. Chọn **"Start a program"**
2. Click **Next**
3. **Program/script**: Click **Browse** và chọn file:
   ```
   C:\Code\khoga\myproject\send_low_stock_alert.bat
   ```
4. **Start in**: Để trống (không cần điền)
5. Click **Next**

#### Bước 3.5: Hoàn tất

1. Review lại thông tin
2. ☑️ Tick vào **"Open the Properties dialog for this task when I click Finish"**
3. Click **Finish**

#### Bước 3.6: Cấu hình nâng cao

Trong hộp thoại Properties:

**Tab General:**
- ☑️ Chọn **"Run whether user is logged on or not"**
- ☑️ Chọn **"Run with highest privileges"**

**Tab Conditions:**
- ☐ Bỏ chọn **"Start the task only if the computer is on AC power"**

**Tab Settings:**
- ☑️ Chọn **"Allow task to be run on demand"**
- ☑️ Chọn **"Run task as soon as possible after a scheduled start is missed"**

Click **OK** để lưu.

## 🧪 Bước 4: Test Task Scheduler

1. Trong Task Scheduler, tìm task **"Low Stock Email Alert"**
2. Click chuột phải → **"Run"**
3. Kiểm tra log file:

```powershell
Get-Content C:\Code\khoga\myproject\logs\low_stock_email.log -Tail 20
```

## 📊 Bước 5: Xem Log

Mỗi lần chạy, hệ thống sẽ ghi log vào:
```
C:\Code\khoga\myproject\logs\low_stock_email.log
```

Xem log:

```powershell
# Xem 20 dòng cuối
Get-Content C:\Code\khoga\myproject\logs\low_stock_email.log -Tail 20

# Xem toàn bộ
notepad C:\Code\khoga\myproject\logs\low_stock_email.log
```

## 🔧 Tùy chỉnh Lịch chạy

Nếu muốn thay đổi lịch chạy:

### Chạy mỗi giờ:

1. Mở task trong Task Scheduler
2. Tab **Triggers** → Double click trigger hiện tại
3. Tick **"Repeat task every"**: **1 hour**
4. **For a duration of**: **1 day**
5. Click OK

### Chạy nhiều lần trong ngày:

Tạo nhiều trigger:
- Tab **Triggers** → Click **New...**
- Thêm trigger mới với thời gian khác (ví dụ: 8:00 AM, 1:00 PM, 5:00 PM)

## ⚠️ Xử lý sự cố

### Lỗi: "Không có người nhận mặc định"

**Giải pháp**: 
- Quay lại **Bước 1** và cấu hình email người nhận trong mẫu email

### Lỗi: Task không chạy

**Kiểm tra**:
1. Mở Task Scheduler
2. Tìm task → Tab **History** (phải enable trước)
3. Xem lỗi chi tiết

**Enable History**:
- Task Scheduler → Actions menu → **Enable All Tasks History**

### Lỗi: SMTP connection timeout

**Giải pháp**: Kiểm tra cấu hình SMTP trong settings:
- Mở file `C:\Code\khoga\myproject\myproject\settings.py`
- Tìm phần `EMAIL_*` và đảm bảo đúng thông tin

## 📝 Checklist

- [ ] Đã cấu hình email người nhận trong mẫu email
- [ ] Đã test command thủ công thành công
- [ ] Đã tạo task trong Task Scheduler
- [ ] Đã chạy test task thành công
- [ ] Đã kiểm tra log file
- [ ] Đã verify email nhận được

## 💡 Lưu ý

- Task sẽ chạy ngay cả khi bạn không đăng nhập Windows (nếu chọn "Run whether user is logged on or not")
- Máy tính phải bật để task chạy được
- Nếu máy tắt vào giờ đã lên lịch, task sẽ chạy ngay khi máy bật lại (nếu bật "Run task as soon as possible...")

## 🆘 Cần trợ giúp?

Nếu gặp vấn đề, hãy:
1. Kiểm tra log file
2. Chạy command thủ công để debug
3. Kiểm tra Task History trong Task Scheduler

---

**Cập nhật**: 21/10/2025
