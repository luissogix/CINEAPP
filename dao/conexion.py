import sqlite3
import os

class ConexionDB:
    """
    Gestor centralizado de conexión segura a la base de datos SQLite.
    Garantiza la creación automática de tablas para que el programa
    se ejecute de inmediato en cualquier entorno nuevo.
    """
    DB_NAME = "cineapp.db"
    
    @classmethod
    def get_db_path(cls) -> str:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, cls.DB_NAME)

    @classmethod
    def obtener_conexion(cls) -> sqlite3.Connection:
        """
        Retorna una conexión a la base de datos con soporte para claves foráneas.
        """
        conn = sqlite3.connect(cls.get_db_path())
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def inicializar_tablas(cls) -> None:
        """
        Crea las tablas requeridas por el negocio si no existen.
        """
        conn = cls.obtener_conexion()
        try:
            with conn:
                # 1. Tabla Peliculas (CRUD principal)
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS peliculas (
                        id_pelicula TEXT PRIMARY KEY,
                        titulo TEXT NOT NULL,
                        duracion_minutos INTEGER NOT NULL,
                        clasificacion TEXT NOT NULL,
                        edad_minima INTEGER NOT NULL
                    );
                """)

                # 2. Tabla Clientes
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS clientes (
                        rut TEXT PRIMARY KEY,
                        nombre TEXT NOT NULL,
                        edad INTEGER NOT NULL
                    );
                """)

                # 3. Tabla Ventas (Cabecera de transacción unificada)
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS ventas (
                        id_venta TEXT PRIMARY KEY,
                        fecha TEXT NOT NULL,
                        rut_cliente TEXT NOT NULL,
                        nombre_cliente TEXT NOT NULL,
                        edad_cliente INTEGER NOT NULL,
                        total REAL NOT NULL,
                        FOREIGN KEY (rut_cliente) REFERENCES clientes(rut)
                    );
                """)

                # 4. Tabla Detalles de Venta (Líneas de detalle - Composición)
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS detalles_venta (
                        id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_venta TEXT NOT NULL,
                        tipo_item TEXT NOT NULL,
                        descripcion TEXT NOT NULL,
                        cantidad INTEGER NOT NULL,
                        precio_unitario REAL NOT NULL,
                        subtotal REAL NOT NULL,
                        FOREIGN KEY (id_venta) REFERENCES ventas(id_venta) ON DELETE CASCADE
                    );
                """)
        finally:
            conn.close()
