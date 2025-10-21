@echo off
REM ========================================
REM Script tự động gửi email cảnh báo tồn kho thấp
REM ========================================

REM Chuyển đến thư mục project
cd /d "C:\Code\khoga\myproject"

REM Tạo thư mục logs nếu chưa có
if not exist "logs" mkdir logs

REM Ghi thời gian bắt đầu
echo. >> logs\low_stock_email.log
echo ========================================== >> logs\low_stock_email.log
echo [%date% %time%] Bat dau kiem tra ton kho >> logs\low_stock_email.log
echo ========================================== >> logs\low_stock_email.log

REM Chạy command
"C:\Code\khoga\venv\Scripts\python.exe" manage.py send_low_stock_notifications >> logs\low_stock_email.log 2>&1

REM Ghi thời gian kết thúc
echo [%date% %time%] Hoan thanh >> logs\low_stock_email.log
echo. >> logs\low_stock_email.log
