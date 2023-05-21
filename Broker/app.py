import math

from flask import Flask, jsonify, request,render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import socketio
app = Flask(__name__)
CORS(app)
socket = SocketIO(app,cors_allowed_origins='http://127.0.0.1:5000',async_mode='threading', transport='xhr-polling')

# Kiwi
sio_kiwi = socketio.Client()
sio_kiwi.connect('http://localhost:5001')
@sio_kiwi.on('service_response')
def service_response(quotation):
    print(f"Received quotation: {quotation}")
    socket.emit('kiwi_update',quotation)
    sio_booking.disconnect()

# Booking
sio_booking = socketio.Client()
sio_booking.connect('http://localhost:5004')
@sio_booking.on('service_response')
def service_response(quotation):
    print(f"Received quotation: {quotation}")
    socket.emit('booking_update',quotation)
    sio_booking.disconnect()


@socket.on('get_input')
def get_input(data):
    print(f"Received quotation: {data}")
    sio_kiwi.emit('calculate_service',data)
    sio_booking.emit('calculate_service',data)




if __name__ == '__main__':
    socket.run(app, port=5005)