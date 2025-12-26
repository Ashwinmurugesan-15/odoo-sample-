import sys
import os

# Ensure we are in the right directory to find odoo module
sys.path.append(os.getcwd())

import odoo
from odoo import api, SUPERUSER_ID

def run():
    # Load configuration
    odoo.tools.config.parse_config(['-d', 'odoo']) 
    
    # Initialize registry
    registry = odoo.modules.registry.Registry.new(odoo.tools.config['db_name'])
    
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        User = env['res.users']
        print("Model: res.users")
        print(f"Has 'groups_id'? {'groups_id' in User._fields}")
        print(f"Has 'password'? {'password' in User._fields}")
        
        # Try to read user 5
        try:
            u = User.browse(5)
            print(f"User 5: {u.name} (Active: {u.active}, Login: {u.login})")
            
            # 1. Force Password Write
            u.sudo().write({'password': '123456'})
            print("Direct Write: Password updated to '123456'.")
            
            # 2. Force Group Add
            ref = env.ref('base.group_user')
            if ref not in u.groups_id:
                u.sudo().write({'groups_id': [(4, ref.id)]})
                print("Direct Write: Internal Group added.")
            else:
                print("Direct Write: Internal Group already present.")
                
            cr.commit()
            print("TRANSACTION COMMITTED.")
            
        except Exception as e:
            print(f"Direct Operation Failed: {e}")
            cr.rollback()

if __name__ == '__main__':
    run()
