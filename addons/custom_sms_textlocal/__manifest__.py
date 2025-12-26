{
    'name': 'TextLocal SMS Provider',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Send SMS via TextLocal API',
    'description': """
        Overrides Odoo's default IAP SMS to use TextLocal.
        Configuration:
        Set system parameters:
        - sms.textlocal.apikey
        - sms.textlocal.sender
    """,
    'depends': ['sms'],
    'data': [],
    'installable': True,
    'application': False,
}
