from .google_client import authenticate_google_client

def get_spreadsheet_by_key(spreadsheet_key):
    """
    Obtiene una hoja de cálculo utilizando su key.
    """
    client = authenticate_google_client()
    return client.open_by_key(spreadsheet_key)

def get_all_values_from_sheet(spreadsheet_key):
    """
    Obtiene todos los valores de la primera hoja de cálculo.
    """
    spreadsheet = get_spreadsheet_by_key(spreadsheet_key)
    worksheet = spreadsheet.sheet1
    return worksheet.get_all_values()
