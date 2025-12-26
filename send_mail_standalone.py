import sys
import os

# Ensure we are in the right directory to find odoo module
sys.path.append(os.getcwd())

import odoo
import odoo.tools.config

def run():
    print("Initializing Odoo Environment...")
    # Load configuration
    try:
        odoo.tools.config.parse_config(['-c', 'odoo.conf', '-d', 'odoo'])
    except Exception:
        odoo.tools.config.parse_config(['-d', 'odoo']) 
    
    # Lazy imports to avoid circular issues
    from odoo import api, SUPERUSER_ID
    from odoo.modules.registry import Registry

    try:
        db_name = odoo.tools.config['db_name']
        if isinstance(db_name, list):
            db_name = db_name[0]
        print(f"Using DB Name: {db_name}")
        registry = Registry.new(db_name)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Failed to initialize registry: {e}")
        return

    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        email = "test_standalone@example.com"
        subject = "Standalone Script Email"
        
        print(f"Processing email for: {email}")
        
        # 1. Find or Create Partner
        partner = env['res.partner'].search([('email', '=', email)], limit=1)
        if not partner:
            print("Partner not found. Creating new partner.")
            partner = env['res.partner'].create({'name': email, 'email': email})
        else:
            print(f"Partner found: {partner.name}")

        # 2. Get Template
        template = env.ref('mail_plugin.mail_plugin_custom_template', raise_if_not_found=False)
        
        if not template:
            print("ERROR: Template 'mail_plugin.mail_plugin_custom_template' not found.")
            print("Make sure you have updated the module: odoo-bin -u mail_plugin")
            return
            
        print(f"Template found: {template.name}")
        
        # 3. Send Mail
        email_values = {'subject': subject}
        print("Sending email...")
        template.send_mail(partner.id, email_values=email_values, force_send=True)
        
        print("Email sent successfully.")
        cr.commit()
        print("Transaction Committed.")

if __name__ == '__main__':
    run()
