"""Demostración del modelo de clases del Cine (Sumativa N°2)."""
from datetime import datetime

from model import (Boletero, Cliente, CotizacionDolar, EdadInsuficienteError,
                   Empleado, EncargadoDulceria, Funcion2D, Funcion3D,
                   FuncionVIP, Pelicula, ProductoImportado, ProductoNacional,
                   SalaLlenaError, Venta)


def titulo(texto):
    print("\n" + "=" * 62)
    print(texto)
    print("=" * 62)


def clp(monto):
    return "$" + f"{monto:,.0f}".replace(",", ".")


# ---------------------------------------------------------------- datos base
toy = Pelicula("P1", "Toy Story 5", 100, "TE", 0)
conjuro = Pelicula("P2", "El Conjuro", 112, "+18", 18)
horario = datetime(2026, 10, 10, 20, 0)

f2d = Funcion2D("F2D", horario, toy, 5000, 2)                  # capacidad 2 (para llenar la sala)
f3d = Funcion3D("F3D", horario, toy, 5000, 100, recargo_3d=2000)
fvip = FuncionVIP("FVIP", horario, conjuro, 5000, 20, recargo_vip=5000)

boletero = Boletero("E1", "Ana Rojas", "11.111.111-1", "Caja 1")
dulcero = EncargadoDulceria("E2", "Pedro Soto", "22.222.222-2", "Tarde")

cotizacion = CotizacionDolar(900)
ProductoImportado.configurar_cotizacion(cotizacion)
palomitas = ProductoNacional("D1", "Palomitas grandes", 10, 3500)
nachos = ProductoImportado("D2", "Nachos importados", 5, 4.0)   # USD 4

# ------------------------------------------- 1) Tres subtipos, método distinto
titulo("1) POLIMORFISMO: calcular_precio() en los 3 subtipos de Funcion")
for funcion in (f2d, f3d, fvip):
    print(f"{type(funcion).__name__:<11} -> {clp(funcion.calcular_precio())}")

# ------------------------------------------------------- 2) Dato con validación
titulo("2) VALIDACIÓN en el setter (Cliente.edad)")
cliente = Cliente("33.333.333-3", "Luis Lugo", 25)
print(f"Cliente válido creado: {cliente.nombre}, {cliente.edad} años")
try:
    Cliente("44.444.444-4", "Dato Erróneo", -5)
except ValueError as e:
    print(f"ValueError capturado: {e}")
try:
    nachos.stock = -3
except ValueError as e:
    print(f"ValueError capturado (ProductoDulceria.stock): {e}")
try:
    Empleado("E9", "X", "0-0")
except TypeError as e:
    print(f"TypeError capturado (Empleado es abstracta): {e}")

# ----------------------------------------- 3) Transacción con líneas de detalle
titulo("3) TRANSACCIÓN con líneas de detalle (Venta + DetalleVenta)")
venta = Venta("V001", cliente)
entrada = boletero.emitir_entrada(cliente, f3d, "A1")
venta.agregar_detalle(entrada, 1)
dulcero.registrar_venta_dulceria(venta, palomitas, 2)
dulcero.registrar_venta_dulceria(venta, nachos, 1)
print(venta.emitir_comprobante())
print(f"Stock restante -> palomitas: {palomitas.stock}, nachos: {nachos.stock}")

# ------------------------------------------------------- 4) Las dos reglas
titulo("4) REGLAS DEL NEGOCIO (provocadas a propósito)")
menor = Cliente("55.555.555-5", "Nico Menor", 15)
try:
    boletero.emitir_entrada(menor, fvip, "B1")
except EdadInsuficienteError as e:
    print(f"[Regla 1 - Boletero.validar_venta] {e}")

boletero.emitir_entrada(cliente, f2d, "C1")
boletero.emitir_entrada(cliente, f2d, "C2")
try:
    boletero.emitir_entrada(cliente, f2d, "C3")
except SalaLlenaError as e:
    print(f"[Regla 2 - Funcion.ocupar_asiento] {e}")

# ------------------------------------------- 5) Indicador externo (dólar)
titulo("5) PRECIO según indicador externo (CotizacionDolar)")
print(f"Nachos con dólar a {clp(cotizacion.get_valor_dolar())}: {clp(nachos.get_precio_unitario())}")
cotizacion.actualizar_valor(950)
print(f"Nachos con dólar a {clp(cotizacion.get_valor_dolar())}: {clp(nachos.get_precio_unitario())}")

print("\nDemostración finalizada sin errores no controlados.")
