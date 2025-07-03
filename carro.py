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
    tiempo     = float(datos.get("tiempo", 0))
    giros      = int(datos.get("giros", 0))
    colisiones = int(datos.get("colisiones", 0))

    X = np.array([[tiempo, giros, colisiones]])
    # No int(): cojo directamente la etiqueta (string)
    nivel = modelo.predict(X)[0]

    return jsonify({"nivel": nivel}) 


# Archivos estáticos (HTML, imágenes, css...)
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory('.', filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
