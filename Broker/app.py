import math

from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import socketio
import time

app = Flask(__name__)
CORS(app)
socket = SocketIO(app, cors_allowed_origins='http://127.0.0.1:5000', async_mode='threading', transport='xhr-polling')

# Kiwi
sio_kiwi = socketio.Client()
connected = False
while not connected:
    try:
        sio_kiwi.connect('http://service-kiwi:5001')
        print("Socket established")
        connected = True
        @sio_kiwi.on('service_response')
        def service_response(quotation):
            print(f"Received quotation: {quotation}")
            socket.emit('kiwi_update', quotation)
    except Exception as ex:
        time.sleep(1)

# Trip
sio_trip = socketio.Client()
connected = False
while not connected:
    try:
        sio_trip.connect('http://service-trip:5002')
        print("Socket established")
        connected = True
        @sio_trip.on('service_response')
        def service_response(quotation):
            print(f"Received quotation: {quotation}")
            socket.emit('trip_update', quotation)
    except Exception as ex:
        time.sleep(1)

# Skyscanner
sio_skyscanner = socketio.Client()
connected = False
while not connected:
    try:
        sio_skyscanner.connect('http://service-skyscanner:5003')
        print("Socket established")
        connected = True
        @sio_skyscanner.on('service_response')
        def service_response(quotation):
            print(f"Received quotation: {quotation}")
            socket.emit('skyscanner_update', quotation)  # send quotation to client
    except Exception as ex:
        time.sleep(1)

# Booking
sio_booking = socketio.Client()
connected = False
while not connected:
    try:
        sio_booking.connect('http://service-booking:5004')
        print("Socket established")
        connected = True
        @sio_booking.on('service_response')
        def service_response(quotation):
            print(f"Received quotation: {quotation}")
            socket.emit('booking_update', quotation)
    except Exception as ex:
        time.sleep(1)

@socket.on('get_input')
def get_input(data):
    print(f"Received quotation: {data}")
    sio_kiwi.emit('calculate_service', data)
    sio_trip.emit('calculate_service', data)
    sio_skyscanner.emit('calculate_service', data)
    sio_booking.emit('calculate_service', data)


if __name__ == '__main__':
    socket.run(app, port=5005, allow_unsafe_werkzeug=True)
