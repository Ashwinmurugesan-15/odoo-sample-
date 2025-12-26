import xmlrpc.client
import sys

# Credentials provided by user
GMAIL_USER = "ashlog559@gmail.com"
GMAIL_PASS = "eyyn mslm zvij shaw"  # App password

url = "http://localhost:8069"
db = "odoo"
username = "admin"
password = "admin"

try:
    print("Authenticating...")
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    if not uid:
        print("Authentication failed.")
        sys.exit(1)

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    # 1. Archive the Local Debug Server if it exists, to avoid conflict/confusion
    print("Checking for existing 'Local Debug Server'...")
    debug_server_ids = models.execute_kw(db, uid, password, 'ir.mail_server', 'search', [[['smtp_host', '=', 'localhost'], ['smtp_port', '=', 1025]]])
    if debug_server_ids:
        print(f"Archiving 'Local Debug Server' (ID: {debug_server_ids})...")
        models.execute_kw(db, uid, password, 'ir.mail_server', 'write', [debug_server_ids, {'active': False}])

    # 2. Check/Create Gmail Server
    print("Checking for existing Gmail configuration...")
    gmail_server_ids = models.execute_kw(db, uid, password, 'ir.mail_server', 'search', [[['smtp_host', '=', 'smtp.gmail.com'], ['smtp_user', '=', GMAIL_USER]]])
    
    server_values = {
        'name': 'Gmail Server',
        'smtp_host': 'smtp.gmail.com',
        'smtp_port': 587,
        'smtp_encryption': 'starttls',
        'smtp_user': GMAIL_USER,
        'smtp_pass': GMAIL_PASS,
        'sequence': 10,
        'active': True
    }

    if gmail_server_ids:
        print(f"Updating existing Gmail Server (ID: {gmail_server_ids})...")
        models.execute_kw(db, uid, password, 'ir.mail_server', 'write', [gmail_server_ids, server_values])
    else:
        print("Creating new Gmail Server...")
        new_id = models.execute_kw(db, uid, password, 'ir.mail_server', 'create', [server_values])
        print(f"Gmail Server created successfully with ID: {new_id}")

    print("Success! Gmail configured.")

except Exception as e:
    print(f"ERROR: {e}")
