from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Endpoint per aggiornare la posizione del veicolo
@app.route('/api/update_location', methods=['POST'])
def update_location():
    vehicle_id = request.form['vehicle_id']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    # Per ora, stampiamo semplicemente i dati ricevuti
    print(f"Ricevuta posizione per {vehicle_id}: {latitude}, {longitude}")
    return "Posizione aggiornata con successo", 200

# Endpoint per segnalare un errore del veicolo
@app.route('/api/report_error', methods=['POST'])
def report_error():
    vehicle_id = request.form['vehicle_id']
    error_code = request.form['error_code']
    error_message = request.form['error_message']
    # Per ora, stampiamo semplicemente i dati ricevuti
    print(f"Ricevuto errore per {vehicle_id}: {error_code} - {error_message}")
    return "Errore segnalato con successo", 200

# Pagina principale per visualizzare le posizioni dei veicoli
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint per ottenere la posizione corrente dei veicoli
@app.route('/api/current_locations', methods=['GET'])
def get_current_locations():
    # Dati simulati per ora
    locations = [
        {'vehicle_id': 'VEH001', 'latitude': 41.9028, 'longitude': 12.4964, 'last_seen': '2023-06-15 14:00:00'},
        {'vehicle_id': 'VEH002', 'latitude': 45.4642, 'longitude': 9.1900, 'last_seen': '2023-06-15 14:05:00'},
    ]
    return jsonify(locations)

# Endpoint per ottenere lo storico delle posizioni di un veicolo
@app.route('/vehicle_history/<vehicle_id>')
def vehicle_history(vehicle_id):
    return render_template('vehicle_history.html', vehicle_id=vehicle_id)

# Endpoint per ottenere i dati storici del veicolo
@app.route('/api/vehicle_history/<vehicle_id>', methods=['GET'])
def get_vehicle_history(vehicle_id):
    # Dati simulati per ora
    history = [
        {'latitude': 41.9028, 'longitude': 12.4964, 'timestamp': '2023-06-15 13:00:00'},
        {'latitude': 41.9030, 'longitude': 12.4970, 'timestamp': '2023-06-15 13:10:00'},
    ]
    return jsonify(history)

if __name__ == "__main__":
    app.run(debug=True)
