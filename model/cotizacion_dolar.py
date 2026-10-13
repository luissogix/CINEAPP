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
    def obtener_cotizacion_del_dia(cls, timeout: int = 3):
        """
        Consulta la API de mindicador.cl para obtener el valor del dólar en tiempo real.
        Si no hay conexión a internet o el servicio no responde, aplica fallback sin caerse.
        """
        url = "https://mindicador.cl/api/dolar"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CineApp/1.0",
                "Accept": "application/json"
            }
        )
        
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as response:
                data = json.loads(response.read().decode("utf-8"))
                valor_hoy = float(data["serie"][0]["valor"])
                fecha_str = data["serie"][0].get("fecha", str(date.today()))[:10]
                print(f"[OK] Cotización del dólar obtenida en vivo desde {url}: ${valor_hoy:,.2f} CLP (Fecha: {fecha_str})")
                return cls(valor_hoy, fecha_actualizacion=fecha_str, origen="mindicador.cl (en vivo)")
        except Exception as e:
            print(f"[ADVERTENCIA] No fue posible conectar con {url} ({type(e).__name__}).")
            print(f"[CONTINGENCIA] Usando valor de respaldo referencial: ${cls.VALOR_RESPALDO:,.2f} CLP.")
            return cls(cls.VALOR_RESPALDO, fecha_actualizacion=date.today(), origen="Respaldo referencial (sin internet)")

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
