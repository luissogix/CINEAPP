from typing import List, Optional
from dao.conexion import ConexionDB
from model.pelicula import Pelicula

class PeliculaDAO:
    """
    Data Access Object (DAO) para la entidad Pelicula.
    Implementa operaciones CRUD completas utilizando consultas parametrizadas
    para garantizar la protección absoluta contra inyección SQL.
    """

    @classmethod
    def insertar(cls, pelicula: Pelicula) -> bool:
        """
        Inserta una nueva película en la base de datos (CREATE).
        Consulta parametrizada con marcadores '?'.
        """
        sql = """
            INSERT INTO peliculas (id_pelicula, titulo, duracion_minutos, clasificacion, edad_minima)
            VALUES (?, ?, ?, ?, ?);
        """
        conn = ConexionDB.obtener_conexion()
        try:
            with conn:
                conn.execute(sql, (
                    pelicula.id_pelicula,
                    pelicula.titulo,
                    pelicula.duracion_minutos,
                    pelicula.clasificacion,
                    pelicula.edad_minima
                ))
            return True
        except Exception as e:
            print(f"[ERROR DAO] No se pudo insertar la película {pelicula.titulo}: {e}")
            return False
        finally:
            conn.close()

    @classmethod
    def obtener_todas(cls) -> List[Pelicula]:
        """
        Retorna todas las películas registradas en la base de datos (READ All).
        Convierte cada registro en un objeto Pelicula del modelo POO.
        """
        sql = "SELECT id_pelicula, titulo, duracion_minutos, clasificacion, edad_minima FROM peliculas ORDER BY id_pelicula ASC;"
        conn = ConexionDB.obtener_conexion()
        peliculas: List[Pelicula] = []
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            for row in cursor.fetchall():
                p = Pelicula(
                    id_pelicula=row["id_pelicula"],
                    titulo=row["titulo"],
                    duracion_minutos=row["duracion_minutos"],
                    clasificacion=row["clasificacion"],
                    edad_minima=row["edad_minima"]
                )
                peliculas.append(p)
        finally:
            conn.close()
        return peliculas

    @classmethod
    def obtener_por_id(cls, id_pelicula: str) -> Optional[Pelicula]:
        """
        Busca una película por su clave primaria (READ by ID).
        Consulta parametrizada con marcador '?'.
        """
        sql = "SELECT id_pelicula, titulo, duracion_minutos, clasificacion, edad_minima FROM peliculas WHERE id_pelicula = ?;"
        conn = ConexionDB.obtener_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (id_pelicula,))
            row = cursor.fetchone()
            if row:
                return Pelicula(
                    id_pelicula=row["id_pelicula"],
                    titulo=row["titulo"],
                    duracion_minutos=row["duracion_minutos"],
                    clasificacion=row["clasificacion"],
                    edad_minima=row["edad_minima"]
                )
            return None
        finally:
            conn.close()

    @classmethod
    def actualizar(cls, pelicula: Pelicula) -> bool:
        """
        Actualiza los datos de una película existente (UPDATE).
        Consulta parametrizada con marcadores '?'.
        """
        sql = """
            UPDATE peliculas
            SET titulo = ?, duracion_minutos = ?, clasificacion = ?, edad_minima = ?
            WHERE id_pelicula = ?;
        """
        conn = ConexionDB.obtener_conexion()
        try:
            with conn:
                cursor = conn.execute(sql, (
                    pelicula.titulo,
                    pelicula.duracion_minutos,
                    pelicula.clasificacion,
                    pelicula.edad_minima,
                    pelicula.id_pelicula
                ))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"[ERROR DAO] No se pudo actualizar la película {pelicula.id_pelicula}: {e}")
            return False
        finally:
            conn.close()

    @classmethod
    def eliminar(cls, id_pelicula: str) -> bool:
        """
        Elimina una película de la base de datos (DELETE).
        Consulta parametrizada con marcador '?'.
        """
        sql = "DELETE FROM peliculas WHERE id_pelicula = ?;"
        conn = ConexionDB.obtener_conexion()
        try:
            with conn:
                cursor = conn.execute(sql, (id_pelicula,))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"[ERROR DAO] No se pudo eliminar la película {id_pelicula}: {e}")
            return False
        finally:
            conn.close()

    @classmethod
    def inicializar_catalogo_defecto(cls, peliculas_defecto: List[Pelicula]) -> None:
        """
        Verifica si la tabla está vacía y puebla el catálogo inicial
        para garantizar ejecución inmediata en un entorno nuevo.
        """
        if len(cls.obtener_todas()) == 0:
            for p in peliculas_defecto:
                cls.insertar(p)
