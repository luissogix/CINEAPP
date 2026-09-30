from abc import ABC, abstractmethod


class ItemVendible(ABC):
    """Cualquier producto o servicio que el cine vende."""

    def __init__(self, id_item, descripcion):
        self._id_item = id_item
        self._descripcion = descripcion

    @property
    def id_item(self):
        return self._id_item

    @property
    def descripcion(self):
        return self._descripcion

    def get_descripcion(self):
        return self._descripcion

    @abstractmethod
    def get_precio_unitario(self):
        """Precio en pesos chilenos (polimorfismo)."""
