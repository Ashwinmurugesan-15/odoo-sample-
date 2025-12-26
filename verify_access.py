import xmlrpc.client

url = "http://localhost:8069"
db = "odoo"
username = "admin"
password = "admin"

try:
    print("Connecting as admin...")
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    # Check if 'ash' is in 'base.group_user' (Internal User)
    group_ids = models.execute_kw(db, uid, password, 'ir.model.data', 'check_object_reference', ['base', 'group_user'])
    internal_group_id = group_ids[1]
    
    # Read users in this group
    group = models.execute_kw(db, uid, password, 'res.groups', 'read', [internal_group_id], {'fields': ['users']})[0]
    user_ids = group['users']
    
    print(f"Internal User Group ID: {internal_group_id}")
    print(f"Member User IDs: {user_ids}")
    
    # Find ID of 'ash'
    ash_users = models.execute_kw(db, uid, password, 'res.users', 'search_read', [[['login', '=', 'ashlog559@gmail.com']]], {'fields': ['id', 'name']})
    if ash_users:
        ash_id = ash_users[0]['id']
        print(f"Ash ID: {ash_id}")
        
        if ash_id in user_ids:
            print("VERIFIED: 'ash' is an Internal User.")
        else:
            print("FAILURE: 'ash' is NOT in Internal User group.")
    else:
        print("User 'ash' not found.")

except Exception as e:
    print(f"ERROR: {e}")
