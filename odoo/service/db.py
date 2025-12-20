import logging
import odoo.modules.db
import odoo.tools
from odoo.tools import config
from odoo.exceptions import AccessDenied

_logger = logging.getLogger(__name__)

def dispatch(method, params):
    g = globals()
    exp_method_name = 'exp_' + method
    if exp_method_name in g:
        return g[exp_method_name](*params)
    
    # Fallback to odoo.modules.db if it has a matching function
    # but map some names first
    mapping = {
        'create_database': 'create',
        'duplicate_database': 'duplicate',
        'drop': 'drop',
        'dump_db': 'dump',
        'restore_db': 'restore',
    }
    mapped_method = mapping.get(method, method)
    if hasattr(odoo.modules.db, mapped_method):
        return getattr(odoo.modules.db, mapped_method)(*params)
    
    raise Exception("Method not found: %s" % method)

def exp_create_database(admin_password, db_name, demo, lang, user_password, user_login='admin', country_code=None, phone=None):
    check_super(admin_password)
    return odoo.modules.db.create(db_name, demo=demo, lang=lang, user_password=user_password, user_login=user_login, country_code=country_code, phone=phone)

def exp_duplicate_database(admin_password, db_original_name, db_name, neutralize_database=False):
    check_super(admin_password)
    return odoo.modules.db.duplicate(db_original_name, db_name, neutralize_database=neutralize_database)

def exp_drop(admin_password, db_name):
    check_super(admin_password)
    return odoo.modules.db.drop(db_name)

def exp_dump_db(db_name, dump_file, backup_format='zip', with_filestore=True):
    import io
    if dump_file is None:
        stream = io.BytesIO()
        odoo.modules.db.dump(db_name, stream, backup_format=backup_format, with_filestore=with_filestore)
        stream.seek(0)
        return stream
    else:
        return odoo.modules.db.dump(db_name, dump_file, backup_format=backup_format, with_filestore=with_filestore)

def exp_restore_db(db_name, dump_path, copy=False, neutralize_database=False):
    return odoo.modules.db.restore(db_name, dump_path, copy=copy, neutralize_database=neutralize_database)

def exp_change_admin_password(old_password, new_password):
    if not config.verify_admin_password(old_password):
        raise AccessDenied()
    config['admin_passwd'] = new_password
    config.save()
    return True

def exp_list_lang():
    return [('en_US', 'English (US)')]

def exp_list_countries():
    return []

def exp_list_db_incompatible(dbs):
    return []

def exp_list_db(force=False):
    return odoo.modules.db.list_dbs(force=force)

def check_super(passwd):
    if not config.verify_admin_password(passwd):
        raise AccessDenied()
    return True

# For compatibility with direct imports in database.py
list_db_incompatible = exp_list_db_incompatible
restore_db = exp_restore_db
dump_db = exp_dump_db
