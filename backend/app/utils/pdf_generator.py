"""
Módulo para generar reportes en formato PDF a partir de datos formateados.
"""
import os
from datetime import datetime
from typing import Dict, Any
from reportlab.lib.pagesizes import A4, letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, Chart, PageBreak
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing

def generate_pdf_report(report_data: Dict[str, Any], output_file: str, options: Dict[str, Any]) -> str:
    """
    Genera un reporte PDF a partir de los datos formateados.
    
    Args:
        report_data: Datos formateados para el reporte
        output_file: Ruta donde se guardará el archivo PDF
        options: Opciones de configuración para el PDF
        
    Returns:
        Ruta al archivo PDF generado
    """
    # Configurar opciones del PDF
    page_size_name = options.get('page_size', 'A4').upper()
    page_size = A4 if page_size_name == 'A4' else letter
    
    if options.get('orientation', 'portrait').lower() == 'landscape':
        page_size = landscape(page_size)
    
    # Crear el documento
    doc = SimpleDocTemplate(
        output_file,
        pagesize=page_size,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=options.get('title_font_size', 16),
        alignment=1  # Centrado
    )
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Heading2'],
        fontSize=options.get('header_font_size', 12)
    )
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=options.get('body_font_size', 10)
    )
    
    # Elementos del documento
    elements = []
    
    # Añadir logo si está especificado
    logo_path = options.get('company_logo', '')
    if logo_path and os.path.exists(logo_path):
        logo = Image(logo_path, width=150, height=70)
        elements.append(logo)
        elements.append(Spacer(1, 12))
    
    # Título del reporte
    company_name = report_data.get('company_name', 'Empresa')
    report_date = report_data.get('report_date', datetime.now().strftime('%Y-%m-%d'))
    title_text = f"Reporte Financiero: {company_name}"
    elements.append(Paragraph(title_text, title_style))
    elements.append(Spacer(1, 12))
    
    # Fecha del reporte
    date_text = f"Fecha: {report_date}"
    elements.append(Paragraph(date_text, body_style))
    elements.append(Spacer(1, 24))
    
    # Resumen financiero
    elements.append(Paragraph("Resumen Financiero", header_style))
    elements.append(Spacer(1, 12))
    
    financial_summary = report_data.get('financial_summary', {})
    summary_data = [["Concepto", "Valor"]]
    
    for key, value in financial_summary.items():
        # Formatear nombres de conceptos para mejor legibilidad
        formatted_key = key.replace('_', ' ').title()
        # Formatear valores numéricos con separador de miles y dos decimales
        formatted_value = f"${value:,.2f}" if isinstance(value, (int, float)) else str(value)
        summary_data.append([formatted_key, formatted_value])
    
    summary_table = Table(summary_data, colWidths=[doc.width/2.0]*2)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 24))
    
    # Ratios financieros
    if 'key_ratios' in report_data:
        elements.append(Paragraph("Ratios Financieros Clave", header_style))
        elements.append(Spacer(1, 12))
        
        ratios = report_data.get('key_ratios', {})
        ratio_data = [["Ratio", "Valor"]]
        
        for key, value in ratios.items():
            # Formatear nombres de ratios para mejor legibilidad
            formatted_key = key.replace('_', ' ').title()
            # Formatear valores con dos decimales
            formatted_value = f"{value:.2f}" if isinstance(value, (int, float)) else str(value)
            ratio_data.append([formatted_key, formatted_value])
        
        ratio_table = Table(ratio_data, colWidths=[doc.width/2.0]*2)
        ratio_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ]))
        elements.append(ratio_table)
        elements.append(Spacer(1, 24))
    
    # Gráficos
    if 'charts' in report_data:
        elements.append(Paragraph("Análisis Gráfico", header_style))
        elements.append(Spacer(1, 12))
        
        for chart_data in report_data.get('charts', []):
            chart_title = chart_data.get('title', 'Gráfico')
            chart_type = chart_data.get('type', 'bar')
            
            elements.append(Paragraph(chart_title, header_style))
            elements.append(Spacer(1, 12))
            
            if chart_type == 'bar':
                chart = _create_bar_chart(chart_data.get('data', {}), doc.width)
                elements.append(chart)
            elif chart_type == 'pie':
                chart = _create_pie_chart(chart_data.get('data', {}), doc.width)
                elements.append(chart)
            
            elements.append(Spacer(1, 24))
    
    # Datos históricos si están disponibles
    if 'historical_data' in report_data:
        elements.append(PageBreak())
        elements.append(Paragraph("Análisis Histórico", header_style))
        elements.append(Spacer(1, 12))
        
        # Aquí se podrían añadir tablas o gráficos con datos históricos
        # Esta implementación dependerá de la estructura específica de los datos históricos
    
    # Construir el PDF
    doc.build(
        elements,
        onFirstPage=lambda canvas, doc: _add_page_number(canvas, doc, options) if options.get('include_page_numbers', True) else None,
        onLaterPages=lambda canvas, doc: _add_page_number(canvas, doc, options) if options.get('include_page_numbers', True) else None
    )
    
    return output_file

def _create_bar_chart(data: Dict[str, Any], width: float) -> Drawing:
    """Crea un gráfico de barras a partir de los datos proporcionados."""
    drawing = Drawing(width, 250)
    
    chart = VerticalBarChart()
    chart.x = 50
    chart.y = 50
    chart.height = 150
    chart.width = width - 100
    chart.data = [data.get('values', [])]
    chart.strokeColor = colors.black
    
    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = max(data.get('values', [0])) * 1.2
    chart.valueAxis.valueStep = chart.valueAxis.valueMax / 10
    
    chart.categoryAxis.labels.boxAnchor = 'ne'
    chart.categoryAxis.labels.dx = 8
    chart.categoryAxis.labels.dy = -2
    chart.categoryAxis.labels.angle = 30
    chart.categoryAxis.categoryNames = data.get('labels', [])
    
    drawing.add(chart)
    return drawing

def _create_pie_chart(data: Dict[str, Any], width: float) -> Drawing:
    """Crea un gráfico circular a partir de los datos proporcionados."""
    drawing = Drawing(width, 250)
    
    chart = Pie()
    chart.x = width / 2
    chart.y = 125
    chart.width = 200
    chart.height = 200
    chart.data = data.get('values', [])
    chart.labels = data.get('labels', [])
    chart.slices.strokeWidth = 0.5
    
    # Colores para las secciones del pie
    chart.slices[0].fillColor = colors.steelblue
    if len(chart.data) > 1:
        chart.slices[1].fillColor = colors.thistle
    if len(chart.data) > 2:
        chart.slices[2].fillColor = colors.cornflower
    
    drawing.add(chart)
    return drawing

def _add_page_number(canvas, doc, options: Dict[str, Any]):
    """Añade números de página y pie de página al documento."""
    footer_text = options.get('footer_text', '')
    
    # Añadir pie de página
    if footer_text:
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.drawString(72, 36, footer_text)
        canvas.restoreState()
    
    # Añadir número de página
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    page_num_text = f"Página {doc.page}"
    canvas.drawRightString(doc.pagesize[0] - 72, 36, page_num_text)
    canvas.restoreState()
    
    # Añadir timestamp si está configurado
    if options.get('include_timestamp', False):
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        canvas.drawCentredString(doc.pagesize[0] / 2, 36, f"Generado: {timestamp}")
        canvas.restoreState()
