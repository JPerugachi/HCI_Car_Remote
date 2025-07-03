from flask import Flask, request, render_template, jsonify
import joblib
import numpy as np
from flask_cors import CORS

# Indico dónde están mis assets estáticos y mis templates
app = Flask(
    __name__,
    static_folder="static",        # carpeta con .png, .js, .css...
    template_folder="templates"    # carpeta con carrito_virtual_con_imagen.html
)
CORS(app)

# Cargo el modelo de ML
modelo = joblib.load("modelo_carrito.pkl")

# Ruta raíz: renderiza la plantilla HTML
@app.route("/")
def home():
    return render_template("carrito_virtual_con_imagen.html")

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
