from datetime import date
import json
import urllib.request
import ssl


class CotizacionDolar:
    """
    Indicador externo: valor del dólar en pesos chilenos (CLP).
    Permite sincronización con https://mindicador.cl/api/dolar
    y cuenta con mecanismo de contingencia defensivo sin internet.
    """

    VALOR_RESPALDO = 950.0

    def __init__(self, valor_dolar_del_dia, fecha_actualizacion=None, origen="Local"):
        self.valor_dolar_del_dia = valor_dolar_del_dia
        self._fecha_actualizacion = fecha_actualizacion or date.today()
        self._origen = origen

    @classmethod
    def obtener_cotizacion_del_dia(cls, timeout: int = 5):
        """
        Consulta la API pública de mindicador.cl mediante la librería 'requests'
        para obtener el valor oficial del dólar en tiempo real.
        Define un tiempo límite (timeout) y maneja caídas, demoras o respuestas
        inesperadas aplicando un valor de respaldo para garantizar continuidad (Criterios 3.1.1 y 3.1.3).
        """
        url = "https://mindicador.cl/api/dolar"
        
        try:
            import requests
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CineApp/1.0",
                "Accept": "application/json"
            }
            response = requests.get(url, headers=headers, timeout=timeout)
            
            if response.status_code == 200:
                data = response.json()
                serie = data.get("serie", [])
                if serie:
                    valor_hoy = float(serie[0]["valor"])
                    fecha_str = str(serie[0].get("fecha", date.today()))[:10]
                    print(f"[OK API] Cotización del dólar obtenida en vivo vía requests ({url}): ${valor_hoy:,.2f} CLP (Fecha: {fecha_str})")
                    return cls(valor_hoy, fecha_actualizacion=fecha_str, origen="mindicador.cl (en vivo)")
                else:
                    print(f"[ADVERTENCIA API] Respuesta inesperada: no se encontró la serie de datos en {url}.")
            else:
                print(f"[ADVERTENCIA API] Respuesta HTTP con código de estado inesperado: {response.status_code}.")

        except Exception as e:
            # Captura de Timeout, ConnectionError o fallas de red
            error_tipo = type(e).__name__
            if "Timeout" in error_tipo:
                print(f"[ADVERTENCIA API] Tiempo máximo de espera agotado ({timeout}s) al consultar {url}.")
            elif "Connection" in error_tipo:
                print(f"[ADVERTENCIA API] Sin conexión a internet o endpoint inalcanzable ({url}).")
            else:
                print(f"[ADVERTENCIA API] Error al consultar servicio externo ({error_tipo}): {e}")

        # Mecanismo de contingencia defensivo: continuidad y estabilidad del sistema
        print(f"[CONTINGENCIA API] Aplicando valor de respaldo referencial: ${cls.VALOR_RESPALDO:,.2f} CLP.")
        return cls(cls.VALOR_RESPALDO, fecha_actualizacion=date.today(), origen="Respaldo referencial (modo contingencia)")

    @property
    def valor_dolar_del_dia(self):
        return self._valor_dolar_del_dia

    @valor_dolar_del_dia.setter
    def valor_dolar_del_dia(self, valor):
        val_float = float(valor)
        if val_float <= 0:
            raise ValueError("El valor del dólar debe ser mayor a 0.")
        self._valor_dolar_del_dia = val_float

    @property
    def fecha_actualizacion(self):
        return self._fecha_actualizacion

    @property
    def origen(self):
        return self._origen

    def get_valor_dolar(self):
        return self._valor_dolar_del_dia

    def actualizar_valor(self, nuevo_valor, fecha=None):
        self.valor_dolar_del_dia = nuevo_valor
        self._fecha_actualizacion = fecha or date.today()
        self._origen = "Manual"

    def __str__(self):
        return f"CotizacionDolar(${self._valor_dolar_del_dia:,.2f} CLP | Origen: {self._origen} | Fecha: {self._fecha_actualizacion})"
