from typing import List, Optional, Dict, Any
from dao.conexion import ConexionDB
from dao.cliente_dao import ClienteDAO
from model.venta import Venta

class VentaDAO:
    """
    Data Access Object (DAO) para la transacción de Venta y sus Detalles.
    Asegura la atomicidad de la transacción (Composición Todo/Partes)
    y previene inyección SQL mediante consultas parametrizadas.
    """

    @classmethod
    def registrar_transaccion(cls, venta: Venta) -> bool:
        """
        Registra la venta unificada junto con todas sus líneas de detalle
        dentro de una única transacción atómica de SQLite.
        """
        # Asegurar cliente en BD primero
        ClienteDAO.guardar_o_actualizar(venta.cliente)

        sql_venta = """
            INSERT INTO ventas (id_venta, fecha, rut_cliente, nombre_cliente, edad_cliente, total)
            VALUES (?, ?, ?, ?, ?, ?);
        """

        sql_detalle = """
            INSERT INTO detalles_venta (id_venta, tipo_item, descripcion, cantidad, precio_unitario, subtotal)
            VALUES (?, ?, ?, ?, ?, ?);
        """

        conn = ConexionDB.obtener_conexion()
        try:
            with conn: # Inicia transacción atómica (BEGIN ... COMMIT/ROLLBACK)
                # 1. Insertar Cabecera de Venta
                conn.execute(sql_venta, (
                    venta.id_venta,
                    venta.fecha.isoformat(),
                    venta.cliente.rut,
                    venta.cliente.nombre,
                    venta.cliente.edad,
                    venta.total
                ))

                # 2. Insertar cada Línea de Detalle
                for det in venta.detalles:
                    tipo = type(det.item).__name__
                    desc = det.item.get_descripcion()
                    conn.execute(sql_detalle, (
                        venta.id_venta,
                        tipo,
                        desc,
                        det.cantidad,
                        det.precio_unitario,
                        det.calcular_subtotal()
                    ))
            return True
        except Exception as e:
            print(f"[ERROR DAO] Error al registrar la venta {venta.id_venta}: {e}")
            return False
        finally:
            conn.close()

    @classmethod
    def obtener_historial_ventas(cls) -> List[Dict[str, Any]]:
        """
        Retorna la lista de ventas registradas con sus datos principales.
        """
        sql = "SELECT id_venta, fecha, rut_cliente, nombre_cliente, edad_cliente, total FROM ventas ORDER BY fecha DESC;"
        conn = ConexionDB.obtener_conexion()
        ventas = []
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            for row in cursor.fetchall():
                ventas.append(dict(row))
        finally:
            conn.close()
        return ventas

    @classmethod
    def obtener_venta_con_detalles(cls, id_venta: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene una venta completa con su desglose de líneas de detalle.
        Consulta parametrizada.
        """
        sql_v = "SELECT id_venta, fecha, rut_cliente, nombre_cliente, edad_cliente, total FROM ventas WHERE id_venta = ?;"
        sql_d = "SELECT id_detalle, tipo_item, descripcion, cantidad, precio_unitario, subtotal FROM detalles_venta WHERE id_venta = ?;"

        conn = ConexionDB.obtener_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(sql_v, (id_venta,))
            v_row = cursor.fetchone()
            if not v_row:
                return None

            venta_dict = dict(v_row)
            cursor.execute(sql_d, (id_venta,))
            detalles = [dict(d_row) for d_row in cursor.fetchall()]
            venta_dict["detalles"] = detalles
            return venta_dict
        finally:
            conn.close()
