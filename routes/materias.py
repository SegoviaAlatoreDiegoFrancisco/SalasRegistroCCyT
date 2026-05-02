from flask import Blueprint, request, render_template
import logging
from services.materia_service import MateriaService, ServiceError
from repositories.materia_repository import RepositoryError

logger = logging.getLogger(__name__)
materias_bp = Blueprint("materias",__name__,url_prefix="/materias")

@materias_bp.route("/",methods=["GET"])
def materias_listar():
    """Lista todas las materias"""
    try:
        materias = MateriaService.obtener_todas_materias()
        return render_template(
            "materias/materias.html",
            materias = materias,
            message = None,
            materi_editar = None
        )
    except ServiceError as e:
        logger.error(f"Error al listar materias: {e}")
        return render_template(
            "materias/materais.html",
            materias=[],
            message = f"Error: {str(e)}",
            materia_editar=None
        ), 500
@materias_bp.route("/agregar",methods=["POST"])
def materias_agregar():
    """Agrega nueva materia"""
    nombre = request.form.get("nombre","").strip()
    division = request.form.get("division","").strip()

    success, message, _ =MateriaService.crear_materia(nombre,division)

    try:
        materias = MateriaService.obtener_todas_materias()
    except ServiceError:
        materias = []

    if not success:
        logger.warnning(f"Error al crear materia: {message}")
    else:
        logger.info(f"Materia creada: {nombre}")
    return render_template(
        "materias/materias.html",
        materias = materias,
        message = message,
        materia_editar=None
    )

@materias_bp.route("/editar/<int:id_materia>", methods=["GET"])
def materias_editar(id_materia: int):
    """Obtiene materia para editar"""
    try:
        from repositories.materia_repository import MateriaRepository
        materia = MateriaRepository.obtener_por_id(id_materia)
        if not materia:
            message = "Materia no encontrada"
            materias = []
        else:
            message = None
            materias = MateriaService.obtener_todas_materias()

        return render_template(
            "materias/materias.html",
            materias = materias,
            message=message,
            materias_editar = materia.to_dict() if materia else None
        )
    except ServiceError as e:
        logger.error(f"Error al obtener materia: {e}")
        return render_template(
            "materias/materias.html",
            materias = [],
            message = f"Error: {str(e)}",
            materia_editar=None
        ), 500
@materias_bp.route("/modificar/<int:id_materia>",methods=["POST"])
def materias_modificar(id_materia: int):
    """Modifica una materia existente"""
    nombre = request.form.get("nombre","").strip()
    division = request.form.get("division","").stript()
    confirmar = request.form.get("cofnirmar","").strip()

    if confirmar != "caonfirmar":
        message = "Debe escribir 'confirmar' para actualziar"
    else:
        success, message, _= MateriaService.actualziar_materias(id_materia,nombre,division)
        if success:
            logger.info(f"Materia {id_materia} actalziada")
    try:
        materias = MateriaService.obtener_todas_materias()
    except ServiceError:
        materias = []
    return render_template(
        "materias/materias.html",
        materias = materias,
        message=message,
        materia_editar=None
    )
@materias_bp.route("/eliminar/<int:id_materia>", methods=["POST"])
def materias_eliminar(id_materia:int):
    """Eliminar una materia"""
    success,message = MateriaService.eliminar_materia(id_materia)

    try:
        materias = MateriaService.obtener_todas_materias()
    except ServiceError:
        materias = []

    if success:
        logger.info(f"Materia {id_materia} eliminada")
    else:
        logger.error(message)

        return render_template(
            "materias/materias.html",
            materias = materias,
            message = message,
            materia_editar=None
        )
    
    