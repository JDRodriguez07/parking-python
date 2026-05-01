import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        "Trusted_Connection=yes;"
    )