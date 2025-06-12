import os
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Configuración de la app para servir archivos estáticos desde la raíz del proyecto
def create_app():
    app = Flask(__name__, static_folder='.', static_url_path='')
    CORS(app)

    # Ruta principal: sirve index.html
    @app.route('/')
    def root():
        return send_from_directory('.', 'index.html')

    # Sirve cualquier otro archivo estático (.html, .js, .css) de la raíz
    @app.route('/<path:path>')
    def static_proxy(path):
        return send_from_directory('.', path)

    # Ejemplo de endpoint para crear sesión de Stripe (ajustar en tu backend)
    @app.route('/create-checkout-session', methods=['POST'])
    def create_checkout_session():
        data = request.get_json()
        test = data.get('test')
        score = data.get('score')
        # Aquí iría la lógica de Stripe: crear sesión y devolver sessionId
        return jsonify({'sessionId': 'dummy_session_id'})

    # Endpoint para guardar resultado y enviar email
    @app.route('/guardar_resultado', methods=['POST'])
    def guardar_resultado():
        payload = request.get_json()
        email = payload.get('email')
        score = payload.get('score')
        test = payload.get('test')
        # Lógica para enviar email con SendGrid
        try:
            message = Mail(
                from_email=os.getenv('SENDGRID_FROM'),
                to_emails=email,
                subject=f'Resultado de tu test {test}',
                html_content=f'<p>Tu puntaje fue: {score}%</p>'
            )
            sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
            sg.send(message)
            return '', 200
        except Exception as e:
            return str(e), 500

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
