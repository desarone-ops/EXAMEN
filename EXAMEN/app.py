from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)


PRECIO_LATA = 9000

# Usuarios segun solicitud
USUARIOS = {
    "juan": {"password": "juanito123", "rol": "administrador"},
    "pepe": {"password": "pepito123", "rol": "usuario"},
}

@app.route("/")
def index():
    return render_template("index.html")

# ------------------ EJERCICIO 1 ------------------
@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    resultado = None
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        edad_raw = request.form.get("edad", "").strip()
        tarros_raw = request.form.get("tarros", "").strip()

        # Validaciones básicas
        if not nombre or not edad_raw or not tarros_raw:
            flash("Todos los campos son obligatorios.", "error")
            return redirect(url_for("ejercicio1"))

        try:
            edad = int(edad_raw)
            tarros = int(tarros_raw)
            if edad < 0 or tarros <= 0:
                raise ValueError
        except ValueError:
            flash("Edad y cantidad de tarros deben ser números válidos (edad ≥ 0, tarros ≥ 1).", "error")
            return redirect(url_for("ejercicio1"))

        # Calculamos totales y descuentos
        total_sin_desc = tarros * PRECIO_LATA

        if 18 <= edad <= 30:
            desc_pct = 0.15
        elif edad > 30:
            desc_pct = 0.25
        else:
            desc_pct = 0.0

        monto_desc = round(total_sin_desc * desc_pct)
        total_pagar = total_sin_desc - monto_desc

        resultado = {
            "nombre": nombre,
            "edad": edad,
            "tarros": tarros,
            "precio": PRECIO_LATA,
            "total_sin_desc": total_sin_desc,
            "desc_pct": int(desc_pct * 100),
            "monto_desc": monto_desc,
            "total_pagar": total_pagar,
        }

    return render_template("ejercicio1.html", resultado=resultado)


# ------------------ EJERCICIO 2 ------------------
@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    mensaje = None
    clase = "ok"

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip().lower()
        clave = request.form.get("password", "").strip()

        if usuario in USUARIOS and USUARIOS[usuario]["password"] == clave:
            rol = USUARIOS[usuario]["rol"]
            mensaje = f"Bienvenido {rol} {usuario}"
            clase = "ok"
        else:
            mensaje = "Usuario o contraseña incorrectos"
            clase = "error"

    return render_template("ejercicio2.html", mensaje=mensaje, clase=clase)


if __name__ == "__main__":
    app.run(debug=True)
