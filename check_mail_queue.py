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
    
    # Search for last 10 mails
    mail_ids = models.execute_kw(db, uid, password, 'mail.mail', 'search', [[]], {'limit': 10, 'order': 'id desc'})
    
    if not mail_ids:
        print("No emails found in queue.")
    else:
        mails = models.execute_kw(db, uid, password, 'mail.mail', 'read', [mail_ids], {'fields': ['id', 'subject', 'email_to', 'state', 'failure_reason', 'date']})
        
        print(f"Found {len(mails)} recent emails:")
        for m in mails:
            print(f"ID: {m['id']} | Date: {m['date']} | To: {m['email_to']} | State: {m['state']}")
            if m['failure_reason']:
                print(f"    FAILURE REASON: {m['failure_reason']}")

except Exception as e:
    print(f"ERROR: {e}")
