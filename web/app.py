from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Memorizzare le posizioni attuali in una struttura in memoria
current_positions = {}
vehicle_histories = {}

# Endpoint per aggiornare la posizione del veicolo
@app.route('/api/update_location', methods=['POST'])
def update_location():
    vehicle_id = request.form['vehicle_id']
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])
    timestamp = request.form['timestamp']
    temp_acqua = float(request.form['temp_acqua'])
    pressione_olio = float(request.form['pressione_olio'])
    voltaggio_batteria = float(request.form['voltaggio_batteria'])
    contaore_motore = int(request.form['contaore_motore'])
    errori = request.form.getlist('errori')

    # Aggiornare la posizione attuale del veicolo con i nuovi dati
    current_positions[vehicle_id] = {
        'latitude': latitude,
        'longitude': longitude,
        'last_seen': timestamp,
        'temp_acqua': temp_acqua,
        'pressione_olio': pressione_olio,
        'voltaggio_batteria': voltaggio_batteria,
        'contaore_motore': contaore_motore,
        'errori': errori
    }

    # Aggiungere la posizione allo storico con i nuovi dati
    if vehicle_id not in vehicle_histories:
        vehicle_histories[vehicle_id] = []
    vehicle_histories[vehicle_id].append({
        'latitude': latitude,
        'longitude': longitude,
        'timestamp': timestamp,
        'temp_acqua': temp_acqua,
        'pressione_olio': pressione_olio,
        'voltaggio_batteria': voltaggio_batteria,
        'contaore_motore': contaore_motore,
        'errori': errori
    })

    print(f"Dati ricevuti per {vehicle_id}: {latitude}, {longitude}, temp_acqua: {temp_acqua}, pressione_olio: {pressione_olio}, voltaggio_batteria: {voltaggio_batteria}, contaore_motore: {contaore_motore}, errori: {errori}")
    return "Dati aggiornati con successo", 200

# Endpoint per ottenere la posizione corrente dei veicoli
@app.route('/api/current_locations', methods=['GET'])
def get_current_locations():
    return jsonify([{'vehicle_id': vehicle_id, **data} for vehicle_id, data in current_positions.items()])

# Endpoint per ottenere lo storico delle posizioni di un veicolo specifico
@app.route('/api/vehicle_history/<vehicle_id>', methods=['GET'])
def get_vehicle_history(vehicle_id):
    return jsonify(vehicle_histories.get(vehicle_id, []))

# Pagina principale per visualizzare le posizioni dei veicoli
@app.route('/')
def index():
    return render_template('index.html')

# Pagina di storico delle posizioni di un veicolo
@app.route('/vehicle_history/<vehicle_id>')
def vehicle_history(vehicle_id):
    return render_template('vehicle_history.html', vehicle_id=vehicle_id)

if __name__ == "__main__":
    app.run(debug=True)
