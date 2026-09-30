class DetalleVenta:
    """Línea de una Venta. Solo debe crearla Venta.agregar_detalle (composición)."""

    def __init__(self, item, cantidad):
        self._item = item                              # ItemVendible ya existente
        self.cantidad = cantidad
        self._precio_unitario = item.get_precio_unitario()  # precio del momento

    @property
    def item(self):
        return self._item

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("La cantidad debe ser un entero mayor a 0.")
        self._cantidad = valor

    @property
    def precio_unitario(self):
        return self._precio_unitario

    def calcular_subtotal(self):
        return self._cantidad * self._precio_unitario
