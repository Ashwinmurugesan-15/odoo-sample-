# Shell script to be run via odoo-bin shell
import sys

try:
    print("Starting shell script execution for LEAD...")
    email = "test_lead@example.com"
    subject = "Standalone Shell Lead Email"
    
    # 1. Start with Lead
    Lead = env['crm.lead']
    lead = Lead.search([('email_from', '=', email)], limit=1)
    if not lead:
        print(f"Creating Lead for {email}")
        lead = Lead.create({
            'name': f'Lead from {email}', 
            'email_from': email,
            'description': 'Created via standalone script'
        })
    else:
        print(f"Lead found: {lead.name}")

    # 2. Template for Lead
    template_name = 'Custom Plugin Lead Template'
    template = env['mail.template'].search([('name', '=', template_name)], limit=1)
    
    # Read custom HTML from file
    import os
    html_file_path = os.path.join(os.getcwd(), 'custom_lead_template.html')
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            custom_body = f.read()
            print("Loaded custom HTML template from file.")
    except Exception as e:
        print(f"WARNING: Could not read custom_lead_template.html: {e}")
        custom_body = '<p>Default Fallback Body</p>'
        
    if not template:
        print("Creating Lead template programmatically...")
        template = env['mail.template'].create({
            'name': template_name,
            'model_id': env.ref('crm.model_crm_lead').id,
            'subject': 'Custom Notification for Lead',
            'email_from': '{{ object.email_from }}',
            'body_html': custom_body
        })
        print(f"Created template with ID: {template.id}")
    else:
        # Update existing template with new file content
        print("Updating existing template with new HTML content...")
        template.write({'body_html': custom_body})
    
    if template:
        print(f"Sending email using template: {template.name}")
        # force_send=True ensures it goes out immediately
        template.send_mail(lead.id, email_values={'subject': subject}, force_send=True)
        env.cr.commit()
        print("SUCCESS: Email sent to Lead and transaction committed.")
        
        # Verify in mail.mail or mail.message
        last_msg = env['mail.message'].search([('model', '=', 'crm.lead'), ('res_id', '=', lead.id)], order='id desc', limit=1)
        if last_msg:
             print(f"Last Message on Lead: {last_msg.subject} (Type: {last_msg.message_type})")
    else:
        print("FATAL: Could not get or create template.")

except Exception as e:
    import traceback
    traceback.print_exc()
