from datetime import datetime

from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from socketIO_client import SocketIO as ClientSocketIO
from flask_sqlalchemy import SQLAlchemy

# from Service_Booking.ext import db
# from Service_Booking.models import Plans
# from Service_Booking import settting
from ext import db
from models import Plans
import settting
from flask_migrate import Migrate

import csv

# Initialise the APP
app = Flask(__name__)
## Set the configure of app
app.config.from_object(settting.DevelopmentConfig)
CORS(app)
socketio = SocketIO(app)
#connect the db to the app

db.init_app(app)
with app.app_context():
    db.create_all()
#handles the SQLAChemy database migration
Migrate(app=app,db=db)


# Define a function to generate a quotation
def generate_quotation():
    # Business logic for generating a quotation goes here
    quotation = {
        'id': 1,
        'description': 'Trip\'s Quotation',
        'price': 100.00
    }
    return quotation

# Listen for a 'quotation' event and send back a quotation
@socketio.on('quotation')
def get_quotation():
    quotation = generate_quotation()
    print("receive the request from the broker")
    emit('quotation_response', quotation)

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

    plan_response = {
        'location': plan.location,
        'price': total_price,
        'description': plan.description,
        'plan_type':plan.plan_type
    }

    emit('service_response', plan_response)








@app.route('/')
def upload_csv_to_database():
    with open('plans.csv', 'r') as file:
        csv_data = csv.reader(file)
        next(csv_data)  # Skip the header row
        for row in csv_data:
            location = row[0]
            price = float(row[1])
            description = row[2]
            plan_type = row[3]

            # Create a new Plans object and assign the values from the CSV row
            plan = Plans(location=location, price=price, description=description, plan_type=plan_type)

            # Add the new object to the session
            db.session.add(plan)

    # Commit the changes to the database
    db.session.commit()
    return "hello world"

if __name__ == '__main__':
    socketio.run(app, port=5004)