import json
import requests
import sys

url = "http://localhost:8069"
db = "odoo"
username = "admin"
password = "admin"

def test_custom_mail():
    session = requests.Session()
    
    # 1. Authenticate
    print("Authenticating...")
    auth_url = f"{url}/web/session/authenticate"
    auth_data = {
        "jsonrpc": "2.0",
        "params": {
            "db": db,
            "login": username,
            "password": password
        }
    }
    headers = {"Content-Type": "application/json"}
    
    response = session.post(auth_url, data=json.dumps(auth_data), headers=headers)
    result = response.json()
    
    if result.get("error"):
        print("Authentication failed:", result["error"])
        return

    print("Authenticated successfully.")

    # 2. Call custom endpoint
    print("Calling custom email endpoint...")
    endpoint = f"{url}/mail_plugin/send_custom_email"
    payload = {
        "jsonrpc": "2.0",
        "params": {
            "email": "test@example.com",
            "subject": "Test Verification Email",
            "body": "This is a test body."
        }
    }
    
    response = session.post(endpoint, data=json.dumps(payload), headers=headers)
    print("Response:", response.text)
    
    try:
        res_json = response.json()
        if res_json.get("result", {}).get("success"):
            print("SUCCESS: Email request sent.")
        else:
            print("FAILURE: Request processed but returned error or unexpected result.")
    except Exception as e:
        print(f"Error parsing response: {e}")

if __name__ == "__main__":
    test_custom_mail()

