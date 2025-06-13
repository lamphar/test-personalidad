
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os, stripe, json, datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__, static_folder='static')
CORS(app)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")  # set in Render env
PRICE_ID = os.getenv("STRIPE_PRICE_50C")        # 0.50€ price id
BASE_URL = os.getenv("BASE_URL","https://test-personalidad.onrender.com")

@app.route("/")
def root(): return send_from_directory(app.static_folder,"index.html")

@app.route('/<path:path>')
def static_proxy(path): return send_from_directory(app.static_folder, path)

@app.route("/create-checkout-session", methods=["POST"])
def create_checkout():
    data = request.json
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[{"price": PRICE_ID, "quantity": 1}],
        metadata={"test": data["test"], "score": data["score"]},
        success_url=f"{BASE_URL}/resultado.html?test={data['test']}&score={data['score']}&session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{BASE_URL}/resultado.html?test={data['test']}&score={data['score']}"
    )
    return jsonify(sessionId=session["id"])

@app.route("/stripe/webhook", methods=["POST"])
def webhook():
    payload = request.data
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET"))
    except Exception as e:
        return str(e), 400
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        email = session["customer_details"]["email"]
        test = session["metadata"]["test"]
        score = session["metadata"]["score"]
        enviar_correo(email, test, score)
    return "", 200

def enviar_correo(email, test, score):
    """Envía email con resultado (simple)."""
    html = f"<p>Gracias por usar MindPath.</p><p>Test: {test}<br>Puntaje: {score}%</p>"
    message = Mail(
        from_email="noreply@mindpath.ai",
        to_emails=email,
        subject="Tu informe MindPath",
        html_content=html
    )
    SendGridAPIClient(os.getenv("SENDGRID_API_KEY")).send(message)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
