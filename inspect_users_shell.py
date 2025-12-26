import sys
from odoo import api, SUPERUSER_ID, modules

def check_fields():
    env = api.Environment(modules.registry.Registry('odoo').cursor(), SUPERUSER_ID, {})
    User = env['res.users']
    print("Model: res.users")
    print(f"Has 'groups_id'? {'groups_id' in User._fields}")
    print(f"Has 'password'? {'password' in User._fields}")
    print(f"Has 'login'? {'login' in User._fields}")
    
    # Try to read user 5
    u = User.browse(5)
    print(f"User 5: {u.name} (Active: {u.active})")
    
    # Try to write password directly here
    try:
        u.password = '123456'
        print("Shell: Password write successful.")
        env.cr.commit() # Commit transaction
    except Exception as e:
        print(f"Shell: Password write failed: {e}")
        env.cr.rollback()

    # Try to add group directly here
    try:
        ref = env.ref('base.group_user')
        if ref not in u.groups_id:
            u.groups_id = [(4, ref.id)]
            print("Shell: Group added successful.")
            env.cr.commit()
        else:
            print("Shell: Group already present.")
    except Exception as e:
        print(f"Shell: Group add failed: {e}")
        env.cr.rollback()

if __name__ == '__main__':
    check_fields()
