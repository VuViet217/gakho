import mysql.connector

# Kết nối với MySQL server
try:
    # Kết nối với MySQL mà không chỉ định database
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        port=3306
    )
    
    cursor = mydb.cursor()
    
    # Xóa cơ sở dữ liệu nếu tồn tại
    cursor.execute("DROP DATABASE IF EXISTS khoga")
    
    # Tạo cơ sở dữ liệu mới
    cursor.execute("CREATE DATABASE khoga CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    
    print("Đã tạo lại cơ sở dữ liệu thành công!")
    
except mysql.connector.Error as err:
    print(f"Lỗi: {err}")
finally:
    if 'mydb' in locals() and mydb.is_connected():
        cursor.close()
        mydb.close()
        print("Đã đóng kết nối MySQL.")