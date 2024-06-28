from flask import Flask, render_template, request, jsonify
import json
import os
import matplotlib.pyplot as plt

app = Flask(__name__)

DATA_FILE = 'data/vehicle_data.json'

# Ensure the data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Initialize the data file if it does not exist
if not os.path.isfile(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

# Load data from the JSON file
def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Save data to the JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Endpoint to get current vehicle locations
@app.route('/api/current_locations')
def current_locations():
    data = load_data()
    latest_locations = {d['vehicle_id']: d for d in sorted(data, key=lambda x: x['timestamp'], reverse=True)}
    return jsonify(list(latest_locations.values()))

# Endpoint to update vehicle location
@app.route('/api/update_location', methods=['POST'])
def update_location():
    data = request.json
    vehicle_id = data['vehicle_id']
    latitude = float(data['latitude'])
    longitude = float(data['longitude'])
    timestamp = data['timestamp']
    temp_acqua = float(data['temp_acqua'])
    pressione_olio = float(data['pressione_olio'])
    voltaggio_batteria = float(data['voltaggio_batteria'])
    contaore_motore = float(data['contaore_motore'])
    errori = data['errori']

    new_data = {
        'vehicle_id': vehicle_id,
        'latitude': latitude,
        'longitude': longitude,
        'timestamp': timestamp,
        'temp_acqua': temp_acqua,
        'pressione_olio': pressione_olio,
        'voltaggio_batteria': voltaggio_batteria,
        'contaore_motore': contaore_motore,
        'errori': errori
    }

    data = load_data()
    data.append(new_data)
    save_data(data)

    return jsonify({'message': 'Position Updated'}), 200

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Function to create charts
def create_charts(vehicle_id):
    data = load_data()
    vehicle_data = [d for d in data if d['vehicle_id'] == vehicle_id]
    timestamps = [d['timestamp'] for d in vehicle_data]
    temp_acqua = [d['temp_acqua'] for d in vehicle_data]
    pressione_olio = [d['pressione_olio'] for d in vehicle_data]
    voltaggio_batteria = [d['voltaggio_batteria'] for d in vehicle_data]
    contaore_motore = [d['contaore_motore'] for d in vehicle_data]

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, temp_acqua, label='Temperatura Acqua')
    plt.xlabel('Timestamp')
    plt.ylabel('Temperatura Acqua')
    plt.title('Temperatura Acqua nel tempo')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/temp_acqua_chart.png')
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, pressione_olio, label='Pressione Olio')
    plt.xlabel('Timestamp')
    plt.ylabel('Pressione Olio')
    plt.title('Pressione Olio nel tempo')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/pressione_olio_chart.png')
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, voltaggio_batteria, label='Voltaggio Batteria')
    plt.xlabel('Timestamp')
    plt.ylabel('Voltaggio Batteria')
    plt.title('Voltaggio Batteria nel tempo')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/voltaggio_batteria_chart.png')
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, contaore_motore, label='Contaore Motore')
    plt.xlabel('Timestamp')
    plt.ylabel('Contaore Motore')
    plt.title('Contaore Motore nel tempo')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/contaore_motore_chart.png')
    plt.close()

# Vehicle history page
@app.route('/vehicle_history/<vehicle_id>')
def vehicle_history(vehicle_id):
    create_charts(vehicle_id)
    data = load_data()
    vehicle_data = [d for d in data if d['vehicle_id'] == vehicle_id]
    return render_template('vehicle_history.html', vehicle_id=vehicle_id, vehicle_data=vehicle_data)

#suca

if __name__ == '__main__':
    app.run(debug=True)
