# backend/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database.connection import get_db, Base, engine
from auth.router import router as auth_router
import asyncio
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PyME Reporter API",
    description="API para el sistema de reportes PyME con autenticación",
    version="1.0.0"
)

# Configura CORS (para desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluye el router de autenticación
app.include_router(auth_router, prefix="/api/v1")

# Evento de startup para crear tablas (solo para desarrollo)
@app.on_event("startup")
async def startup_db():
    logger.info("Creando tablas de la base de datos...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Tablas creadas correctamente")

@app.get("/")
async def root():
    return {"message": "¡Bienvenido a PyME Reporter API!"}

@app.get("/healthcheck")
async def healthcheck(db: AsyncSession = Depends(get_db)):
    try:
        # Prueba conexión a DB
        await db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected",
            "services": ["auth", "reports"]
        }
    except Exception as e:
        logger.error(f"Healthcheck failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Database connection error")