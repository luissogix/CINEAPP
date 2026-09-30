from model.edad_insuficiente_error import EdadInsuficienteError
from model.empleado import Empleado
from model.entrada import Entrada


class Boletero(Empleado):
    def __init__(self, id_empleado, nombre, rut, modulo_caja):
        super().__init__(id_empleado, nombre, rut)
        self._modulo_caja = modulo_caja

    @property
    def modulo_caja(self):
        return self._modulo_caja

    def get_rol(self):
        return "Boletero"

    def validar_venta(self, cliente, funcion):
        """Regla 1: lanza EdadInsuficienteError si el cliente no cumple la edad."""
        pelicula = funcion.pelicula
        if not pelicula.es_apta_para(cliente.edad):
            raise EdadInsuficienteError(cliente.edad, pelicula.edad_minima, pelicula.titulo)
        return True

    def emitir_entrada(self, cliente, funcion, asiento):
        self.validar_venta(cliente, funcion)      # Regla 1
        funcion.ocupar_asiento()                  # Regla 2 (SalaLlenaError)
        return Entrada(f"ENT-{funcion.id_funcion}-{asiento}", funcion, asiento)
