import math

from flask import Flask, jsonify, request,render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import socketio
app = Flask(__name__)
CORS(app)
socket = SocketIO(app,cors_allowed_origins='http://127.0.0.1:5000',async_mode='threading', transport='xhr-polling')
sio_booking = socketio.Client()
sio_booking.connect('http://localhost:5004')


# Define a function to handle the response from the Auldfella's Quotation Service

@sio_booking.on('service_response')
def service_response(quotation):
    print(f"Received quotation: {quotation}")
    socket.emit('update_plan',quotation)
    sio_booking.disconnect()





@socket.on('get_input')
def get_input(data):
    print(f"Received quotation: {data}")

    sio_booking.emit('calculate_service',data)




if __name__ == '__main__':
    socket.run(app, port=5002)