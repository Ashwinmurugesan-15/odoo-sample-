import odoo
from odoo import api, SUPERUSER_ID
import sys

def setup_mail_server():
    try:
        # standard Odoo initialization (assuming running via odoo-bin shell or similar context)
        # But this script is meant to be run via `odoo-bin shell`
        # usage: python odoo-bin shell -d odoo < setup_mail_server.py --no-http
        
        # However, passing file to shell via stdin is tricky in some terminals. 
        # Better to run it as a standalone script importing odoo if possible, or use xmlrpc.
        # Given we are on the server machine, we can just use `odoo-bin shell`.
        
        env = api.Environment(odoo.modules.registry.Registry('odoo').cursor(), SUPERUSER_ID, {})
        
        MailServer = env['ir.mail_server']
        existing = MailServer.search([('smtp_host', '=', 'localhost'), ('smtp_port', '=', 1025)])
        
        if existing:
            print("Mail server already configured.")
        else:
            MailServer.create({
                'name': 'Local Debug Server',
                'smtp_host': 'localhost',
                'smtp_port': 1025,
                'smtp_encryption': 'none',
                'sequence': 1,
            })
            print("Mail server created successfully.")
            
        env.cr.commit()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    setup_mail_server()
