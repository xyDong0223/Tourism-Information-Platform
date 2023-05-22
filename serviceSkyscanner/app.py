from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import socketio

app = Flask(__name__)
CORS(app)
socket = SocketIO(app, cors_allowed_origins='http://127.0.0.1:5005', async_mode='threading', transport='xhr-polling')

def calculate_quotation(start_date, end_date, city, travel_type):
    # Base prices for each city (replace with real prices)
    city_prices = {
        'Rome': 2000,
        'Paris': 2500,
        'Dublin': 1500
    }

    # Percentage adjustments for each travel type
    travel_type_adjustments = {
        'all inclusive': 1.0,  # 100%
        'semi inclusive': 0.9,  # 90%
        'only "transport and hotel': 0.6   # 60%
    }

    base_price = city_prices.get(city, 0)
    adjustment_factor = travel_type_adjustments.get(travel_type, 1)
    price = base_price * adjustment_factor

    description = f"{travel_type.capitalize()} trip to {city} from {start_date} to {end_date}."
    return {"location": city, "price": price, "description": description}


@socket.on('calculate_service')
def get_input(data):
    print(f"Received quotation request: {data}")
    start_date = data['start_date']
    end_date = data['end_date']
    city = data['city']
    travel_type = data['travel_type']
    quotation = calculate_quotation(start_date, end_date, city, travel_type)
    socket.emit('service_response', quotation)

if __name__ == '__main__':
    socket.run(app, port=5003)

