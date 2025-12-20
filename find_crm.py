import inspect
import os

try:
    crm_lead_model = env['crm.lead']
    file_path = inspect.getfile(crm_lead_model.__class__)
    print(f"CRM_LEAD_FILE_PATH: {file_path}")
    
    # Also check where 'crm' module is defined
    import odoo.addons.crm as crm_module
    print(f"CRM_MODULE_PATH: {crm_module.__file__}")
    
    # Check if the file actually exists on disk from Python's perspective
    if os.path.exists(file_path):
        print("FILE_EXISTS_ON_DISK: True")
    else:
        print("FILE_EXISTS_ON_DISK: False")
        
except Exception as e:
    print(f"ERROR: {e}")
