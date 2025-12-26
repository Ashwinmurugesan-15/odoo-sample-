import xmlrpc.client
import sys

url = "http://localhost:8069"
db = "odoo"
username = "admin"
password = "admin"

try:
    print("Connecting as admin...")
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    # 1. Get Group IDs
    def get_group_id(xml_id):
        try:
            res = models.execute_kw(db, uid, password, 'ir.model.data', 'check_object_reference', [xml_id.split('.')[0], xml_id.split('.')[1]])
            return res[1]
        except:
             return None

    group_internal_id = get_group_id('base.group_user')
    group_sale_manager_id = get_group_id('sales_team.group_sale_manager')
    
    print(f"Adding Groups: Internal={group_internal_id}, SalesManager={group_sale_manager_id}")

    # 2. Find User 'ash'
    users = models.execute_kw(db, uid, password, 'res.users', 'search_read', [[['login', '=', 'ashlog559@gmail.com']]], {'fields': ['id', 'name']})
    
    if not users:
        print("User 'ashlog559@gmail.com' not found.")
        sys.exit(1)
        
    user_id = users[0]['id']
    print(f"Updating details for User ID: {user_id}")
    
    # 3. Blindly ADD groups using (4, id) syntax
    # We don't read current groups to avoid KeyError if the field is protected/invisible.
    
    commands = []
    if group_internal_id:
        commands.append((4, group_internal_id))
    if group_sale_manager_id:
        commands.append((4, group_sale_manager_id))
        
    if commands:
        models.execute_kw(db, uid, password, 'res.users', 'write', [[user_id], {'groups_id': commands}])
        print("SUCCESS: Groups added.")
    else:
        print("No groups found to add.")

except Exception as e:
    print(f"ERROR: {e}")
