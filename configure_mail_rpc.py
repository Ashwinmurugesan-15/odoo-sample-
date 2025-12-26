import xmlrpc.client

url = "http://localhost:8069"
db = "odoo"
username = "admin"
password = "admin"  # Assuming default admin credentials given local dev env

try:
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    
    parts = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    # Check if server exists
    existing_ids = parts.execute_kw(db, uid, password, 'ir.mail_server', 'search', [[['smtp_host', '=', 'localhost'], ['smtp_port', '=', 1025]]])
    
    if existing_ids:
        print("Mail server already configured.")
    else:
        new_id = parts.execute_kw(db, uid, password, 'ir.mail_server', 'create', [{
            'name': 'Local Debug Server',
            'smtp_host': 'localhost',
            'smtp_port': 1025,
            'smtp_encryption': 'none',
            'sequence': 1,
        }])
        print(f"Mail server created successfully with ID: {new_id}")

except Exception as e:
    print(f"Error: {e}")
