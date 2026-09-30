from model.funcion import Funcion


class FuncionVIP(Funcion):
    def __init__(self, id_funcion, horario, pelicula, precio_base, capacidad_total, recargo_vip):
        super().__init__(id_funcion, horario, pelicula, precio_base, capacidad_total)
        self.recargo_vip = recargo_vip

    @property
    def recargo_vip(self):
        return self._recargo_vip

    @recargo_vip.setter
    def recargo_vip(self, valor):
        if valor < 0:
            raise ValueError("El recargo VIP no puede ser negativo.")
        self._recargo_vip = valor

    def calcular_precio(self):
        return self.precio_base + self._recargo_vip
