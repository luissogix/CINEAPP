from model.funcion import Funcion


class Funcion2D(Funcion):
    def __init__(self, id_funcion, horario, pelicula, precio_base, capacidad_total):
        super().__init__(id_funcion, horario, pelicula, precio_base, capacidad_total)

    def calcular_precio(self):
        return self.precio_base
