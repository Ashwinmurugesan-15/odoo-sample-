import psycopg2
import sys

try:
    conn = psycopg2.connect(
        host="localhost",
        database="odoo",
        user="odoo",
        password="odoo"
    )
    cur = conn.cursor()
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'crm_lead' AND column_name = 'commercial_partner_id';")
    result = cur.fetchone()
    
    if result:
        print("SUCCESS: Column 'commercial_partner_id' exists.")
    else:
        print("FAILURE: Column 'commercial_partner_id' MISSING.")
        sys.exit(1)
        
    cur.close()
    conn.close()
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
