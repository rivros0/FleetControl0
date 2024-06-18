from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
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
    contaore_motore = float(request.form.get('contaore_motore', 0.0))
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

# Pagina principale per visualizzare le posizioni dei veicoli
@app.route('/')
def index():
    return render_template('index.html')

# Pagina di storico delle posizioni di un veicolo
@app.route('/vehicle_history/<vehicle_id>')
def vehicle_history(vehicle_id):
    return render_template('vehicle_history.html', vehicle_id=vehicle_id)

# Funzione per generare grafici
def generate_graphs(data):
    timestamps = [point['timestamp'] for point in data]
    temp_acqua = [point['temp_acqua'] for point in data]
    pressione_olio = [point['pressione_olio'] for point in data]
    voltaggio_batteria = [point['voltaggio_batteria'] for point in data]
    contaore_motore = [point['contaore_motore'] for point in data]

    fig, axs = plt.subplots(4, 1, figsize=(8, 12))

    axs[0].plot(timestamps, temp_acqua, marker='o', linestyle='-')
    axs[0].set_title('Temperatura Acqua')
    axs[0].set_ylabel('Temperatura (°C)')
    axs[0].grid(True)

    axs[1].plot(timestamps, pressione_olio, marker='o', linestyle='-')
    axs[1].set_title('Pressione Olio')
    axs[1].set_ylabel('Pressione (psi)')
    axs[1].grid(True)

    axs[2].plot(timestamps, voltaggio_batteria, marker='o', linestyle='-')
    axs[2].set_title('Voltaggio Batteria')
    axs[2].set_ylabel('Voltaggio (V)')
    axs[2].grid(True)

    axs[3].plot(timestamps, contaore_motore, marker='o', linestyle='-')
    axs[3].set_title('Contaore Motore')
    axs[3].set_ylabel('Contatore')
    axs[3].grid(True)

    plt.tight_layout()
    
    # Salvataggio del grafico in formato base64 per l'integrazione in HTML
    img_stream = BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    img_base64 = base64.b64encode(img_stream.read()).decode('utf-8')
    plt.close()

    return img_base64

if __name__ == "__main__":
    app.run(debug=True)
