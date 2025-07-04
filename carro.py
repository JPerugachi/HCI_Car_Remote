from flask import Flask, request, send_from_directory, jsonify
import joblib
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Carga tu modelo entrenado con características: tiempo, giros, colisiones y puntos
modelo = joblib.load("modelo_carrito.pkl")

# Manejador de comandos (joystick/teclado)
last_cmd = ""
@app.route("/")
def comando():
    global last_cmd
    cmd = request.args.get("cmd")
    if cmd:
        last_cmd = cmd.strip().upper()
    return last_cmd

# Endpoint ML: recibe tiempo, giros, colisiones y puntos, devuelve nivel
@app.route("/predecir", methods=["POST"])
def predecir():
    datos = request.get_json() or {}
    tiempo     = float(datos.get("tiempo", 0))
    giros      = int(datos.get("giros", 0))
    colisiones = int(datos.get("colisiones", 0))
    puntos     = int(datos.get("puntos", 0))

    # Pasamos las cuatro características al modelo
    X = np.array([[tiempo, giros, colisiones, puntos]])
    nivel = modelo.predict(X)[0]
    return jsonify({"nivel": nivel})

# Servir archivos estáticos (HTML, imágenes, CSS)
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory('.', filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)