from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Define a route for the home page
@app.route('/')
def home():
    cities = [
        "Rome",
        "Paris",
        "Venice",
        "Florence",
        "Vienna",
        "Prague",
        "Dublin",
        "Budapest",
        "Krakow",
        "Stockholm",
        "Lisbon",
        "Amsterdam",
        "Madrid",
        "Athens",
        "Edinburgh",
        "Copenhagen",
        "Zurich",
        "Oslo",
        "Bergen",
        "Seville",
        "Helsinki",
        "Dubrovnik"
    ]

    return render_template('index.html',cities=cities)




if __name__ == '__main__':
    socketio.run(app, port=5000)
