
# Search for templates containing "Odoo"
templates = env['mail.template'].search(['|', ('body_html', 'ilike', 'Odoo'), ('subject', 'ilike', 'Odoo')])
print(f"Found {len(templates)} templates with 'Odoo' branding:")
for t in templates:
    print(f"- [{t.get_external_id().get(t.id)}] {t.name}")
