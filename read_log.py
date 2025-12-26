import os

log_file = r"d:\odoo-19.0\odoo-19.0\odoo.log"

try:
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        # Seek to end and read last 10KB
        f.seek(0, os.SEEK_END)
        size = f.tell()
        read_size = min(size, 20000)
        f.seek(size - read_size)
        content = f.read()
        print(content)
except Exception as e:
    print(f"Error reading log: {e}")
