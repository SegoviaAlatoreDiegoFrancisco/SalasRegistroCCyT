import logging
from typing import List, Optional
import pyodbc
from config.db import get_db_connection
from models.materia import Materia
logger = logging.getLogger(__name__)

class MateriaRepository:
    """Abstrae acceso a datos de Materias"""

    @staticmethod
    def listar_todas() -> List [Materia]:
        """Obtiene todas las maeterias"""
        conn = None
        try: 
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("[SP_MATERIAS_LISTAR]")
            filas = cursor.fetchall()

            materias = [ 
                Materia(
                    id_materia = r.id_materia,
                    nombre = r.nombre,
                    division = r.division
                )
                for r in filas
            ]
            return materias
        except pyodbc.Error as e:
            logger.error(f"Error al listar materias: {e}")
        finally:
            if conn:
                conn.close()
    @staticmethod
    def crear(nombre:str,division:str) -> Materia:
        """Inserta una nueva materia"""
        # Validación en capa de modelo
        materia = Materia(id_materia = None, nombre = nombre, division = division)

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "{Call [SP_MATERIA_INSERTAR] (?,?)}",
                (nombre, division)
            )
            conn.commit()
            logger.info(f"Materia creada: {nombre}")

            cursor.execute("SELECT @@IDENTITY as id")
            new_id = cursor.fetchone().id
            materia.id_materia = new_id
            return materia
        except pyodbc.Error as e:
            conn.rollback() if conn else None
            logger.error(f"Error al crear materia: {e}")
            #Manejo de errores
            #raise RepositoryError(f"No se pudo crear la materia: {e}")
            raise RepositoryError(f"No se pudo crear la materia: {e}")
        finally:
            if conn:
                conn.close()
    @staticmethod
    def obtener_por_id(id_materia: int) -> Optional[Materia]:
        """Obtener una materia por ID"""
        conn = None
        try:
            con = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("[SP_MATERIA_OBTENER] ?",(id_materia,))
            row = cursor.fetchone()

            if not row:
                return None
            return Materia(
                id_materia = row.id_materia,
                nombre=row.nombre,
                division = row.division
            )
        except pyodbc.Error as e:
            logger.error(f"Error al obtener materia {id_materia}: {e}")
            raise RepositoryError(f"Error al obtener materia: {e}")
        finally:
            if conn:
                conn.close()
    @staticmethod
    def actualizar(id_materia:int, nombre: str, division:str) -> Materia:
        """Actaulzia una materia existente"""
        materia = Materia(id_materia=id_materia, nombre = nombre, division=division)

        conn = None
        try:
            conn = get_db_connection
            cursor = conn.cursor()
            cursor.execute(
                "{CALL [SP_MATERIA_ACTUALIZAR] (?,?,?)}",
                (id_materia, nombre, division)
            )
            conn.commit()
            logger.info(f"Materia actualziada: {id_materia}" )
            return materia
        except pyodbc.Error as e:
            conn.rollback if conn else None
            logger.error(f"Error al actaulziar materia {id_materia}: {e}")
            raise RepositoryError(f"Error al actualziar materia: {e}")
        finally:
            if conn:
                conn.close()

    @staticmethod
    def eliminar(id_materia: int)-> bool:
        """Elimina una materia"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("{CALL [SP_MATERIA_ELIMINAR] (?)}", (id_materia,))
            conn.commit()
            logger.info(f"Materia eliminada: {id_materia}")
            return True
        except pyodbc.Error as e:
            conn.rollback() if conn else None
            logger.error(f"Error al eliminar materia {id_materia}: {e}")
            raise RepositoryError(f"Error al eliminar materia: {e}")
        finally: 
            if conn:
                conn.close()
class RepositoryError(Exception):
    """Excepcion customizada para errores de repositorio"""
    pass