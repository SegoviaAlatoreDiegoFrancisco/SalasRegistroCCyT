from flask import Blueprint, request, render_template
import pyodbc
from config.db import get_db_connection

docentes_bp = Blueprint("docentes",__name__,url_prefix="/docentes")
@docentes_bp.route("/", methods=["GET"])
def listar_docentes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SP_DOCENTES_ACTIVOS_LISTAR")
    filas_activas = cursor.fetchall()
    docentes_activos = [{"clave": r.clave_docente, "nombre": r.nombre, "correo": r.correo} for r in filas_activas]
    cursor.execute("SP_DOCENTES_INACTIVOS_LISTAR")
    filas_inactivas = cursor.fetchall()
    docentes_inactivos = [{"clave":r.clave_docente,"nombre":r.nombre,"correo":r.correo} for r in filas_inactivas]
    conn.close()
    return render_template("docentes/docentes.html", docentes_activos=docentes_activos,docentes_inactivos=docentes_inactivos, message=None)

@docentes_bp.route("/agregar", methods=["POST"])
def agregar_docente():
    nombre = request.form.get("nombre")
    correo = request.form.get("correo")
    clave = request.form.get("clave")

    if not nombre or not correo or not clave:
        return render_template("docentes/docentes.html", docentes=[], message="Entradas inválidas")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("{CALL SP_DOCENTE_INSERTAR (?,?,?)}", (clave, nombre, correo))
        conn.commit()
        message = "Docente registrado satisfactoriamente"
    except pyodbc.Error as e:
        message = f"Error al registrar docente: {e}"
    finally:
        cursor.execute("SP_DOCENTES_ACTIVOS_LISTAR")
        filas_activas = cursor.fetchall()
        docentes_activos = [{"clave": r.clave_docente, "nombre": r.nombre, "correo": r.correo} for r in filas_activas]
        cursor.execute("SP_DOCENTES_INACTIVOS_LISTAR")
        filas_inactivas = cursor.fetchall()
        docentes_inactivos = [{"clave":r.clave_docente,"nombre":r.nombre,"correo":r.correo} for r in filas_inactivas]
        conn.close()
        return render_template("docentes/docentes.html", docentes_activos=docentes_activos,docentes_inactivos=docentes_inactivos, message=message)

@docentes_bp.route("/alta/<clave_docente>", methods=["POST"])
def docente_alta(clave_docente):
    """Cambia el estado del docente a alta """
    conn= get_db_connection()
    cursor=conn.cursor()
    try:
        cursor.execute("{CALL SP_DOCENTE_ACTIVAR (?)}", (clave_docente))
        conn.commit()
        message = "Docente cambio de estado correctamente"
    except pyodbc.Error as e:
        message = f"Error al activar Docente: {e}"
    finally:
        cursor.execute("SP_DOCENTES_ACTIVOS_LISTAR")
        filas_activas = cursor.fetchall()
        docentes_activos = [{"clave": r.clave_docente, "nombre": r.nombre, "correo": r.correo} for r in filas_activas]
        cursor.execute("SP_DOCENTES_INACTIVOS_LISTAR")
        filas_inactivas = cursor.fetchall()
        docentes_inactivos = [{"clave":r.clave_docente,"nombre":r.nombre,"correo":r.correo} for r in filas_inactivas]
        conn.close()
        return render_template("docentes/docentes.html", docentes_activos=docentes_activos,docentes_inactivos=docentes_inactivos, message=message)


@docentes_bp.route("/borrar/<clave_docente>", methods=["POST"])
def docentes_borrar(clave_docente):
    """Elimina lógicamente el docente"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("{CALL [SP_DOCENTE_ELIMINAR_BAJA_LOGICA] (?)}",(clave_docente,))
        conn.commit()
        message = "Docente dado de baja correctamente."
    except pyodbc.Error as e:
        message = f"Error al dar de baja el docente: {e}"
    finally:
        cursor.execute("SP_DOCENTES_ACTIVOS_LISTAR")
        filas_activas = cursor.fetchall()
        docentes_activos = [{"clave": r.clave_docente, "nombre": r.nombre, "correo": r.correo} for r in filas_activas]
        cursor.execute("SP_DOCENTES_INACTIVOS_LISTAR")
        filas_inactivas = cursor.fetchall()
        docentes_inactivos = [{"clave":r.clave_docente,"nombre":r.nombre,"correo":r.correo} for r in filas_inactivas]
        conn.close()
        return render_template("docentes/docentes.html", docentes_activos=docentes_activos,docentes_inactivos=docentes_inactivos, message=message)

@docentes_bp.route("/editar/<clave_docente>", methods=["GET"])
def docente_editar(clave_docente):
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("{CALL [SP_DOCENTE_CONSULTAR] (?)}",(clave_docente,))
    row = cursor.fetchone()
    cursor.execute("SP_DOCENTES_ACTIVOS_LISTAR")
    filas_activas = cursor.fetchall()
    docentes_activos = [{"clave": r.clave_docente, "nombre": r.nombre, "correo": r.correo} for r in filas_activas]
    cursor.execute("SP_DOCENTES_INACTIVOS_LISTAR")
    filas_inactivas = cursor.fetchall()
    docentes_inactivos = [{"clave":r.clave_docente,"nombre":r.nombre,"correo":r.correo} for r in filas_inactivas]
    conn.close()
    if row:
        docente ={"clave_docente":row.clave_docente,"nombre":row.nombre,"correo":row.correo,"activo":row.activo}
        return render_template("docentes/docentes.html", docentes_activos=docentes_activos,docentes_inactivos=docentes_inactivos, docente_editar=docente,message=None)
    else:
        return render_template("docentes/docentes.html", docentes_activos=docentes_activos,docentes_inactivos=docentes_inactivos, docente_editar=None,message="Docente no encontrado")

@docentes_bp.route("/modificar/<clave_docente>", methods=["POST"])
def docente_modificar(clave_docente):
    """Modificar el docente enctontrado"""
    nombre = request.form.get("nombre")
    correo = request.form.get("correo")
    activo = request.form.get("activo")
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("{CALL [SP_DOCENTE_MODIFICAR] (?,?,?,?)}",(clave_docente,nombre,correo,activo))
        conn.commit()
        message="Docente modificado correctamente"
    except pyodbc.Error as e:
        message = f"Error al registra Docente: {e}"
    finally:
        cursor.execute("SP_DOCENTES_ACTIVOS_LISTAR")
        filas_activas = cursor.fetchall()
        docentes_activos = [{"clave": r.clave_docente, "nombre": r.nombre, "correo": r.correo} for r in filas_activas]
        cursor.execute("SP_DOCENTES_INACTIVOS_LISTAR")
        filas_inactivas = cursor.fetchall()
        docentes_inactivos = [{"clave":r.clave_docente,"nombre":r.nombre,"correo":r.correo} for r in filas_inactivas]
        conn.close()
        return render_template("/docentes/docentes.html",docentes_activos=docentes_activos,docentes_inactivos=docentes_inactivos,message=message)