from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from socketIO_client import SocketIO as ClientSocketIO
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

# Define a function to generate a quotation
def generate_quotation():
    # Business logic for generating a quotation goes here
    quotation = {
        'id': 1,
        'description': 'Service_Trip\'s Quotation',
        'price': 33.00
    }
    return quotation

# Listen for a 'quotation' event and send back a quotation
@socketio.on('quotation')
def get_quotation():
    quotation = generate_quotation()
    print("receive the request from the broker")
    emit('quotation_response', quotation)

if __name__ == '__main__':
    socketio.run(app, port=5003)
