import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Credentials extracted from Odoo configuration
# Host: smtp.gmail.com, Port: 587
# User: ashlog559@gmail.com
# Pass: eyyn mslm zvij shaw

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "ashlog559@gmail.com"
SMTP_PASS = "eyyn mslm zvij shaw"

def send_pure_email(to_email, subject, body_html):
    try:
        print(f"Connecting to {SMTP_SERVER}:{SMTP_PORT}...")
        
        # Create message container
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = SMTP_USER
        msg['To'] = to_email

        # Attach body
        part1 = MIMEText(body_html, 'html')
        msg.attach(part1)

        # Connect and send
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls() # Secure the connection
            print("Logging in...")
            server.login(SMTP_USER, SMTP_PASS)
            print("Sending email...")
            server.sendmail(SMTP_USER, to_email, msg.as_string())
            
        print("SUCCESS: Email sent successfully via direct SMTP.")
        print("No data was recorded in the Odoo database.")
        
    except Exception as e:
        print(f"FAILURE: Could not send email. Error: {e}")

if __name__ == "__main__":
    # Test data
    TO = "test_lead_direct@example.com"
    SUBJECT = "Pure Python SMTP Email (No Odoo Data)"
    BODY = """
    <html>
      <body>
        <h2>Hello,</h2>
        <p>This email was sent via a standalone Python script.</p>
        <p><b>No Odoo records (Leads, Partners, Messages) were created.</b></p>
        <p>Regards,<br/>Standalone Script</p>
      </body>
    </html>
    """
    
    send_pure_email(TO, SUBJECT, BODY)
