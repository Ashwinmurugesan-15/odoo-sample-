import requests
import logging
from odoo import models, api, tools

_logger = logging.getLogger(__name__)

class SmsSms(models.Model):
    _inherit = 'sms.sms'

    def _send(self, unlink_failed=False, unlink_sent=True, raise_exception=False):
        """ Override _send to use TextLocal API """
        
        # 1. Fetch Credentials
        apikey = self.env['ir.config_parameter'].sudo().get_param('sms.textlocal.apikey')
        sender = self.env['ir.config_parameter'].sudo().get_param('sms.textlocal.sender', default='TXTLCL')
        
        if not apikey:
            _logger.warning("TextLocal SMS: No API Key found in System Parameters (sms.textlocal.apikey)")
            # Fallback to super/original behavior OR just fail? 
            # Better to log and return to avoid sending via IAP unexpectedly if that's the goal.
            return super(SmsSms, self)._send(unlink_failed, unlink_sent, raise_exception)

        # 2. Iterate over SMS records to send
        for sms in self:
            try:
                # Prepare number (Ensure it has country code if needed, TextLocal usually expects it)
                number = sms.number
                message = sms.body
                
                # 3. Call TextLocal API
                # Using India endpoint by default, change to 'https://api.txtlocal.com/send/' for global if needed
                url = "https://api.textlocal.in/send/"
                params = {
                    'apikey': apikey,
                    'numbers': number,
                    'message': message,
                    'sender': sender
                }
                
                _logger.info(f"Sending SMS to {number} via TextLocal...")
                response = requests.post(url, data=params)
                result = response.json()
                
                # 4. Handle Response
                if result.get('status') == 'success':
                    _logger.info(f"TextLocal Success: {result}")
                    sms.write({'state': 'sent', 'failure_type': False})
                else:
                    error_msg = f"TextLocal Error: {result.get('errors', 'Unknown')}"
                    _logger.error(error_msg)
                    sms.write({
                        'state': 'error',
                        'failure_type': 'sms_server',
                    })
                    
            except Exception as e:
                _logger.exception("TextLocal Exception")
                sms.write({
                    'state': 'error',
                    'failure_type': 'unknown',
                })

        # Process cleanups (unlink sent)
        if unlink_sent:
            self.filtered(lambda s: s.state == 'sent').unlink()
            
        return True
