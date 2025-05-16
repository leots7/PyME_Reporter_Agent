"""
Módulo para interactuar con hojas de cálculo de Google Sheets.
"""
from typing import List, Dict, Any, Optional, Union
import pandas as pd
from .google_client import get_google_client
from ...exceptions.sync_exceptions import SheetNotFoundError, DataFormatError

class SheetHandler:
    """
    Clase para manejar operaciones con Google Sheets.
    """
    
    def __init__(self):
        """Inicializa el manejador con el cliente de Google."""
        self.client = get_google_client().get_sheets_client()
    
    def get_spreadsheet(self, spreadsheet_key: str):
        """
        Obtiene una hoja de cálculo por su clave.
        
        Args:
            spreadsheet_key: ID único de la hoja de cálculo
            
        Returns:
            Objeto Spreadsheet de gspread
            
        Raises:
            SheetNotFoundError: Si no se encuentra la hoja de cálculo
        """
        try:
            return self.client.open_by_key(spreadsheet_key)
        except Exception as e:
            raise SheetNotFoundError(f"No se pudo abrir la hoja de cálculo: {str(e)}")
    
    def get_worksheet(self, spreadsheet_key: str, worksheet_index: int = 0, worksheet_name: Optional[str] = None):
        """
        Obtiene una hoja específica de una hoja de cálculo.
        
        Args:
            spreadsheet_key: ID único de la hoja de cálculo
            worksheet_index: Índice de la hoja (por defecto 0, primera hoja)
            worksheet_name: Nombre de la hoja (opcional, tiene prioridad sobre el índice)
            
        Returns:
            Objeto Worksheet de gspread
        """
        spreadsheet = self.get_spreadsheet(spreadsheet_key)
        
        try:
            if worksheet_name:
                return spreadsheet.worksheet(worksheet_name)
            else:
                return spreadsheet.get_worksheet(worksheet_index)
        except Exception as e:
            raise SheetNotFoundError(f"No se pudo acceder a la hoja especificada: {str(e)}")
    
    def get_all_values(self, spreadsheet_key: str, worksheet_index: int = 0, 
                      worksheet_name: Optional[str] = None) -> List[List[Any]]:
        """
        Obtiene todos los valores de una hoja específica.
        
        Args:
            spreadsheet_key: ID único de la hoja de cálculo
            worksheet_index: Índice de la hoja (por defecto 0)
            worksheet_name: Nombre de la hoja (opcional)
            
        Returns:
            Lista de listas con todos los valores
        """
        worksheet = self.get_worksheet(spreadsheet_key, worksheet_index, worksheet_name)
        return worksheet.get_all_values()
    
    def get_as_dataframe(self, spreadsheet_key: str, worksheet_index: int = 0,
                        worksheet_name: Optional[str] = None, has_header: bool = True) -> pd.DataFrame:
        """
        Obtiene los datos de una hoja como un DataFrame de pandas.
        
        Args:
            spreadsheet_key: ID único de la hoja de cálculo
            worksheet_index: Índice de la hoja (por defecto 0)
            worksheet_name: Nombre de la hoja (opcional)
            has_header: Si la primera fila contiene encabezados
            
        Returns:
            DataFrame de pandas con los datos
        """
        worksheet = self.get_worksheet(spreadsheet_key, worksheet_index, worksheet_name)
        
        try:
            if has_header:
                return pd.DataFrame(worksheet.get_all_records())
            else:
                values = worksheet.get_all_values()
                return pd.DataFrame(values[1:], columns=values[0] if values else [])
        except Exception as e:
            raise DataFormatError(f"Error al convertir datos a DataFrame: {str(e)}")
    
    def update_values(self, spreadsheet_key: str, values: List[List[Any]], 
                     range_name: str, worksheet_name: Optional[str] = None) -> dict:
        """
        Actualiza valores en una hoja de cálculo.
        
        Args:
            spreadsheet_key: ID único de la hoja de cálculo
            values: Lista de listas con los valores a actualizar
            range_name: Rango a actualizar (ej: 'A1:B10')
            worksheet_name: Nombre de la hoja (opcional)
            
        Returns:
            Diccionario con el resultado de la operación
        """
        worksheet = self.get_worksheet(spreadsheet_key, worksheet_name=worksheet_name)
        
        try:
            result = worksheet.update(range_name, values)
            return {
                "status": "success",
                "updated_cells": result.get('updatedCells', 0),
                "updated_range": result.get('updatedRange', '')
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error al actualizar valores: {str(e)}"
            }
    
    def append_values(self, spreadsheet_key: str, values: List[List[Any]], 
                     worksheet_name: Optional[str] = None) -> dict:
        """
        Añade filas al final de una hoja de cálculo.
        
        Args:
            spreadsheet_key: ID único de la hoja de cálculo
            values: Lista de listas con los valores a añadir
            worksheet_name: Nombre de la hoja (opcional)
            
        Returns:
            Diccionario con el resultado de la operación
        """
        worksheet = self.get_worksheet(spreadsheet_key, worksheet_name=worksheet_name)
        
        try:
            # Encontrar la primera fila vacía
            values_list = worksheet.get_all_values()
            next_row = len(values_list) + 1
            
            # Añadir valores
            for i, row in enumerate(values):
                worksheet.insert_row(row, next_row + i)
            
            return {
                "status": "success",
                "rows_added": len(values),
                "starting_row": next_row
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error al añadir valores: {str(e)}"
            }
    
    def get_available_spreadsheets(self) -> List[Dict[str, str]]:
        """
        Obtiene una lista de todas las hojas de cálculo disponibles.
        
        Returns:
            Lista de diccionarios con información de las hojas de cálculo
        """
        try:
            spreadsheets = self.client.openall()
            return [
                {"id": sheet.id, "title": sheet.title, "url": sheet.url}
                for sheet in spreadsheets
            ]
        except Exception as e:
            return []

# Instancia para uso directo
sheet_handler = SheetHandler()

# Funciones de conveniencia para compatibilidad con código existente
def get_spreadsheet_by_key(spreadsheet_key):
    """Obtiene una hoja de cálculo utilizando su key."""
    return sheet_handler.get_spreadsheet(spreadsheet_key)

def get_all_values_from_sheet(spreadsheet_key):
    """Obtiene todos los valores de la primera hoja de cálculo."""
    return sheet_handler.get_all_values(spreadsheet_key)

