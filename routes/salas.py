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

@salas_bp.route("/agregar", methods=["POST"])
def salas_agregar():
    """Agrega una nueva sala"""
    nombre = request.form.get("nombre")
    division= request.form.get("division")
    num_computadoras = request.form.get("num_computadoras")

    if not nombre or not division:
        return render_template("salas/salas.html", salas = [], message = "Entradas invalidas")
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "{CALL SP_SALAS_INSERTAR (?,?,?)}",(nombre,division,num_computadoras,)
        )
        conn.commit()
        message = "Sala registrada con exito."
    except pyodbc.Error as e:
        message = f"Error la registrar la sala: {e}"
    finally:
        cursor.execute("[SP_SALAS_LISTAR]")
        filas = cursor.fetchall()
        salas=[{"id_sala":r.id_sala,"nombre":r.nombre,"division":r.division,"num_computadoras":r.num_computadoras} for r in filas]
        conn.close()
        return render_template("salas/salas.html", salas = salas , message = message)
@salas_bp.route("/editar/<id_sala>", methods=["GET"])
def sala_editar(id_sala):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "{CALL  [SP_SALA_CONSULTA] (?)}", (id_sala,)
    )
    row = cursor.fetchone()
    cursor.execute("[SP_SALAS_LISTAR]")
    filas = cursor.fetchall()
    salas = [{"id_sala":r.id_sala,"nombre":r.nombre,"division":r.division,"num_computadoras":r.num_computadoras} for r in filas]
    conn.close()
    if row:
        sala_editar = {"id_sala":row.id_sala,"nombre":row.nombre,"division":row.division,"num_computadoras":row.num_computadoras}
        return render_template("salas/salas.html", sala_editar=sala_editar, salas=salas, message=None)
    else:
        return render_template("salas/salas.html", sala_editar=None, salas=salas, message="Sala no encontrada")

@salas_bp.route("/modificar/<id_sala>", methods=["POST"])
def sala_modificar(id_sala):
    nombre = request.form.get("nombre")
    division = request.form.get("division")
    num_computadoras = request.form.get("num_computadoras")

    if not nombre or not division or not num_computadoras:
        message = "Entradas invalidas. Completa todos los campos."
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "{CALL [SP_SALA_MODIFICAR] (?,?,?,?)}", (id_sala, nombre, division, num_computadoras)
            )
            conn.commit()
            message = "Sala modificada con éxito."
        except pyodbc.Error as e:
            message = f"Error al modificar la sala: {e}"
        finally:
            cursor.execute("[SP_SALAS_LISTAR]")
            filas = cursor.fetchall()
            salas = [{"id_sala":r.id_sala,"nombre":r.nombre,"division":r.division,"num_computadoras":r.num_computadoras} for r in filas]
            conn.close()
    return render_template("salas/salas.html", salas=salas, message=message, sala_editar=None)

