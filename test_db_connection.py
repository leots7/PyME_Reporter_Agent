import psycopg2
from dotenv import load_dotenv
import os

print("🚀 Iniciando conexión...")
load_dotenv()
print("🔄 Variables de entorno cargadas.")

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT")
)

print("✅ Conexión exitosa a PostgreSQL")
conn.close()
