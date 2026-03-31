from flask import Blueprint, render_template,request
import pyodbc
from config.db import get_db_connection

salas_bp = Blueprint("salas",__name__,url_prefix="/salas")

@salas_bp.route("/", methods=["GET"])
def salas_listar():
    """Listar las salas"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("[SP_SALAS_LISTAR]")
    filas = cursor.fetchall()
    salas = [{"id_sala":r.id_sala,"nombre":r.nombre,"division":r.division,"num_computadoras":r.num_computadoras} for r in filas]
    conn.close()
    return render_template("salas/salas.html",salas = salas, message=None)