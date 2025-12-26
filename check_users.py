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
    
    # 1. List all users
    users = models.execute_kw(db, uid, password, 'res.users', 'search_read', [[]], {'fields': ['id', 'name', 'login', 'email']}) 
    # sel_groups_... is a bit tricky to guess field names for groups.
    # Instead let's just inspect basic info first.
    
    print(f"Found {len(users)} users:")
    for u in users:
        print(f"ID: {u['id']}, Name: {u['name']}, Login: {u['login']}, Email: {u['email']}")
        
        # Check if they are 'ash'
        if 'ash' in u['name'].lower() or 'ash' in u['login'].lower():
            print(f"--> FOUND TARGET USER: {u['name']}")
            # Check groups for this user
            # We want to see if they belong to group_user (Internal User) or group_portal (Portal)
            # 'base.group_user' is Internal
            # 'base.group_portal' is Portal
            
            user_groups = models.execute_kw(db, uid, password, 'res.users', 'read', [u['id']], {'fields': ['groups_id']})
            group_ids = user_groups[0]['groups_id']
            
            groups = models.execute_kw(db, uid, password, 'res.groups', 'read', [group_ids], {'fields': ['name', 'xml_id']}) # xml_id might not be readable simply like this due to it being computed or external
            # Actually just 'name' or 'full_name'
            
            print("    Groups:")
            for g in groups:
                 print(f"    - {g['name']}")

except Exception as e:
    print(f"ERROR: {e}")
