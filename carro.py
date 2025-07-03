from flask import Flask, request, render_template, jsonify
import joblib
import numpy as np
from flask_cors import CORS

# Configuración de la aplicación Flask
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)
app = Flask(__name__)
last_cmd = ""

# Cargo el modelo de ML
modelo = joblib.load("modelo_carrito.pkl")

# Ruta raíz: renderiza la plantilla HTML
@app.route('/')
def handle_cmd():
    global last_cmd
    cmd = request.args.get('cmd')
    if cmd:
        last_cmd = cmd
    return last_cmd  # Siempre responde el último comando (NO "ok")


# Endpoint de ML
@app.route("/predecir", methods=["POST"])
def predecir():
    datos = request.get_json() or {}
    tiempo     = datos.get("tiempo", 0)
    giros      = datos.get("giros", 0)
    colisiones = datos.get("colisiones", 0)

    entrada = np.array([[tiempo, giros, colisiones]])
    nivel    = modelo.predict(entrada)[0]
    return jsonify({"nivel": int(nivel)})

if __name__ == "__main__":
    # debug=True solo durante desarrollo
    app.run(host="0.0.0.0", port=5000, debug=True)
