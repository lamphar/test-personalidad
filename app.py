from flask import Flask, request, jsonify, send_from_directory
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    email = data.get('email')
    resultado = data.get('resultado')

    if not email or not resultado:
        return jsonify({'error': 'Faltan datos'}), 400

    message = Mail(
        from_email='tucorreo@tuweb.com',
        to_emails=email,
        subject='Tus resultados del test de personalidad',
        html_content=f"""
        <p>Gracias por completar el test.</p>
        <p><strong>Tu resultado:</strong></p>
        <p>{resultado}</p>
        <p>Este resultado es orientativo y no sustituye una evaluación profesional.</p>
        """)

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg.send(message)
        return jsonify({'message': 'Correo enviado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
