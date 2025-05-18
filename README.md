PyME Reporter Agent

Descripción:
PyME Reporter Agent es una API diseñada para la generación automatizada de reportes financieros para pequeñas y medianas empresas (PyMEs). 
Utiliza inteligencia artificial y sincronización de datos desde Google Sheets, Dropbox y postgreSQL para proporcionar análisis y recomendaciones estratégicas.

Características:
- Autenticación segura con FastAPI
- Sincronización de datos financieros desde Google Sheets y Dropbox
- Generación de reportes personalizados en formato PDF
- Monitorización del estado del sistema con /healthcheck
- Integración con PostgreSQL utilizando SQLAlchemy

Instalación:
1. Clona el repositorio:
   git clone https://github.com/leots7/PyME_Reporter_Agent.git
   cd PyME_Reporter_Agent

2. Instala las dependencias:
   pip install -r requirements.txt

3. Configura el archivo .env con tus credenciales.

4. Ejecuta la API:
   uvicorn backend.main:app --reload

Uso:
- Verificar estado del servicio:
  http://127.0.0.1:8000/healthcheck
- Sincronizar datos desde Google Sheets:
  http://127.0.0.1:8000/sync-google-sheets/{spreadsheet_key}
- Sincronizar archivos desde Dropbox:
  http://127.0.0.1:8000/sync-dropbox/{folder_path}

Contribución:
Si deseas mejorar el proyecto, puedes hacer un fork, agregar tus cambios y enviar un pull request.
Las mejoras en integración de APIs y optimización de procesamiento de datos siempre son bienvenidas.


