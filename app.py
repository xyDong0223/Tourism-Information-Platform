from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Define a route for the home page
@app.route('/')
def home():
    return render_template('index.html')



if __name__ == '__main__':
    socketio.run(app, port=5000)
