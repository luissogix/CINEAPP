from typing import Optional
from dao.conexion import ConexionDB
from model.cliente import Cliente

class ClienteDAO:
    """
    Data Access Object (DAO) para la entidad Cliente.
    Consultas parametrizadas que previenen inyección SQL.
    """

    @classmethod
    def guardar_o_actualizar(cls, cliente: Cliente) -> bool:
        sql = """
            INSERT INTO clientes (rut, nombre, edad)
            VALUES (?, ?, ?)
            ON CONFLICT(rut) DO UPDATE SET
                nombre = excluded.nombre,
                edad = excluded.edad;
        """
        conn = ConexionDB.obtener_conexion()
        try:
            with conn:
                conn.execute(sql, (cliente.rut, cliente.nombre, cliente.edad))
            return True
        except Exception as e:
            print(f"[ERROR DAO] No se pudo guardar cliente {cliente.rut}: {e}")
            return False
        finally:
            conn.close()

    @classmethod
    def obtener_por_rut(cls, rut: str) -> Optional[Cliente]:
        sql = "SELECT rut, nombre, edad FROM clientes WHERE rut = ?;"
        conn = ConexionDB.obtener_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (rut,))
            row = cursor.fetchone()
            if row:
                return Cliente(rut=row["rut"], nombre=row["nombre"], edad=row["edad"])
            return None
        finally:
            conn.close()
