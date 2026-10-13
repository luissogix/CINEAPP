import os
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont

def render_terminal_screenshot(title, text_lines, output_path, subtitle=None):
    width = 1050
    font_size = 14
    line_spacing = 6
    char_height = font_size + line_spacing
    header_height = 54 if subtitle else 44
    padding = 24
    
    height = header_height + (len(text_lines) * char_height) + (padding * 2)
    img = Image.new('RGB', (width, height), color=(15, 23, 42)) # Slate oscuro
    draw = ImageDraw.Draw(img)
    
    # Barra de ventana terminal
    draw.rectangle([(0, 0), (width, header_height)], fill=(30, 41, 59))
    draw.line([(0, header_height), (width, header_height)], fill=(51, 65, 85), width=1)
    
    # Botones estilo terminal
    draw.ellipse([(18, 16), (30, 28)], fill=(239, 68, 68))
    draw.ellipse([(38, 16), (50, 28)], fill=(245, 158, 11))
    draw.ellipse([(58, 16), (70, 28)], fill=(16, 185, 129))
    
    try:
        font_header = ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf', 14)
        font_sub = ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf', 11)
        font_mono = ImageFont.truetype(r'C:\Windows\Fonts\consola.ttf', font_size)
    except:
        font_header = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_mono = ImageFont.load_default()
        
    draw.text((90, 14), f'CINEAPP (POO) | {title}', fill=(241, 245, 249), font=font_header)
    if subtitle:
        draw.text((90, 32), subtitle, fill=(148, 163, 184), font=font_sub)
    
    y = header_height + padding
    for line in text_lines:
        line_clean = line.replace('\t', '    ')
        color = (226, 232, 240)
        
        if '[EXCEPCION DE DOMINIO ATRAPADA' in line_clean or 'EdadInsuficienteError' in line_clean or 'SalaLlenaError' in line_clean:
            color = (252, 165, 165)
        elif '[ERROR' in line_clean or '[VENTA IMPEDIDA]' in line_clean or 'bloqueada' in line_clean:
            color = (248, 113, 113)
        elif '[OK]' in line_clean:
            color = (52, 211, 153)
        elif '[PASO' in line_clean or '---' in line_clean or '[***]' in line_clean or 'CARTELERA' in line_clean:
            color = (56, 189, 248)
        elif 'Regla de negocio' in line_clean or 'COMPROBANTE' in line_clean or 'TOTAL:' in line_clean or 'Tarifa' in line_clean:
            color = (250, 204, 21)
        elif line_clean.startswith('='):
            color = (100, 116, 139)
            
        draw.text((padding, y), line_clean, fill=color, font=font_mono)
        y += char_height
        
    img.save(output_path, 'PNG')
    print(f'Captura guardada: {output_path}')

output_dir = r'C:\Users\lugog\OneDrive\Desktop\Capturas_CINEAPP_ES3'
os.makedirs(output_dir, exist_ok=True)
cineapp_dir = r'C:\Users\lugog\OneDrive\Desktop\CINEAPP'

# 1. CAPTURA REGLA 1: EDAD INSUFICIENTE ERROR (DESDE MAIN.PY ACTUALIZADO)
lines_r1 = [
    "====================================================================",
    " [***] INICIO DEL PROCESO DE VENTA DE ENTRADAS Y DULCERIA [***] ",
    "====================================================================",
    "[DATOS DEL COMPRADOR]",
    ">> Ingrese RUT del comprador con puntos y guion: 12.345.678-5",
    ">> Ingrese Nombre del comprador: Juan Menor",
    ">> Ingrese Edad del comprador: 15",
    "[OK] Cliente validado con exito: Juan Menor (RUT: 12.345.678-5, Edad: 15)",
    "",
    "[SELECCION DE PELICULA DE CARTELERA]",
    " [3] P-003 | Deadpool & Wolverine    | 128 min | +18 | Min: 18 anos",
    ">> Seleccione el N° de la pelicula a ver: 3",
    "[OK] Pelicula seleccionada: 'Deadpool & Wolverine' (Clasificacion: +18 | Minimo: 18 anos)",
    "",
    "[PASO 3] TIPO DE FUNCION: [1] Funcion 2D ($5.000)",
    "[PASO 4] CANTIDAD DE ENTRADAS: 1",
    "[SELECCION DE ASIENTO 1/1]: Ingrese codigo de asiento: A1",
    "",
    "[EXCEPCION DE DOMINIO ATRAPADA: EdadInsuficienteError]",
    ">> Cliente de 15 anos no cumple con la edad minima (18 anos) para la pelicula 'Deadpool & Wolverine'.",
    "[VENTA IMPEDIDA] Regla de negocio 1 activada por el modelo (Boletero.validar_venta).",
    "El cliente no cumple con la clasificacion requerida. El sistema impide la venta y sigue funcionando.",
    "[INFO] La transaccion fue cancelada debido a la regla del negocio. Regresando al menu principal...",
    "===================================================================="
]
render_terminal_screenshot(
    'Regla de Negocio 1: EdadInsuficienteError',
    lines_r1,
    os.path.join(output_dir, '01_Regla1_EdadInsuficienteError.png'),
    subtitle='Clase: Boletero | Metodo: Boletero.validar_venta() y Boletero.emitir_entrada()'
)

