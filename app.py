from flask import Flask, render_template
from routes.alumnos import alumnos_bp

app = Flask(__name__)
app.register_blueprint(alumnos_bp)

@app.route("/admin")
def admin_dashboard():
    return render_template("admin.html")
if __name__ == "__main__":
    app.run(debug=True)