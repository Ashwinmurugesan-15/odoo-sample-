# Walkthrough: Custom Email Template (Standalone Logic)

I have updated the standalone solution to use an **external HTML file** for the email template. This allows you to design your "Own Template" easily without touching Python code.

## How to Customize the Template
1.  Open `d:\odoo-19.0\odoo-19.0\custom_lead_template.html`.
2.  Edit the HTML as you see fit. You can use standard Odoo QWeb placeholders like `<t t-out="object.name"/>`.

## How to Send with the New Template
Run the shell command as before. The script will automatically read your updated HTML file, update the Odoo template, and send the email.

```powershell
Get-Content send_mail_shell.py | d:\odoo-19.0\odoo-19.0\venv_odoo312\Scripts\python.exe odoo-bin shell -d odoo --no-http
```

## Solution Files
- `send_mail_shell.py`: Main logic script (don't need to touch this often).
- `custom_lead_template.html`: **Your Custom Email Design**.
