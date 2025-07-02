from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite que tu HTML pueda hacer fetch al backend

# Cargar el modelo
modelo = joblib.load("modelo_carrito.pkl")


# Ruta principal compatible con MIT App Inventor
@app.route("/", methods=["GET"])
def home():
    cmd = request.args.get("cmd")
    if cmd:
        print(f"Comando recibido desde MIT: {cmd}")
        return f"Comando recibido: {cmd}", 200
    return "Servidor activo", 200


# Ruta para predicción ML
@app.route('/predecir', methods=['POST'])
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
