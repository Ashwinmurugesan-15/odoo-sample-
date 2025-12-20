# Part of Odoo. See LICENSE file for full copyright and licensing details.

import odoo
from odoo.tools.misc import consteq

def check_session(session, env, request=None):
    if not session.uid:
        return False
    user = env['res.users'].browse(session.uid)
    expected = user._compute_session_token(session.sid)
    if expected and consteq(expected, session.session_token):
        if request:
            # res.device.log is not always available or needed for simple check
            # but we try to follow what odoo/http.py does if possible
            if 'res.device.log' in env:
                env['res.device.log']._update_device(request)
        return True
    return False

def compute_session_token(session, env):
    user = env['res.users'].browse(session.uid)
    return user._compute_session_token(session.sid)
