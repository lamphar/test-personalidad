from flask import Flask, request, jsonify
from flask_cors import CORS
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

app = Flask(__name__)
CORS(app)  # permite solicitudes desde tu frontend

# Sirve la landing y todos los archivos estáticos
app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def serve_static(path):
    return app.send_static_file(path)


@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        email = data.get('email')
        resultado = data.get('resultado')

        if not email or not resultado:
            return jsonify({'error': 'Faltan datos'}), 400

        message = Mail(
            from_email='TU_CORREO_VERIFICADO@tudominio.com',  # Cambia esto por uno verificado en SendGrid
            to_emails=email,
            subject='Tus resultados del test de personalidad',
            html_content=f"""
                <h2>Gracias por completar el test</h2>
                <p><strong>Resultado:</strong> {resultado}</p>
                <p>Este resultado es solo una guía general basada en herramientas científicas, no un diagnóstico clínico.</p>
            """
        )

        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg.send(message)

        return jsonify({'message': 'Correo enviado correctamente'}), 200

    except Exception as e:
        print(f'Error al enviar correo: {e}')
        return jsonify({'error': str(e)}), 500

# Requerido para funcionar en Render.com
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
