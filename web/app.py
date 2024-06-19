from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

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
    temp_acqua = float(request.form.get('temp_acqua', 0.0))
    pressione_olio = float(request.form.get('pressione_olio', 0.0))
    voltaggio_batteria = float(request.form.get('voltaggio_batteria', 0.0))
    contaore_motore = int(request.form.get('contaore_motore', 0))
    errori = request.form.getlist('errori')

    # Aggiornare la posizione attuale del veicolo
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
    
    # Aggiungere la posizione allo storico
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
    
    print(f"Ricevuta posizione per {vehicle_id}: {latitude}, {longitude}")
    return "Posizione aggiornata con successo", 200

# Endpoint per ottenere la posizione corrente dei veicoli
@app.route('/api/current_locations', methods=['GET'])
def get_current_locations():
    return jsonify([{'vehicle_id': vehicle_id, **data} for vehicle_id, data in current_positions.items()])

# Endpoint per ottenere lo storico delle posizioni di un veicolo specifico
@app.route('/api/vehicle_history/<vehicle_id>', methods=['GET'])
def get_vehicle_history(vehicle_id):
    return jsonify(vehicle_histories.get(vehicle_id, []))

# Funzione per generare grafici
def generate_chart(timestamps, values, title, ylabel):
    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, values, marker='o')
    plt.xlabel('Timestamp')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.grid(True)
    
    mean_value = np.mean(values)
    plt.axhline(y=mean_value, color='r', linestyle='--', label=f'Media: {mean_value:.2f}')
    plt.legend()
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    return graph_data

# Pagina principale per visualizzare le posizioni dei veicoli
@app.route('/')
def index():
    return render_template('index.html')

# Pagina di storico delle posizioni di un veicolo
@app.route('/vehicle_history/<vehicle_id>')
def vehicle_history(vehicle_id):
    if vehicle_id not in vehicle_histories:
        return "Veicolo non trovato", 404

    data = vehicle_histories[vehicle_id]
    timestamps = [entry['timestamp'] for entry in data]
    temp_acqua_data = [entry['temp_acqua'] for entry in data]
    pressione_olio_data = [entry['pressione_olio'] for entry in data]
    voltaggio_batteria_data = [entry['voltaggio_batteria'] for entry in data]
    contaore_motore_data = [entry['contaore_motore'] for entry in data]

    # Generare grafici per ciascun tipo di dato
    temp_acqua_chart = generate_chart(timestamps, temp_acqua_data, 'Temperatura Acqua', 'Gradi Celsius')
    pressione_olio_chart = generate_chart(timestamps, pressione_olio_data, 'Pressione Olio', 'Pascal')
    voltaggio_batteria_chart = generate_chart(timestamps, voltaggio_batteria_data, 'Voltaggio Batteria', 'Volt')
    contaore_motore_chart = generate_chart(timestamps, contaore_motore_data, 'Contaore Motore', 'Ore')

    return render_template(
        'vehicle_history.html',
        vehicle_id=vehicle_id,
        temp_acqua_chart=temp_acqua_chart,
        pressione_olio_chart=pressione_olio_chart,
        voltaggio_batteria_chart=voltaggio_batteria_chart,
        contaore_motore_chart=contaore_motore_chart,
        vehicle_history=data
    )

if __name__ == "__main__":
    app.run(debug=True)
