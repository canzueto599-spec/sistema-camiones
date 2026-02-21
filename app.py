from flask import Flask, render_template, request, redirect
import sqlite3
import os
import qrcode

app = Flask(__name__)

# =========================
# BASE DE DATOS
# =========================

DB_PATH = os.path.join(os.getcwd(), "camiones.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS camiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marca TEXT,
            modelo TEXT,
            anio TEXT,
            placas TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# =========================
# INICIO
# =========================

@app.route("/")
def index():
    conn = get_db()
    camiones = conn.execute("SELECT * FROM camiones").fetchall()
    conn.close()
    return render_template("ver_camiones.html", camiones=camiones)

# =========================
# AGREGAR
# =========================

@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        marca = request.form.get("marca")
        modelo = request.form.get("modelo")
        anio = request.form.get("anio")
        placas = request.form.get("placas")

        conn = get_db()
        conn.execute(
            "INSERT INTO camiones (marca, modelo, anio, placas) VALUES (?, ?, ?, ?)",
            (marca, modelo, anio, placas)
        )
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("agregar.html")

# =========================
# VER CAMIÓN
# =========================

@app.route("/camion/<int:id>")
def ver_camion(id):
    conn = get_db()
    camion = conn.execute(
        "SELECT * FROM camiones WHERE id = ?", (id,)
    ).fetchone()
    conn.close()

    return render_template("camion.html", camion=camion)

# =========================
# GENERAR QR
# =========================

@app.route("/qr/<int:id>")
def generar_qr(id):
    url = f"https://sistema-camiones.onrender.com/camion/{id}"
    img = qrcode.make(url)

    if not os.path.exists("static"):
        os.makedirs("static")

    path = os.path.join("static", f"qr_{id}.png")
    img.save(path)

    return render_template("qr.html", imagen=f"qr_{id}.png")

# =========================

if __name__ == "__main__":
    app.run()