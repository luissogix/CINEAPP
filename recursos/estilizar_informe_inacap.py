"""
Script de Estilización Integral del Informe Oficial CINEAPP - Diseño INACAP
Aplica:
1. Paleta de colores oficial INACAP (Rojo #C41230, Azul Marino #1A2B49, Gris Pizarra #475569).
2. Jerarquía tipográfica ordenada y coherente (Heading 1, 2 y 3 sin numeración automática duplicada).
3. Saltos de página estratégicos para que cada sección principal inicie limpia.
4. Unificación, remarcado y reubicación ("dale su sitio") de la Matriz de Pruebas P01-P19 en una tabla destacada con cabecera repetible y badges de estado.
5. Eliminación de propiedades flotantes de la tabla (tblpPr) para que fluya inline con su encabezado 5.6.
6. Estilización de bloques de código (Tables 1-4) con borde acentuado INACAP.
7. Re-exportación limpia a PDF mediante Word COM.
"""

import os
import shutil
import io
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

DOCX_PATH = r"C:\Users\lugog\OneDrive\Desktop\Informe_Sumativa2_CINEAPP.docx"
PDF_PATH = r"C:\Users\lugog\OneDrive\Desktop\Informe_Sumativa2_CINEAPP.pdf"
BACKUP_PATH = r"C:\Users\lugog\OneDrive\Desktop\Informe_Sumativa2_CINEAPP_pre_inacap.docx"

# Colores Oficiales INACAP
HEX_ROJO_INACAP = "C41230"
HEX_AZUL_INACAP = "1A2B49"
HEX_GRIS_PIZARRA = "475569"
HEX_GRIS_FONDO = "F8FAFC"
HEX_BORDE_SUAVE = "CBD5E1"
HEX_VERDE_TEXTO = "166534"
HEX_VERDE_FONDO = "DCFCE7"

RGB_ROJO_INACAP = RGBColor(196, 18, 48)
RGB_AZUL_INACAP = RGBColor(26, 43, 73)
RGB_GRIS_PIZARRA = RGBColor(71, 85, 105)
RGB_TEXTO_OSCURO = RGBColor(30, 41, 59)


def set_cell_background(cell, hex_color):
    """Establece el color de fondo de una celda XML."""
    tcPr = cell._tc.get_or_add_tcPr()
    for child in list(tcPr):
        if child.tag.endswith('shd'):
            tcPr.remove(child)
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'))


def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    """Establece los márgenes internos (padding) de una celda en dxa."""
    tcPr = cell._tc.get_or_add_tcPr()
    for child in list(tcPr):
        if child.tag.endswith('tcMar'):
            tcPr.remove(child)
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def set_cell_valign_center(cell):
    """Alinea verticalmente al centro el contenido de una celda."""
    tcPr = cell._tc.get_or_add_tcPr()
    for child in list(tcPr):
        if child.tag.endswith('vAlign'):
            tcPr.remove(child)
    tcPr.append(parse_xml(f'<w:vAlign {nsdecls("w")} w:val="center"/>'))


def format_heading(paragraph, text, level=1, page_break_before=False):
    """Aplica formato visual y estilo institucional INACAP a un encabezado eliminando numeraciones automáticas obsoletas."""
    paragraph.text = text
    if page_break_before:
        paragraph.paragraph_format.page_break_before = True

    # Eliminar numPr si existe para evitar números automáticos duplicados como 1.1 1.
    if paragraph._p.pPr is not None:
        for child in list(paragraph._p.pPr):
            if child.tag.endswith('numPr'):
                paragraph._p.pPr.remove(child)

    if level == 1:
        if 'Heading 1' in paragraph.part.styles:
            paragraph.style = 'Heading 1'
        paragraph.paragraph_format.space_before = Pt(16)
        paragraph.paragraph_format.space_after = Pt(6)
        for r in paragraph.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(14.5)
            r.font.bold = True
            r.font.color.rgb = RGB_ROJO_INACAP

    elif level == 2:
        if 'Heading 2' in paragraph.part.styles:
            paragraph.style = 'Heading 2'
        paragraph.paragraph_format.space_before = Pt(12)
        paragraph.paragraph_format.space_after = Pt(4)
        for r in paragraph.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(12.0)
            r.font.bold = True
            r.font.color.rgb = RGB_AZUL_INACAP

    elif level == 3:
        paragraph.style = 'Normal'
        paragraph.paragraph_format.space_before = Pt(8)
        paragraph.paragraph_format.space_after = Pt(3)
        for r in paragraph.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(11.0)
            r.font.bold = True
            r.font.color.rgb = RGB_GRIS_PIZARRA


