# data/db.py

import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

DB_TYPE = os.getenv("DB_TYPE", "postgresql")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# ✅ Debug print for verification
print(f"🔍 [Debug] DB_HOST = '{DB_HOST}'")  

# ✅ Secure Supabase-compatible connection string
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    query={"sslmode": "require"}
)

engine = create_engine(DATABASE_URL)

def fetch_table(table_name):
    try:
        query = f"SELECT * FROM {table_name}"
        return pd.read_sql(query, engine)
    except Exception as e:
        print(f"❌ Error fetching table {table_name}: {e}")
        raise

def fetch_query(query):
    try:
        return pd.read_sql(query, engine)
    except Exception as e:
        print(f"❌ Error running query: {e}")
        raise
