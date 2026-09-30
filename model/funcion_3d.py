from model.funcion import Funcion


class Funcion3D(Funcion):
    def __init__(self, id_funcion, horario, pelicula, precio_base, capacidad_total, recargo_3d):
        super().__init__(id_funcion, horario, pelicula, precio_base, capacidad_total)
        self.recargo_3d = recargo_3d

    @property
    def recargo_3d(self):
        return self._recargo_3d

    @recargo_3d.setter
    def recargo_3d(self, valor):
        if valor < 0:
            raise ValueError("El recargo 3D no puede ser negativo.")
        self._recargo_3d = valor

    def calcular_precio(self):
        return self.precio_base + self._recargo_3d
