import xmlrpc.client

url = "http://localhost:8069"
db = "odoo"
username = "admin"
password = "admin"

try:
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    # Search all
    ids = models.execute_kw(db, uid, password, 'ir.mail_server', 'search', [[]])
    servers = models.execute_kw(db, uid, password, 'ir.mail_server', 'read', [ids, ['name', 'smtp_host', 'smtp_port', 'smtp_user', 'active', 'sequence']])
    
    print(f"Found {len(servers)} mail servers:")
    for s in servers:
        print(f"ID: {s['id']}, Name: {s['name']}, Host: {s['smtp_host']}:{s['smtp_port']}, User: {s['smtp_user']}, Active: {s['active']}, Seq: {s['sequence']}")

except Exception as e:
    print(f"ERROR: {e}")
