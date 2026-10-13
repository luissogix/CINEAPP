import json
import os
from datetime import datetime
from model.pelicula import Pelicula


ARCHIVO_DATOS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "datos_cine.json")


class GestorPersistencia:
    """
    Gestiona la persistencia de datos (Películas, Funciones y Ventas)
    en almacenamiento local JSON para garantizar persistencia entre ejecuciones (P05).
    """

    @staticmethod
    def _obtener_datos_iniciales():
        return {
            "peliculas": [
                {"id_pelicula": "P-001", "titulo": "Transformers One", "duracion_minutos": 104, "clasificacion": "TE", "edad_minima": 0},
                {"id_pelicula": "P-002", "titulo": "Alien: Romulus", "duracion_minutos": 119, "clasificacion": "+14", "edad_minima": 14},
                {"id_pelicula": "P-003", "titulo": "Deadpool & Wolverine", "duracion_minutos": 128, "clasificacion": "+18", "edad_minima": 18},
                {"id_pelicula": "P-004", "titulo": "Intensamente 2", "duracion_minutos": 96, "clasificacion": "TE", "edad_minima": 0},
                {"id_pelicula": "P-005", "titulo": "Sonrie 2", "duracion_minutos": 127, "clasificacion": "+18", "edad_minima": 18}
            ],
            "ventas": []
        }

    @classmethod
    def cargar_datos(cls):
        if not os.path.exists(ARCHIVO_DATOS):
            datos_base = cls._obtener_datos_iniciales()
            cls.guardar_datos(datos_base)
            return datos_base
        try:
            with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            datos_base = cls._obtener_datos_iniciales()
            cls.guardar_datos(datos_base)
            return datos_base

    @classmethod
    def guardar_datos(cls, datos):
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    @classmethod
    def cargar_peliculas(cls):
        datos = cls.cargar_datos()
        peliculas = []
        for p_data in datos.get("peliculas", []):
            peliculas.append(Pelicula.from_dict(p_data))
        return peliculas

    @classmethod
    def guardar_peliculas(cls, lista_peliculas):
        datos = cls.cargar_datos()
        datos["peliculas"] = [p.to_dict() for p in lista_peliculas]
        cls.guardar_datos(datos)

    @classmethod
    def guardar_venta_registro(cls, venta_dict):
        datos = cls.cargar_datos()
        if "ventas" not in datos:
            datos["ventas"] = []
        datos["ventas"].append(venta_dict)
        cls.guardar_datos(datos)

    @classmethod
    def cargar_ventas(cls):
        datos = cls.cargar_datos()
        return datos.get("ventas", [])
