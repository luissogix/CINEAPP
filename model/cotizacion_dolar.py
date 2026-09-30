from datetime import date


class CotizacionDolar:
    """Indicador externo: valor del dólar en pesos chilenos."""

    def __init__(self, valor_dolar_del_dia, fecha_actualizacion=None):
        self.valor_dolar_del_dia = valor_dolar_del_dia
        self._fecha_actualizacion = fecha_actualizacion or date.today()

    @property
    def valor_dolar_del_dia(self):
        return self._valor_dolar_del_dia

    @valor_dolar_del_dia.setter
    def valor_dolar_del_dia(self, valor):
        if valor <= 0:
            raise ValueError("El valor del dólar debe ser mayor a 0.")
        self._valor_dolar_del_dia = valor

    @property
    def fecha_actualizacion(self):
        return self._fecha_actualizacion

    def get_valor_dolar(self):
        return self._valor_dolar_del_dia

    def actualizar_valor(self, nuevo_valor, fecha=None):
        self.valor_dolar_del_dia = nuevo_valor
        self._fecha_actualizacion = fecha or date.today()
