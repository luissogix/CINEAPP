from model.item_vendible import ItemVendible


class Entrada(ItemVendible):
    """Derecho a un asiento. AGREGACIÓN: recibe una Funcion ya existente."""

    def __init__(self, id_item, funcion, asiento_asignado):
        super().__init__(id_item, f"Entrada '{funcion.pelicula.titulo}' asiento {asiento_asignado}")
        self._funcion = funcion
        self._asiento_asignado = asiento_asignado

    @property
    def funcion(self):
        return self._funcion

    @property
    def asiento_asignado(self):
        return self._asiento_asignado

    def get_precio_unitario(self):
        # Polimorfismo: no se pregunta el tipo de función.
        return self._funcion.calcular_precio()
