import matplotlib.pyplot as plt
from flask import Flask, render_template, jsonify, request
import io
import base64
import threading

app = Flask(__name__)

# Dati di posizione dei veicoli e storico
current_positions = {}
vehicle_histories = {}
vehicle_data = {
    'VEHICLE001': {
        'temp_acqua': [],
        'pressione_olio': [],
        'voltaggio_batteria': [],
        'contaore_motore': [],
        'errori': []
    },
    'VEHICLE002': {
        'temp_acqua': [],
        'pressione_olio': [],
        'voltaggio_batteria': [],
        'contaore_motore': [],
        'errori': []
    },
    'VEHICLE003': {
        'temp_acqua': [],
        'pressione_olio': [],
        'voltaggio_batteria': [],
        'contaore_motore': [],
        'errori': []
    }
}

# Funzione per formattare la data nel formato desiderato
def format_date(date_str):
    return date_str.split('.')[0].replace('T', ' ')

# Endpoint per aggiornare la posizione del veicolo
@app.route('/api/update_location', methods=['POST'])
def update_location():
    vehicle_id = request.form['vehicle_id']
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])
    timestamp = format_date(request.form['timestamp'])
    
    # Aggiornare la posizione attuale del veicolo
    current_positions[vehicle_id] = {
        'latitude': latitude,
        'longitude': longitude,
        'last_seen': timestamp
    }
    
    # Aggiungere la posizione allo storico
    if vehicle_id not in vehicle_histories:
        vehicle_histories[vehicle_id] = []
    vehicle_histories[vehicle_id].append({
        'latitude': latitude,
        'longitude': longitude,
        'timestamp': timestamp
    })
    
    # Aggiornare i dati relativi ai veicoli
    if vehicle_id in vehicle_data:
        vehicle_data[vehicle_id]['temp_acqua'].append((timestamp, random.uniform(60, 100)))
        vehicle_data[vehicle_id]['pressione_olio'].append((timestamp, random.uniform(10, 100)))
        vehicle_data[vehicle_id]['voltaggio_batteria'].append((timestamp, random.uniform(11, 14)))
        vehicle_data[vehicle_id]['contaore_motore'].append((timestamp, random.randint(1000, 5000)))
        vehicle_data[vehicle_id]['errori'].append((timestamp, random.randint(0, 5)))
    
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
def generate_chart(data, title, ylabel):
    fig, ax = plt.subplots()
    timestamps = [entry[0] for entry in data]
    values = [entry[1] for entry in data]
    ax.plot(timestamps, values)
    ax.set_title(title)
    ax.set_xlabel('Timestamp')
    ax.set_ylabel(ylabel)
    ax.grid(True)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close(fig)
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

# Pagina principale per visualizzare le posizioni dei veicoli
@app.route('/')
def index():
    return render_template('index.html')

# Pagina di storico delle posizioni di un veicolo
@app.route('/vehicle_history/<vehicle_id>')
def vehicle_history(vehicle_id):
    if vehicle_id not in vehicle_data:
        return "Veicolo non trovato", 404
    
    temp_acqua_chart = generate_chart(vehicle_data[vehicle_id]['temp_acqua'], 'Temperatura Acqua', 'Gradi Celsius')
    pressione_olio_chart = generate_chart(vehicle_data[vehicle_id]['pressione_olio'], 'Pressione Olio', 'Pascal')
    voltaggio_batteria_chart = generate_chart(vehicle_data[vehicle_id]['voltaggio_batteria'], 'Voltaggio Batteria', 'Volt')
    contaore_motore_chart = generate_chart(vehicle_data[vehicle_id]['contaore_motore'], 'Contaore Motore', 'Ore')

    return render_template(
        'vehicle_history.html',
        vehicle_id=vehicle_id,
        temp_acqua_chart=temp_acqua_chart,
        pressione_olio_chart=pressione_olio_chart,
        voltaggio_batteria_chart=voltaggio_batteria_chart,
        contaore_motore_chart=contaore_motore_chart,
        vehicle_history=vehicle_histories.get(vehicle_id, [])
    )

if __name__ == "__main__":
    app.run(debug=True)
