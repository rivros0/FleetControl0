from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import datetime
from pytz import timezone
from OBDerrors import error_codes  # Importa il dizionario degli errori

app = Flask(__name__)

# Memorizzare le posizioni attuali in una struttura in memoria
current_positions = {}
vehicle_histories = {}

# Funzione per convertire timestamp in fuso orario di Roma
def convert_to_rome_timezone(timestamp):
    utc_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    utc_time = utc_time.replace(tzinfo=timezone('UTC'))
    rome_time = utc_time.astimezone(timezone('Europe/Rome'))
    return rome_time.strftime('%Y-%m-%d %H:%M:%S')

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
    timestamps = [convert_to_rome_timezone(entry['timestamp']) for entry in data]
    temp_acqua_data = [entry['temp_acqua'] for entry in data]
    pressione_olio_data = [entry['pressione_olio'] for entry in data]
    voltaggio_batteria_data = [entry['voltaggio_batteria'] for entry in data]
    contaore_motore_data = [entry['contaore_motore'] for entry in data]
    errori_data = [entry['errori'] for entry in data]

    # Creazione dei quattro grafici con Matplotlib
    fig, axs = plt.subplots(4, 1, figsize=(12, 16))

    axs[0].plot(timestamps, temp_acqua_data, marker='o', label='Temperatura Acqua', color='blue')
    axs[0].set_ylabel('Temperatura Acqua')
    axs[0].set_title(f'Statistiche per il veicolo {vehicle_id}')
    axs[0].grid(True)
    axs[0].legend()

    axs[1].plot(timestamps, pressione_olio_data, marker='o', label='Pressione Olio', color='green')
    axs[1].set_ylabel('Pressione Olio')
    axs[1].grid(True)
    axs[1].legend()

    axs[2].plot(timestamps, voltaggio_batteria_data, marker='o', label='Voltaggio Batteria', color='orange')
    axs[2].set_ylabel('Voltaggio Batteria')
    axs[2].grid(True)
    axs[2].legend()

    axs[3].plot(timestamps, contaore_motore_data, marker='o', label='Contaore Motore', color='red')
    axs[3].set_ylabel('Contaore Motore')
    axs[3].set_xlabel('Timestamp')
    axs[3].grid(True)
    axs[3].legend()

    plt.tight_layout()

    # Salvataggio dei grafici in formato base64 per l'inclusione nella pagina HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()

    # Prepara le informazioni sugli errori per visualizzazione
    error_descriptions = []
    for errors in errori_data:
        for error in errors:
            if error in error_codes:
                error_info = error_codes[error]
                error_description = f"{error_info['category']} - {error_info['name']}: {error_info['description']}"
                error_descriptions.append(error_description)

    return render_template('vehicle_history.html', vehicle_id=vehicle_id, graph_data=graph_data, error_descriptions=error_descriptions)

# Pagina di dettaglio di un errore
@app.route('/error_detail/<error_code>')
def error_detail(error_code):
    # Trova l'errore con il codice specificato
    error_info = error_codes.get(error_code)
    if error_info:
        return render_template('error_detail.html', error=error_info)
    else:
        return "Errore non trovato", 404

if __name__ == "__main__":
    app.run(debug=True)

