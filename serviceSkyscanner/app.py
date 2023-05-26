from serviceSkyscanner.ext import db
import csv
from serviceSkyscanner import setting
from datetime import datetime
from serviceSkyscanner.models import Plans
from flask_migrate import Migrate
from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(setting.DevelopmentConfig)
CORS(app)
socket = SocketIO(app, cors_allowed_origins='http://127.0.0.1:5005', async_mode='threading', transport='xhr-polling')

db.init_app(app)
with app.app_context():
    db.create_all()
Migrate(app=app, db=db)


def calculate_quotation(start_date, end_date, city, plan_type, promo_code):
    # Base prices for each city (replace with real prices)
    plan = Plans.query.filter_by(location=city, plan_type=plan_type).first()


    # Convert string dates to datetime objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Calculate the number of days for the trip
    num_days = (end_date - start_date).days
    base_price = plan.price
    price = base_price * num_days
    promo_validation = 0

    if promo_code == '':
        promo_validation = -1
    elif promo_code == 'MEMBERSHIP':
        promo_validation = 1
        price *= 0.95

    print(promo_validation)



    description = f"{plan_type.capitalize()} trip to {city} from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}."
    return {"location": city, "price": price, "description": plan.description, "promo_validation": promo_validation}


@socket.on('calculate_service')
def get_input(data):
    print(f"Received quotation request: {data}")
    start_date = data['start_date']
    end_date = data['end_date']
    city = data['city']
    plan_type = data['travel_type']
    promo_code = data['promo'].upper()
    quotation = calculate_quotation(start_date, end_date, city, plan_type, promo_code)
    socket.emit('service_response', quotation)


@app.route('/')
def upload_csv_to_database():
    try:
        plans_list = []
        with open('serviceSkyscanner/Skyplans.csv', 'r') as file:
            csv_data = csv.reader(file)
            next(csv_data)  # Skip the header row
            for row in csv_data:
                location = row[0]
                price = float(row[1])
                description = row[2]
                plan_type = row[3]

                # Create a new Plans object and assign the values from the CSV row
                plan = Plans(location=location, price=price, description=description, plan_type=plan_type)
                plans_list.append(plan)

        if plans_list:
            # Add all objects to the session at once and commit the transaction
            db.session.bulk_save_objects(plans_list)
            db.session.commit()

        return "Data uploaded successfully."

    except FileNotFoundError:
        return "The file 'Skyplans.csv' does not exist."

    except Exception as e:
        # Log the error message for debugging purposes
        app.logger.error(str(e))
        return "An error occurred while processing the data."



if __name__ == '__main__':
    socket.run(app, port=5003, allow_unsafe_werkzeug=True)
