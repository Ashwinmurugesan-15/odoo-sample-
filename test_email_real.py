import xmlrpc.client
import sys

# User's email to test receiving
TO_EMAIL = "ashwinm26735@gmail.com"

url = "http://localhost:8069"
db = "odoo"
username = "admin"
password = "admin"

try:
    print(f"Connecting to Odoo to send test email to {TO_EMAIL}...")
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)
    
    # Create a simple mail.message or use ir.mail_server.send_email (lower level)
    # Using mail.mail to simulate a real Odoo email
    
    mail_id = models.execute_kw(db, uid, password, 'mail.mail', 'create', [{
        'subject': 'Odoo CRM: Real Email Test',
        'body_html': '<p>Hello!</p><p>This is a test email from your local Odoo CRM via Gmail.</p><p>If you see this, <b>it works!</b></p>',
        'email_to': TO_EMAIL,
        'email_from': 'ashlog559@gmail.com',
    }])
    
    print(f"Mail created (ID: {mail_id}). Sending now...")
    models.execute_kw(db, uid, password, 'mail.mail', 'send', [[mail_id]])
    print("Email sent command execution completed.")

except Exception as e:
    print(f"ERROR: {e}")
