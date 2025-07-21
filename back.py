from flask import Flask, request, jsonify, send_from_directory
from twilio.rest import Client
import datetime

# 🔐 Twilio credentials (⚠️ Move to environment variables in production!)
account_sid = 'AC06fc3dabb38d357fe8394580d02c97a9'
auth_token = '8eff4772e706b20b0b6fed5ee94c7e46'
twilio_number = '+17853678119'  # Your Twilio number

client = Client(account_sid, auth_token)

app = Flask(__name__, static_folder='static')

@app.route('/')
def serve_ui():
    return send_from_directory('static', 'index.html')

@app.route('/send-sms', methods=['POST'])
def send_sms():
    data = request.get_json()
    number = data.get('number')
    message = data.get('message')

    if not number or not message:
        return jsonify(success=False, error="Phone number and message are required.")

    try:
        sms = client.messages.create(
            body=message,
            from_=twilio_number,
            to=number
        )

        return jsonify(success=True, sid=sms.sid)
    except Exception as e:
        return jsonify(success=False, error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
