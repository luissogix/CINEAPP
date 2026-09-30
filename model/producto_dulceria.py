from abc import ABC

from model.item_vendible import ItemVendible


class ProductoDulceria(ItemVendible, ABC):
    """Base de los productos de dulcería; controla el stock."""

    def __init__(self, id_item, descripcion, stock):
        super().__init__(id_item, descripcion)
        self.stock = stock

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        if not isinstance(valor, int) or valor < 0:
            raise ValueError(f"Stock inválido: {valor}. Debe ser un entero mayor o igual a 0.")
        self._stock = valor

    def hay_stock(self, cantidad):
        return self._stock >= cantidad

    def descontar_stock(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad a descontar debe ser mayor a 0.")
        if not self.hay_stock(cantidad):
            raise ValueError(
                f"Stock insuficiente de '{self.descripcion}': "
                f"solicitado {cantidad}, disponible {self._stock}."
            )
        self.stock = self._stock - cantidad
