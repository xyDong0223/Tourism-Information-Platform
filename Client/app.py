from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

# Define a route for the home page
@app.route('/')
def home():
    return render_template('index.html')



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
