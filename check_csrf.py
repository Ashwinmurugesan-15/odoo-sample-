from odoo import api, SUPERUSER_ID
from odoo.modules.registry import Registry

def check_csrf_config():
    registry = Registry('odoo')
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        secret = env['ir.config_parameter'].sudo().get_str('database.secret')
        print(f"database.secret: {secret}")
        
        if not secret:
            print("database.secret is missing! Re-initializing...")
            env['ir.config_parameter'].init(force=True)
            new_secret = env['ir.config_parameter'].sudo().get_str('database.secret')
            print(f"New database.secret: {new_secret}")
        
        # Check session_id from cookie vs what Odoo thinks
        # (This is harder to check from here, but we can verify the secret is stable)

if __name__ == "__main__":
    check_csrf_config()
