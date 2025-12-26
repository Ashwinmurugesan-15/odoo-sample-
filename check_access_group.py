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
    
    # helper to find group id
    def get_group_id(xml_id):
        try:
            res = models.execute_kw(db, uid, password, 'ir.model.data', 'check_object_reference', [xml_id.split('.')[0], xml_id.split('.')[1]])
            return res[1]
        except:
             return None

    group_internal_id = get_group_id('base.group_user')
    print(f"Internal User Group ID: {group_internal_id}")
    
    # Search for user 'ashlog559@gmail.com' AND having the group
    # Domain: [('login', '=', 'ashlog559@gmail.com'), ('groups_id', 'in', [group_internal_id])]
    
    target_user_in_group = models.execute_kw(db, uid, password, 'res.users', 'search_count', [[['login', '=', 'ashlog559@gmail.com'], ['groups_id', 'in', [group_internal_id]]]])
    
    if target_user_in_group:
        print("VERIFIED: User 'ashlog559@gmail.com' IS in 'Internal User' group.")
    else:
        print("FAILURE: User 'ashlog559@gmail.com' is NOT in 'Internal User' group.")
        
        # Check if user exists at all
        user_exists = models.execute_kw(db, uid, password, 'res.users', 'search_count', [[['login', '=', 'ashlog559@gmail.com']]])
        if user_exists:
            print("User exists but missing permission.")
        else:
            print("User does NOT exist.")

except Exception as e:
    print(f"ERROR: {e}")
