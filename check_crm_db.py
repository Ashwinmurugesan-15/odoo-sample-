crm_module = env['ir.module.module'].search([('name', '=', 'crm')])
if crm_module:
    print(f"CRM_MODULE_STATE: {crm_module.state}")
else:
    print("CRM_MODULE_NOT_FOUND_IN_DB")
