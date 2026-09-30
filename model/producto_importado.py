from model.producto_dulceria import ProductoDulceria


class ProductoImportado(ProductoDulceria):
    """Precio en USD. DEPENDENCIA «use» con CotizacionDolar: no la posee,
    solo la consulta en el momento de calcular el precio."""

    _cotizacion = None  # indicador externo compartido por todos los importados

    def __init__(self, id_item, descripcion, stock, precio_usd):
        super().__init__(id_item, descripcion, stock)
        self.precio_usd = precio_usd

    @classmethod
    def configurar_cotizacion(cls, cotizacion):
        cls._cotizacion = cotizacion

    @property
    def precio_usd(self):
        return self._precio_usd

    @precio_usd.setter
    def precio_usd(self, valor):
        if valor <= 0:
            raise ValueError("El precio en USD debe ser mayor a 0.")
        self._precio_usd = valor

    def get_precio_unitario(self):
        if ProductoImportado._cotizacion is None:
            raise ValueError("No hay cotización del dólar configurada.")
        return self._precio_usd * ProductoImportado._cotizacion.get_valor_dolar()
