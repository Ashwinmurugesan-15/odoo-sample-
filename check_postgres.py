import psycopg2
from psycopg2 import sql

DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "odoo"
DB_PASSWORD = "odoo"
DB_NAME = "odoo"

def check_db():
    try:
        # Connect to default 'postgres' db to check for 'odoo' db existence
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        # Check if 'odoo' database exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        exists = cur.fetchone()
        
        if not exists:
            print(f"Database '{DB_NAME}' does not exist. Attempting to create...")
            try:
                cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
                print(f"Database '{DB_NAME}' created successfully.")
            except Exception as e:
                print(f"Failed to create database: {e}")
        else:
            print(f"Database '{DB_NAME}' already exists.")
            
        cur.close()
        conn.close()
        print("PostgreSQL connection verified.")
        
    except psycopg2.OperationalError as e:
        print(f"Error connecting to PostgreSQL: {e}")
        print("Please ensure PostgreSQL is running and credentials are correct.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    check_db()
