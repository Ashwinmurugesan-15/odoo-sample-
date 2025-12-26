import xmlrpc.client

url = "http://localhost:8069"
db = "odoo"
username = "ashlog559@gmail.com"
password = "123456"

try:
    print(f"Attempting login for {username} with password '{password}'...")
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    
    if uid:
        print(f"SUCCESS: Login successful! UID: {uid}")
    else:
        print("FAILURE: Login failed (Wrong password or account disabled).")

except Exception as e:
    print(f"ERROR: {e}")
