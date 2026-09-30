from abc import ABC, abstractmethod


class Empleado(ABC):
    """Clase abstracta: generaliza a cualquier trabajador del cine."""

    def __init__(self, id_empleado, nombre, rut):
        self._id_empleado = id_empleado
        self._nombre = nombre
        self._rut = rut

    @property
    def id_empleado(self):
        return self._id_empleado

    @property
    def nombre(self):
        return self._nombre

    @property
    def rut(self):
        return self._rut

    @abstractmethod
    def get_rol(self):
        """Cada tipo de empleado declara su rol (impide instanciar Empleado)."""
