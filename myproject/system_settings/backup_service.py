"""
Service xử lý backup và restore database và media files
"""
import os
import shutil
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path
import zipfile
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import timezone
from .models import BackupHistory, BackupConfiguration


class BackupService:
    """Service để backup và restore database và media files"""
    
    def __init__(self):
        self.db_config = settings.DATABASES['default']
        self.db_engine = self.db_config['ENGINE']
        self.db_name = self.db_config['NAME']
        self.media_root = settings.MEDIA_ROOT
        self.backup_dir = os.path.join(settings.MEDIA_ROOT, 'backups')
        
        # Tạo thư mục backup nếu chưa có
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def create_backup(self, backup_type='full', user=None, is_auto=False):
        """
        Tạo backup mới
        
        Args:
            backup_type: 'full', 'database', hoặc 'media'
            user: User object tạo backup
            is_auto: Boolean - backup tự động hay không
        
        Returns:
            BackupHistory object
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_{backup_type}_{timestamp}.zip"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        # Tạo backup history record
        backup_history = BackupHistory.objects.create(
            backup_type=backup_type,
            backup_name=backup_name,
            status='pending',
            created_by=user,
            is_auto=is_auto
        )
        
        try:
            # Tạo file zip
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Backup database
                if backup_type in ['full', 'database']:
                    self._backup_database(zipf)
                
                # Backup media files
                if backup_type in ['full', 'media']:
                    self._backup_media(zipf)
            
            # Lưu thông tin file
            file_size = os.path.getsize(backup_path)
            
            # Save to model's FileField
            with open(backup_path, 'rb') as f:
                backup_history.backup_file.save(
                    backup_name,
                    ContentFile(f.read()),
                    save=False
                )
            
            backup_history.file_size = file_size
            backup_history.status = 'success'
            backup_history.save()
            
            # Xóa file tạm
            if os.path.exists(backup_path):
                os.remove(backup_path)
            
            # Cập nhật cấu hình backup
            self._update_backup_config(success=True)
            
            # Cleanup old backups
            self._cleanup_old_backups()
            
            return backup_history
            
        except Exception as e:
            backup_history.status = 'failed'
            backup_history.error_message = str(e)
            backup_history.save()
            
            # Xóa file backup nếu có lỗi
            if os.path.exists(backup_path):
                os.remove(backup_path)
            
            # Cập nhật cấu hình backup
            self._update_backup_config(success=False)
            
            raise e
    
    def _backup_database(self, zipf):
        """Backup database (MySQL hoặc SQLite)"""
        if 'mysql' in self.db_engine:
            self._backup_mysql(zipf)
        elif 'sqlite' in self.db_engine:
            self._backup_sqlite(zipf)
        else:
            raise Exception(f"Database engine không được hỗ trợ: {self.db_engine}")
    
    def _backup_mysql(self, zipf):
        """Backup MySQL database bằng Python"""
        import MySQLdb
        backup_sql_path = os.path.join(self.backup_dir, 'db_temp.sql')
        
        # Lấy thông tin database
        db_user = self.db_config.get('USER', 'root')
        db_password = self.db_config.get('PASSWORD', '')
        db_host = self.db_config.get('HOST', 'localhost')
        db_port = int(self.db_config.get('PORT', '3306'))
        db_name = self.db_name
        
        try:
            # Kết nối database
            conn = MySQLdb.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_password,
                database=db_name
            )
            cursor = conn.cursor()
            
            # Mở file để ghi
            with open(backup_sql_path, 'w', encoding='utf-8') as f:
                # Lấy danh sách tables
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                
                # Ghi header
                f.write(f"-- MySQL dump\n")
                f.write(f"-- Database: {db_name}\n")
                f.write(f"-- Date: {datetime.now()}\n\n")
                f.write("SET FOREIGN_KEY_CHECKS=0;\n\n")
                
                # Backup từng table
                for (table_name,) in tables:
                    # DROP TABLE
                    f.write(f"DROP TABLE IF EXISTS `{table_name}`;\n")
                    
                    # CREATE TABLE
                    cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
                    create_table = cursor.fetchone()[1]
                    f.write(f"{create_table};\n\n")
                    
                    # INSERT DATA
                    cursor.execute(f"SELECT * FROM `{table_name}`")
                    rows = cursor.fetchall()
                    
                    if rows:
                        # Lấy column names
                        cursor.execute(f"DESCRIBE `{table_name}`")
                        columns = [col[0] for col in cursor.fetchall()]
                        
                        f.write(f"INSERT INTO `{table_name}` (`{'`, `'.join(columns)}`) VALUES\n")
                        
                        for i, row in enumerate(rows):
                            # Escape và format values
                            values = []
                            for val in row:
                                if val is None:
                                    values.append('NULL')
                                elif isinstance(val, (int, float)):
                                    values.append(str(val))
                                elif isinstance(val, bytes):
                                    values.append(f"'{val.hex()}'")
                                else:
                                    # Escape single quotes
                                    escaped_val = str(val).replace("'", "''")
                                    values.append(f"'{escaped_val}'")
                            
                            row_sql = f"({', '.join(values)})"
                            if i < len(rows) - 1:
                                f.write(f"{row_sql},\n")
                            else:
                                f.write(f"{row_sql};\n\n")
                
                f.write("SET FOREIGN_KEY_CHECKS=1;\n")
            
            cursor.close()
            conn.close()
            
            # Thêm vào zip file
            zipf.write(backup_sql_path, 'database/backup.sql')
            
        finally:
            # Xóa file tạm
            if os.path.exists(backup_sql_path):
                os.remove(backup_sql_path)
    
    def _backup_sqlite(self, zipf):
        """Backup SQLite database"""
        import sqlite3
        
        backup_db_path = os.path.join(self.backup_dir, 'db_temp.sqlite3')
        
        # Sử dụng SQLite backup API
        source = sqlite3.connect(self.db_name)
        dest = sqlite3.connect(backup_db_path)
        
        with dest:
            source.backup(dest)
        
        source.close()
        dest.close()
        
        # Thêm vào zip file
        zipf.write(backup_db_path, 'database/db.sqlite3')
        
        # Xóa file tạm
        os.remove(backup_db_path)
    
    def _backup_media(self, zipf):
        """Backup media files"""
        media_path = Path(self.media_root)
        
        for file_path in media_path.rglob('*'):
            if file_path.is_file():
                # Bỏ qua thư mục backups
                if 'backups' not in file_path.parts:
                    arcname = os.path.join('media', file_path.relative_to(media_path))
                    zipf.write(file_path, arcname)
    
    def restore_backup(self, backup_history, user=None):
        """
        Restore từ backup
        
        Args:
            backup_history: BackupHistory object để restore
            user: User object thực hiện restore
        
        Returns:
            Boolean - thành công hay không
        """
        try:
            backup_file_path = backup_history.backup_file.path
            
            # Extract backup file
            with zipfile.ZipFile(backup_file_path, 'r') as zipf:
                # Restore database
                db_files = [f for f in zipf.namelist() if f.startswith('database/')]
                if db_files:
                    self._restore_database(zipf)
                
                # Restore media files
                media_files = [f for f in zipf.namelist() if f.startswith('media/')]
                if media_files:
                    self._restore_media(zipf)
            
            # Cập nhật restore info
            backup_history.restored_at = timezone.now()
            backup_history.restored_by = user
            backup_history.save()
            
            return True
            
        except Exception as e:
            raise e
    
    def _restore_database(self, zipf):
        """Restore database từ backup"""
        if 'mysql' in self.db_engine:
            self._restore_mysql(zipf)
        elif 'sqlite' in self.db_engine:
            self._restore_sqlite(zipf)
        else:
            raise Exception(f"Database engine không được hỗ trợ: {self.db_engine}")
    
    def _restore_mysql(self, zipf):
        """Restore MySQL database từ SQL backup"""
        import MySQLdb
        temp_sql_path = os.path.join(self.backup_dir, 'restore_temp.sql')
        
        try:
            # Extract SQL file từ backup
            with zipf.open('database/backup.sql') as source:
                with open(temp_sql_path, 'wb') as target:
                    shutil.copyfileobj(source, target)
            
            # Lấy thông tin database
            db_user = self.db_config.get('USER', 'root')
            db_password = self.db_config.get('PASSWORD', '')
            db_host = self.db_config.get('HOST', 'localhost')
            db_port = int(self.db_config.get('PORT', '3306'))
            db_name = self.db_name
            
            # Kết nối database
            conn = MySQLdb.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_password,
                database=db_name
            )
            cursor = conn.cursor()
            
            # Đọc và thực thi SQL file
            with open(temp_sql_path, 'r', encoding='utf-8') as f:
                sql_content = f.read()
                
                # Split bằng dấu ; và thực thi từng statement
                statements = sql_content.split(';\n')
                for statement in statements:
                    statement = statement.strip()
                    if statement:
                        try:
                            cursor.execute(statement)
                        except Exception as e:
                            # Log lỗi nhưng tiếp tục
                            print(f"Warning: {e}")
                            continue
            
            conn.commit()
            cursor.close()
            conn.close()
            
        finally:
            # Cleanup
            if os.path.exists(temp_sql_path):
                os.remove(temp_sql_path)
    
    def _restore_sqlite(self, zipf):
        """Restore SQLite database từ backup"""
        import sqlite3
        
        temp_db_path = os.path.join(self.backup_dir, 'restore_temp.sqlite3')
        
        with zipf.open('database/db.sqlite3') as source:
            with open(temp_db_path, 'wb') as target:
                shutil.copyfileobj(source, target)
        
        # Backup database hiện tại trước khi restore
        current_backup = self.db_name + '.before_restore'
        shutil.copy2(self.db_name, current_backup)
        
        try:
            # Replace với database từ backup
            shutil.copy2(temp_db_path, self.db_name)
        except Exception as e:
            # Nếu có lỗi, restore lại database cũ
            shutil.copy2(current_backup, self.db_name)
            raise e
        finally:
            # Cleanup
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
            if os.path.exists(current_backup):
                os.remove(current_backup)
    
    def _restore_media(self, zipf):
        """Restore media files từ backup"""
        # Extract media files
        for file_info in zipf.infolist():
            if file_info.filename.startswith('media/'):
                # Remove 'media/' prefix
                relative_path = file_info.filename[6:]  # len('media/') = 6
                target_path = os.path.join(self.media_root, relative_path)
                
                # Tạo thư mục nếu cần
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                
                # Extract file
                with zipf.open(file_info) as source:
                    with open(target_path, 'wb') as target:
                        shutil.copyfileobj(source, target)
    
    def _update_backup_config(self, success):
        """Cập nhật thông tin backup config"""
        try:
            config = BackupConfiguration.objects.first()
            if config:
                config.last_backup_date = timezone.now()
                config.last_backup_success = success
                config.save()
        except Exception:
            pass
    
    def _cleanup_old_backups(self):
        """Xóa các backup cũ theo cấu hình"""
        try:
            config = BackupConfiguration.objects.first()
            if config and config.max_backups_keep:
                # Lấy các backup thành công, sắp xếp theo ngày tạo
                backups = BackupHistory.objects.filter(
                    status='success'
                ).order_by('-created_at')
                
                # Xóa các backup thừa
                backups_to_delete = backups[config.max_backups_keep:]
                for backup in backups_to_delete:
                    if backup.backup_file:
                        # Xóa file
                        if os.path.exists(backup.backup_file.path):
                            os.remove(backup.backup_file.path)
                    # Xóa record
                    backup.delete()
        except Exception:
            pass
    
    def delete_backup(self, backup_history):
        """Xóa backup"""
        try:
            if backup_history.backup_file:
                if os.path.exists(backup_history.backup_file.path):
                    os.remove(backup_history.backup_file.path)
            backup_history.delete()
            return True
        except Exception as e:
            raise e
