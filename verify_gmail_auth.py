import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "ashlog559@gmail.com"
SMTP_PASS = "eyyn mslm zvij shaw"  # User provided

try:
    print(f"Connecting to {SMTP_SERVER}:{SMTP_PORT}...")
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.set_debuglevel(1)  # Verbose output
    
    print("Starting TLS...")
    server.starttls()
    
    print(f"Logging in as {SMTP_USER}...")
    server.login(SMTP_USER, SMTP_PASS)
    print("LOGIN SUCCESSFUL!")
    
    # Try sending a test mail
    msg = MIMEText("This is a direct smtplib test.")
    msg['Subject'] = "Direct SMTP Test"
    msg['From'] = SMTP_USER
    msg['To'] = SMTP_USER
    
    print("Sending test email...")
    server.sendmail(SMTP_USER, SMTP_USER, msg.as_string())
    print("EMAIL SENT SUCCESSFULLY!")
    
    server.quit()

except Exception as e:
    print(f"\nLOGIN/SEND FAILED: {e}")
