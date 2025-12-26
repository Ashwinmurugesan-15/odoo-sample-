import xmlrpc.client
import sys

url = "http://localhost:8069"
db = "odoo"
username = "admin"
password = "admin"

TARGET_LOGIN = "ashlog559@gmail.com" # Or name 'ash', usually email is login for portal
# Wait, let's find the user by name "ash" first if we don't know the login.
# The user said their email is ashlog559...

try:
    print("Connecting as admin...")
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    # helper to find group id
    def get_group_id(xml_id):
        # xml_id is like 'base.group_user'
        # in RPC we can use ir.model.data
        try:
            res = models.execute_kw(db, uid, password, 'ir.model.data', 'check_object_reference', [xml_id.split('.')[0], xml_id.split('.')[1]])
            return res[1]
        except:
             return None

    group_internal_id = get_group_id('base.group_user')
    group_portal_id = get_group_id('base.group_portal')
    group_crm_manager_id = get_group_id('sales_team.group_sale_manager')

    print(f"Group IDs: Internal={group_internal_id}, Portal={group_portal_id}, CRM={group_crm_manager_id}")

    # Find the user
    users = models.execute_kw(db, uid, password, 'res.users', 'search_read', [[['name', 'ilike', 'ash']]], {'fields': ['id', 'name', 'groups_id']})
    
    if not users:
        print("User 'ash' not found via search.")
        sys.exit(1)
        
    user = users[0]
    print(f"Found User: {user['name']} (ID: {user['id']})")
    
    current_groups = user['groups_id']
    
    # Update logic:
    # 1. Remove Portal group if present
    # 2. Add Internal User group
    # 3. Add CRM Manager group
    
    new_groups = list(current_groups)
    
    if group_portal_id in new_groups:
        print("Removing Portal group...")
        new_groups.remove(group_portal_id)
        
    if group_internal_id and group_internal_id not in new_groups:
        print("Adding Internal User group...")
        new_groups.append(group_internal_id)
        
    if group_crm_manager_id and group_crm_manager_id not in new_groups:
        print("Adding CRM Manager group...")
        new_groups.append(group_crm_manager_id)
        
    if new_groups != current_groups:
        models.execute_kw(db, uid, password, 'res.users', 'write', [[user['id']], {'groups_id': [(6, 0, new_groups)]}])
        print("User permissions updated successfully!")
    else:
        print("User already has correct permissions.")

except Exception as e:
    print(f"ERROR: {e}")
