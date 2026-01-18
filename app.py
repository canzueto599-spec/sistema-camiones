from flask import Flask, render_template, request, redirect, url_for, abort
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "camiones.db"

# -------------------------
# CONEXIÓN A LA BASE DE DATOS
# -------------------------
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# -------------------------
# INICIO
# -------------------------
@app.route("/")
def inicio():
    return render_template("inicio.html")

# -------------------------
# VER CAMIÓN (PÚBLICO)
# -------------------------
@app.route("/camion/<int:id>")
def ver_camion(id):
    db = get_db()
    camion = db.execute(
        "SELECT * FROM camiones WHERE id = ?",
        (id,)
    ).fetchone()
    db.close()

    if camion is None:
        return "Camión no encontrado", 404

    return render_template("camion.html", camion=camion)

# -------------------------
# AGREGAR CAMIÓN (PRIVADO / PAPÁ)
# -------------------------
@app.route("/agregar", methods=["GET", "POST"])
def agregar_camion():
    if request.method == "POST":
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        anio = request.form["anio"]
        color = request.form["color"]

        db = get_db()
        db.execute(
            "INSERT INTO camiones (marca, modelo, anio, color) VALUES (?, ?, ?, ?)",
            (marca, modelo, anio, color)
        )
        db.commit()
        db.close()

        return redirect(url_for("inicio"))

    return render_template("agregar.html")

# -------------------------
# ARRANQUE (RENDER)
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
