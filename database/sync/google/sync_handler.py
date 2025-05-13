from .sheet_handler import get_all_values_from_sheet

def sync_data_from_google_sheets(spreadsheet_key):
    """
    Llama a la función para obtener todos los datos de la hoja de Google Sheets.
    """
    data = get_all_values_from_sheet(spreadsheet_key)
    # Lógica de sincronización o procesamiento de los datos
    return data


