from model.funcion import Funcion


class Funcion2D(Funcion):
    def __init__(self, id_funcion, horario, pelicula, precio_base, capacidad_total, descuento: float = 0.0):
        super().__init__(id_funcion, horario, pelicula, precio_base, capacidad_total)
        self.descuento = descuento  # porcentaje ej: 0.10 (10%)

    def calcular_precio(self):
        precio_final = self.precio_base * (1 - self.descuento)
        return precio_final
