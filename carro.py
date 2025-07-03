from flask import Flask, request, send_from_directory, jsonify
import joblib
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Modelo entrenado
modelo = joblib.load("modelo_carrito.pkl")

# Manejar ruta raíz con ?cmd= desde MIT
@app.route("/")
def home():
    return send_from_directory('.', 'carrito_virtual_con_imagen.html')

# Archivos estáticos: JS, imágenes, etc.
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory('.', filename)

# Ruta ML para clasificación
@app.route("/predecir", methods=["POST"])
def predecir():
    datos = request.get_json()
    tiempo = datos.get("tiempo", 0)
    giros = datos.get("giros", 0)
    colisiones = datos.get("colisiones", 0)

    entrada = np.array([[tiempo, giros, colisiones]])
    prediccion = modelo.predict(entrada)[0]

    return jsonify({"nivel": prediccion})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
