import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import streamlit as st
from dotenv import load_dotenv

# === Safe secrets check ===
def is_secrets_available():
    try:
        return bool(st.secrets._parse())
    except:
        return False

# === Load from st.secrets (Cloud) or .env (Local) ===
if is_secrets_available():
    config = {
        "type": st.secrets.get("DB_TYPE"),
        "host": st.secrets.get("DB_HOST"),
        "port": st.secrets.get("DB_PORT", "5432"),
        "name": st.secrets.get("DB_NAME"),
        "user": st.secrets.get("DB_USER"),
        "password": st.secrets.get("DB_PASSWORD"),
    }
else:
    load_dotenv()
    config = {
        "type": os.getenv("DB_TYPE"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT", "5432"),
        "name": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }

# === Check missing ===
missing = [k for k, v in config.items() if not v]
if missing:
    raise EnvironmentError(f"❌ Missing required DB environment variables: {', '.join(missing)}")

# === Connect to DB ===
DATABASE_URL = URL.create(
    drivername=f"{config['type']}+psycopg2",
    username=config["user"],
    password=config["password"],
    host=config["host"],
    port=config["port"],
    database=config["name"],
    query={"sslmode": "require"}
)

engine = create_engine(DATABASE_URL)

# === Utility functions ===
def fetch_table(table_name):
    return pd.read_sql(f"SELECT * FROM {table_name}", engine)

def fetch_query(query):
    return pd.read_sql(query, engine)
