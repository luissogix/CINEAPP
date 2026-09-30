class SalaLlenaError(Exception):
    """Regla 2: la función no tiene asientos disponibles."""

    def __init__(self, id_funcion, capacidad_total):
        self.id_funcion = id_funcion
        self.capacidad_total = capacidad_total
        super().__init__(
            f"Venta bloqueada: la función {id_funcion} está llena "
            f"({capacidad_total}/{capacidad_total} asientos vendidos)."
        )
