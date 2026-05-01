from database.connection import get_connection

conn = get_connection()
print("Conexión OK")
conn.close()