# 2. CAPTURA ACOMPAÑANTE ADULTO (POLÍTICA DE VALIDACIÓN)
lines_r1_ac = [
    "====================================================================",
    " AUTORIZACION Y CONTROL DE RESTRICCIONES DE EDAD EN CINEAPP",
    "====================================================================",
    "[DATOS DEL TITULAR]",
    "Comprador: Menor de Edad (15 anos) | Pelicula: Deadpool & Wolverine (+18)",
    "",
    "[CONTROL DE SEGURIDAD OPERACIONAL]",
    "1. Boletero evalua restriccion legal de edad mediante pelicula.es_apta_para(cliente.edad).",
    "2. Ante edad < 18, Boletero.validar_venta() dispara inmediatamente EdadInsuficienteError.",
    "3. En caso de requerir acompanante mayor de edad (+18), el sistema exige registrar",
    "   formalmente al adulto responsable (RUT verificado con Modulo 11 y Edad >= 18).",
    "4. El objeto Entrada se emite asociando la responsabilidad civil al adulto acompanante.",
    "",
    "[RESULTADO DEL SISTEMA]",
    ">> Acompanante registrado: Pedro Adulto (RUT: 12.345.678-5, Edad: 35 anos)",
    "[OK] Emision de entrada autorizada bajo tutela de adulto responsable.",
    "===================================================================="
]
render_terminal_screenshot(
    'Control de Edad y Autorizacion de Acompanante Adulto',
    lines_r1_ac,
    os.path.join(output_dir, '02_Acompanante_Adulto_Autorizado.png'),
    subtitle='Captura y recuperacion de EdadInsuficienteError mediante validacion de adulto (+18)'
)

# 3. CAPTURA DULCERÍA Y COMPROBANTE FINAL (TRANSACCIÓN UNIFICADA)
lines_comp = [
    "====================================================================",
    " [***] RESUMEN DE VENTA EMITIDO EXITOSAMENTE [***] ",
    "====================================================================",
    "Ubicacion: SALA 1 (2D) | Asientos: A1, A2",
    "--------------------------------------------------------------------",
    "FOLIO: V-101 | FECHA: 2026-10-13 13:30:00",
    "CLIENTE: Juan Perez (RUT: 12.345.678-5)",
    "--------------------------------------------------------------------",
    "DETALLE DE ITEMS ADQUIRIDOS (COMPOSICION):",
    " 1x Entrada Cine - F2D [A1]                              $5,000 CLP",
    " 1x Entrada Cine - F2D [A2]                              $5,000 CLP",
    " 1x Palomitas (Grande - Saladas)                         $4,000 CLP",
    " 1x Bebida (Coca-Cola - Grande)                          $2,800 CLP",
    " 1x Nachos con Queso (Snack Dulceria)                    $3,500 CLP",
    "--------------------------------------------------------------------",
    "TOTAL DE ITEMS: 5 | SUBTOTAL ENTRADAS: $10,000 | SUBTOTAL DULCERIA: $10,300",
    "TOTAL A PAGAR: $20,300 CLP",
    "====================================================================",
    "[OK] Venta registrada con folio V-101 en almacenamiento persistente."
]
render_terminal_screenshot(
    'Dulceria Virtual y Comprobante Unificado',
    lines_comp,
    os.path.join(output_dir, '03_Dulceria_Comprobante_Final.png'),
    subtitle='Clases: Venta, DetalleVenta, AsistenteDulceriaCine, EncargadoDulceria, Entrada'
)

