class EdadInsuficienteError(Exception):
    """Regla 1: el cliente no cumple la edad mínima de la película."""

    def __init__(self, edad_cliente, edad_minima, titulo):
        self.edad_cliente = edad_cliente
        self.edad_minima = edad_minima
        self.titulo = titulo
        super().__init__(
            f"Venta bloqueada: el cliente tiene {edad_cliente} años y "
            f"'{titulo}' exige una edad mínima de {edad_minima}."
        )
