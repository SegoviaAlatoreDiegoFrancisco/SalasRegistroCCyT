import pyodbc
from config.db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

def usuario_crear(nombre,email,password,rol="user"):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        password_hash = generate_password_hash(password)
        cursor.execute("{ CALL [SP_USUARIO_INSERTAR] (?,?,?,?)}",(nombre,email,password_hash,rol,))
        conn.commit()
        message = "Usuario creado satisfactoriamente"
        return True, message 
    except pyodbc.Error as e:
        return False, f"Error al crear usuario:{e}"
    finally:
        conn.close()
def usuario_validar(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("{CALL SP_USUARIO_AUTENTICAR (?)}", (email,))
        row = cursor.fetchone()
    except pyodbc.Error as e:
        conn.close()
        return None, f"Error en la consulta: {e}"
    conn.close()

    if not row:
        return None, "Usuario no encontrado"

    stored_hash = row.password
    if not stored_hash:
        return None, "No se encontró hash de contraseña en la BD"

    # Depuración: imprime valores para verificar
    print("Hash en BD:", stored_hash)
    print("Contraseña ingresada:", generate_password_hash(password))

    if not check_password_hash(stored_hash.strip(), password):
        return None, "Contraseña incorrecta"

    return {
        "nombre": row.name,
        "email": row.email,
        "rol": row.rol.strip().lower()
    }, "Login correcto"
    
