import inspect
import odoo
from odoo import api, SUPERUSER_ID

# Create a registry and environment
registry = odoo.registry('odoo')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    try:
        model = env['crm.lead']
        file_path = inspect.getfile(model.__class__)
        print(f"CRM_LEAD_FILE_PATH: {file_path}")
    except Exception as e:
        print(f"ERROR: {e}")
