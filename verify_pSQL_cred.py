import os
from dotenv import load_dotenv

print("🚀 Cargando configuración del entorno...")
load_dotenv()

# Listado de variables de entorno necesarias
env_vars = ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB", "POSTGRES_HOST", "POSTGRES_PORT"]

# Verificamos si cada variable está disponible
for var in env_vars:
    value = os.getenv(var)
    if value:
        print(f"✅ {var}: {value}")
    else:
        print(f"❌ {var} no está definida en .env")

print("🔄 Si alguna variable falta, revisa tu archivo .env y corrige los valores.")
