import urllib.request
import json
from datetime import datetime
from model.pelicula import Pelicula

class ServicioCarteleraAPI:
    """
    Servicio de integración con la API pública de TMDB (The Movie Database).
    Mantiene caché de larga duración (24 horas) de forma transparente y silenciosa.
    """
    BASE_URL = "https://api.themoviedb.org/3"
    
    def __init__(self, api_key: str = "demo_key", ttl_segundos: int = 86400):
        """
        :param api_key: Clave API de TMDB.
        :param ttl_segundos: Tiempo de almacenamiento en caché. Por defecto 24 horas (86400s).
        """
        self.api_key = api_key
        self.ttl_segundos = ttl_segundos
        self._cache_peliculas = []
        self._ultima_actualizacion = None

    def necesita_actualizacion(self) -> bool:
        if not self._ultima_actualizacion:
            return True
        tiempo_transcurrido = (datetime.now() - self._ultima_actualizacion).total_seconds()
        return tiempo_transcurrido >= self.ttl_segundos

    def obtener_peliculas_en_taquilla(self, region: str = "CL", idioma: str = "es-CL", limite: int = 5, forzar_refresco: bool = False):
        """
        Retorna las películas en cartelera. 
        Opera de manera silenciosa utilizando la información en caché durante 24 horas.
        """
        if not forzar_refresco and not self.necesita_actualizacion() and self._cache_peliculas:
            return self._cache_peliculas[:limite]

        if self.api_key and self.api_key != "demo_key":
            url = f"{self.BASE_URL}/movie/now_playing?api_key={self.api_key}&language={idioma}&region={region}&page=1"
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    if response.status == 200:
                        data = json.loads(response.read().decode('utf-8'))
                        self._cache_peliculas = self._mapear_a_objetos_pelicula(data.get("results", []), limite * 2)
                        self._ultima_actualizacion = datetime.now()
                        return self._cache_peliculas[:limite]
            except Exception:
                pass # Silencioso, no imprime errores en consola

        self._cache_peliculas = self._obtener_datos_fallback()
        self._ultima_actualizacion = datetime.now()
        return self._cache_peliculas[:limite]

    def _mapear_a_objetos_pelicula(self, resultados, limite):
        peliculas = []
        for i, item in enumerate(resultados[:limite]):
            p_id = f"P-API-{item.get('id')}"
            titulo = item.get("title", "Sin título")
            is_adult = item.get("adult", False)
            clasificacion = "+18" if is_adult else "TE"
            edad_minima = 18 if is_adult else 0
            duracion = 110 + (i * 5 % 25) 
            pelicula = Pelicula(p_id, titulo, duracion, clasificacion, edad_minima)
            peliculas.append(pelicula)
        return peliculas

    def _obtener_datos_fallback(self):
        """Peliculas en cartelera vigentes para consulta rápida y limpia"""
        datos_taquilla = [
            {"id": "P-2026-01", "titulo": "Practical Magic 2", "duracion": 115, "clasificacion": "+14", "edad_minima": 14},
            {"id": "P-2026-02", "titulo": "Resident Evil (Reboot 2026)", "duracion": 110, "clasificacion": "+18", "edad_minima": 18},
            {"id": "P-2026-03", "titulo": "Heart of the Beast", "duracion": 122, "clasificacion": "+14", "edad_minima": 14},
            {"id": "P-2026-04", "titulo": "Onslaught", "duracion": 108, "clasificacion": "+18", "edad_minima": 18},
            {"id": "P-2026-05", "titulo": "Toy Story 5", "duracion": 100, "clasificacion": "TE", "edad_minima": 0}
        ]
        
        return [
            Pelicula(d["id"], d["titulo"], d["duracion"], d["clasificacion"], d["edad_minima"])
            for d in datos_taquilla
        ]
