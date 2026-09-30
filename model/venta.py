from datetime import datetime

from model.detalle_venta import DetalleVenta


def _clp(monto):
    return "$" + f"{monto:,.0f}".replace(",", ".")


class Venta:
    """Transacción. COMPOSICIÓN con DetalleVenta (crea sus líneas por dentro).
    AGREGACIÓN con Cliente (lo recibe ya existente)."""

    def __init__(self, id_venta, cliente):
        self._id_venta = id_venta
        self._fecha = datetime.now()
        self._cliente = cliente        # agregación
        self._detalles = []            # composición: las partes viven aquí

    @property
    def id_venta(self):
        return self._id_venta

    @property
    def fecha(self):
        return self._fecha

    @property
    def cliente(self):
        return self._cliente

    @property
    def detalles(self):
        return tuple(self._detalles)   # solo lectura desde afuera

    @property
    def total(self):
        return self.calcular_total()

    def agregar_detalle(self, item, cantidad):
        detalle = DetalleVenta(item, cantidad)   # la parte se crea dentro del todo
        self._detalles.append(detalle)
        return detalle

    def calcular_total(self):
        return sum(d.calcular_subtotal() for d in self._detalles)

    def emitir_comprobante(self):
        if not self._detalles:
            raise ValueError("Una venta debe tener al menos una línea de detalle.")
        lineas = [f"COMPROBANTE #{self._id_venta} - {self._fecha:%d/%m/%Y %H:%M}",
                  f"Cliente: {self._cliente.nombre} ({self._cliente.rut})"]
        for d in self._detalles:
            lineas.append(f"  {d.cantidad} x {d.item.get_descripcion()} "
                          f"@ {_clp(d.precio_unitario)} = {_clp(d.calcular_subtotal())}")
        lineas.append(f"TOTAL: {_clp(self.calcular_total())}")
        return "\n".join(lineas)
