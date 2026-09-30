from model.producto_dulceria import ProductoDulceria


class ProductoNacional(ProductoDulceria):
    def __init__(self, id_item, descripcion, stock, precio_pesos):
        super().__init__(id_item, descripcion, stock)
        self.precio_pesos = precio_pesos

    @property
    def precio_pesos(self):
        return self._precio_pesos

    @precio_pesos.setter
    def precio_pesos(self, valor):
        if valor <= 0:
            raise ValueError("El precio en pesos debe ser mayor a 0.")
        self._precio_pesos = valor

    def get_precio_unitario(self):
        return self._precio_pesos
