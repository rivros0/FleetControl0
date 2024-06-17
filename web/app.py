from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Memorizzare le posizioni attuali in una struttura in memoria
current_positions = {}

# Endpoint per aggiornare la posizione del veicolo
@app.route('/api/update_location', methods=['POST'])
def update_location():
    vehicle_id = request.form['vehicle_id']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    timestamp = request.form['timestamp']
    
    # Aggiornare la posizione attuale del veicolo
    current_positions[vehicle_id] = {
        'latitude': latitude,
        'longitude': longitude,
        'last_seen': timestamp
    }
    
    print(f"Ricevuta posizione per {vehicle_id}: {latitude}, {longitude}")
    return "Posizione aggiornata con successo", 200

# Endpoint per ottenere la posizione corrente dei veicoli
@app.route('/api/current_locations', methods=['GET'])
def get_current_locations():
    return jsonify([{'vehicle_id': vehicle_id, **data} for vehicle_id, data in current_positions.items()])

# Pagina principale per visualizzare le posizioni dei veicoli
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint per ottenere lo storico delle posizioni di un veicolo
@app.route('/vehicle_history/<vehicle_id>')
def vehicle_history(vehicle_id):
    return render_template('vehicle_history.html', vehicle_id=vehicle_id)

if __name__ == "__main__":
    app.run(debug=True)
