import xmlrpc.client

url = "http://localhost:8069"
db = "odoo"
username = "admin"
password = "admin"

PROPER_EMAIL = "ashlog559@gmail.com"

try:
    print("Connecting...")
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    # 1. Check Admin User Email
    user = models.execute_kw(db, uid, password, 'res.users', 'read', [uid], {'fields': ['name', 'email', 'login']})[0]
    print(f"Current User: {user['name']}")
    print(f"Current Email: {user['email']}")
    
    if user['email'] != PROPER_EMAIL:
        print(f"MISMATCH: Fixing email to {PROPER_EMAIL}...")
        models.execute_kw(db, uid, password, 'res.users', 'write', [[uid], {'email': PROPER_EMAIL}])
        print("User email updated.")
    else:
        print("User email matches.")

    # 2. Check Company Email
    company_id = models.execute_kw(db, uid, password, 'res.users', 'read', [uid], {'fields': ['company_id']})[0]['company_id'][0]
    company = models.execute_kw(db, uid, password, 'res.company', 'read', [company_id], {'fields': ['email', 'name']})[0]
    print(f"Company: {company['name']}")
    print(f"Company Email: {company['email']}")
    
    if company['email'] != PROPER_EMAIL:
        print(f"Fixing company email to {PROPER_EMAIL}...")
        models.execute_kw(db, uid, password, 'res.company', 'write', [[company_id], {'email': PROPER_EMAIL}])
        print("Company email updated.")

    # 3. Check System Parameters (mail.catchall.domain)
    # If catchall domain is set (e.g. 'odoo.com'), Odoo might try to construct emails like 'postmaster@odoo.com'
    # For Gmail SMTP, we usually want to avoid this rewriting or ensure it matches.
    # Actually, simpler is to ensure 'mail.default.from' is correct if it exists.
    
    params = models.execute_kw(db, uid, password, 'ir.config_parameter', 'search_read', [[['key', 'in', ['mail.catchall.domain', 'mail.default.from']]]], {'fields': ['key', 'value']})
    print("System Parameters:")
    for p in params:
        print(f"{p['key']}: {p['value']}")

except Exception as e:
    print(f"ERROR: {e}")
