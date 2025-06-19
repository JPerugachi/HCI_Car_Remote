import csv
from flask import Flask, request, send_from_directory, jsonify
import joblib, os

app = Flask(__name__)
last_cmd = ""

# Modelo (opcional en desarrollo)
try:
    modelo = joblib.load("modelo_tipo_conductor.pkl")
except:
    modelo = None

CSV_FILENAME = "datos_conduccion.csv"

# Inicializa el CSV si no existe
if not os.path.exists(CSV_FILENAME):
    with open(CSV_FILENAME, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["tiempo", "giros", "colisiones", "tipo"])  # encabezados

@app.route('/')
def handle_cmd():
    global last_cmd
    cmd = request.args.get('cmd')
    if cmd:
        last_cmd = cmd
    return last_cmd

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

@app.route('/clasificar', methods=["POST"])
def clasificar_usuario():
    datos = request.get_json()
    tiempo = datos.get("tiempo", 5)
    giros = datos.get("giros", 0)
    colisiones = datos.get("colisiones", 0)

    # Clasificación: usa modelo real o fallback por reglas
    if modelo:
        entrada = [[tiempo, giros, colisiones]]
        tipo = modelo.predict(entrada)[0]
    else:
        if colisiones >= 3:
            tipo = "agresivo"
        elif tiempo <= 2:
            tipo = "preciso"
        else:
            tipo = "normal"

    # Guardar en CSV para dataset
    with open(CSV_FILENAME, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([tiempo, giros, colisiones, tipo])

    return jsonify({"tipo": tipo})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
# Para ejecutar el servidor, usa: python carro.py
# Asegúrate de tener Flask y joblib instalados: pip install Flask joblib