import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv

# Carga variables de entorno
load_dotenv()

# Configuración de la conexión (usa asyncpg para PostgreSQL)
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://postgres:password@localhost:5432/pyme_reporter"
)

# Motor de base de datos asíncrono
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Muestra logs de SQL en consola (útil para desarrollo)
    poolclass=NullPool  # Opcional: Evita problemas con conexiones persistentes
)

# SessionLocal para inyección de dependencias
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# Base para modelos
Base = declarative_base()

# Función para obtener sesión (usada en FastAPI)
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Función para probar la conexión
async def test_connection():
    try:
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
            return {"status": "✅ ¡Conexión a PostgreSQL exitosa!"}
    except Exception as e:
        return {"error": f"❌ Error de conexión: {str(e)}"}