from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.session import get_async_session as get_db, engine
from backend.app.db.base import Base
from backend.auth.router import router as auth_router
from database.sync.google import sync_data_from_google_sheets
from database.exceptions import DatabaseError

import logging
import traceback
from dotenv import load_dotenv

load_dotenv()

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializa la app
app = FastAPI(
    title="PyME Reporter API",
    description="API para el sistema de reportes PyME con autenticación",
    version="1.0.0"
)

# Middleware CORS (desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rutas
app.include_router(auth_router, prefix="/api/v1")

# Evento de inicio: creación de tablas
@app.on_event("startup")
async def startup_db():
    logger.info("Creando tablas de la base de datos...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Tablas creadas correctamente")
    except Exception as e:
        logger.error(f"Error al crear las tablas: {e}")
        traceback.print_exc()
        raise DatabaseError(detail="Error al crear las tablas")

# Ruta raíz
@app.get("/")
async def root():
    return {"message": "¡Bienvenido a PyME Reporter API!"}

# Ruta healthcheck
@app.get("/healthcheck")
async def healthcheck(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected",
            "services": ["auth", "reports"]
        }
    except DatabaseError as e:
        logger.error(f"Healthcheck failed: {str(e)}")
        raise DatabaseError(detail="Database connection error")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Unexpected error occurred")

# Ruta de sincronización con Google Sheets
@app.get("/sync-google-sheets/{spreadsheet_key}")
async def sync_google_sheets(spreadsheet_key: str):
    try:
        data = await sync_data_from_google_sheets(spreadsheet_key)
        return {"message": "Datos sincronizados correctamente", "data": data}
    except Exception as e:
        logger.error(f"Error al sincronizar datos desde Google Sheets: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error al sincronizar los datos")
