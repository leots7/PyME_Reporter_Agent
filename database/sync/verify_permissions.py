"""
Script para verificar permisos y acceso a servicios externos.
"""
import sys
import os
import json
from typing import Dict, Any

# Añadir directorio raíz al path para importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.sync.google.google_client import get_google_client
from database.sync.dropbox.dropbox_client import get_dropbox_client
from database.config import validate_config, GOOGLE_API_CONFIG, get_service_account_path

def check_google_permissions() -> Dict[str, Any]:
    """
    Verifica los permisos para las APIs de Google.
    
    Returns:
        Diccionario con resultados de la verificación
    """
    results = {
        "service_account_file": {
            "path": get_service_account_path(),
            "exists": False,
            "valid": False
        },
        "connection": {
            "status": "not_tested",
            "message": ""
        },
        "sheets_access": {
            "status": "not_tested",
            "available_sheets": []
        },
        "drive_access": {
            "status": "not_tested",
            "file_count": 0
        }
    }
    
    # Verificar archivo de cuenta de servicio
    sa_path = results["service_account_file"]["path"]
    if os.path.exists(sa_path):
        results["service_account_file"]["exists"] = True
        try:
            with open(sa_path, 'r') as f:
                sa_data = json.load(f)
                required_keys = ["client_email", "private_key", "project_id"]
                if all(key in sa_data for key in required_keys):
                    results["service_account_file"]["valid"] = True
                    results["service_account_file"]["client_email"] = sa_data.get("client_email")
        except Exception as e:
            results["service_account_file"]["error"] = str(e)
    
    # Verificar conexión
    try:
        client = get_google_client()
        connection_result = client.test_connection()
        results["connection"] = connection_result
        
        # Verificar acceso a Sheets
        sheets_client = client.get_sheets_client()
        try:
            spreadsheets = sheets_client.openall()
            results["sheets_access"]["status"] = "success"
            results["sheets_access"]["available_sheets"] = [
                {"id": sheet.id, "title": sheet.title} for sheet in spreadsheets
            ]
        except Exception as e:
            results["sheets_access"]["status"] = "error"
            results["sheets_access"]["message"] = str(e)
        
        # Verificar acceso a Drive
        drive_service = client.get_drive_service()
        try:
            response = drive_service.files().list(
                pageSize=10,
                fields="nextPageToken, files(id, name, mimeType)"
            ).execute()
            files = response.get('files', [])
            results["drive_access"]["status"] = "success"
            results["drive_access"]["file_count"] = len(files)
            results["drive_access"]["files"] = [
                {"id": f.get('id'), "name": f.get('name'), "type": f.get('mimeType')} 
                for f in files[:5]  # Mostrar solo los primeros 5 archivos
            ]
        except Exception as e:
            results["drive_access"]["status"] = "error"
            results["drive_access"]["message"] = str(e)
            
    except Exception as e:
        results["connection"]["status"] = "error"
        results["connection"]["message"] = str(e)
    
    return results

def check_dropbox_permissions() -> Dict[str, Any]:
    """
    Verifica los permisos para la API de Dropbox.
    
    Returns:
        Diccionario con resultados de la verificación
    """
    results = {
        "config": {
            "app_key_present": False,
            "app_secret_present": False,
            "token_present": False
        },
        "connection": {
            "status": "not_tested",
            "message": ""
        }
    }
    
    # Verificar configuración
    from database.config import DROPBOX_CONFIG
    results["config"]["app_key_present"] = bool(DROPBOX_CONFIG.get("app_key"))
    results["config"]["app_secret_present"] = bool(DROPBOX_CONFIG.get("app_secret"))
    results["config"]["token_present"] = bool(DROPBOX_CONFIG.get("access_token") or DROPBOX_CONFIG.get("refresh_token"))
    
    # Si hay suficiente configuración, probar conexión
    if results["config"]["token_present"]:
        try:
            client = get_dropbox_client()
            results["connection"] = client.test_connection()
        except Exception as e:
            results["connection"]["status"] = "error"
            results["connection"]["message"] = str(e)
    
    return results

