from flask import Flask, request, jsonify
import joblib
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Cargar el modelo entrenado
modelo = joblib.load("modelo_carrito.pkl")

@app.route('/predecir', methods=['POST'])
def predecir():
    datos = request.get_json()
    tiempo = datos.get("tiempo", 0)
    giros = datos.get("giros", 0)
    colisiones = datos.get("colisiones", 0)

    entrada = np.array([[tiempo, giros, colisiones]])
    prediccion = modelo.predict(entrada)[0]  # 'novato', 'intermedio', 'experto'

    return jsonify({"nivel": prediccion})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
