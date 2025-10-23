#!/usr/bin/env python
"""
Script để thay thế tất cả 'GA' thành 'GA' trong project
"""
import os
import re

# Các thư mục và file cần bỏ qua
EXCLUDE_DIRS = {'venv', '__pycache__', '.git', 'node_modules', 'staticfiles', 'media'}
EXCLUDE_FILES = {'.pyc', '.pyo', '.sqlite3', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.woff', '.woff2', '.ttf', '.eot', '.svg'}

def should_process_file(filepath):
    """Kiểm tra xem file có nên xử lý không"""
    # Bỏ qua các file binary và generated
    for ext in EXCLUDE_FILES:
        if filepath.endswith(ext):
            return False
    
    # Bỏ qua file vfs_fonts.js (file rất lớn của pdfmake)
    if 'vfs_fonts.js' in filepath:
        return False
        
    # Chỉ xử lý các file text
    text_extensions = {'.py', '.html', '.js', '.css', '.md', '.po', '.pot', '.txt', '.json', '.xml', '.yml', '.yaml'}
    return any(filepath.endswith(ext) for ext in text_extensions)

def replace_in_file(filepath):
    """Thay thế GA thành GA trong file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Thay thế các biến thể của GA
        replacements = [
            (r'\bOVNC\b', 'GA'),  # GA -> GA
            (r'<b>GA</b>', '<b>GA</b>'),  # <b>GA</b> -> <b>GA</b>
            (r'alt="GA Logo"', 'alt="GA Logo"'),  # alt text
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        # Chỉ ghi file nếu có thay đổi
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'✓ Updated: {filepath}')
            return True
        return False
            
    except Exception as e:
        print(f'✗ Error processing {filepath}: {e}')
        return False

def main():
    """Main function"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    updated_count = 0
    
    print('Starting GA -> GA replacement...\n')
    
    for root, dirs, files in os.walk(base_dir):
        # Loại bỏ các thư mục không cần xử lý
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            filepath = os.path.join(root, file)
            
            if should_process_file(filepath):
                if replace_in_file(filepath):
                    updated_count += 1
    
    print(f'\n✓ Complete! Updated {updated_count} files.')
    print('\nNotes:')
    print('- Skipped staticfiles/, venv/, __pycache__, and binary files')
    print('- Remember to compile translations after updating .po files')
    print('  Run: python manage.py compilemessages')

if __name__ == '__main__':
    main()
