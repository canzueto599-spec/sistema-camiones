from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import qrcode
import os

app = Flask(__name__)

# =========================
# DATABASE
# =========================

def get_db():
    conn = sqlite3.connect("camiones.db")
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
# HOME - VER CAMIONES
# =========================

@app.route("/")
def index():
    conn = get_db()
    camiones = conn.execute("SELECT * FROM camiones").fetchall()
    conn.close()
    return render_template("vercamiones.html", camiones=camiones)

# =========================
# AGREGAR CAMIÓN
# =========================

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

        return redirect(url_for("index"))

    return render_template("agregar.html")

# =========================
# ELIMINAR CAMIÓN
# =========================

@app.route("/eliminar/<int:id>")
def eliminar(id):
    conn = get_db()
    conn.execute("DELETE FROM camiones WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

# =========================
# GENERAR QR
# =========================

@app.route("/qr/<int:id>")
def generar_qr(id):
    conn = get_db()
    camion = conn.execute("SELECT * FROM camiones WHERE id = ?", (id,)).fetchone()
    conn.close()

    if not camion:
        return "Camión no encontrado"

    data = f"""
    Camión:
    Marca: {camion['marca']}
    Modelo: {camion['modelo']}
    Año: {camion['anio']}
    Placas: {camion['placas']}
    """

    img = qrcode.make(data)

    if not os.path.exists("static"):
        os.makedirs("static")

    path = f"static/qr_{id}.png"
    img.save(path)

    return render_template("qr.html", imagen=path)

# =========================
# RUN (IMPORTANTE PARA RENDER)
# =========================

if __name__ == "__main__":
    app.run()