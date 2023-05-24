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


# Define a function to generate a quotation
# def generate_quotation():
#     # Business logic for generating a quotation goes here
#     quotation = {
#         'id': 1,
#         'description': 'Service_Trip\'s Quotation',
#         'price': 33.00
#     }
#     return quotation
#
#
# # Listen for a 'quotation' event and send back a quotation
# @socketio.on('quotation')
# def get_quotation():
#     quotation = generate_quotation()
#     print("receive the request from the broker")
#     emit('quotation_response', quotation)


@socketio.on('calculate_service')
def calculate_service(data):
    start = data["start_date"]
    end = data["end_date"]
    city = data["city"]
    type = data["travel_type"]

    start = datetime.strptime(start, '%Y-%m-%d').date()
    end = datetime.strptime(end, '%Y-%m-%d').date()
    days_past = (end - start).days

    plan = Plans.query.filter_by(location=city, plan_type=type).first()

    base_price = plan.price
    price = base_price * days_past

    if days_past >= 30:
        total_price = price * 0.75
    elif days_past >= 14:
        total_price = price * 0.85
    elif days_past >= 7:
        total_price = price * 0.85
    else:
        total_price = price

    plan_response = {
        'location': plan.location,
        'price':  round(total_price),
        'description': plan.description,
        'plan_type': plan.plan_type
    }
    emit('service_response', plan_response)

@app.route('/')
def upload_csv_to_database():
    with open('serviceTrip/Tripplans.csv', 'r') as file:
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
    return "Upload Finished"


if __name__ == '__main__':
    socketio.run(app, port=5002)
