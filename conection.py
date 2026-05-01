from flask import Flask, request, jsonify
import pyodbc
import os
from dotenv import load_dotenv
from config.db import get_db_connection
app = Flask(__name__)


@app.route("/users", methods=["GET"])
def get_users():
    """Fetch all users from the database."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM Users")
        rows = cursor.fetchall()
        users = [{"id": row.id, "name": row.name, "email": row.email} for row in rows]
        return jsonify(users)
    except pyodbc.Error as e:
        app.logger.error(f"Query failed: {e}")
        return jsonify({"error": "Query execution failed"}), 500
    finally:
        conn.close()

@app.route("/users", methods=["POST"])
def add_user():
    """Insert a new user into the database."""
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Invalid input"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Users (name, email) VALUES (?, ?)",
            (data["name"], data["email"])
        )
        conn.commit()
        return jsonify({"message": "User added successfully"}), 201
    except pyodbc.Error as e:
        app.logger.error(f"Insert failed: {e}")
        return jsonify({"error": "Insert failed"}), 500
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)