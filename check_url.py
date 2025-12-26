
base_url = env['ir.config_parameter'].sudo().get_param('web.base.url')
print(f"Current Base URL: {base_url}")
