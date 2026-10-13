"""
Script para restaurar fielmente la portada anterior del informe
Restablece exclusivamente la portada (Table 0, P2, P3, P7, P9, P12, P13, P14)
a su diseño original exacto, garantizando que quepa en la Página 1,
y preservando intactos todos los títulos INACAP, capturas, diagramas y la matriz P01-P19.
"""

import os
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

DOCX_PATH = r"C:\Users\lugog\OneDrive\Desktop\Informe_Sumativa2_CINEAPP.docx"
PDF_PATH = r"C:\Users\lugog\OneDrive\Desktop\Informe_Sumativa2_CINEAPP.pdf"

HEX_ROJO_ORIGINAL = "943634"
HEX_AZUL_ORIGINAL = "003366"
RGB_ROJO_ORIGINAL = RGBColor(148, 54, 52)
RGB_AZUL_ORIGINAL = RGBColor(0, 51, 102)
RGB_NEGRO = RGBColor(0, 0, 0)
RGB_BLANCO = RGBColor(255, 255, 255)


def restaurar_portada():
    print("Restaurando portada anterior en Informe_Sumativa2_CINEAPP.docx...")
    doc = docx.Document(DOCX_PATH)

    # 1. Restaurar Table 0 (Caja grande de Unidad 2 en rojo oscuro con texto blanco)
    if len(doc.tables) > 0:
        t0 = doc.tables[0]
        c0 = t0.rows[0].cells[0]
        c0.text = ""

        lineas_unidad = [
            "UNIDAD 2:",
            "Implementación de",
            "software orientado a",
            "objeto en Python"
        ]

        for i, linea in enumerate(lineas_unidad):
            p = c0.add_paragraph() if i > 0 else c0.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            run = p.add_run(linea)
            run.font.name = "Arial"
            run.font.size = Pt(36.0)
            run.font.bold = True
            run.font.color.rgb = RGB_BLANCO

        # Fondo rojo oscuro original (#943634)
        tcPr = c0._tc.get_or_add_tcPr()
        for child in list(tcPr):
            if child.tag.endswith('shd') or child.tag.endswith('tcMar'):
                tcPr.remove(child)

        tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{HEX_ROJO_ORIGINAL}"/>'))
        tcMar = parse_xml(
            f'<w:tcMar {nsdecls("w")}>'
            f'<w:top w:w="160" w:type="dxa"/>'
            f'<w:bottom w:w="160" w:type="dxa"/>'
            f'<w:left w:w="200" w:type="dxa"/>'
            f'<w:right w:w="200" w:type="dxa"/>'
            f'</w:tcMar>'
        )
        tcPr.append(tcMar)

        t0_tblPr = t0._tbl.tblPr
        for child in list(t0_tblPr):
            if child.tag.endswith('tblBorders'):
                t0_tblPr.remove(child)
        t0_borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="none"/>'
            f'<w:left w:val="none"/>'
            f'<w:bottom w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'<w:insideH w:val="none"/>'
            f'<w:insideV w:val="none"/>'
            f'</w:tblBorders>'
        )
        t0_tblPr.append(t0_borders)

    # 2. Resetear márgenes de párrafos en la portada para que no empujen hacia la página 2
    for i in range(18):
        doc.paragraphs[i].paragraph_format.space_before = Pt(0)
        doc.paragraphs[i].paragraph_format.space_after = Pt(0)

    # 3. Restaurar P2 y P3 (Asignatura y Sumativa N2 en azul #003366, 18 pt negrita)
    if len(doc.paragraphs) > 2:
        p2 = doc.paragraphs[2]
        p2.text = "Programación Orientada a Objeto Seguro"
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p2.runs:
            r.font.name = "Arial"
            r.font.size = Pt(18.0)
            r.font.bold = True
            r.font.color.rgb = RGB_AZUL_ORIGINAL

    if len(doc.paragraphs) > 3:
        p3 = doc.paragraphs[3]
        p3.text = "Sumativa N2"
        p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p3.runs:
            r.font.name = "Arial"
            r.font.size = Pt(18.0)
            r.font.bold = True
            r.font.color.rgb = RGB_AZUL_ORIGINAL

    # 4. Restaurar P7 (Proyecto)
    if len(doc.paragraphs) > 7:
        p7 = doc.paragraphs[7]
        p7.text = ""
        p7.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_lbl = p7.add_run("PROYECTO: ")
        r_lbl.font.name = "Arial"
        r_lbl.font.size = Pt(14.0)
        r_lbl.font.bold = True
        r_lbl.font.color.rgb = RGB_NEGRO

        r_val = p7.add_run("CINEAPP - Sistema de Venta de Entradas y Dulcería")
        r_val.font.name = "Arial"
        r_val.font.size = Pt(14.0)
        r_val.font.bold = False
        r_val.font.color.rgb = RGB_NEGRO

    # 5. Restaurar P9 (Repositorio GitHub)
    if len(doc.paragraphs) > 9:
        p9 = doc.paragraphs[9]
        p9.text = ""
        p9.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_lbl = p9.add_run("REPOSITORIO GITHUB: ")
        r_lbl.font.name = "Arial"
        r_lbl.font.size = Pt(14.0)
        r_lbl.font.bold = True
        r_lbl.font.color.rgb = RGB_NEGRO

        r_val = p9.add_run("https://github.com/luissogix/CINEAPP.git")
        r_val.font.name = "Arial"
        r_val.font.size = Pt(14.0)
        r_val.font.bold = False
        r_val.font.color.rgb = RGB_NEGRO

    # 6. Restaurar P12, P13 y P14 (Integrantes)
    if len(doc.paragraphs) > 14:
        p12 = doc.paragraphs[12]
        p12.text = "Integrantes del Equipo:"
        p12.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for r in p12.runs:
            r.font.name = "Arial"
            r.font.size = Pt(14.0)
            r.font.bold = True
            r.font.color.rgb = RGB_ROJO_ORIGINAL

        p13 = doc.paragraphs[13]
        p13.text = "Debora Sepulveda"
        p13.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for r in p13.runs:
            r.font.name = "Arial"
            r.font.size = Pt(12.0)
            r.font.bold = False
            r.font.color.rgb = RGB_NEGRO

        p14 = doc.paragraphs[14]
        p14.text = "Luis Lugo"
        p14.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for r in p14.runs:
            r.font.name = "Arial"
            r.font.size = Pt(12.0)
            r.font.bold = False
            r.font.color.rgb = RGB_NEGRO

    # Guardar cambios
    doc.save(DOCX_PATH)
    print("Portada anterior restaurada exitosamente en Informe_Sumativa2_CINEAPP.docx.")


def exportar_a_pdf():
    print("Re-exportando a PDF mediante Word COM...")
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
    ps_file = os.path.join(os.path.dirname(__file__), "export_temp_portada.ps1")
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
    restaurar_portada()
    exportar_a_pdf()
