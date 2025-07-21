from flask import Flask, request, jsonify, send_from_directory
from twilio.rest import Client
import os

app = Flask(__name__, static_folder='static')

# Allow loading static HTML directly
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

# Replace with your credentials
account_sid = 'AC06fc3dabb38d357fe8394580d02c97a9'
auth_token = '8eff4772e706b20b0b6fed5ee94c7e46'
from_number = '+17853678119'

client = Client(account_sid, auth_token)

@app.route('/make-call', methods=['POST'])
def make_call():
    data = request.get_json()
    to_number = data.get('number')

    try:
        call = client.calls.create(
            twiml='<Response><Say>Hey! This is a test call from Python. Have a great day!</Say></Response>',
            to=to_number,
            from_=from_number
        )
        return jsonify({'success': True, 'sid': call.sid})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)