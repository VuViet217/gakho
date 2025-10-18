# Hướng dẫn thiết lập chức năng yêu cầu cấp phát

## 1. Chạy các lệnh để tạo mẫu email và menu

```bash
# Tạo các mẫu email mặc định cho chức năng yêu cầu cấp phát
python manage.py create_request_email_templates

# Tạo/cập nhật các menu cho chức năng yêu cầu cấp phát
python manage.py create_inventory_menus
```

## 2. Quy trình xử lý yêu cầu cấp phát

Chức năng yêu cầu cấp phát có quy trình xử lý như sau:

1. **Người dùng tạo yêu cầu**:
   - Tạo yêu cầu mới với trạng thái "Bản nháp"
   - Có thể chỉnh sửa, xóa hoặc gửi yêu cầu để phê duyệt

2. **Gửi yêu cầu phê duyệt**:
   - Khi người dùng gửi yêu cầu, trạng thái chuyển thành "Chờ phê duyệt"
   - Hệ thống gửi email thông báo cho người quản lý

3. **Quản lý phê duyệt/từ chối**:
   - Quản lý có thể phê duyệt hoặc từ chối yêu cầu
   - Nếu phê duyệt: trạng thái chuyển thành "Đã phê duyệt" và gửi email thông báo
   - Nếu từ chối: trạng thái chuyển thành "Bị từ chối" và gửi email thông báo với lý do từ chối

4. **Quản lý kho lên lịch cấp phát**:
   - Sau khi yêu cầu được phê duyệt, quản lý kho lên lịch cấp phát
   - Trạng thái chuyển thành "Đã lên lịch" và gửi email thông báo

5. **Hoàn thành yêu cầu**:
   - Quản lý kho đánh dấu yêu cầu đã hoàn thành
   - Trạng thái chuyển thành "Đã hoàn thành" và gửi email thông báo

## 3. Phân quyền người dùng

Chức năng yêu cầu cấp phát phân quyền người dùng như sau:

- **Tất cả người dùng**:
  - Tạo yêu cầu mới
  - Xem danh sách yêu cầu của mình

- **Quản lý (Manager)**:
  - Phê duyệt/từ chối yêu cầu của nhân viên

- **Quản lý kho (Warehouse)**:
  - Lên lịch cấp phát
  - Đánh dấu yêu cầu đã hoàn thành

- **Quản trị viên (Admin)**:
  - Có tất cả quyền trên
  - Xem danh sách tất cả các yêu cầu

## 4. Cấu trúc thư mục

```
inventory_requests/
├── management/
│   └── commands/
│       ├── __init__.py
│       ├── create_request_email_templates.py
│       └── create_inventory_menus.py
├── migrations/
├── templates/
│   └── inventory_requests/
│       ├── my_approvals.html
│       ├── my_requests.html
│       ├── request_detail.html
│       ├── request_form.html
│       ├── request_list.html
│       └── warehouse_requests.html
├── __init__.py
├── admin.py
├── apps.py
├── forms.py
├── models.py
├── tests.py
├── urls.py
└── views.py
```

## 5. Các mẫu email được tạo

1. **request_created**: Thông báo tạo yêu cầu mới
2. **pending_approval**: Thông báo yêu cầu chờ phê duyệt
3. **request_approved**: Thông báo yêu cầu được phê duyệt
4. **request_rejected**: Thông báo yêu cầu bị từ chối
5. **warehouse_scheduled**: Thông báo yêu cầu đã được lên lịch cấp phát
6. **request_completed**: Thông báo yêu cầu đã hoàn thành