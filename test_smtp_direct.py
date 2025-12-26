import xmlrpc.client
import sys

TO_EMAIL = "ashlog559@gmail.com"
FROM_EMAIL = "ashlog559@gmail.com"

url = "http://localhost:8069"
db = "odoo"
username = "admin"
password = "admin"

try:
    print("Authenticating...")
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    # Construct a simple message
    message = models.execute_kw(db, uid, password, 'ir.mail_server', 'build_email', [], {
        'email_from': FROM_EMAIL,
        'email_to': [TO_EMAIL],
        'subject': 'Direct SMTP Test',
        'body': 'This is a direct SMTP test.',
    })
    
    print("Attempting to send email directly via ir.mail_server...")
    # send_email(message, mail_server_id=None, smtp_server=None, smtp_port=None,
    #            smtp_user=None, smtp_password=None, smtp_encryption=None,
    #            smtp_debug=False, smtp_session=None)
    # If we pass mail_server_id, it uses that. If we pass None, it uses the default (priority).
    
    # We want to force using the Gmail server we just created.
    # Let's find it first.
    server_ids = models.execute_kw(db, uid, password, 'ir.mail_server', 'search', [[['smtp_host', '=', 'smtp.gmail.com']]])
    if not server_ids:
        print("ERROR: No Gmail server found!")
        sys.exit(1)
        
    server_id = server_ids[0]
    print(f"Using Mail Server ID: {server_id}")
    
    # RPC call to send_email
    # Note: send_email returns the Message-Id on success
    msg_id = models.execute_kw(db, uid, password, 'ir.mail_server', 'send_email', [message], {'mail_server_id': server_id})
    
    print(f"SUCCESS: Email sent! Message-ID: {msg_id}")

except Exception as e:
    print(f"FAILURE: {e}")
