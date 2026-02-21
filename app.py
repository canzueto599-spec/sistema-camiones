from flask import Flask, render_template, request, redirect
import sqlite3
import qrcode
import os

app = Flask(__name__)

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

# 🏠 INICIO
@app.route("/")
def index():
    conn = get_db()
    camiones = conn.execute("SELECT * FROM camiones").fetchall()
    conn.close()
    return render_template("ver_camiones.html", camiones=camiones)


# ➕ AGREGAR CAMIÓN
@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        anio = request.form["anio"]
        placas = request.form["placas"]

        conn = get_db()
        conn.execute(
            "INSERT INTO camiones (marca, modelo, anio, placas) VALUES (?, ?, ?, ?)",
            (marca, modelo, anio, placas)
        )
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("agregar.html")


# 📱 GENERAR QR
@app.route("/qr/<int:id>")
def generar_qr(id):
    data = f"https://sistema-camiones.onrender.com/camion/{id}"
    img = qrcode.make(data)

    path = os.path.join("static", f"qr_{id}.png")
    img.save(path)

    return render_template("qr.html", qr_image=f"qr_{id}.png")


# 👀 VER CAMIÓN INDIVIDUAL
@app.route("/camion/<int:id>")
def ver_camion(id):
    conn = get_db()
    camion = conn.execute(
        "SELECT * FROM camiones WHERE id = ?", (id,)
    ).fetchone()
    conn.close()

    return render_template("camion.html", camion=camion)


if __name__ == "__main__":
    app.run(debug=True)