def main():
    """Función principal para verificar permisos."""
    print("Verificando configuración y permisos...\n")
    
    # Verificar configuración general
    print("=== Configuración general ===")
    config_validation = validate_config()
    for service, valid in config_validation.items():
        status = "✅ Válida" if valid else "❌ Inválida o incompleta"
        print(f"Configuración de {service}: {status}")
    print()
    
    # Verificar permisos de Google
    print("=== Permisos de Google API ===")
    google_results = check_google_permissions()
    
    # Mostrar resultados de archivo de cuenta de servicio
    sa_info = google_results["service_account_file"]
    if sa_info["exists"] and sa_info["valid"]:
        print(f"✅ Archivo de cuenta de servicio: {sa_info['path']}")
        print(f"   Email de cuenta de servicio: {sa_info.get('client_email', 'No disponible')}")
    else:
        print(f"❌ Problema con archivo de cuenta de servicio: {sa_info['path']}")
        if not sa_info["exists"]:
            print("   El archivo no existe")
        elif not sa_info["valid"]:
            print("   El archivo no es válido o está incompleto")
    
    # Mostrar resultados de conexión
    conn_info = google_results["connection"]
    if conn_info["status"] == "success":
        print("✅ Conexión a Google API: Exitosa")
    else:
        print(f"❌ Conexión a Google API: Error - {conn_info.get('message', '')}")
    
    # Mostrar resultados de acceso a Sheets
    sheets_info = google_results["sheets_access"]
    if sheets_info["status"] == "success":
        sheet_count = len(sheets_info["available_sheets"])
        print(f"✅ Acceso a Google Sheets: {sheet_count} hojas disponibles")
        if sheet_count > 0:
            print("   Hojas disponibles:")
            for sheet in sheets_info["available_sheets"][:3]:  # Mostrar solo las primeras 3
                print(f"   - {sheet['title']} (ID: {sheet['id']})")
            if sheet_count > 3:
                print(f"   ... y {sheet_count - 3} más")
    else:
        print(f"❌ Acceso a Google Sheets: Error - {sheets_info.get('message', '')}")
    
    # Mostrar resultados de acceso a Drive
    drive_info = google_results["drive_access"]
    if drive_info["status"] == "success":
        file_count = drive_info["file_count"]
        print(f"✅ Acceso a Google Drive: {file_count} archivos visibles")
        if file_count > 0 and "files" in drive_info:
            print("   Archivos de ejemplo:")
            for file in drive_info["files"]:
                print(f"   - {file['name']} (ID: {file['id']})")
    else:
        print(f"❌ Acceso a Google Drive: Error - {drive_info.get('message', '')}")
    
    print()
    
    # Verificar permisos de Dropbox
    print("=== Permisos de Dropbox API ===")
    dropbox_results = check_dropbox_permissions()
    
    # Mostrar resultados de configuración
    config_info = dropbox_results["config"]
    if all([config_info["app_key_present"], config_info["app_secret_present"], config_info["token_present"]]):
        print("✅ Configuración de Dropbox: Completa")
    else:
        print("❌ Configuración de Dropbox: Incompleta")
        if not config_info["app_key_present"]:
            print("   Falta App Key")
        if not config_info["app_secret_present"]:
            print("   Falta App Secret")
        if not config_info["token_present"]:
            print("   Falta token de acceso o actualización")
    
    # Mostrar resultados de conexión
    conn_info = dropbox_results["connection"]
    if conn_info["status"] == "success":
        print("✅ Conexión a Dropbox API: Exitosa")
        if "name" in conn_info:
            print(f"   Cuenta: {conn_info['name']} ({conn_info.get('email', 'No disponible')})")
    elif conn_info["status"] == "error":
        print(f"❌ Conexión a Dropbox API: Error - {conn_info.get('message', '')}")
    else:
        print("⚠️ Conexión a Dropbox API: No probada (configuración incompleta)")

if __name__ == "__main__":
    main()
