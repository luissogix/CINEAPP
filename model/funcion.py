from abc import ABC, abstractmethod

from model.sala_llena_error import SalaLlenaError


class Funcion(ABC):
    """Proyección de una película. AGREGACIÓN: recibe una Pelicula ya existente."""

    def __init__(self, id_funcion, horario, pelicula, precio_base, capacidad_total):
        self._id_funcion = id_funcion
        self._horario = horario
        self._pelicula = pelicula          # agregación: objeto creado afuera
        self.precio_base = precio_base
        self.capacidad_total = capacidad_total
        self._asientos_vendidos = 0

    @property
    def id_funcion(self):
        return self._id_funcion

    @property
    def horario(self):
        return self._horario

    @property
    def pelicula(self):
        return self._pelicula

    @property
    def precio_base(self):
        return self._precio_base

    @precio_base.setter
    def precio_base(self, valor):
        if valor <= 0:
            raise ValueError("El precio base debe ser mayor a 0.")
        self._precio_base = valor

    @property
    def capacidad_total(self):
        return self._capacidad_total

    @capacidad_total.setter
    def capacidad_total(self, valor):
        if valor <= 0:
            raise ValueError("La capacidad total debe ser mayor a 0.")
        self._capacidad_total = valor

    @property
    def asientos_vendidos(self):
        return self._asientos_vendidos

    @abstractmethod
    def calcular_precio(self):
        """Cada formato de sala determina su tarifa (polimorfismo)."""

    def hay_asientos_disponibles(self):
        return self._asientos_vendidos < self._capacidad_total

    def ocupar_asiento(self):
        """Regla 2: lanza SalaLlenaError si no quedan asientos."""
        if not self.hay_asientos_disponibles():
            raise SalaLlenaError(self._id_funcion, self._capacidad_total)
        self._asientos_vendidos += 1
