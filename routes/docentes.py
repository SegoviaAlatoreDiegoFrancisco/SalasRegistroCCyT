from flask import Blueprint, request, render_template
import pyodbc
from config.db import get_db_connection

docentes_bp = Blueprint("docentes",__name__,url_prefix="/docentes")
@docentes_bp.route("/", methods=["GET"])
def listar_docentes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT clave_docente, nombre, correo FROM Docentes WHERE activo=1")
    rows = cursor.fetchall()
    docentes = [{"clave": r.clave_docente, "nombre": r.nombre, "correo": r.correo} for r in rows]
    conn.close()
    return render_template("docentes/docentes.html", docentes=docentes, message=None)

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
        cursor.execute("SELECT clave_docente, nombre, correo FROM Docentes WHERE activo=1")
        rows = cursor.fetchall()
        docentes = [{"clave": r.clave_docente, "nombre": r.nombre, "correo": r.correo} for r in rows]
        conn.close()

    return render_template("docentes/docentes.html", docentes=docentes, message=message)