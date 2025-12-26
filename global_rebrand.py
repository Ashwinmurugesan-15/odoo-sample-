
# Script to globally rebrand Odoo -> GuhaTek in all email templates

# List of template XML IDs (or IDs found) to update
# Based on search results:
# - calendar.calendar_template_meeting_changedate
# - calendar.calendar_template_meeting_update
# - calendar.calendar_template_meeting_invitation
# - calendar.calendar_template_meeting_reminder
# - auth_signup.mail_template_user_signup_account_created
# - auth_signup.portal_set_password_email
# - auth_signup.set_password_email (Already done, but good to check)
# - Custom Plugin Lead Template (No XML ID, handle by name search)

def rebrand_text(text):
    if not text:
        return text
    # Generic replacements
    text = text.replace("Odoo", "GuhaTek")
    text = text.replace("odoo.com", "yourcompany.com") # Prevent broken links to odoo.com if desired, or keep specific ones
    # Fix specific phrases
    text = text.replace("Welcome to GuhaTek", "Welcome to GuhaTek") # Redundant check
    text = text.replace("Powered by GuhaTek", "") # Remove powered by completely if desired, or keep branded
    return text

# 1. Search for all candidates again to be safe
templates = env['mail.template'].search(['|', ('body_html', 'ilike', 'Odoo'), ('subject', 'ilike', 'Odoo')])

print(f"Processing {len(templates)} templates...")

for template in templates:
    print(f"Updating: {template.name}")
    vals = {}
    
    # Update Body
    if template.body_html and "Odoo" in template.body_html:
        # Special case: The auth_signup.set_password_email might already satisfy "GuhaTek" but we use simple replace
        # A simple replace "Odoo" -> "GuhaTek" works for most cases
        new_body = template.body_html.replace("Odoo", "GuhaTek")
        
        # Remove "Powered by" footer entirely if it exists and we want it clean
        if "Powered by" in new_body:
             # Simple hack to hide footer if needed, or just let it say "Powered by GuhaTek"
             pass
             
        vals['body_html'] = new_body

    # Update Subject
    if template.subject and "Odoo" in template.subject:
        vals['subject'] = template.subject.replace("Odoo", "GuhaTek")

    if vals:
        template.write(vals)
        print(f"  -> Updated ({list(vals.keys())})")
    else:
        print("  -> No changes needed (already updated?)")

env.cr.commit()
print("SUCCESS: Global rebrand complete.")
