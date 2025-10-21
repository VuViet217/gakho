#!/bin/bash
# ========================================
# Script tự động gửi email cảnh báo tồn kho thấp
# ========================================

# Đường dẫn tuyệt đối (thay đổi cho phù hợp)
PROJECT_DIR="/path/to/khoga/myproject"
PYTHON_BIN="/path/to/khoga/venv/bin/python"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/low_stock_email.log"

# Chuyển đến thư mục project
cd "$PROJECT_DIR" || exit 1

# Tạo thư mục logs nếu chưa có
mkdir -p "$LOG_DIR"

# Ghi thời gian bắt đầu
echo "" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Bắt đầu kiểm tra tồn kho" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"

# Chạy command
"$PYTHON_BIN" manage.py send_low_stock_notifications >> "$LOG_FILE" 2>&1

# Ghi thời gian kết thúc
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Hoàn thành" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
