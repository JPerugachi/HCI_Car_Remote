from flask import Flask, request, send_from_directory, jsonify
import joblib
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Capa de comando
last_cmd = ""

# Carga tu modelo ML
modelo = joblib.load("modelo_carrito.pkl")

@app.route("/")
def comando():
    global last_cmd
    cmd = request.args.get("cmd")
    if cmd:
        last_cmd = cmd
    return last_cmd  # devuelve siempre el último comando

@app.route("/predecir", methods=["POST"])
def predecir():
    datos = request.get_json() or {}
    # <-- Añade esta línea para debug:
    print("ML payload recibido:", datos)

    tiempo     = float(datos.get("tiempo",     0))
    giros      = int(  datos.get("giros",      0))
    colisiones = int(  datos.get("colisiones", 0))

    X = np.array([[tiempo, giros, colisiones]])
    nivel = modelo.predict(X)[0]
    return jsonify({"nivel": nivel})



# Archivos estáticos (HTML, imágenes, css...)
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory('.', filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
# This code is a Flask application that serves as a backend for a machine learning model predicting the level of a shopping cart based on input features.
# It includes endpoints for receiving commands and making predictions, and it uses CORS to allow cross-origin requests.
# The model is loaded from a file named "modelo_carrito.pkl", and the application can serve static files like HTML, images, and CSS from the current directory.
# The application runs on all available IP addresses on port 5000.