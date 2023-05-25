import csv

from flask import Flask, jsonify, render_template
from flask_migrate import Migrate

from ext import db
from flask_socketio import SocketIO, emit
from datetime import datetime
from flask_cors import CORS
from socketIO_client import SocketIO as ClientSocketIO

import setting
from models import Plans

app = Flask(__name__)
CORS(app)
app.config.from_object(setting.DevelopmentConfig)
socketio = SocketIO(app)

db.init_app(app)
with app.app_context():
    db.create_all()
Migrate(app=app, db=db)

@socketio.on('calculate_service')
def calculate_service(data):
    start_date = datetime.strptime(data["start_date"], '%Y-%m-%d').date()
    end_date = datetime.strptime(data["end_date"], '%Y-%m-%d').date()
    total_days = (end_date - start_date).days

    plan = Plans.query.filter_by(location=data["city"]).first()

    base_price = plan.price
    if data["travel_type"] == "semi inclusive":
        base_price *= 1.1
    elif data["travel_type"] == "all inclusive":
        base_price *= 1.2

    total_price = base_price * total_days

    if total_days > 7:
        total_price *= 0.9
    elif total_price >= 30:
        total_price *= 0.8

    promo_validation = 0
    if data['promo'].upper() == '':
        promo_validation = -1
    elif data['promo'].upper() == 'STUDENT':
        promo_validation = 1
        total_price *= 0.9
    print(promo_validation)

    plan_response = {
        'location': plan.location,
        'price':  round(total_price),
        'promo_validation': promo_validation
    }
    emit('service_response', plan_response)


if __name__ == '__main__':
    socketio.run(app, port=5001)
