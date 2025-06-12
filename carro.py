from flask import Flask, request, send_from_directory

app = Flask(__name__)
last_cmd = ""

@app.route('/')
def handle_cmd():
    global last_cmd
    cmd = request.args.get('cmd')
    if cmd:
        last_cmd = cmd
        return "ok"
    return last_cmd

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
