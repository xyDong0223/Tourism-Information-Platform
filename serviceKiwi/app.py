from datetime import datetime

from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from socketIO_client import SocketIO as ClientSocketIO

# Initialise the APP
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

@socketio.on('quotation')
def get_quotation():
    quotation = generate_quotation()
    print("receive the request from the broker")
    emit('quotation_response', quotation)

@socketio.on('calculate_service')
def calculate_service(data):
    city = data["city"]
    plan_response = {
        'location': city,
        'price': 100,
    }
    emit('service_response', plan_response)


if __name__ == '__main__':
    socketio.run(app, port=5001)