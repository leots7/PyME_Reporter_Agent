import os
from dotenv import load_dotenv

# Ruta absoluta al .env en la raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path)

import os
print("SQLALCHEMY_DATABASE_URL =", os.getenv("SQLALCHEMY_DATABASE_URL"))


from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv
import logging
import traceback

# App Internals
from backend.app.db.session import get_async_session as get_db, engine
from backend.app.db.base import Base
from backend.auth.router import router as auth_router
from database.sync.google import sync_data_from_google_sheets
from database.exceptions import DatabaseError

# Cargar variables de entorno
load_dotenv()

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pyme_reporter")

# Inicializa la aplicación
app = FastAPI(
    title="PyME Reporter API",
    description="API para el sistema de reportes PyME con autenticación",
    version="1.0.0"
)

# Configurar CORS (permitir todo en desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(auth_router, prefix="/api/v1")

# Evento de inicio: crear tablas
@app.on_event("startup")
async def startup_db():
    logger.info("Iniciando servicio y creando tablas...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Tablas creadas correctamente")
    except Exception as e:
        logger.exception("❌ Error al crear las tablas")
        raise DatabaseError(detail="Error al crear las tablas")

# Ruta raíz
@app.get("/")
async def root():
    return {"message": "¡Bienvenido a PyME Reporter API!"}

# Ruta de verificación de salud
@app.get("/healthcheck")
async def healthcheck(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected",
            "services": ["auth", "reports"]
        }
    except Exception as e:
        logger.exception("❌ Fallo en healthcheck")
        raise HTTPException(status_code=500, detail="Database connection error")

# Sincronización con Google Sheets
@app.get("/sync-google-sheets/{spreadsheet_key}")
async def sync_google_sheets(spreadsheet_key: str):
    try:
        data = await sync_data_from_google_sheets(spreadsheet_key)
        return {"message": "Datos sincronizados correctamente", "data": data}
    except Exception as e:
        logger.exception("❌ Error al sincronizar con Google Sheets")
        raise HTTPException(status_code=500, detail="Error al sincronizar los datos")
