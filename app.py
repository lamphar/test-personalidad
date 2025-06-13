import os
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Crea la aplicación y configura carpeta estática
app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Ruta principal: sirve index.html desde /static
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

# Sirve cualquier archivo estático en /static
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# Endpoint para crear sesión de Stripe Checkout
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    from stripe import Stripe
    stripe_api_key = os.getenv('STRIPE_SECRET_KEY')
    stripe = Stripe(stripe_api_key)
    data = request.get_json()
    test = data.get('test')
    score = data.get('score')
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {'name': f'Test {test} - Informe'},
                'unit_amount': 50,  # 0.50 € in cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=f"{os.getenv('BASE_URL')}/resultado.html?test={test}&score={score}&session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{os.getenv('BASE_URL')}/resultado.html?test={test}&score={score}",
    )
    return jsonify({'sessionId': session.id})

# Endpoint para guardar resultado y enviar email
@app.route('/guardar_resultado', methods=['POST'])
def guardar_resultado():
    payload = request.get_json()
    email = payload.get('email')
    score = payload.get('score')
    test = payload.get('test')
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
