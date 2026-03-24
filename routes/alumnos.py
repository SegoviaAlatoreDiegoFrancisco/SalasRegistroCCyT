from flask import Blueprint, render_template,request
import pyodbc
from config.db import get_db_connection


alumnos_bp = Blueprint("alumnos",__name__,url_prefix="/alumnos")

@alumnos_bp.route("/", methods=["GET"])
def alumnos_listar():
    """Lista todos los alumnos"""
    conn=get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "[SP_ALUMNOS_LISTAR_ACTIVOS]"
    )
    filas_activas = cursor.fetchall()
    alumnos_activos =[{"matricula":r.matricula,"nombre":r.nombre} for r in filas_activas]
    cursor.execute(
        "[SP_ALUMNOS_LISTAR_INACTIVOS]"
    )
    filas_inactivas = cursor.fetchall()
    alumnos_inactivos =[{"matricula":r.matricula,"nombre":r.nombre} for r in filas_inactivas]
    conn.close()
    return render_template("alumnos/alumnos.html",alumnos_activos=alumnos_activos, alumnos_inactivos=alumnos_inactivos,message=None,alumno_editar=None)


@alumnos_bp.route("/agregar", methods=["POST"])
def alumnos_agregar():

    """Agrega un nuevo alumno"""
    nombre = request.form.get("nombre")
    matricula=request.form.get("matricula")

    if not nombre or not matricula:
        return render_template("alumnos/alumnos.html",alumnos=[],message="Entradas invalidas- Verifique los campos.")
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
        cursor.execute("[SP_ALUMNOS_LISTAR_ACTIVOS]")
        filas_activas = cursor.fetchall()
        alumnos_activos =[{"matricula":r.matricula,"nombre":r.nombre} for r in filas_activas]
        cursor.execute("[SP_ALUMNOS_LISTAR_INACTIVOS]")
        filas_inactivas = cursor.fetchall()
        alumnos_inactivos =[{"matricula":r.matricula,"nombre":r.nombre} for r in filas_inactivas]
        conn.close()
    return render_template("alumnos/alumnos.html",alumnos_activos=alumnos_activos,alumnos_inactivos=alumnos_inactivos, message=None,alumno_editar=None)

@alumnos_bp.route("/alta/<matricula>", methods=["POST"])
def alumno_alta(matricula):
    """Agrega un True al campo 'activo' de alumno'"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("{CALL [SP_ALUMNO_ACTIVAR] (?)}",(matricula,))
        cursor.commit()
        message="Almuno cambió a activo en el sistema."
    except pyodbc.Error as e:
        message=f"Error al cambiar estado (activo) de alumno: {e}"
    finally:
        cursor.execute("[SP_ALUMNOS_LISTAR_ACTIVOS]")
        filas_activas = cursor.fetchall()
        alumnos_activos = [{"matricula": r.matricula, "nombre": r.nombre} for r in filas_activas]
        cursor.execute("[SP_ALUMNOS_LISTAR_INACTIVOS]")
        filas_inactivas =cursor.fetchall()
        alumnos_inactivos = [{"matricula": r.matricula, "nombre": r.nombre} for r in filas_inactivas]
        conn.close()
    return render_template("alumnos/alumnos.html",alumnos_activos=alumnos_activos,alumnos_inactivos=alumnos_inactivos, message=message,alumno_editar=None)


@alumnos_bp.route("/borrar/<matricula>", methods=["POST"])
def alumno_eliminar(matricula):
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
        cursor.execute("[SP_ALUMNOS_LISTAR_ACTIVOS]")
        filas_activas = cursor.fetchall()
        alumnos_activos = [{"matricula": r.matricula, "nombre": r.nombre} for r in filas_activas]
        cursor.execute("[SP_ALUMNOS_LISTAR_INACTIVOS]")
        filas_inactivas =cursor.fetchall()
        alumnos_inactivos = [{"matricula": r.matricula, "nombre": r.nombre} for r in filas_inactivas]
        conn.close()
    return render_template("alumnos/alumnos.html",alumnos_activos=alumnos_activos,alumnos_inactivos=alumnos_inactivos, message=message,alumno_editar=None)

'''
El bloque para EDITAR rellena el formulario mientras que el Bloque MODIFICAR efectua la accion en la BD
EDITAR -> CONSULTA  y rellena el formulario con los datos a editar + vuelve a rellenar la tabla de ACTIVOS
MODIFICAR -> ACTUALIZACIÓN Realiza la accion en la BD
'''
@alumnos_bp.route("/editar/<matricula>", methods=["GET"])
def editar_alumno(matricula):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("{CALL SP_ALUMNO_CONSULTAR (?)}", (matricula,))
    row = cursor.fetchone()
    cursor.execute("[SP_ALUMNOS_LISTAR_ACTIVOS]")
    filas_activas = cursor.fetchall()
    alumnos_activos = [{"matricula": r.matricula, "nombre": r.nombre} for r in filas_activas]
    cursor.execute("[SP_ALUMNOS_LISTAR_INACTIVOS]")
    filas_inactivas = cursor.fetchall()
    alumnos_inactivos = [{"matricula": r.matricula, "nombre": r.nombre} for r in filas_inactivas]
    conn.close()

    if row:
        alumno = {"matricula": row.matricula, "nombre": row.nombre, "activo": row.activo}
        return render_template("alumnos/alumnos.html", alumnos_activos=alumnos_activos,alumnos_inactivos=alumnos_inactivos, alumno_editar=alumno, message=None)
    else:
        return render_template("alumnos/alumnos.html", alumnos_activos=alumnos_activos,alumnos_inactivos=alumnos_inactivos, alumno_editar=None, message="Alumno no encontrado")

@alumnos_bp.route("/modificar/<matricula>",methods=["POST"])
def modificar_alumno(matricula):
    """Modifica el alumno con nuevos datos"""
    nombre = request.form.get("nombre")
    activo = request.form.get("activo")
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "{CALL SP_ALUMNO_MODIFICAR (?,?,?)}",(matricula,nombre,activo)
        )
        conn.commit()
        message="Usuario modificado con exito"
    except pyodbc.Error as e:
        message = f"Error al modificar usuario: {e}"
    finally:
        cursor.execute("SP_ALUMNOS_LISTAR_ACTIVOS")
        filas_activas = cursor.fetchall()
        alumnos_activos = [{"matricula": r.matricula, "nombre": r.nombre} for r in filas_activas]
        cursor.execute("SP_ALUMNOS_LISTAR_INACTIVOS")
        filas_inactivas = cursor.fetchall()
        alumnos_inactivos = [{"matricula": r.matricula, "nombre": r.nombre} for r in filas_inactivas]
        conn.close()
    return render_template("alumnos/alumnos.html",alumnos_activos=alumnos_activos,alumnos_inactivos=alumnos_inactivos, message=message,alumno_editar=None)
