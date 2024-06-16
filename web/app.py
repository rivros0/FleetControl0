from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

LOCATIONS_FILE = os.path.join(DATA_DIR, 'locations.json')
ERRORS_FILE = os.path.join(DATA_DIR, 'errors.json')

def read_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return []

def write_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/api/update_location', methods=['POST'])
def update_location():
    vehicle_id = request.form['vehicle_id']
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])
    timestamp = request.form.get('timestamp', 'unknown')

    locations = read_data(LOCATIONS_FILE)
    locations.append({'vehicle_id': vehicle_id, 'latitude': latitude, 'longitude': longitude, 'timestamp': timestamp})
    write_data(LOCATIONS_FILE, locations)
    return "Location updated successfully", 200

@app.route('/api/report_error', methods=['POST'])
def report_error():
    vehicle_id = request.form['vehicle_id']
    error_code = request.form['error_code']
    error_message = request.form['error_message']
    timestamp = request.form.get('timestamp', 'unknown')

    errors = read_data(ERRORS_FILE)
    errors.append({'vehicle_id': vehicle_id, 'error_code': error_code, 'error_message': error_message, 'timestamp': timestamp})
    write_data(ERRORS_FILE, errors)
    return "Error reported successfully", 200

@app.route('/api/current_locations', methods=['GET'])
def get_current_locations():
    locations = read_data(LOCATIONS_FILE)
    return jsonify(locations)

@app.route('/api/get_errors/<vehicle_id>', methods=['GET'])
def get_errors(vehicle_id):
    errors = read_data(ERRORS_FILE)
    vehicle_errors = [error for error in errors if error['vehicle_id'] == vehicle_id]
    return jsonify(vehicle_errors)

@app.route('/api/vehicle_history/<vehicle_id>', methods=['GET'])
def get_vehicle_history(vehicle_id):
    locations = read_data(LOCATIONS_FILE)
    vehicle_locations = [location for 
