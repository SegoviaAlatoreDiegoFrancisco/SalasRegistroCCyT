from flask import Blueprint, request, render_template
import pyodbc
from config.db import get_db_connection

materias_bp = Blueprint("materias",__name__,url_prefix="/materias")

@materias_bp.route("/", methods=["GET"])
def materias_listar():
    """Lista todas las materias"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "[SP_MATERIAS_LISTAR]"
    )
    filas = cursor.fetchall()
    materias = [{"id_materia":r.id_materia,"nombre":r.nombre,"division":r.division} for r in filas]
    conn.close()
    return render_template("materias/materias.html", materias=materias, message = None, materia_editar=None)

@materias_bp.route("/agregar", methods=["POST"])
def materias_agregar():
    """Agrega nuevas materias al sistema"""
    nombre = request.form.get("nombre")
    division = request.form.get("division")
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "{CALL [SP_MATERIA_INSERTAR] (?,?)}",(nombre,division)
        )
        conn.commit()
        message="Alumno agregado satisfactoriamente"
    except pyodbc.Error as e:
        message = f"Error al registrar alumno: {e}"
    finally:
        cursor.execute(
            "[SP_MATERIAS_LISTAR]"
        )
        filas = cursor.fetchall()
        materias = [{"id_materia":r.id_materia,"nombre":r.nombre,"division":r.division} for r in filas]
        conn.close()
        return render_template("materias/materias.html", materias=materias, message = None, materia_editar=None)

@materias_bp.route("/eliminar/<id_materia>", methods=["POST"])
def materia_eliminar(id_materia):
    """Elimina el registro de la materia en la BD """
    conn = get_db_connection()
    cursor= conn.cursor()
    try:
        cursor.execute("{CALL SP_MATERIA_ELIMINAR (?)}", id_materia)
        conn.commit()
        message ="Materia eliminada"
    except pyodbc.Error as e:
        message = f"Error al eliminar el registro de la base de datos"
    finally: 
        cursor.execute("[SP_MATERIAS_LISTAR]")
        filas = cursor.fetchall()
        materias = [{"id_materia":r.id_materia,"nombre":r.nombre,"division":r.division} for r in filas]
        conn.close()
        return render_template("materias/materias.html", materias=materias, message = None, materia_editar=None)
    