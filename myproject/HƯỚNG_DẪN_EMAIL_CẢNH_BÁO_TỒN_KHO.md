# 📧 Hướng dẫn sử dụng Email Cảnh báo Tồn kho Thấp

## 🎯 Tổng quan
Mẫu email này được thiết kế chuyên nghiệp, tương thích hoàn toàn với Outlook và các email client phổ biến khác. Email sẽ tự động gửi thông báo khi có sản phẩm đạt ngưỡng cảnh báo sắp hết hàng.

## ✨ Tính năng nổi bật

### 1. **Thiết kế chuyên nghiệp**
- ✅ Tương thích 100% với Outlook
- ✅ Responsive design - hiển thị đẹp trên mọi thiết bị
- ✅ Sử dụng table-based layout cho độ tương thích cao
- ✅ Màu sắc và typography chuyên nghiệp
- ✅ Icon và badge trạng thái trực quan

### 2. **Cấu trúc email**
- **Header**: Logo với icon cảnh báo và gradient đỏ nổi bật
- **Alert Box**: Thông báo tóm tắt số lượng sản phẩm cảnh báo
- **Bảng sản phẩm**: Hiển thị chi tiết các sản phẩm cần nhập hàng
  - Mã sản phẩm
  - Tên sản phẩm
  - Tồn kho hiện tại (màu đỏ nhấn mạnh)
  - Ngưỡng tối thiểu
  - Badge trạng thái
- **Khuyến nghị hành động**: Gợi ý các bước cần thực hiện
- **Footer**: Thông tin timestamp và copyright

### 3. **Hỗ trợ người nhận và CC**
Trong form quản lý mẫu email, bạn có thể cấu hình:
- **Người nhận mặc định (To)**: Danh sách email người nhận chính
- **CC mặc định**: Danh sách email được CC

## 🚀 Cách sử dụng

### Bước 1: Truy cập quản lý mẫu email
```
URL: http://127.0.0.1:8000/system/email/templates/
```

### Bước 2: Tìm mẫu "Cảnh báo tồn kho thấp"
- Tìm mẫu có tên: **"Cảnh báo tồn kho thấp"**
- Mã mẫu: `low_stock_alert`

### Bước 3: Cấu hình người nhận
1. Click vào mẫu email để chỉnh sửa
2. Điền vào trường **"Người nhận mặc định"**:
   ```
   Ví dụ: kho@company.com,quanly@company.com
   ```
3. Điền vào trường **"CC mặc định"** (nếu cần):
   ```
   Ví dụ: giamdoc@company.com,ketoan@company.com
   ```
4. Lưu lại

### Bước 4: Kiểm tra mẫu email
- Mở file `PREVIEW_LOW_STOCK_EMAIL.html` trong trình duyệt để xem trước
- Hoặc sử dụng chức năng "Test Email" trong hệ thống

## 📝 Các biến có sẵn trong mẫu

Mẫu email hỗ trợ các biến sau (sử dụng cú pháp `{{ variable_name }}`):

| Biến | Mô tả | Ví dụ |
|------|-------|-------|
| `{{ count }}` | Số lượng sản phẩm cảnh báo | 3 |
| `{{ products }}` | Danh sách sản phẩm (list) | Array các object sản phẩm |
| `{{ date }}` | Ngày giờ gửi email | 21/10/2025 15:45:30 |

### Cấu trúc object `products`:
```python
{
    'product_code': 'SP001',
    'name': 'Bút bi xanh Parker',
    'current_quantity': 5,
    'minimum_quantity': 10,
    'unit': 'cái'
}
```

## 🔧 Tùy chỉnh mẫu email

### Thay đổi màu sắc chủ đạo
Tìm và thay đổi các giá trị màu trong mẫu:
- **Header gradient**: `#dc3545` và `#c82333` (đỏ)
- **Primary color**: `#0d6efd` (xanh dương)
- **Warning color**: `#ffc107` (vàng)

### Thay đổi logo/tên công ty
Tìm dòng:
```html
<strong style="color: #0d6efd;">Hệ thống quản lý kho OVNC</strong>
```
Thay "OVNC" bằng tên công ty của bạn.

### Thêm/bớt cột trong bảng
Chỉnh sửa phần `<th>` (header) và `<td>` (data) trong bảng sản phẩm.

## 🔄 Cách tự động gửi email

### Tạo scheduled task (Cronjob)
```python
# Trong file views.py hoặc management command
from system_settings.template_email_service import TemplateEmailService

def send_low_stock_alerts():
    # Lấy danh sách sản phẩm tồn kho thấp
    low_stock_products = Product.objects.filter(
        current_quantity__lte=F('minimum_quantity')
    )
    
    if low_stock_products.exists():
        # Chuẩn bị dữ liệu
        products_data = [{
            'product_code': p.product_code,
            'name': p.name,
            'current_quantity': p.current_quantity,
            'minimum_quantity': p.minimum_quantity,
            'unit': p.unit
        } for p in low_stock_products]
        
        context = {
            'count': len(products_data),
            'products': products_data,
            'date': timezone.now().strftime('%d/%m/%Y %H:%M:%S')
        }
        
        # Gửi email
        service = TemplateEmailService()
        service.send_template_email(
            template_code='low_stock_alert',
            context=context
        )
```

### Lên lịch tự động (Django Celery)
```python
# tasks.py
from celery import shared_task

@shared_task
def daily_low_stock_check():
    send_low_stock_alerts()

# Cấu hình trong settings.py
CELERY_BEAT_SCHEDULE = {
    'check-low-stock-daily': {
        'task': 'tasks.daily_low_stock_check',
        'schedule': crontab(hour=8, minute=0),  # 8:00 AM mỗi ngày
    },
}
```

## 🎨 Preview

Xem trước mẫu email tại: `PREVIEW_LOW_STOCK_EMAIL.html`

## ✅ Checklist triển khai

- [ ] Đã tạo mẫu email trong database (chạy `python manage.py create_low_stock_template`)
- [ ] Đã cấu hình người nhận mặc định và CC
- [ ] Đã test gửi email thử
- [ ] Đã thiết lập cronjob/celery task để gửi tự động
- [ ] Đã kiểm tra email trên Outlook
- [ ] Đã kiểm tra email trên Gmail/Yahoo (nếu cần)

## 🆘 Troubleshooting

### Email không hiển thị đúng trong Outlook?
- Kiểm tra xem có sử dụng CSS inline không (đã hỗ trợ)
- Tránh sử dụng flexbox, grid (đã không dùng)
- Sử dụng table-based layout (đã implement)

### Email không được gửi?
- Kiểm tra cấu hình SMTP trong settings
- Kiểm tra log Django để xem lỗi
- Verify email người gửi đã được cấu hình

### Biến không được thay thế?
- Kiểm tra tên biến trong template
- Kiểm tra context được truyền vào có đầy đủ không
- Xem log để debug

## 📞 Hỗ trợ

Nếu có vấn đề, vui lòng liên hệ team IT hoặc tạo issue trong hệ thống.

---
**Cập nhật lần cuối**: 21/10/2025
**Version**: 2.0 - Professional Edition
