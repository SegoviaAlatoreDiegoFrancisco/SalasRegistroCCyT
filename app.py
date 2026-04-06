import os
from flask import url_for
from flask import session
from flask import redirect, request
from flask import Flask, render_template

from auth.auth import usuario_crear, usuario_validar

from routes.alumnos import alumnos_bp
from routes.docentes import docentes_bp
from routes.salas import salas_bp

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "default_fallback_key")
app.register_blueprint(alumnos_bp)
app.register_blueprint(docentes_bp)
app.register_blueprint(salas_bp)

@app.route("/login", methods =["GET","POST"])
def login():
    if request.method=="POST":
        email = request.form.get("email")
        password = request.form.get("password")
        datos , msg= usuario_validar(email, password)
        if datos:
            print("Rol en datos: ", datos["rol"])
            session["usuario"] = datos["nombre"]
            session["rol"] = datos["rol"]
            if datos["rol"] == "admin":
                return redirect(url_for("admin_dashboard"))
            else: 
                return redirect(url_for("user_dashboard"))
        else:                   
            return render_template("login.html",error =msg)
    return render_template("login.html")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method =="POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmar = request.form.get("confirmar")

        if password != confirmar:
            return render_template("register.html",error="Las contraseñas no coinciden")
        ok, msg = usuario_crear(nombre,email,password)
        if ok:
            return redirect(url_for("login"))
        else:
            return render_template("register.html",error=msg)
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/user")
def user_dashboard():
    if not session.get("usuario"):
        return redirect(url_for("login"))
    return F"Bienvenido {session['usuario']} (usuario común) con rol {session['rol']}. Consulta tus permisos con el administrador"

@app.route("/admin")
def admin_dashboard():
    if session.get("rol") != "admin":
        return redirect(url_for("login"))
    return render_template("admin.html")
if __name__ == "__main__":
    app.run(debug=True)