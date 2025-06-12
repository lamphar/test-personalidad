import os
from flask import Flask, send_from_directory

# 1) Dile a Flask dónde está la carpeta de tus HTML/CSS/JS
app = Flask(__name__, static_folder='static', static_url_path='')

# 2) Ruta raíz → sirve index.html
@app.route('/')
def root():
    return app.send_static_file('index.html')

# 3) Cualquier otra ruta sirve archivos estáticos de /static
@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)

# 4) Tu endpoint de correo sigue aquí abajo...
# @app.route('/send-email', methods=['POST'])
# def send_email(): ...

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
