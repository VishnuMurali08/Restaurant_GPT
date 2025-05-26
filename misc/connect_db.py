import os
import pyodbc
from dotenv import load_dotenv

def main():
    load_dotenv()

    DB_SERVER = os.getenv("SERVER")
    DB_DATABASE = os.getenv("DATABASE")
    DB_DRIVER = os.getenv("DRIVER")
    DB_USERNAME = os.getenv("USERNAME")
    DB_PASSWORD = os.getenv("PASSWORD")

    conn_str = (
        f"DRIVER={{{DB_DRIVER}}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_DATABASE};"
        f"UID={DB_USERNAME};"
        f"PWD={DB_PASSWORD};"
        "TrustServerCertificate=yes;"
    )

    try:
        conn = pyodbc.connect(conn_str)
        print(f"✅ Connected to '{DB_DATABASE}' database using SQL Authentication!")
        conn.close()
    except Exception as e:
        print("❌ Connection failed.")
        print("Error:", e)

if __name__ == "__main__":
    main()
