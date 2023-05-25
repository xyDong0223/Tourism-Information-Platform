from datetime import datetime

from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from socketIO_client import SocketIO as ClientSocketIO
from flask_sqlalchemy import SQLAlchemy

from serviceBooking.ext import db
from serviceBooking.models import Plans
from serviceBooking import settting
# from ext import db
# from models import Plans
# import settting
from flask_migrate import Migrate

import csv

# Initialise the APP
app = Flask(__name__)
## Set the configure of app
app.config.from_object(settting.ProducationConfig)
CORS(app)
socketio = SocketIO(app)
#connect the db to the app

db.init_app(app)
with app.app_context():
    db.create_all()
#handles the SQLAChemy database migration
Migrate(app=app,db=db)


#calcuate the total price with discount
def calculate_price(price, days):
    price = price * days
    if days >= 20:
        total_price = price * 0.7
    elif days >= 14:
        total_price = price * 0.8
    elif days >= 7:
        total_price = price * 0.9
    else:
        total_price = price
    return total_price


@socketio.on('calculate_service')
def calculate_service(data):
    # calculate how many days of the trip
    start_date = data["start_date"]
    end_date = data["end_date"]
    city = data["city"]
    plan_type = data["travel_type"]

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    print(start_date,end_date)
    delta = end_date - start_date
    days_between = delta.days

    plan = Plans.query.filter_by(location=city, plan_type=plan_type).first()

    total_price = calculate_price(plan.price,days_between)

    promotion_codes = {
        "SUMMER2023": 0.8,
        "TRAVELNOW": 0.75,
        "GETAWAY25": 0.85,
        "SAVEBIG10": 0.6,
        "EXPLORE15": 0.65
    }
    promo_validation=0
    if data['promo'].upper() in promotion_codes.keys():
        promo_validation = 1
        total_price *= promotion_codes[data['promo'].upper()]
    elif data['promo'].upper() == "":
        promo_validation = -1

    plan_response = {
        'location': plan.location,
        'price': round(total_price),
        'promo_validation': promo_validation

    }

    emit('service_response', plan_response)


@app.route('/')
def upload_csv_to_database():
    return "helloworld"

if __name__ == '__main__':
    socketio.run(app, port=5004,allow_unsafe_werkzeug=True)