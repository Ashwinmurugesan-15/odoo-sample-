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
    
    # Find user 'ash'
    users = models.execute_kw(db, uid, password, 'res.users', 'search_read', [[['login', '=', 'ashlog559@gmail.com']]], {'fields': ['id', 'name']})
    
    if not users:
        print("User 'ashlog559@gmail.com' not found.")
        sys.exit(1)
        
    user_id = users[0]['id']
    print(f"Resetting password for User ID: {user_id}")
    
    models.execute_kw(db, uid, password, 'res.users', 'write', [[user_id], {'password': '123456'}])
    print("SUCCESS: Password reset to '123456'.")

except Exception as e:
    print(f"ERROR: {e}")
