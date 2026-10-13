class Cliente:
    """
    Representa a un cliente del cine.
    Aplica encapsulamiento defensivo en sus atributos privados (_rut, _nombre, _edad)
    con propiedades y validaciones matemáticas estrictas (RUT con Módulo 11 y Rango de Edad).
    """

    def __init__(self, rut, nombre, edad):
        self.rut = rut        # pasa por @rut.setter (validación Módulo 11)
        self.nombre = nombre  # pasa por @nombre.setter
        self.edad = edad      # pasa por @edad.setter

    @staticmethod
    def validar_rut(rut_str: str) -> bool:
        """
        Valida un RUT chileno usando el algoritmo Módulo 11.
        Acepta formatos con puntos y guion (ej: 12.345.678-5) o limpios (123456785).
        """
        if not rut_str or not isinstance(rut_str, str):
            return False
        
        limpio = rut_str.strip().replace(".", "").replace("-", "").upper()
        if limpio == "INVITADO":
            return True
        if len(limpio) < 2:
            return False

        cuerpo = limpio[:-1]
        dv = limpio[-1]

        if not cuerpo.isdigit():
            return False

        suma = 0
        multiplicador = 2
        for digito in reversed(cuerpo):
            suma += int(digito) * multiplicador
            multiplicador = 2 if multiplicador == 7 else multiplicador + 1

        resto = suma % 11
        dv_esperado = 11 - resto
        if dv_esperado == 11:
            dv_calc = "0"
        elif dv_esperado == 10:
            dv_calc = "K"
        else:
            dv_calc = str(dv_esperado)

        return dv == dv_calc

    @property
    def rut(self):
        return self._rut

    @rut.setter
    def rut(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("El RUT del cliente no puede estar vacío.")
        valor_str = str(valor).strip()
        if valor_str.upper() != "INVITADO" and not self.validar_rut(valor_str):
            raise ValueError(f"RUT inválido: '{valor_str}'. El dígito verificador no coincide con el cuerpo del RUT.")
        self._rut = valor_str

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

    def __str__(self):
        return f"Cliente(RUT={self.rut}, Nombre='{self.nombre}', Edad={self.edad})"
