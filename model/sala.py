class Sala:
    """
    Representa una sala del cine clasificada por formato de función (2D, 3D, VIP).
    Las salas VIP cuentan con aforo exclusivo reducido (asientos limitados) para
    garantizar confort y permitir pruebas rápidas de llenado de aforo (Regla 2).
    """
    def __init__(self, numero_sala: int, formato: str = "2D", capacidad: int = None):
        self.numero_sala = numero_sala
        self.formato = formato.upper().strip()  # "2D", "3D", "VIP"
        
        if capacidad is not None:
            self.capacidad = capacidad
        elif self.formato == "VIP":
            self.capacidad = 4  # Aforo exclusivo VIP (asientos limitados: V1, V2, V3, V4)
        else:
            self.capacidad = 30  # Salas estándar 2D / 3D (5 filas x 6 columnas)

        # Configuración de mapa de asientos según capacidad
        if self.formato == "VIP":
            self.filas = ['V']
            self.asientos_por_fila = self.capacidad
        else:
            self.filas = ['A', 'B', 'C', 'D', 'E']
            self.asientos_por_fila = max(1, self.capacidad // len(self.filas))

        self.asientos = {}
        self._inicializar_asientos()

    def _inicializar_asientos(self):
        self.asientos.clear()
        for fila in self.filas:
            for num in range(1, self.asientos_por_fila + 1):
                codigo = f"{fila}{num}"
                self.asientos[codigo] = True  # True = Disponible

    def esta_disponible(self, codigo_asiento: str) -> bool:
        codigo_asiento = codigo_asiento.upper().strip()
        return self.asientos.get(codigo_asiento, False)

    def ocupar_asiento(self, codigo_asiento: str) -> bool:
        codigo_asiento = codigo_asiento.upper().strip()
        if self.esta_disponible(codigo_asiento):
            self.asientos[codigo_asiento] = False  # Marcar ocupado
            return True
        return False

    def obtener_asientos_disponibles(self):
        return [cod for cod, disponible in self.asientos.items() if disponible]

    def mostrar_mapa_asientos(self):
        tipo_label = "SALA VIP EXCLUSIVA (Asientos Limitados)" if self.formato == "VIP" else f"SALA {self.numero_sala} ({self.formato})"
        print(f"\n   --- PANTALLA: {tipo_label} ---")
        for fila in self.filas:
            linea = f"{fila} | "
            for num in range(1, self.asientos_por_fila + 1):
                cod = f"{fila}{num}"
                if self.asientos.get(cod, False):
                    linea += f"[{cod}] "
                else:
                    linea += f"[XX] "  # Ocupado
            print(linea)
        print("  " + "-" * 35)
        print("  Leyenda: [V1] Disponible | [XX] Ocupado\n")
