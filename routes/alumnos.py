from flask import Blueprint, render_template,request
import pyodbc
from config.db import get_db_connection


alumnos_bp = Blueprint("alumnos",__name__,url_prefix="/alumnos")

@alumnos_bp.route("/", methods=["GET"])
def listar_alumnos():
    """Lista todos los alumnos"""
    conn=get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "[SP_ALUMNOS_LISTAR]"
    )
    rows = cursor.fetchall()
    alumnos =[{"matricula":r.matricula,"nombre":r.nombre} for r in rows]
    conn.close()
    return render_template("alumnos.html",alumnos=alumnos,message=None)
@alumnos_bp.route("/agregar", methods=["POST"])
def agregar_alumnos():
    """Agrega un nuevo alumno"""
    nombre = request.form.get("nombre")
    matricula=request.form.get("matricula")

    if not nombre or not matricula:
        return render_template("alumnos.html",alumnos=[],message="Entradas invalidas- Verifique los campos.")
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "{CALL SP_ALUMNO_INSERTAR (?,?)}",(nombre,matricula)
        )
        conn.commit()
        message="Alumno resigtrado satisfactoriamente"
    except pyodbc.Error as e:
        message=f"Error al registrar el usuario: {e}"
    finally:
        cursor.execute("[SP_ALUMNOS_LISTAR]")
        rows = cursor.fetchall()
        alumnos =[{"matricula":r.matricula,"nombre":r.nombre} for r in rows]
        conn.close()
    return render_template("alumnos.html",alumnos=alumnos, message=None)
@alumnos_bp.route("/borrar/<matricula>", methods=["POST"])
def eliminar_alumno(matricula):
    """Elimina lógicamente un alumno"""
    conn = get_db_connection()
    cursor= conn.cursor()
    try:
        cursor.execute("{CALL SP_ALUMNO_ELIMINAR_BAJA_LOGICA (?)}", (matricula,))
        conn.commit()
        message="Alumno eliminado lógicamente"
    except pyodbc.Error as e:
        message =f"Error al eliminar alumno: {e}"
    finally:
        cursor.execute("SELECT matricula, nombre FROM Alumnos WHERE activo=1")
        rows = cursor.fetchall()
        alumnos = [{"matricula": r.matricula, "nombre": r.nombre} for r in rows]
        conn.close()
    return render_template("alumnos.html",alumnos=alumnos, message=message)
