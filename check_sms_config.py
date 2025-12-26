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
    
    # 1. Check if 'sms' module is installed
    modules = models.execute_kw(db, uid, password, 'ir.module.module', 'search_count', [[['name', '=', 'sms'], ['state', '=', 'installed']]])
    if not modules:
        print("SMS module NOT installed.")
    else:
        print("SMS module is installed.")
        
        # 2. Check IAP Accounts (Odoo's default SMS provider)
        # Model: iap.account
        iap_accounts = models.execute_kw(db, uid, password, 'iap.account', 'search_read', [[]], {'fields': ['service_name', 'account_token', 'company_id']})
        
        print(f"Found {len(iap_accounts)} IAP Accounts:")
        for acc in iap_accounts:
            print(f"  - Service: {acc['service_name']} | Token: {acc['account_token']}")
            
        # 3. Check SMS log for specific error
        # Model: sms.sms
        failed_sms = models.execute_kw(db, uid, password, 'sms.sms', 'search_read', [[['state', '=', 'error']]], {'fields': ['number', 'error_code', 'failure_type'], 'limit': 5})
        
        if failed_sms:
            print("Recent Failed SMS:")
            for sms in failed_sms:
                print(f"  - To: {sms['number']} | Error: {sms['error_code']} ({sms['failure_type']})")
        else:
            print("No failed SMS records found in database.")

except Exception as e:
    print(f"ERROR: {e}")
