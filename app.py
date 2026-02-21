from flask import Flask, render_template, request, redirect
import sqlite3
import qrcode
import os

app = Flask(__name__)

# ======================
# CONEXIÓN A BASE DE DATOS
# ======================

def get_db():
    conn = sqlite3.connect("camiones.db")
    conn.row_factory = sqlite3.Row
    return conn


# ======================
# CREAR TABLA SI NO EXISTE
# ======================

def crear_tabla():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS camiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marca TEXT,
            modelo TEXT,
            cilindros TEXT,
            asientos TEXT,
            combustible TEXT,
            puertas TEXT,
            tonelaje TEXT,
            ejes TEXT
        )
    """)
    conn.commit()
    conn.close()

crear_tabla()


# ======================
# INICIO
# ======================

@app.route("/")
def inicio():
    return redirect("/ver_camiones")


# ======================
# AGREGAR CAMIÓN
# ======================

@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        cilindros = request.form["cilindros"]
        asientos = request.form["asientos"]
        combustible = request.form["combustible"]
        puertas = request.form["puertas"]
        tonelaje = request.form["tonelaje"]
        ejes = request.form["ejes"]

        conn = get_db()
        conn.execute("""
            INSERT INTO camiones 
            (marca, modelo, cilindros, asientos, combustible, puertas, tonelaje, ejes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (marca, modelo, cilindros, asientos, combustible, puertas, tonelaje, ejes))
        conn.commit()
        conn.close()

        return redirect("/ver_camiones")

    return render_template("agregar.html")


# ======================
# VER CAMIONES
# ======================

@app.route("/ver_camiones")
def ver_camiones():
    conn = get_db()
    camiones = conn.execute("SELECT * FROM camiones").fetchall()
    conn.close()
    return render_template("ver_camiones.html", camiones=camiones)


# ======================
# ELIMINAR
# ======================

@app.route("/eliminar/<int:id>")
def eliminar(id):
    conn = get_db()
    conn.execute("DELETE FROM camiones WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/ver_camiones")


# ======================
# EDITAR
# ======================

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conn = get_db()

    if request.method == "POST":
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        cilindros = request.form["cilindros"]
        asientos = request.form["asientos"]
        combustible = request.form["combustible"]
        puertas = request.form["puertas"]
        tonelaje = request.form["tonelaje"]
        ejes = request.form["ejes"]

        conn.execute("""
            UPDATE camiones
            SET marca=?, modelo=?, cilindros=?, asientos=?, combustible=?, puertas=?, tonelaje=?, ejes=?
            WHERE id=?
        """, (marca, modelo, cilindros, asientos, combustible, puertas, tonelaje, ejes, id))
        conn.commit()
        conn.close()
        return redirect("/ver_camiones")

    camion = conn.execute("SELECT * FROM camiones WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template("agregar.html", camion=camion)


# ======================
# GENERAR QR
# ======================

@app.route("/qr/<int:id>")
def qr_camion(id):
    conn = get_db()
    camion = conn.execute(
        "SELECT * FROM camiones WHERE id = ?", (id,)
    ).fetchone()
    conn.close()

    if not camion:
        return "Camión no encontrado"

    data = f"""
    Camión
    Marca: {camion['marca']}
    Modelo: {camion['modelo']}
    Cilindros: {camion['cilindros']}
    Asientos: {camion['asientos']}
    Combustible: {camion['combustible']}
    Puertas: {camion['puertas']}
    Tonelaje: {camion['tonelaje']}
    Ejes: {camion['ejes']}
    """

    img = qrcode.make(data)

    os.makedirs("static/qrs", exist_ok=True)
    path = f"static/qrs/camion_{id}.png"
    img.save(path)

    return render_template("qr.html", camion=camion, qr=path)


# ======================
# RUN
# ======================

if __name__ == "__main__":
    app.run(debug=True)