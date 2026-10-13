class Pelicula:
    """
    Representa una película en el catálogo del cine.
    Permite encapsulamiento de datos y modificación de atributos como título y clasificación.
    """

    def __init__(self, id_pelicula, titulo, duracion_minutos, clasificacion, edad_minima=None):
        self._id_pelicula = str(id_pelicula)
        self.titulo = titulo
        self.duracion_minutos = duracion_minutos
        self.clasificacion = clasificacion
        if edad_minima is not None:
            self.edad_minima = edad_minima

    @property
    def id_pelicula(self):
        return self._id_pelicula

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("El título de la película no puede estar vacío.")
        self._titulo = str(valor).strip()

    @property
    def clasificacion(self):
        return self._clasificacion

    @clasificacion.setter
    def clasificacion(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("La clasificación no puede estar vacía.")
        val_limpio = str(valor).strip().upper()
        self._clasificacion = val_limpio
        # Ajuste automático de edad mínima sugerida según estándar de cine chileno
        if "+18" in val_limpio or "18" in val_limpio:
            self._edad_minima = 18
        elif "+14" in val_limpio or "14" in val_limpio:
            self._edad_minima = 14
        elif "+7" in val_limpio or "7" in val_limpio:
            self._edad_minima = 7
        elif "TE" in val_limpio:
            self._edad_minima = 0

    @property
    def duracion_minutos(self):
        return self._duracion_minutos

    @duracion_minutos.setter
    def duracion_minutos(self, valor):
        val_int = int(valor)
        if val_int <= 0:
            raise ValueError("La duración debe ser mayor a 0 minutos.")
        self._duracion_minutos = val_int

    @property
    def edad_minima(self):
        return self._edad_minima

    @edad_minima.setter
    def edad_minima(self, valor):
        val_int = int(valor)
        if val_int < 0:
            raise ValueError("La edad mínima no puede ser negativa.")
        self._edad_minima = val_int

    def es_apta_para(self, edad_cliente):
        return edad_cliente >= self._edad_minima

    def to_dict(self):
        return {
            "id_pelicula": self.id_pelicula,
            "titulo": self.titulo,
            "duracion_minutos": self.duracion_minutos,
            "clasificacion": self.clasificacion,
            "edad_minima": self.edad_minima
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id_pelicula=data["id_pelicula"],
            titulo=data["titulo"],
            duracion_minutos=data["duracion_minutos"],
            clasificacion=data["clasificacion"],
            edad_minima=data.get("edad_minima")
        )

    def __str__(self):
        return f"Pelicula[{self.id_pelicula}] '{self.titulo}' ({self.duracion_minutos} min | {self.clasificacion} | Min: {self.edad_minima} años)"
