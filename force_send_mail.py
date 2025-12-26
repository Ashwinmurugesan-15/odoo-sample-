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
    
    # Force send
    print("Forcing processing of outgoing mail queue...")
    # This calls mail.mail.process_email_queue()
    # Or specifically finding ids and calling send()
    
    ids = models.execute_kw(db, uid, password, 'mail.mail', 'search', [[['state', '=', 'outgoing']]])
    if ids:
        print(f"Found {len(ids)} outgoing emails. Sending now...")
        res = models.execute_kw(db, uid, password, 'mail.mail', 'send', [ids])
        print("Queue processed.")
    else:
        print("No outgoing emails found in queue.")

except Exception as e:
    print(f"ERROR: {e}")
