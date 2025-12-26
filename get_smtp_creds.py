
# Extract SMTP credentials safely
servers = env['ir.mail_server'].search([])
for s in servers:
    print(f"Host: {s.smtp_host}, Port: {s.smtp_port}, User: {s.smtp_user}, Pass: {s.smtp_pass}")
