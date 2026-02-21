from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import qrcode

app = Flask(__name__)

DATABASE = "camiones.db"

# ===============================
# CREAR BASE DE DATOS
# ===============================
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS camiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            anio TEXT NOT NULL,
            placas TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ===============================
# INICIO
# ===============================
@app.route("/")
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM camiones")
    camiones = cursor.fetchall()
    conn.close()
    return render_template("ver_camiones.html", camiones=camiones)

# ===============================
# AGREGAR CAMION
# ===============================
@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        marca = request.form.get("marca")
        modelo = request.form.get("modelo")
        anio = request.form.get("anio")
        placas = request.form.get("placas")

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO camiones (marca, modelo, anio, placas) VALUES (?, ?, ?, ?)",
            (marca, modelo, anio, placas)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("agregar.html")

# ===============================
# VER DETALLE
# ===============================
@app.route("/camion/<int:id>")
def ver_camion(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM camiones WHERE id = ?", (id,))
    camion = cursor.fetchone()
    conn.close()

    return render_template("camion.html", camion=camion)

# ===============================
# GENERAR QR
# ===============================
@app.route("/qr/<int:id>")
def generar_qr(id):
    url = request.host_url + "camion/" + str(id)
    img = qrcode.make(url)

    if not os.path.exists("static"):
        os.makedirs("static")

    path = os.path.join("static", f"qr_{id}.png")
    img.save(path)

    return render_template("qr.html", imagen=f"qr_{id}.png")

# ===============================
if __name__ == "__main__":
    app.run(debug=True)