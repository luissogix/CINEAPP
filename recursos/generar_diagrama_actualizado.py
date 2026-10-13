import os
import urllib.parse
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin

# 1. GENERAR EL ARCHIVO XML / DRAW.IO COMPLETO Y ACTUALIZADO
xml_content = """<mxfile host="app.diagrams.net" agent="Antigravity AI" scale="1" border="0">
  <diagram id="cineapp-uml-class" name="Diagrama de Clases CINEAPP">
    <mxGraphModel dx="3757" dy="2338" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="2300" pageHeight="1450" background="#121212" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <!-- TITULO -->
        <mxCell id="title" parent="1" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=20;fontStyle=1;fontColor=#F8FAFC;" value="DIAGRAMA DE CLASES UML - CINEAPP (POO SEGURO - SISTEMA ACTUALIZADO)" vertex="1">
          <mxGeometry height="40" width="800" x="750" y="30" as="geometry" />
        </mxCell>

        <!-- EMPLEADO -->
        <mxCell id="Empleado" parent="1" style="swipeable=0;html=1;fillColor=#1E1E2E;strokeColor=#6366F1;fontColor=#E2E8F0;align=left;spacingLeft=8;verticalAlign=top;fontFamily=Consolas;fontSize=11;rounded=1;shadow=1;" value="&lt;B&gt;&amp;lt;&amp;lt;Abstract&amp;gt;&amp;gt;&lt;br&gt;Empleado&lt;/B&gt;&lt;hr&gt;- _id_empleado: str&lt;br&gt;- _nombre: str&lt;br&gt;- _rut: str&lt;hr&gt;+ id_empleado(): str&lt;br&gt;+ nombre(): str&lt;br&gt;+ rut(): str&lt;br&gt;+ &lt;i&gt;get_rol()&lt;/i&gt;: str" vertex="1">
          <mxGeometry height="150" width="220" x="180" y="100" as="geometry" />
        </mxCell>

        <!-- BOLETERO -->
        <mxCell id="Boletero" parent="1" style="swipeable=0;html=1;fillColor=#1E1E2E;strokeColor=#6366F1;fontColor=#E2E8F0;align=left;spacingLeft=8;verticalAlign=top;fontFamily=Consolas;fontSize=11;rounded=1;shadow=1;" value="&lt;B&gt;Boletero&lt;/B&gt;&lt;hr&gt;- _modulo_caja: str&lt;hr&gt;+ modulo_caja(): str&lt;br&gt;+ get_rol(): str&lt;br&gt;+ validar_venta(cliente, funcion): bool&lt;br&gt;+ emitir_entrada(cliente, funcion, asiento): Entrada" vertex="1">
          <mxGeometry height="150" width="340" x="30" y="320" as="geometry" />
        </mxCell>

        <!-- ENCARGADO DULCERIA -->
        <mxCell id="EncargadoDulceria" parent="1" style="swipeable=0;html=1;fillColor=#1E1E2E;strokeColor=#6366F1;fontColor=#E2E8F0;align=left;spacingLeft=8;verticalAlign=top;fontFamily=Consolas;fontSize=11;rounded=1;shadow=1;" value="&lt;B&gt;EncargadoDulceria&lt;/B&gt;&lt;hr&gt;- _turno: str&lt;hr&gt;+ turno(): str&lt;br&gt;+ get_rol(): str&lt;br&gt;+ registrar_venta_dulceria(venta, prod, cant): DetalleVenta" vertex="1">
          <mxGeometry height="150" width="370" x="390" y="320" as="geometry" />
        </mxCell>

        <!-- HERENCIA EMPLEADO -->
        <mxCell id="h1" edge="1" parent="1" source="Boletero" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=0;strokeColor=#818CF8;strokeWidth=2;" target="Empleado">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="h2" edge="1" parent="1" source="EncargadoDulceria" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=0;strokeColor=#818CF8;strokeWidth=2;" target="Empleado">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- CLIENTE (ACTUALIZADO: VALIDACIÓN RUT MODULO 11) -->
        <mxCell id="Cliente" parent="1" style="swipeable=0;html=1;fillColor=#142E1F;strokeColor=#22C55E;fontColor=#DCFCE7;align=left;spacingLeft=8;verticalAlign=top;fontFamily=Consolas;fontSize=11;rounded=1;shadow=1;" value="&lt;B&gt;Cliente&lt;/B&gt;&lt;hr&gt;- _rut: str&lt;br&gt;- _nombre: str&lt;br&gt;- _edad: int&lt;hr&gt;+ rut(): str / setter [valida M&amp;oacute;dulo 11]&lt;br&gt;+ validar_rut(rut_str): bool [static]&lt;br&gt;+ nombre(): str / setter [valida non-empty]&lt;br&gt;+ edad(): int / setter [valida 0..120]" vertex="1">
          <mxGeometry height="170" width="330" x="830" y="90" as="geometry" />
        </mxCell>

        <!-- PELICULA (ACTUALIZADO: CLASIFICACION SETTER Y DICT) -->
        <mxCell id="Pelicula" parent="1" style="swipeable=0;html=1;fillColor=#2E2010;strokeColor=#F59E0B;fontColor=#FEF3C7;align=left;spacingLeft=8;verticalAlign=top;fontFamily=Consolas;fontSize=11;rounded=1;shadow=1;" value="&lt;B&gt;Pelicula&lt;/B&gt;&lt;hr&gt;- _id_pelicula: str&lt;br&gt;- _titulo: str&lt;br&gt;- _duracion_minutos: int&lt;br&gt;- _clasificacion: str&lt;br&gt;- _edad_minima: int&lt;hr&gt;+ id_pelicula(): str&lt;br&gt;+ titulo(): str / setter&lt;br&gt;+ duracion_minutos(): int / setter&lt;br&gt;+ clasificacion(): str / setter [autocalcula]&lt;br&gt;+ edad_minima(): int / setter&lt;br&gt;+ es_apta_para(edad_cliente): bool&lt;br&gt;+ to_dict(): dict / from_dict(): Pelicula" vertex="1">
          <mxGeometry height="220" width="300" x="1440" y="80" as="geometry" />
        </mxCell>

        <!-- FUNCION -->
        <mxCell id="Funcion" parent="1" style="swipeable=0;html=1;fillColor=#1E1E2E;strokeColor=#6366F1;fontColor=#E2E8F0;align=left;spacingLeft=8;verticalAlign=top;fontFamily=Consolas;fontSize=11;rounded=1;shadow=1;" value="&lt;B&gt;&amp;lt;&amp;lt;Abstract&amp;gt;&amp;gt;&lt;br&gt;Funcion&lt;/B&gt;&lt;hr&gt;- _id_funcion: str&lt;br&gt;- _horario: datetime&lt;br&gt;- _pelicula: Pelicula&lt;br&gt;- _precio_base: float&lt;br&gt;- _capacidad_total: int&lt;br&gt;- _asientos_vendidos: int&lt;hr&gt;+ id_funcion(): str&lt;br&gt;+ horario(): datetime&lt;br&gt;+ pelicula(): Pelicula&lt;br&gt;+ precio_base(): float / setter&lt;br&gt;+ capacidad_total(): int / setter&lt;br&gt;+ &lt;i&gt;calcular_precio()&lt;/i&gt;: float&lt;br&gt;+ hay_asientos_disponibles(): bool&lt;br&gt;+ ocupar_asiento(): void [throws SalaLlenaError]" vertex="1">
          <mxGeometry height="240" width="340" x="1410" y="350" as="geometry" />
        </mxCell>

        <!-- AGREGACION FUNCION - PELICULA -->
        <mxCell id="agg1" edge="1" parent="1" source="Funcion" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=open;endFill=0;startArrow=diamond;startFill=0;strokeColor=#F59E0B;strokeWidth=2;" target="Pelicula" value="1..*">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- SUBTIPOS FUNCION -->
        <mxCell id="Funcion2D" parent="1" style="swipeable=0;html=1;fillColor=#1E1E2E;strokeColor=#6366F1;fontColor=#E2E8F0;align=left;spacingLeft=8;verticalAlign=top;fontFamily=Consolas;fontSize=11;rounded=1;shadow=1;" value="&lt;B&gt;Funcion2D&lt;/B&gt;&lt;hr&gt;+ descuento: float&lt;hr&gt;+ calcular_precio(): float" vertex="1">
          <mxGeometry height="80" width="180" x="1485" y="660" as="geometry" />
        </mxCell>
        <mxCell id="Funcion3D" parent="1" style="swipeable=0;html=1;fillColor=#1E1E2E;strokeColor=#6366F1;fontColor=#E2E8F0;align=left;spacingLeft=8;verticalAlign=top;fontFamily=Consolas;fontSize=11;rounded=1;shadow=1;" value="&lt;B&gt;Funcion3D&lt;/B&gt;&lt;hr&gt;+ recargo_3d: float&lt;hr&gt;+ calcular_precio(): float" vertex="1">
          <mxGeometry height="80" width="180" x="1275" y="660" as="geometry" />
        </mxCell>
        <mxCell id="FuncionVIP" parent="1" style="swipeable=0;html=1;fillColor=#1E1E2E;strokeColor=#6366F1;fontColor=#E2E8F0;align=left;spacingLeft=8;verticalAlign=top;fontFamily=Consolas;fontSize=11;rounded=1;shadow=1;" value="&lt;B&gt;FuncionVIP&lt;/B&gt;&lt;hr&gt;+ recargo_vip: float&lt;hr&gt;+ calcular_precio(): float" vertex="1">
          <mxGeometry height="80" width="180" x="1695" y="660" as="geometry" />
        </mxCell>
        <mxCell id="h3" edge="1" parent="1" source="Funcion2D" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=0;strokeColor=#818CF8;strokeWidth=2;" target="Funcion">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="h4" edge="1" parent="1" source="Funcion3D" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=0;strokeColor=#818CF8;strokeWidth=2;" target="Funcion">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="h5" edge="1" parent="1" source="FuncionVIP" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=0;strokeColor=#818CF8;strokeWidth=2;" target="Funcion">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- SALA (AFORO Y BUTACAS VIP) -->
        <mxCell id="Sala" parent="1" style="swipeable=0;html=1;fillColor=#2A1E35;strokeColor=#D946EF;fontColor=#FAE8FF;align=left;spacingLeft=8;verticalAlign=top;fontFamily=Consolas;fontSize=11;rounded=1;shadow=1;" value="&lt;B&gt;Sala&lt;/B&gt;&lt;hr&gt;+ numero_sala: int&lt;br&gt;+ formato: str [2D/3D/VIP]&lt;br&gt;+ capacidad: int [VIP: 4]&lt;br&gt;+ asientos: dict&lt;hr&gt;+ esta_disponible(asiento): bool&lt;br&gt;+ ocupar_asiento(asiento): bool&lt;br&gt;+ mostrar_mapa_asientos(): void" vertex="1">
          <mxGeometry height="160" width="260" x="1800" y="370" as="geometry" />
        </mxCell>

        <!-- VENTA -->
        <mxCell id="Venta" parent="1" style="swipeable=0;html=1;fillColor=#2E1022;strokeColor=#EC4899;fontColor=#FCE7F3;align=left;spacingLeft=8;verticalAlign=top;fontFamily=Consolas;fontSize=11;rounded=1;shadow=1;" value="&lt;B&gt;Venta&lt;/B&gt;&lt;hr&gt;- _id_venta: str&lt;br&gt;- _fecha: datetime&lt;br&gt;- _cliente: Cliente&lt;br&gt;- _detalles: list&lt;hr&gt;+ id_venta(): str&lt;br&gt;+ fecha(): datetime&lt;br&gt;+ cliente(): Cliente&lt;br&gt;+ detalles(): tuple&lt;br&gt;+ total(): float&lt;br&gt;+ agregar_detalle(item, cantidad): DetalleVenta&lt;br&gt;+ calcular_total(): float&lt;br&gt;+ emitir_comprobante(): str" vertex="1">
          <mxGeometry height="210" width="340" x="825" y="340" as="geometry" />
        </mxCell>
        <mxCell id="agg2" edge="1" parent="1" source="Venta" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=open;endFill=0;startArrow=diamond;startFill=0;strokeColor=#22C55E;strokeWidth=2;" target="Cliente" value="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- DETALLE VENTA -->
        <mxCell id="DetalleVenta" parent="1" style="swipeable=0;html=1;fillColor=#25103A;strokeColor=#A855F7;fontColor=#F3E8FF;align=left;spacingLeft=8;verticalAlign=top;fontFamily=Consolas;fontSize=11;rounded=1;shadow=1;" value="&lt;B&gt;DetalleVenta&lt;/B&gt;&lt;hr&gt;- _item: ItemVendible&lt;br&gt;- _cantidad: int&lt;br&gt;- _precio_unitario: float&lt;hr&gt;+ item(): ItemVendible&lt;br&gt;+ cantidad(): int / setter&lt;br&gt;+ precio_unitario(): float&lt;br&gt;+ calcular_subtotal(): float" vertex="1">
          <mxGeometry height="150" width="250" x="870" y="620" as="geometry" />
        </mxCell>
        <mxCell id="comp1" edge="1" parent="1" source="Venta" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=open;endFill=0;startArrow=diamond;startFill=1;strokeColor=#EC4899;strokeWidth=2;" target="DetalleVenta" value="1..*">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- ITEM VENDIBLE -->
        <mxCell id="ItemVendible" parent="1" style="swipeable=0;html=1;fillColor=#1E293B;strokeColor=#94A3B8;fontColor=#F8FAFC;align=left;spacingLeft=8;verticalAlign=top;fontFamily=Consolas;fontSize=11;rounded=1;shadow=1;" value="&lt;B&gt;&amp;lt;&amp;lt;Interface&amp;gt;&amp;gt;&lt;br&gt;ItemVendible&lt;/B&gt;&lt;hr&gt;+ &lt;i&gt;get_precio_unitario()&lt;/i&gt;: float&lt;br&gt;+ &lt;i&gt;get_descripcion()&lt;/i&gt;: str" vertex="1">
          <mxGeometry height="90" width="240" x="520" y="640" as="geometry" />
        </mxCell>
        <mxCell id="agg3" edge="1" parent="1" source="DetalleVenta" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=open;endFill=0;startArrow=diamond;startFill=0;strokeColor=#A855F7;strokeWidth=2;" target="ItemVendible" value="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- ENTRADA -->
        <mxCell id="Entrada" parent="1" style="swipeable=0;html=1;fillColor=#1E293B;strokeColor=#94A3B8;fontColor=#F8FAFC;align=left;spacingLeft=8;verticalAlign=top;fontFamily=Consolas;fontSize=11;rounded=1;shadow=1;" value="&lt;B&gt;Entrada&lt;/B&gt;&lt;hr&gt;- _id_item: str&lt;br&gt;- _funcion: Funcion&lt;br&gt;- _asiento_asignado: str&lt;hr&gt;+ get_precio_unitario(): float&lt;br&gt;+ get_descripcion(): str" vertex="1">
          <mxGeometry height="130" width="230" x="240" y="800" as="geometry" />
        </mxCell>
        <mxCell id="h6" edge="1" parent="1" source="Entrada" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=0;strokeColor=#94A3B8;strokeWidth=2;" target="ItemVendible">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- PRODUCTO DULCERIA -->
        <mxCell id="ProductoDulceria" parent="1" style="swipeable=0;html=1;fillColor=#1E293B;strokeColor=#94A3B8;fontColor=#F8FAFC;align=left;spacingLeft=8;verticalAlign=top;fontFamily=Consolas;fontSize=11;rounded=1;shadow=1;" value="&lt;B&gt;&amp;lt;&amp;lt;Abstract&amp;gt;&amp;gt;&lt;br&gt;ProductoDulceria&lt;/B&gt;&lt;hr&gt;- _id_item: str&lt;br&gt;- _descripcion: str&lt;br&gt;- _stock: int&lt;hr&gt;+ hay_stock(cant): bool&lt;br&gt;+ descontar_stock(cant): void&lt;br&gt;+ &lt;i&gt;get_precio_unitario()&lt;/i&gt;: float" vertex="1">
          <mxGeometry height="140" width="240" x="520" y="800" as="geometry" />
        </mxCell>
        <mxCell id="h7" edge="1" parent="1" source="ProductoDulceria" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=0;strokeColor=#94A3B8;strokeWidth=2;" target="ItemVendible">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- PRODUCTO NACIONAL -->
        <mxCell id="ProductoNacional" parent="1" style="swipeable=0;html=1;fillColor=#1E293B;strokeColor=#38BDF8;fontColor=#F0F9FF;align=left;spacingLeft=8;verticalAlign=top;fontFamily=Consolas;fontSize=11;rounded=1;shadow=1;" value="&lt;B&gt;ProductoNacional&lt;/B&gt;&lt;hr&gt;- _precio_pesos: float&lt;hr&gt;+ precio_pesos(): float / setter&lt;br&gt;+ get_precio_unitario(): float" vertex="1">
          <mxGeometry height="100" width="230" x="390" y="990" as="geometry" />
        </mxCell>
        <mxCell id="h8" edge="1" parent="1" source="ProductoNacional" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=0;strokeColor=#38BDF8;strokeWidth=2;" target="ProductoDulceria">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- PRODUCTO IMPORTADO -->
        <mxCell id="ProductoImportado" parent="1" style="swipeable=0;html=1;fillColor=#1E293B;strokeColor=#38BDF8;fontColor=#F0F9FF;align=left;spacingLeft=8;verticalAlign=top;fontFamily=Consolas;fontSize=11;rounded=1;shadow=1;" value="&lt;B&gt;ProductoImportado&lt;/B&gt;&lt;hr&gt;- _precio_usd: float&lt;br&gt;- _cotizacion: CotizacionDolar [static]&lt;hr&gt;+ precio_usd(): float / setter&lt;br&gt;+ configurar_cotizacion(cotiz): void&lt;br&gt;+ get_precio_unitario(): float" vertex="1">
          <mxGeometry height="130" width="260" x="650" y="990" as="geometry" />
        </mxCell>
        <mxCell id="h9" edge="1" parent="1" source="ProductoImportado" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=0;strokeColor=#38BDF8;strokeWidth=2;" target="ProductoDulceria">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- COTIZACION DOLAR (ACTUALIZADO: API MINDICADOR.CL + FALLBACK) -->
        <mxCell id="CotizacionDolar" parent="1" style="swipeable=0;html=1;fillColor=#142E1F;strokeColor=#22C55E;fontColor=#DCFCE7;align=left;spacingLeft=8;verticalAlign=top;fontFamily=Consolas;fontSize=11;rounded=1;shadow=1;" value="&lt;B&gt;CotizacionDolar&lt;/B&gt;&lt;hr&gt;- _valor_dolar_del_dia: float&lt;br&gt;- _fecha_actualizacion: date&lt;br&gt;- _origen: str&lt;br&gt;+ VALOR_RESPALDO = 950.0&lt;hr&gt;+ obtener_cotizacion_del_dia(): Cotiz [API]&lt;br&gt;+ get_valor_dolar(): float&lt;br&gt;+ actualizar_valor(nuevo_val, fecha): void" vertex="1">
          <mxGeometry height="145" width="290" x="950" y="990" as="geometry" />
        </mxCell>
        <mxCell id="dep1" edge="1" parent="1" source="ProductoImportado" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;dashed=1;endArrow=open;endFill=0;strokeColor=#22C55E;strokeWidth=2;" target="CotizacionDolar" value="&amp;laquo;use&amp;raquo;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- GESTOR PERSISTENCIA (NUEVO: ALMACENAMIENTO JSON P05) -->
        <mxCell id="GestorPersistencia" parent="1" style="swipeable=0;html=1;fillColor=#1E293B;strokeColor=#38BDF8;fontColor=#F0F9FF;align=left;spacingLeft=8;verticalAlign=top;fontFamily=Consolas;fontSize=11;rounded=1;shadow=1;" value="&lt;B&gt;GestorPersistencia&lt;/B&gt;&lt;hr&gt;+ ARCHIVO_DATOS = datos_cine.json&lt;hr&gt;+ cargar_peliculas(): list[Pelicula]&lt;br&gt;+ guardar_peliculas(lista): void&lt;br&gt;+ cargar_ventas(): list&lt;br&gt;+ guardar_venta_registro(dict): void" vertex="1">
          <mxGeometry height="145" width="280" x="1300" y="990" as="geometry" />
        </mxCell>

        <!-- EXCEPCIONES DE NEGOCIO -->
        <mxCell id="EdadInsuficienteError" parent="1" style="swipeable=0;html=1;fillColor=#3B1212;strokeColor=#EF4444;fontColor=#FEE2E2;align=left;spacingLeft=8;verticalAlign=top;fontFamily=Consolas;fontSize=10;rounded=1;shadow=1;" value="&lt;B&gt;EdadInsuficienteError&lt;/B&gt;&lt;br&gt;&amp;lt;&amp;lt;Exception&amp;gt;&amp;gt; [Regla 1]&lt;hr&gt;+ edad_cliente: int&lt;br&gt;+ edad_minima: int&lt;br&gt;+ titulo: str" vertex="1">
          <mxGeometry height="95" width="200" x="20" y="520" as="geometry" />
        </mxCell>
        <mxCell id="dep_ex1" edge="1" parent="1" source="Boletero" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;dashed=1;endArrow=open;endFill=0;strokeColor=#EF4444;strokeWidth=1;" target="EdadInsuficienteError" value="&amp;laquo;lanza&amp;raquo;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="SalaLlenaError" parent="1" style="swipeable=0;html=1;fillColor=#38240D;strokeColor=#F59E0B;fontColor=#FEF3C7;align=left;spacingLeft=8;verticalAlign=top;fontFamily=Consolas;fontSize=10;rounded=1;shadow=1;" value="&lt;B&gt;SalaLlenaError&lt;/B&gt;&lt;br&gt;&amp;lt;&amp;lt;Exception&amp;gt;&amp;gt; [Regla 2]&lt;hr&gt;+ id_funcion: str&lt;br&gt;+ capacidad_total: int" vertex="1">
          <mxGeometry height="95" width="200" x="1190" y="470" as="geometry" />
        </mxCell>
        <mxCell id="dep_ex2" edge="1" parent="1" source="Funcion" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;dashed=1;endArrow=open;endFill=0;strokeColor=#F59E0B;strokeWidth=1;" target="SalaLlenaError" value="&amp;laquo;lanza&amp;raquo;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""

output_drawio = r'C:\Users\lugog\OneDrive\Desktop\CINEAPP\recursos\diagrama_actualizado.drawio'
with open(output_drawio, 'w', encoding='utf-8') as f:
    f.write(xml_content)
print(f"Archivo {output_drawio} creado con éxito.")

# 2. RENDERIZAR EN IMAGEN DE ALTA RESOLUCIÓN (PNG)
W, H = 2200, 1350
img = Image.new('RGB', (W, H), color=(18, 18, 18))
draw = ImageDraw.Draw(img)

# Fuentes
try:
    f_title = ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', 20)
    f_sub = ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf', 12)
    f_box_h = ImageFont.truetype(r'C:\Windows\Fonts\consola.ttf', 13)
    f_box_meta = ImageFont.truetype(r'C:\Windows\Fonts\consola.ttf', 10)
    f_box_b = ImageFont.truetype(r'C:\Windows\Fonts\consola.ttf', 11)
except Exception:
    f_title = ImageFont.load_default()
    f_sub = ImageFont.load_default()
    f_box_h = ImageFont.load_default()
    f_box_meta = ImageFont.load_default()
    f_box_b = ImageFont.load_default()

# Dibujar Cabecera
draw.text((W//2, 30), "DIAGRAMA DE CLASES UML - CINEAPP (POO SEGURO - SISTEMA ACTUALIZADO)", fill=(248, 250, 252), font=f_title, anchor="mt")
draw.text((W//2, 60), "Programación Orientada a Objeto Seguro (TI3V21) | Arquitectura Completa con Guion de Pruebas P01-P19", fill=(148, 163, 184), font=f_sub, anchor="mt")

PALETTE = {
    "empleado": {"bg": (30, 27, 75), "border": (99, 102, 241), "text": (224, 231, 255), "accent": (129, 140, 248)},
    "cliente":  {"bg": (20, 50, 30), "border": (34, 197, 94), "text": (220, 252, 231), "accent": (74, 222, 128)},
    "pelicula": {"bg": (45, 30, 15), "border": (245, 158, 11), "text": (254, 243, 199), "accent": (251, 191, 36)},
    "funcion":  {"bg": (30, 27, 75), "border": (99, 102, 241), "text": (224, 231, 255), "accent": (129, 140, 248)},
    "venta":    {"bg": (45, 15, 35), "border": (236, 72, 153), "text": (252, 231, 243), "accent": (244, 114, 182)},
    "detalle":  {"bg": (35, 15, 55), "border": (168, 85, 247), "text": (243, 232, 255), "accent": (192, 132, 252)},
    "item":     {"bg": (30, 41, 59), "border": (148, 163, 184), "text": (241, 245, 249), "accent": (203, 213, 225)},
    "error1":   {"bg": (55, 18, 18), "border": (239, 68, 68), "text": (254, 226, 226), "accent": (248, 113, 113)},
    "error2":   {"bg": (55, 35, 15), "border": (245, 158, 11), "text": (254, 243, 199), "accent": (251, 191, 36)},
    "dolar":    {"bg": (20, 50, 30), "border": (34, 197, 94), "text": (220, 252, 231), "accent": (74, 222, 128)},
    "sala":     {"bg": (40, 20, 50), "border": (217, 70, 239), "text": (250, 232, 255), "accent": (240, 171, 252)},
    "persistencia": {"bg": (20, 35, 55), "border": (56, 189, 248), "text": (240, 249, 255), "accent": (125, 211, 252)},
}

def draw_class_box(x, y, w, h, title, meta, attrs, methods, theme):
    col = PALETTE[theme]
    draw.rounded_rectangle([x+4, y+4, x+w+4, y+h+4], radius=6, fill=(10, 10, 10))
    draw.rounded_rectangle([x, y, x+w, y+h], radius=6, fill=col["bg"], outline=col["border"], width=2)
    
    curr_y = y + 8
    if meta:
        draw.text((x + w//2, curr_y), meta, fill=col["accent"], font=f_box_meta, anchor="mt")
        curr_y += 14
    draw.text((x + w//2, curr_y), title, fill=(255, 255, 255), font=f_box_h, anchor="mt")
    curr_y += 18
    
    draw.line([(x+6, curr_y), (x+w-6, curr_y)], fill=col["border"], width=1)
    curr_y += 6
    
    for a in attrs:
        draw.text((x + 10, curr_y), a, fill=col["text"], font=f_box_b)
        curr_y += 15
        
    draw.line([(x+6, curr_y), (x+w-6, curr_y)], fill=col["border"], width=1)
    curr_y += 6
    
    for m in methods:
        draw.text((x + 10, curr_y), m, fill=col["text"], font=f_box_b)
        curr_y += 15

# 1. Empleado y derivadas
draw_class_box(180, 100, 220, 145, "Empleado", "<<Abstract>>",
               ["- _id_empleado: str", "- _nombre: str", "- _rut: str"],
               ["+ id_empleado(): str", "+ nombre(): str", "+ rut(): str", "+ get_rol(): str*"], "empleado")

draw_class_box(30, 290, 320, 130, "Boletero", None,
               ["- _modulo_caja: str"],
               ["+ modulo_caja(): str", "+ get_rol(): str", "+ validar_venta(cli, fun): bool", "+ emitir_entrada(cli, fun, asnt): Ent"], "empleado")

draw_class_box(380, 290, 340, 130, "EncargadoDulceria", None,
               ["- _turno: str"],
               ["+ turno(): str", "+ get_rol(): str", "+ registrar_venta_dulceria(v, p, c)"], "empleado")

# 2. Cliente (Actualizado con Módulo 11)
draw_class_box(830, 90, 330, 160, "Cliente", None,
               ["- _rut: str", "- _nombre: str", "- _edad: int"],
               ["+ rut(): str / setter [valida Módulo 11]", "+ validar_rut(rut_str): bool [static]", "+ nombre(): str / setter [valida]", "+ edad(): int / setter [valida 0..120]"], "cliente")

# 3. Película (Actualizado con clasificación setter y dict)
draw_class_box(1440, 80, 300, 200, "Pelicula", None,
               ["- _id_pelicula: str", "- _titulo: str", "- _duracion_minutos: int", "- _clasificacion: str", "- _edad_minima: int"],
               ["+ id_pelicula(): str", "+ titulo(): str / setter", "+ duracion_minutos(): int/setter", "+ clasificacion(): str / setter [autocalc]", "+ edad_minima(): int/setter", "+ es_apta_para(edad): bool", "+ to_dict(): dict / from_dict(): Pelicula"], "pelicula")

# 4. Función y derivadas
draw_class_box(1410, 340, 340, 240, "Funcion", "<<Abstract>>",
               ["- _id_funcion: str", "- _horario: datetime", "- _pelicula: Pelicula", "- _precio_base: float", "- _capacidad_total: int", "- _asientos_vendidos: int"],
               ["+ id_funcion(): str", "+ horario(): datetime", "+ pelicula(): Pelicula", "+ precio_base(): float / setter", "+ capacidad_total(): int / setter", "+ calcular_precio(): float*", "+ hay_asientos_disponibles(): bool", "+ ocupar_asiento(): void [throws]"], "funcion")

draw_class_box(1260, 645, 180, 80, "Funcion3D", None,
               ["+ recargo_3d: float"],
               ["+ calcular_precio(): float"], "funcion")

draw_class_box(1470, 645, 180, 80, "Funcion2D", None,
               ["+ descuento: float"],
               ["+ calcular_precio(): float"], "funcion")

draw_class_box(1680, 645, 180, 80, "FuncionVIP", None,
               ["+ recargo_vip: float"],
               ["+ calcular_precio(): float"], "funcion")

# 5. Sala (Aforo VIP)
draw_class_box(1800, 350, 260, 150, "Sala", None,
               ["+ numero_sala: int", "+ formato: str [2D/3D/VIP]", "+ capacidad: int [VIP: 4]", "+ asientos: dict"],
               ["+ esta_disponible(asiento): bool", "+ ocupar_asiento(asiento): bool", "+ mostrar_mapa_asientos(): void"], "sala")

# 6. Venta y DetalleVenta
draw_class_box(820, 320, 340, 205, "Venta", None,
               ["- _id_venta: str", "- _fecha: datetime", "- _cliente: Cliente", "- _detalles: list"],
               ["+ id_venta(): str", "+ fecha(): datetime", "+ cliente(): Cliente", "+ detalles(): tuple", "+ total(): float", "+ agregar_detalle(item, cant): Det", "+ calcular_total(): float", "+ emitir_comprobante(): str"], "venta")

draw_class_box(865, 590, 250, 145, "DetalleVenta", None,
               ["- _item: ItemVendible", "- _cantidad: int", "- _precio_unitario: float"],
               ["+ item(): ItemVendible", "+ cantidad(): int / setter", "+ precio_unitario(): float", "+ calcular_subtotal(): float"], "detalle")

# 7. ItemVendible y derivadas
draw_class_box(520, 610, 230, 90, "ItemVendible", "<<Interface>>",
               [],
               ["+ get_precio_unitario(): float*", "+ get_descripcion(): str*"], "item")

draw_class_box(240, 770, 230, 115, "Entrada", None,
               ["- _id_item: str", "- _funcion: Funcion", "- _asiento_asignado: str"],
               ["+ get_precio_unitario(): float", "+ get_descripcion(): str"], "item")

draw_class_box(520, 770, 240, 140, "ProductoDulceria", "<<Abstract>>",
               ["- _id_item: str", "- _descripcion: str", "- _stock: int"],
               ["+ hay_stock(cant): bool", "+ descontar_stock(cant): void", "+ get_precio_unitario(): float*"], "item")

draw_class_box(390, 970, 230, 95, "ProductoNacional", None,
               ["- _precio_pesos: float"],
               ["+ precio_pesos(): float / setter", "+ get_precio_unitario(): float"], "item")

draw_class_box(650, 970, 260, 125, "ProductoImportado", None,
               ["- _precio_usd: float", "- _cotizacion: Cotizacion [static]"],
               ["+ precio_usd(): float / setter", "+ configurar_cotizacion(cot): void", "+ get_precio_unitario(): float"], "item")

# 8. Cotización Dólar Oficial (mindicador.cl)
draw_class_box(940, 970, 290, 135, "CotizacionDolar", None,
               ["- _valor_dolar_del_dia: float", "- _fecha_actualizacion: date", "- _origen: str", "+ VALOR_RESPALDO = 950.0"],
               ["+ obtener_cotizacion_del_dia(): Cotiz", "+ get_valor_dolar(): float", "+ actualizar_valor(val, fecha): void"], "dolar")

# 9. GestorPersistencia (Persistencia JSON P05)
draw_class_box(1260, 970, 310, 135, "GestorPersistencia", None,
               ["+ ARCHIVO_DATOS = datos_cine.json"],
               ["+ cargar_peliculas(): list[Pelicula]", "+ guardar_peliculas(lista): void", "+ cargar_ventas(): list", "+ guardar_venta_registro(dict): void"], "persistencia")

# 10. Excepciones
draw_class_box(40, 480, 240, 90, "EdadInsuficienteError", "<<Exception>> [Regla 1]",
               ["+ edad_cliente: int", "+ edad_minima: int", "+ titulo: str"],
               [], "error1")

draw_class_box(1180, 440, 200, 80, "SalaLlenaError", "<<Exception>> [Regla 2]",
               ["+ id_funcion: str", "+ capacidad_total: int"],
               [], "error2")

# DIBUJAR LÍNEAS DE RELACIONES UML
def draw_line(p1, p2, color=(148, 163, 184), width=2, dashed=False):
    if not dashed:
        draw.line([p1, p2], fill=color, width=width)
    else:
        x1, y1 = p1
        x2, y2 = p2
        dist = int(((x2-x1)**2 + (y2-y1)**2)**0.5)
        for i in range(0, dist, 8):
            t1 = i / dist
            t2 = min((i + 4) / dist, 1.0)
            draw.line([(x1 + (x2-x1)*t1, y1 + (y2-y1)*t1), (x1 + (x2-x1)*t2, y1 + (y2-y1)*t2)], fill=color, width=width)

# Herencia Empleado
draw_line((190, 290), (190, 265), color=(129, 140, 248))
draw_line((550, 290), (550, 265), color=(129, 140, 248))
draw_line((190, 265), (550, 265), color=(129, 140, 248))
draw_line((290, 265), (290, 245), color=(129, 140, 248))
draw.polygon([(290, 245), (284, 257), (296, 257)], outline=(129, 140, 248), fill=(18, 18, 18))

# Herencia Funciones
draw_line((1350, 645), (1350, 615), color=(129, 140, 248))
draw_line((1560, 645), (1560, 615), color=(129, 140, 248))
draw_line((1770, 645), (1770, 615), color=(129, 140, 248))
draw_line((1350, 615), (1770, 615), color=(129, 140, 248))
draw_line((1560, 615), (1560, 580), color=(129, 140, 248))
draw.polygon([(1560, 580), (1554, 592), (1566, 592)], outline=(129, 140, 248), fill=(18, 18, 18))

# Herencia ItemVendible
draw_line((355, 770), (355, 730), color=(148, 163, 184))
draw_line((635, 770), (635, 730), color=(148, 163, 184))
draw_line((355, 730), (635, 730), color=(148, 163, 184))
draw_line((635, 730), (635, 700), color=(148, 163, 184))
draw.polygon([(635, 700), (629, 712), (641, 712)], outline=(148, 163, 184), fill=(18, 18, 18))

# Herencia ProductoDulceria
draw_line((505, 970), (505, 940), color=(56, 189, 248))
draw_line((780, 970), (780, 940), color=(56, 189, 248))
draw_line((505, 940), (780, 940), color=(56, 189, 248))
draw_line((640, 940), (640, 910), color=(56, 189, 248))
draw.polygon([(640, 910), (634, 922), (646, 922)], outline=(56, 189, 248), fill=(18, 18, 18))

# Composición Venta -> DetalleVenta
draw_line((990, 525), (990, 590), color=(236, 72, 153))
draw.polygon([(990, 525), (984, 535), (990, 545), (996, 535)], fill=(236, 72, 153))

# Agregación Venta -> Cliente
draw_line((990, 320), (990, 250), color=(34, 197, 94))
draw.polygon([(990, 320), (984, 310), (990, 300), (996, 310)], outline=(34, 197, 94), fill=(18, 18, 18))

# Agregación Funcion -> Pelicula
draw_line((1580, 340), (1580, 280), color=(245, 158, 11))
draw.polygon([(1580, 340), (1574, 330), (1580, 320), (1586, 330)], outline=(245, 158, 11), fill=(18, 18, 18))

# Agregación DetalleVenta -> ItemVendible
draw_line((865, 655), (750, 655), color=(168, 85, 247))
draw.polygon([(865, 655), (855, 649), (845, 655), (855, 661)], outline=(168, 85, 247), fill=(18, 18, 18))

# Dependencia «use» ProductoImportado -> CotizacionDolar
draw_line((910, 1030), (940, 1030), color=(34, 197, 94), dashed=True)
draw.polygon([(940, 1030), (930, 1025), (930, 1035)], fill=(34, 197, 94))

# Dependencia «lanza» Boletero -> EdadInsuficienteError
draw_line((150, 420), (150, 480), color=(239, 68, 68), dashed=True)
draw.polygon([(150, 480), (145, 470), (155, 470)], fill=(239, 68, 68))

# Dependencia «lanza» Funcion -> SalaLlenaError
draw_line((1410, 480), (1380, 480), color=(245, 158, 11), dashed=True)
draw.polygon([(1380, 480), (1390, 475), (1390, 485)], fill=(245, 158, 11))

# Leyenda
draw.rounded_rectangle([30, 1180, 580, 1310], radius=6, fill=(24, 24, 27), outline=(63, 63, 70), width=1)
draw.text((45, 1190), "CONVENCIONES UML Y REGLAS DE NEGOCIO:", fill=(244, 244, 245), font=f_box_h)
draw.text((45, 1210), "• Visibilidad: (-) Privado | (+) Público | (*) Abstracto / Interfaz", fill=(212, 212, 216), font=f_box_meta)
draw.text((45, 1228), "• Relaciones: Herencia (◄—), Composición (♦—), Agregación (◇—), Uso (- - -►)", fill=(212, 212, 216), font=f_box_meta)
draw.text((45, 1246), "• Regla 1: Boletero.validar_venta() lanza EdadInsuficienteError (P15)", fill=(248, 113, 113), font=f_box_meta)
draw.text((45, 1264), "• Regla 2: Funcion.ocupar_asiento() lanza SalaLlenaError (P14)", fill=(251, 191, 36), font=f_box_meta)
draw.text((45, 1282), "• Persistencia: GestorPersistencia serializa en datos_cine.json (P05)", fill=(125, 211, 252), font=f_box_meta)

output_png = r'C:\Users\lugog\OneDrive\Desktop\CINEAPP\Diagrama actualizado.png'
png_info = PngImagePlugin.PngInfo()
png_info.add_text("mxfile", urllib.parse.quote(xml_content))
img.save(output_png, 'PNG', pnginfo=png_info)
print(f"Diagrama actualizado generado exitosamente en: {output_png}")
