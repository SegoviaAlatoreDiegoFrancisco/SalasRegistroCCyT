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