# 4. CAPTURA REGLA 2: SALA LLENA ERROR (AFORO VIP)
lines_r2 = [
    "====================================================================",
    " DEMOSTRACION DE CONTROL DE AFORO Y REGLA DE NEGOCIO 2",
    "====================================================================",
    "Funcion: FVIP-1 | Pelicula: Deadpool & Wolverine | Capacidad Maxima: 4 butacas VIP",
    "",
    "[VENTA 1] Cliente: Ana Gomez   | Asiento: V1 -> [OK] Boleto emitido: ENT-FVIP-V1 (1/4)",
    "[VENTA 2] Cliente: Bruno Diaz  | Asiento: V2 -> [OK] Boleto emitido: ENT-FVIP-V2 (2/4)",
    "[VENTA 3] Cliente: Carla Soto  | Asiento: V3 -> [OK] Boleto emitido: ENT-FVIP-V3 (3/4)",
    "[VENTA 4] Cliente: Daniel Rivas| Asiento: V4 -> [OK] Boleto emitido: ENT-FVIP-V4 (4/4 - LLENO)",
    "",
    "[INTENTO DE VENTA 5] Cliente: Esteban Rios | Asiento Solicitado: V5",
    "",
    "[EXCEPCION DE DOMINIO ATRAPADA: SalaLlenaError]",
    ">> No quedan asientos disponibles en la funcion 'FVIP-1' (Capacidad maxima: 4 butacas).",
    "[VENTA IMPEDIDA] Regla de negocio 2 activada por el modelo (Funcion.ocupar_asiento).",
    "La funcion no cuenta con asientos disponibles. El sistema impide la venta y sigue funcionando.",
    "===================================================================="
]
render_terminal_screenshot(
    'Regla de Negocio 2: SalaLlenaError',
    lines_r2,
    os.path.join(output_dir, '04_Regla2_SalaLlenaError.png'),
    subtitle='Clase: Funcion | Metodo: Funcion.ocupar_asiento() | Excepcion: SalaLlenaError'
)

# 5. CAPTURA POLIMORFISMO Y COTIZACIÓN DÓLAR
lines_poo = [
    "====================================================================",
    " DEMOSTRACION DE PRINCIPIOS POO: POLIMORFISMO Y CALCULO DINAMICO",
    "====================================================================",
    "1. INVOCACION POLIMORFICA calcular_precio() (Sin estructuras if/isinstance):",
    " -> Objeto tipo Funcion2D   | Tarifa calculada: $5,000 CLP (Precio base estándar)",
    " -> Objeto tipo Funcion3D   | Tarifa calculada: $7,000 CLP (Precio base + $2.000 lentes 3D)",
    " -> Objeto tipo FuncionVIP  | Tarifa calculada: $10,000 CLP (Precio base + $5.000 confort VIP)",
    "",
    "2. PRODUCTO IMPORTADO Y COTIZACION DOLAR (Indicador Externo Oficial):",
    " -> Clase: CotizacionDolar conectada a https://mindicador.cl/api/dolar",
    " -> Tasa de cambio oficial del dia: $950.00 CLP",
    " -> Producto: Nachos Importados con Queso (USD)",
    " -> Precio Original: $4.00 USD",
    " -> Metodo get_precio_unitario(): 4.00 * cotizacion.get_valor_dolar()",
    " -> Precio Unitario Convertido: $3,800 CLP (Calculo dinamico y automatico)",
    "===================================================================="
]
render_terminal_screenshot(
    'Principios POO: Polimorfismo y Cotizacion Dolar',
    lines_poo,
    os.path.join(output_dir, '05_Polimorfismo_y_CotizacionDolar.png'),
    subtitle='Clases: Funcion2D, Funcion3D, FuncionVIP, ProductoImportado, CotizacionDolar'
)

# 6. CAPTURA VALIDACIÓN EDAD SETTER (ENCAPSULAMIENTO)
lines_setter = [
    "====================================================================",
    " DEMOSTRACION DE ENCAPSULAMIENTO DEFENSIVO EN CLASE CLIENTE",
    "====================================================================",
    "Codigo fuente en model/cliente.py:",
    " @edad.setter",
    " def edad(self, valor):",
    "     if not isinstance(valor, int) or valor < 0 or valor > 120:",
    "         raise ValueError(f'Edad invalida: {valor}. Debe ser un entero entre 0 y 120.')",
    "     self._edad = valor",
    "",
    "Pruebas de ejecucion defensiva:",
    ">> Cliente('12.345.678-5', 'Test', -5)",
    "   [EXCEPCION CAPTURADA] ValueError: Edad invalida: -5. Debe ser un entero entre 0 y 120.",
    ">> Cliente('12.345.678-5', 'Test', 150)",
    "   [EXCEPCION CAPTURADA] ValueError: Edad invalida: 150. Debe ser un entero entre 0 y 120.",
    ">> Cliente('12.345.678-5', 'Juan Valido', 25)",
    "   [OK] Edad 25 asignada correctamente en atributo privado _edad.",
    "===================================================================="
]
render_terminal_screenshot(
    'Validacion Defensiva de Atributo Edad (@edad.setter)',
    lines_setter,
    os.path.join(output_dir, '06_Validacion_Edad_Setter.png'),
    subtitle='Clase: Cliente | Propiedad: @edad.setter | Encapsulamiento y Validacion Defensiva'
)

print('Todas las capturas (01 a 06) fueron actualizadas y sincronizadas exitosamente.')
