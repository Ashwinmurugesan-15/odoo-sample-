# Odoo 19.0 CRM Run Walkthrough

I have successfully set up the environment, fixed dependencies, launched the Odoo CRM module, and configured real email delivery.

## How to Run

1.  **Activate Virtual Environment**:
    Use the `venv_odoo312` which contains the correct Python version (3.12).
    ```powershell
    .\venv_odoo312\Scripts\activate
    ```

2.  **Run Odoo**:
    Run the server using a single command (ensure no other instances are running):
    ```powershell
    python odoo-bin -i crm -d odoo
    ```

3.  **Access**:
    Open [http://localhost:8069](http://localhost:8069) in your browser.
    
    **Login Credentials:**
    - **Email**: `admin`
    - **Password**: `admin`

## Features Status

### CRM Module
- **Visibility**: Working (Visible to Admin).
- **Functionality**: Can create, edit, and move Leads/Opportunities.
- **Errors**: 'New' button and database schema errors have been patched.

### Email Delivery (Gmail)
- **Configuration**: Configured to use `ashlog559@gmail.com` via SMTP (Port 587).
- **Sending**: Verified. Emails sent from Odoo are delivered to real recipients.
- **From Address**: The `admin` user has been updated to use `ashlog559@gmail.com` to prevent "Sender Mismatch" errors.

### Reports
- **XLSX Download**: Working (Session expiration fixed by restarting clean server).

## Troubleshooting History
- **Manifest/Static Files**: Restored from git.
- **Timezone**: Installed `tzdata` for Windows.
- **User Permission**: 'ash' user had issues; 'admin' user is verified and recommended.
- **Session Expired (CSRF Error)**: Can happen after server restarts. Fix: Refresh page (Ctrl+F5) and re-login.

## User Guide

### How to Send an Email to a Lead
1.  **Go to CRM**: Click the "CRM" icon on the main dashboard.
2.  **Select Lead**: Click on the specific Lead or Opportunity card you want to contact.
3.  **Check Email**: Ensure the "Email" field in the lead form (left side) contains the correct address (e.g., `ashwinm26735@gmail.com`).
4.  **Send Message**:
    - Look at the **Chatter** area (right side of the screen).
    - Click **"Send Message"**.
    - Type your subject and message body.
    - Click **"Send"** (Paper plane icon).
5.  **Confirmation**: The message will appear in the chatter log below. The recipient will receive it from `ashlog559@gmail.com`.

## Development: How to Make Code Changes

Yes, you can modify the code and see it on the web page.

### 1. Changing Python Code (`.py` files)
*Example: Adding a new field or changing logic.*
1.  **Stop the Server**: Click in the terminal where Odoo is running and press `Ctrl+C`.
2.  **Edit the Code**: Make your changes in VS Code.
3.  **Restart the Server**:
    Run the command again:
    ```powershell
    python odoo-bin -u crm -d odoo
    ```
    *(The `-u crm` flag tells Odoo to update the module and apply your changes).*

### 2. Changing XML/Views (`.xml` files)
*Example: Adding a button or changing the form layout.*
1.  **Stop the Server** (`Ctrl+C`).
2.  **Edit the XML file**.
3.  **Update the Module**:
    ```powershell
    python odoo-bin -u crm -d odoo
    ```

## Database Connection
The code is currently connected to your local **PostgreSQL** database named `odoo`.
- **Config**: Default local connection (Port 5432).
- **Credentials**: Uses your Windows user.

## How to Enable SMS (Paid Feature)
To make SMS work, you must use Odoo's IAP service:
1.  **Search**: In Odoo, search for "Incoming/Outgoing SMS".
2.  **Buy Credits**: You will see a prompt to "Buy Credits" from Odoo.com.
3.  **Register**: You need to register your database with Odoo.com.
*Note: This costs real money per SMS.*

### FREE Alternatives (Advanced)
To avoid Odoo IAP, you must do **Custom Development** or install **3rd Party Apps**:
1.  **Android Gateway**: Use your own phone's SIM card. (Requires finding a "Mobile SMS Gateway" module).
2.  **API Integration**: Code a module to connect to Twilio, TextLocal, etc. (Requires Python coding).
*There is no built-in "Free" button.*

## How to Change Company Logo
1.  **Go to Settings**: Click "Settings" on the main dashboard.
2.  **General Settings**: Under "Companies", you will see "My Company".
3.  **Manage Companies**: Click "Manage Companies" (external link icon).
4.  **Edit**: Select your company and click the **Pencil icon** on the top-right image placeholder.
5.  **Upload**: Select your logo file from your computer.
6.  **Save**: Click the Cloud icon or standard Save button.

## Data Privacy & Storage
**Where is my data?**
-   All data (Leads, Contacts, Emails) is stored **LOCALLY** on your computer.
-   It lives in the **PostgreSQL Database** (`odoo`).
-   **No business data** is sent to Odoo.com.
    *   *Exception:* If you use paid features like SMS or App Store, Odoo.com validates your credits, but does not read your customer data.