def estilizar_informe():
    print("Iniciando estilización y ordenamiento del informe estilo INACAP...")

    # Restaurar desde respaldo si existe para garantizar estado limpio
    if os.path.exists(BACKUP_PATH):
        shutil.copy2(BACKUP_PATH, DOCX_PATH)
        print("Restaurado estado limpio desde respaldo previo.")
    else:
        shutil.copy2(DOCX_PATH, BACKUP_PATH)
        print(f"Respaldo creado en: {BACKUP_PATH}")

    doc = docx.Document(DOCX_PATH)

    # 1. Configurar estilos en styles.xml si están presentes
    styles = doc.styles
    if 'Heading 1' in styles:
        h1 = styles['Heading 1']
        h1.font.name = 'Arial'
        h1.font.size = Pt(14.5)
        h1.font.bold = True
        h1.font.color.rgb = RGB_ROJO_INACAP

    if 'Heading 2' in styles:
        h2 = styles['Heading 2']
        h2.font.name = 'Arial'
        h2.font.size = Pt(12.0)
        h2.font.bold = True
        h2.font.color.rgb = RGB_AZUL_INACAP

    # 2. Formateo y orden de la Portada institucional
    print("Estilizando Portada institucional...")
    if len(doc.paragraphs) > 2:
        p2 = doc.paragraphs[2]
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p2.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(11.5)
            r.font.bold = True
            r.font.color.rgb = RGB_AZUL_INACAP

    if len(doc.paragraphs) > 3:
        p3 = doc.paragraphs[3]
        p3.text = "EVALUACIÓN SUMATIVA N°2 Y N°3: SOFTWARE ORIENTADO A OBJETOS, PERSISTENCIA Y SEGURIDAD"
        p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p3.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(12.5)
            r.font.bold = True
            r.font.color.rgb = RGB_ROJO_INACAP

    # Table 0: Caja institucional de la unidad temática
    if len(doc.tables) > 0:
        t0 = doc.tables[0]
        c0 = t0.rows[0].cells[0]
        c0.text = "UNIDAD 2 Y 3: Implementación de Software Orientado a Objetos, Persistencia en SQLite y Seguridad en Python"
        for p in c0.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = 'Arial'
                r.font.size = Pt(10.5)
                r.font.bold = True
                r.font.color.rgb = RGB_AZUL_INACAP
        set_cell_background(c0, "F1F5F9")
        set_cell_margins(c0, top=140, bottom=140, left=180, right=180)
        t0_tblPr = t0._tbl.tblPr
        for child in list(t0_tblPr):
            if child.tag.endswith('tblBorders'):
                t0_tblPr.remove(child)
        t0_borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="none"/>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{HEX_ROJO_INACAP}"/>'
            f'<w:bottom w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tblBorders>'
        )
        t0_tblPr.append(t0_borders)

    # P7: Título del Proyecto
    if len(doc.paragraphs) > 7:
        p7 = doc.paragraphs[7]
        p7.text = "PROYECTO: CINEAPP - Sistema de Venta de Entradas y Dulcería"
        for r in p7.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(13.5)
            r.font.bold = True
            r.font.color.rgb = RGB_ROJO_INACAP

    # P9: Repositorio GitHub
    if len(doc.paragraphs) > 9:
        p9 = doc.paragraphs[9]
        for r in p9.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(10.0)
            r.font.bold = True
            r.font.color.rgb = RGB_AZUL_INACAP

    # P12, P13, P14: Integrantes
    if len(doc.paragraphs) > 14:
        p12 = doc.paragraphs[12]
        p12.text = "Integrantes del Equipo (Carrera Ingeniería Informática - INACAP Sede Puente Alto):"
        for r in p12.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(10.5)
            r.font.bold = True
            r.font.color.rgb = RGB_AZUL_INACAP
        for p_int in [doc.paragraphs[13], doc.paragraphs[14]]:
            for r in p_int.runs:
                r.font.name = 'Arial'
                r.font.size = Pt(10.0)
                r.font.bold = True
                r.font.color.rgb = RGB_TEXTO_OSCURO

    # 3. Aplicar Jerarquía de Títulos estilo INACAP
    print("Aplicando jerarquía y colores INACAP a títulos del cuerpo...")

    # SECCIÓN 1: Diagrama de Clases
    format_heading(doc.paragraphs[18], "1. Diagrama de Clases UML (1era versión vs 2da versión)", level=1, page_break_before=True)
    format_heading(doc.paragraphs[25], "1.1 Relaciones Orientadas a Objetos Implementadas", level=2)
    format_heading(doc.paragraphs[27], "1.1.1 Herencia y Polimorfismo (model/funcion_2d.py)", level=3)
    format_heading(doc.paragraphs[32], "1.1.2 Composición - El 'Todo' crea las 'Partes' (model/venta.py)", level=3)
    format_heading(doc.paragraphs[36], "1.1.3 Agregación - El 'Todo' recibe una 'Parte' (model/funcion.py)", level=3)

    # SECCIÓN 2: Evidencia de Funcionamiento
    format_heading(doc.paragraphs[40], "2. Evidencia de Funcionamiento del Sistema", level=1, page_break_before=True)
    format_heading(doc.paragraphs[42], "2.1 Tres subtipos con su método distinto (Polimorfismo)", level=2)
    format_heading(doc.paragraphs[45], "2.2 Dato con validación en Setter (Encapsulamiento)", level=2)
    format_heading(doc.paragraphs[48], "2.3 Transacción con sus líneas de detalle (Composición)", level=2)
    format_heading(doc.paragraphs[51], "2.4 Regla del Negocio 1 Capturada (Edad Insuficiente)", level=2)
    format_heading(doc.paragraphs[56], "2.5 Regla del Negocio 2 Capturada (Sala Llena)", level=2)

    # SECCIÓN 3: Uso de Inteligencia Artificial
    format_heading(doc.paragraphs[60], "3. Uso de Inteligencia Artificial", level=1, page_break_before=True)
    format_heading(doc.paragraphs[62], "3.1 Partes del código propuestas por la IA", level=2)
    format_heading(doc.paragraphs[64], "3.2 Ejemplos concretos y justificación técnica (Adoptado, Modificado, Descartado)", level=2)

    # SECCIÓN 4: Consumo de APIs
    format_heading(doc.paragraphs[68], "4. Consumo e Integración de Servicios Externos (API)", level=1, page_break_before=True)
    format_heading(doc.paragraphs[70], "4.1 Propósito del Módulo y Arquitectura Desacoplada", level=2)
    format_heading(doc.paragraphs[75], "4.2 Especificación Técnica de la API Externa", level=2)
    format_heading(doc.paragraphs[84], "4.3 Mapeo y Normalización de Datos hacia la Clase Pelicula", level=2)
    format_heading(doc.paragraphs[91], "4.4 Integración con el Flujo de Venta (main.py)", level=2)

    # SECCIÓN 5: Cumplimiento de Pruebas P01-P19
    format_heading(doc.paragraphs[103], "5. Implementación y Cumplimiento del Guion de Pruebas Oficial (P01 a P19)", level=1, page_break_before=True)
    format_heading(doc.paragraphs[105], "5.1 Validación Matemática de RUT Chileno con Algoritmo Módulo 11 (P07 y P08)", level=2)
    format_heading(doc.paragraphs[110], "5.2 Módulo CRUD de Películas y Persistencia Relacional en SQLite con Arquitectura DAO (P02 a P06)", level=2)
    format_heading(doc.paragraphs[119], "5.3 Transacción Atómica de Venta y Líneas de Detalle en SQLite (VentaDAO) (P12 y P13)", level=2)
    format_heading(doc.paragraphs[123], "5.4 Indicador Oficial del Dólar (mindicador.cl) con Requests, Timeout y Contingencia Defensiva (P16 y P17)", level=2)

    # Limpiar línea residual si existe
    if len(doc.paragraphs) > 125 and "CLP), asegurando que la transacción prosiga" in doc.paragraphs[125].text:
        doc.paragraphs[125].text = ""

    format_heading(doc.paragraphs[128], "5.5 Menú Principal, Control de Opciones Inválidas y Validación de Entradas (P01, P18 y P19)", level=2)

    # 5.6 Matriz de Pruebas Oficial ("DALE SU SITIO": Salto de página para iniciar limpia arriba)
    format_heading(doc.paragraphs[132], "5.6 Matriz Oficial de Cobertura y Cumplimiento de Pruebas (P01 a P19)", level=2, page_break_before=True)

    p134 = doc.paragraphs[134]
    p134.text = (
        "A continuación, se detalla la matriz integral de verificación para cada una de las 19 pruebas oficiales "
        "establecidas en la pauta de evaluación ministerial (P01 a P19), certificando el 100% de cumplimiento operativo en el sistema CineApp:"
    )
    p134.paragraph_format.space_before = Pt(4)
    p134.paragraph_format.space_after = Pt(8)
    for r in p134.runs:
        r.font.name = 'Arial'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGB_TEXTO_OSCURO

    # Limpiar líneas residuales entre el párrafo y la tabla
    for idx_clean in [133, 135, 136]:
        if idx_clean < len(doc.paragraphs):
            doc.paragraphs[idx_clean].text = ""

    # 4. Estilizar Bloques de Código (Tables 1 a 4)
    print("Estilizando bloques de código (Tables 1-4)...")
    for t_idx in [1, 2, 3, 4]:
        if t_idx < len(doc.tables):
            tbl = doc.tables[t_idx]
            cell = tbl.rows[0].cells[0]
            set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
            tbl_pr = tbl._tbl.tblPr
            for child in list(tbl_pr):
                if child.tag.endswith('tblBorders'):
                    tbl_pr.remove(child)
            bdr = parse_xml(
                f'<w:tblBorders {nsdecls("w")}>'
                f'<w:top w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDE_SUAVE}"/>'
                f'<w:left w:val="single" w:sz="18" w:space="0" w:color="{HEX_ROJO_INACAP}"/>'
                f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDE_SUAVE}"/>'
                f'<w:right w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDE_SUAVE}"/>'
                f'</w:tblBorders>'
            )
            tbl_pr.append(bdr)
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.name = 'Consolas'
                    r.font.size = Pt(9.0)
                    r.font.color.rgb = RGB_TEXTO_OSCURO

    # 5. Reconstruir, Remarcar y Unificar la Tabla de Pruebas P01-P19 ("REMARCALAS")
    print("Remarcando y unificando la Matriz Oficial P01-P19...")

    DATOS_P01_P19 = [
        ("P01", "El programa se ejecuta", "requirements.txt y main.py", "El programa inicia y muestra el menú principal interactivo.", "Cumple (100%)"),
        ("P02", "Crear: película o función", "Película 'Estreno', clasif. +14", "El programa confirma que se guardó en la base de datos SQLite.", "Cumple (100%)"),
        ("P03", "Listar: película o función", "Opción listar del menú", "Aparece el registro recién creado consultado desde PeliculaDAO.", "Cumple (100%)"),
        ("P04", "Modificar: película o función", "Cambio a clasificación +18", "El listado muestra el cambio y recalcula la edad mínima requerida.", "Cumple (100%)"),
        ("P05", "Los datos quedan guardados", "Cerrar, reabrir y listar", "El registro sigue guardado intacto en SQLite (cineapp.db) vía PeliculaDAO.", "Cumple (100%)"),
        ("P06", "Eliminar: película o función", "Eliminar 'Estreno' y listar", "El registro ya no aparece en el catálogo ni en la base de datos.", "Cumple (100%)"),
        ("P07", "RUT comprador correcto", "12.345.678-5", "Lo acepta exitosamente mediante algoritmo Módulo 11 en @rut.setter.", "Cumple (100%)"),
        ("P08", "RUT comprador incorrecto", "12.345.678-9", "Rechaza con mensaje descriptivo por Módulo 11 sin caerse el sistema.", "Cumple (100%)"),
        ("P09", "Tipo Función 2D", "Crear y calcular precio 2D", "Precio de entrada propio ($5.000 general / $4.500 con descuento).", "Cumple (100%)"),
        ("P10", "Tipo Función 3D", "Crear y calcular precio 3D", "Precio propio distinto a 2D ($7.000 con recargo de lentes 3D).", "Cumple (100%)"),
        ("P11", "Tipo Función VIP", "Crear y calcular precio VIP", "Precio propio ($10.000) y capacidad exclusiva limitada a 4 butacas.", "Cumple (100%)"),
        ("P12", "Registrar: venta", "2 entradas + dulcería", "Guardado como un solo registro de venta con transacción atómica en VentaDAO.", "Cumple (100%)"),
        ("P13", "Ver el detalle: venta", "Consultar venta por ID", "Se ven todas sus líneas de detalle y subtotales consultadas desde SQLite.", "Cumple (100%)"),
        ("P14", "Función sin asientos", "Llenar sala VIP (4 cupos) + 1", "Venta impedida mediante excepción SalaLlenaError sin caerse el sistema.", "Cumple (100%)"),
        ("P15", "Película clasificada a menor", "Película +18, comprador 15 años", "Venta impedida mediante EdadInsuficienteError (con opción de acompañante).", "Cumple (100%)"),
        ("P16", "Precio dólar del día", "https://mindicador.cl/api/dolar", "Usa cotización oficial en vivo vía requests para cotizar snacks en USD.", "Cumple (100%)"),
        ("P17", "Dólar sin internet", "Desconectar wifi / timeout 5s", "Avisa contingencia en consola, usa valor de respaldo ($950) y no se cae.", "Cumple (100%)"),
        ("P18", "Opción que no existe", "Opción 99 en menú", "Muestra mensaje de opción inválida y vuelve al menú sin abortar.", "Cumple (100%)"),
        ("P19", "Letras donde va número", "Ingresar 'abc' en edad o boletos", "Captura ValueError, muestra mensaje defensivo y solicita reintento.", "Cumple (100%)"),
    ]

    t5 = doc.tables[5]

    # Eliminar todas las filas previas de Table 5
    while len(t5.rows) > 0:
        p_tbl = t5._tbl
        p_tbl.remove(t5.rows[0]._tr)

    ANCHOS = [Inches(0.65), Inches(1.45), Inches(1.40), Inches(2.20), Inches(0.95)]
    CABECERAS = ["N°", "Qué se prueba", "Dato de Prueba", "Resultado Esperado en CINEAPP", "Estado"]

    # Fila de Cabecera con fondo Rojo INACAP y texto blanco
    hdr_row = t5.add_row()
    trPr_hdr = hdr_row._tr.get_or_add_trPr()
    trPr_hdr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    trPr_hdr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

    for c_idx, texto in enumerate(CABECERAS):
        cell = hdr_row.cells[c_idx]
        cell.width = ANCHOS[c_idx]
        set_cell_background(cell, HEX_ROJO_INACAP)
        set_cell_margins(cell, top=140, bottom=140, left=100, right=100)
        set_cell_valign_center(cell)
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 4] else WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(texto)
        run.font.name = 'Arial'
        run.font.size = Pt(9.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)

    # 19 Filas de Datos P01 a P19
    for r_idx, fila in enumerate(DATOS_P01_P19):
        row = t5.add_row()
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        bg_color = HEX_GRIS_FONDO if (r_idx % 2 == 1) else "FFFFFF"

        for c_idx, val in enumerate(fila):
            cell = row.cells[c_idx]
            cell.width = ANCHOS[c_idx]
            
            if c_idx == 4:
                set_cell_background(cell, HEX_VERDE_FONDO)
            else:
                set_cell_background(cell, bg_color)
                
            set_cell_margins(cell, top=90, bottom=90, left=100, right=100)
            set_cell_valign_center(cell)
            cell.text = ""
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 4] else WD_ALIGN_PARAGRAPH.LEFT
            
            run = p.add_run(val)
            run.font.name = 'Arial'
            run.font.size = Pt(8.5)
            
            if c_idx == 0:
                run.font.bold = True
                run.font.color.rgb = RGB_AZUL_INACAP
            elif c_idx == 4:
                run.font.bold = True
                run.font.color.rgb = RGBColor(22, 101, 52)  # Verde éxito
            else:
                run.font.color.rgb = RGB_TEXTO_OSCURO

    # Bordes de Table 5 (Remarcado Institucional INACAP) y eliminación de propiedades flotantes
    t5_tblPr = t5._tbl.tblPr
    for child in list(t5_tblPr):
        if child.tag.endswith('tblBorders') or child.tag.endswith('tblpPr') or child.tag.endswith('tblOverlap'):
            t5_tblPr.remove(child)
            
    t5_borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="16" w:space="0" w:color="{HEX_ROJO_INACAP}"/>'
        f'<w:left w:val="none"/>'
        f'<w:bottom w:val="single" w:sz="16" w:space="0" w:color="{HEX_ROJO_INACAP}"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDE_SUAVE}"/>'
        f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
        f'</w:tblBorders>'
    )
    t5_tblPr.append(t5_borders)
    t5.alignment = WD_TABLE_ALIGNMENT.CENTER

    # 6. Eliminar Table 6 si aún existe
    if len(doc.tables) > 6:
        print("Eliminando tabla secundaria redundante (Table 6)...")
        t6 = doc.tables[6]
        t6_elem = t6._tbl
        parent = t6_elem.getparent()
        if parent is not None:
            parent.remove(t6_elem)

    # 7. Guardar Documento Word Actualizado
    doc.save(DOCX_PATH)
    print(f"Documento Word estilizado y ordenado con éxito en: {DOCX_PATH}")


def exportar_a_pdf():
    print("Re-exportando informe a PDF mediante Word COM...")
    ps_script = f"""
$ErrorActionPreference = 'Stop'
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {{
    $doc = $word.Documents.Open('{DOCX_PATH}')
    $doc.SaveAs([ref]'{PDF_PATH}', [ref]17)
    $doc.Close()
    Write-Host 'PDF exportado exitosamente.'
}} finally {{
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}}
"""
    ps_file = os.path.join(os.path.dirname(__file__), "export_temp_inacap.ps1")
    with open(ps_file, "w", encoding="utf-8") as f:
        f.write(ps_script)

    try:
        proc = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_file],
            capture_output=True,
            text=True,
            check=True
        )
        print(proc.stdout)
    except subprocess.CalledProcessError as e:
        print("Error al exportar PDF:")
        print(e.stderr)
        raise
    finally:
        if os.path.exists(ps_file):
            os.remove(ps_file)


if __name__ == "__main__":
    estilizar_informe()
    exportar_a_pdf()
