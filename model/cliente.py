class Cliente:
    def __init__(self, rut, nombre, edad):
        self._rut = rut
        self.nombre = nombre
        self.edad = edad  # pasa por el setter (validación)

    @property
    def rut(self):
        return self._rut

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not valor.strip():
            raise ValueError("El nombre del cliente no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def edad(self):
        return self._edad

    @edad.setter
    def edad(self, valor):
        if not isinstance(valor, int) or valor < 0 or valor > 120:
            raise ValueError(f"Edad inválida: {valor}. Debe ser un entero entre 0 y 120.")
        self._edad = valor
