import math

from flask import Flask, jsonify, request,render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import socketio
app = Flask(__name__)
CORS(app)
socket = SocketIO(app,cors_allowed_origins='http://127.0.0.1:5000',async_mode='threading', transport='xhr-polling')
sio_auld = socketio.Client()
sio_auld.connect('http://localhost:5001')
sio_GAQ = socketio.Client()
sio_GAQ.connect('http://localhost:5003')

# Define a function to handle the response from the Auldfella's Quotation Service
@sio_auld.on('quotation_response')
def quotation_response(quotation):
    print(f"Received quotation: {quotation}")
    socket.emit('update_price',quotation)
    sio_auld.disconnect()
# Define a function to handle the response from the Auldfella's Quotation Service
@sio_GAQ.on('quotation_response')
def quotation_response(quotation):
    print(f"Received quotation: {quotation}")
    socket.emit('update_price',quotation)
    sio_auld.disconnect()


@socket.on('get_quotation')
def get_quotation():
    sio_auld.emit('quotation')
    sio_GAQ.emit('quotation')




if __name__ == '__main__':
    socket.run(app, port=5002)