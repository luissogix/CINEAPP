from model.empleado import Empleado


class EncargadoDulceria(Empleado):
    def __init__(self, id_empleado, nombre, rut, turno):
        super().__init__(id_empleado, nombre, rut)
        self._turno = turno

    @property
    def turno(self):
        return self._turno

    def get_rol(self):
        return "Encargado de Dulcería"

    def registrar_venta_dulceria(self, venta, producto, cantidad):
        """Descuenta stock y registra la línea en la venta."""
        producto.descontar_stock(cantidad)        # ValueError si no hay stock
        return venta.agregar_detalle(producto, cantidad)
