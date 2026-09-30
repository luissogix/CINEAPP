class Sala:
    """
    Representa una sala del cine clasificada por formato de función (2D, 3D, VIP).
    """
    def __init__(self, numero_sala: int, formato: str = "2D", capacidad: int = 30):
        self.numero_sala = numero_sala
        self.formato = formato.upper().strip()  # "2D", "3D", "VIP"
        self.capacidad = capacidad
        # Asientos etiquetados A1..A6, B1..B6, C1..C6, D1..D6, E1..E6 (5 filas x 6 columnas = 30)
        self.filas = ['A', 'B', 'C', 'D', 'E']
        self.asientos_por_fila = 6
        # Diccionario para controlar disponibilidad: {"A1": True, "A2": False (ocupado)}
        self.asientos = {}
        self._inicializar_asientos()

    def _inicializar_asientos(self):
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
            self.asientos[codigo_asiento] = False # Marcar ocupado
            return True
        return False

    def obtener_asientos_disponibles(self):
        return [cod for cod, disponible in self.asientos.items() if disponible]

    def mostrar_mapa_asientos(self):
        print(f"\n   --- PANTALLA SALA {self.numero_sala} ({self.formato}) ---")
        for fila in self.filas:
            linea = f"{fila} | "
            for num in range(1, self.asientos_por_fila + 1):
                cod = f"{fila}{num}"
                if self.asientos[cod]:
                    linea += f"[{cod}] "
                else:
                    linea += f"[XX] " # Ocupado
            print(linea)
        print("  " + "-" * 35)
        print("  Leyenda: [A1] Disponible | [XX] Ocupado\n")
