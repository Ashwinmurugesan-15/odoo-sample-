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
    
    # ID was found to be 5 in previous outputs
    user_id = 5
    print(f"Force resetting password for User ID: {user_id}")
    
    # Also ensure active=True
    models.execute_kw(db, uid, password, 'res.users', 'write', [[user_id], {'password': '123456', 'active': True}])
    print("SUCCESS: Password reset to '123456' and user activated.")

except Exception as e:
    print(f"ERROR: {e}")
