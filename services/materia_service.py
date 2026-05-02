import logging
from typing import List, Dict
from repositories.materia_repository import MateriaRepository, RepositoryError
from models.materia import Materia

logger = logging.getLogger(__name__)

class MateriaService:
    """Lógica de negocio para Materias"""

    @staticmethod
    def obtener_todas_materias() -> List[Dict]:
        """Obtiene todas las materias formateadas para la vista"""
        try:
            materias = MateriaRepository.listar_todas()
            return [m.to_dict() for m in materias]
        except RepositoryError as e:
            logger.error(f"Error en el servivio: {e}")
            raise ServiceError(str(e))
    
    @staticmethod
    def crear_materia(nombre:str, division: str) -> tuple[bool, str, Dict]:
        """Crea una materia con validaciones"""
        try:
            #Validaciones básicas
            if not nombre or not nombre.strip():
                return False, "El nombre es requerido",{}
            if not division or not division.strip():
                return False, "La división es requerida",{}
            
            #El modelo validará mas profundamente 
            materia = MateriaRepository.crear(nombre.strip(), division.strip())
            return True, "Materia creada satisfactoriamente",materia.to_dict()
        except ValueError as e:
            return False, f"Error de validación: {str(e)}",{}
        except RepositoryError as e: 
            return False, f"Error al guardar: {str(e)}",{}
    
    @staticmethod
    def actualizar_materia(id_materia: int, nombre: str, division: str) -> tuple[bool, str, Dict]:
        """Actualiza una materia"""
        try:
            #Obtener materia existente
            materia_actaul = MateriaRepository.obtener_por_id(id_materia)
            if not materia_actaul:
                return False, "Materia no encontrada",{}
            
            #Actaulziar 
            materia = MateriaRepository.actaulzar(id_materia, nombre.strip(),division.strip())
            return True, "Materia actualziada satisfactoriamente", materia.to_dict()
        except ValueError as e:
            return False, f"Error de validación: {str(e)}",{}
        except RepositoryError as e:
            return False, f"Error al actaulziar: {str(e)}",{}
    @staticmethod
    def eliminar_materia(id_materia: int)-> tuple[bool,str]:
        """Elimina una materia"""
        try: 
            MateriaRepository.eliminar(id_materia)
            return True,"Materia eliminada satisfactoriamente"
        except RepositoryError as e:
            return False, f"Error al eliminar: {str(e)}"

class ServiceError(Exception):
    """Excepción customizada para errores de servicio"""
    pass