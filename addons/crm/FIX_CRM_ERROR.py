# MANUAL FIX FOR CRM PROBABILITY ERROR
# Run this script to fix the "ValueError: not enough values to unpack" error

import sys
import os

# Try different path variations
possible_paths = [
    r'd:\odoo-19.0\odoo-19.0\addons\crm\models\crm_lead.py',
    r'D:\odoo-19.0\odoo-19.0\addons\crm\models\crm_lead.py',
    r'.\models\crm_lead.py'
]

file_path = None
for path in possible_paths:
    if os.path.exists(path):
        file_path = path
        print(f"Found file at: {file_path}")
        break

if not file_path:
    print("ERROR: Could not find crm_lead.py")
    print("Please check if the file exists at:")
    for p in possible_paths:
        print(f"  - {p}")
    sys.exit(1)

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the problematic line
    old_line = 'lead_probabilities, _unused = self._pls_get_naive_bayes_probabilities()'
    new_lines = '''pls_result = self._pls_get_naive_bayes_probabilities()
        lead_probabilities = pls_result[0] if pls_result else {}'''
    
    if old_line in content:
        content = content.replace(old_line, new_lines)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("SUCCESS: File patched!")
        print("\nNow run these commands:")
        print("1. taskkill /F /IM py.exe")
        print("2. cmd /c \"del /s /q models\\__pycache__\"")
        print("3. py -3.12 ../../odoo-bin --addons-path=../../addons,./ -d my_crm_test")
    else:
        print("ERROR: Could not find the line to replace")
        print("The file may have already been patched")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
