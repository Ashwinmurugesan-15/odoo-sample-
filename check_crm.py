try:
    state = env['ir.module.module'].search([('name', '=', 'crm')], limit=1).state
    print(f"CRM Module State: {state}")
except Exception as e:
    print(e)
