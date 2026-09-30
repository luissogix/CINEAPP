class Pelicula:
    def __init__(self, id_pelicula, titulo, duracion_minutos, clasificacion, edad_minima):
        self._id_pelicula = id_pelicula
        self._titulo = titulo
        self.duracion_minutos = duracion_minutos
        self._clasificacion = clasificacion
        self.edad_minima = edad_minima

    @property
    def id_pelicula(self):
        return self._id_pelicula

    @property
    def titulo(self):
        return self._titulo

    @property
    def clasificacion(self):
        return self._clasificacion

    @property
    def duracion_minutos(self):
        return self._duracion_minutos

    @duracion_minutos.setter
    def duracion_minutos(self, valor):
        if valor <= 0:
            raise ValueError("La duración debe ser mayor a 0 minutos.")
        self._duracion_minutos = valor

    @property
    def edad_minima(self):
        return self._edad_minima

    @edad_minima.setter
    def edad_minima(self, valor):
        if valor < 0:
            raise ValueError("La edad mínima no puede ser negativa.")
        self._edad_minima = valor

    def es_apta_para(self, edad_cliente):
        return edad_cliente >= self._edad_minima
