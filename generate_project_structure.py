import os

# Estructura completa del proyecto PyME_Reporter
project_structure = {
    "agent": [
        "__init__.py", "main.py",
        "prompts/base_prompts.py",
        "chains/query_chain.py",
        "tools/data_tools.py",
        "interface/agent_api.py"
    ],
    "backend/app": [
        "__init__.py", "main.py",
        "core/config.py", "core/security.py",
        "api/deps.py",
        "api/routes/users.py", "api/routes/reports.py", "api/routes/auth.py",
        "models/user.py", "models/sale.py", "models/product.py",
        "schemas/user.py", "schemas/sale.py", "schemas/report.py",
        "crud/user.py", "crud/sale.py", "crud/product.py",
        "db/base.py", "db/session.py", "db/init_db.py",
        "utils/helpers.py"
    ],
    "backend/tests": [
        "test_users.py", "test_auth.py", "test_reports.py"
    ],
    "frontend/src": [
        "assets/.keep", "components/.keep", "pages/.keep", "services/.keep",
        "context/.keep", "hooks/.keep", "styles/.keep", "App.tsx", "index.tsx"
    ],
    "frontend/public": [],
    "database/sync": [
        "dropbox_sync.py", "gsheet_sync.py", "scheduler.py"
    ],
    "database": [
        "config.py"
    ],
    ".": [
        ".env", "requirements.txt", "pyproject.toml", "README.md", "docker-compose.yml"
    ]
}

def create_structure():
    for base_folder, files in project_structure.items():
        for file in files:
            file_path = os.path.join(base_folder, file)
            dir_path = os.path.dirname(file_path)
            os.makedirs(dir_path, exist_ok=True)

            # Contenido mínimo según tipo de archivo
            if file.endswith("__init__.py"):
                with open(file_path, "w") as f:
                    f.write("# Paquete Python\n")
            elif file.endswith(".py"):
                with open(file_path, "w") as f:
                    f.write(f"# Archivo: {file}\n")
            elif file.endswith(".tsx"):
                with open(file_path, "w") as f:
                    f.write(f"// Componente React: {file}\n")
            elif file.endswith(".keep"):
                open(file_path, "w").close()
            else:
                with open(file_path, "w") as f:
                    f.write("")

    print("✅ Estructura de PyME_Reporter generada correctamente.")

if __name__ == "__main__":
    create_structure()
