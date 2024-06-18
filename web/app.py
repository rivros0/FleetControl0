from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Memorizzare le posizioni attuali in una struttura in memoria
current_positions = {}
vehicle_histories = {}

# Aggiornamento della posizione del veicolo
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
    errori = request.form.get('errori', '').split(',')

    # Aggiornamento della posizione attuale del veicolo
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

    # Generazione dei grafici
    generate_charts(vehicle_id)

    return "Posizione aggiornata con successo", 200

# Funzione per generare i grafici
def generate_charts(vehicle_id):
    data = vehicle_histories.get(vehicle_id, [])

    if not data:
        return

    timestamps = [entry['timestamp'] for entry in data]
    temp_acqua_values = [entry['temp_acqua'] for entry in data]
    pressione_olio_values = [entry['pressione_olio'] for entry in data]
    voltaggio_batteria_values = [entry['voltaggio_batteria'] for entry in data]
    contaore_motore_values = [entry['contaore_motore'] for entry in data]

    # Grafico per la temperatura dell'acqua
    plt.figure(figsize=(8, 6))
    plt.plot(timestamps, temp_acqua_values, marker='o', linestyle='-', color='b', label='Temperatura Acqua')
    plt.title(f"Temperatura Acqua - Veicolo {vehicle_id}")
    plt.xlabel('Timestamp')
    plt.ylabel('Temperatura')
    plt.xticks(rotation=45)
    plt.legend()
    temp_acqua_chart = get_chart_image()

    # Grafico per la pressione dell'olio
    plt.figure(figsize=(8, 6))
    plt.plot(timestamps, pressione_olio_values, marker='o', linestyle='-', color='g', label='Pressione Olio')
    plt.title(f"Pressione Olio - Veicolo {vehicle_id}")
    plt.xlabel('Timestamp')
    plt.ylabel('Pressione')
    plt.xticks(rotation=45)
    plt.legend()
    pressione_olio_chart = get_chart_image()

    # Grafico per il voltaggio della batteria
    plt.figure(figsize=(8, 6))
    plt.plot(timestamps, voltaggio_batteria_values, marker='o', linestyle='-', color='r', label='Voltaggio Batteria')
    plt.title(f"Voltaggio Batteria - Veicolo {vehicle_id}")
    plt.xlabel('Timestamp')
    plt.ylabel('Voltaggio')
    plt.xticks(rotation=45)
    plt.legend()
    voltaggio_batteria_chart = get_chart_image()

    # Grafico per il contaore del motore
    plt.figure(figsize=(8, 6))
    plt.plot(timestamps, contaore_motore_values, marker='o', linestyle='-', color='purple', label='Contaore Motore')
    plt.title(f"Contaore Motore - Veicolo {vehicle_id}")
    plt.xlabel('Timestamp')
    plt.ylabel('Contaore')
    plt.xticks(rotation=45)
    plt.legend()
    contaore_motore_chart = get_chart_image()

    # Salvataggio dei grafici come immagini
    save_charts(vehicle_id, temp_acqua_chart, pressione_olio_chart, voltaggio_batteria_chart, contaore_motore_chart)

def get_chart_image():
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

def save_charts(vehicle_id, temp_acqua_chart, pressione_olio_chart, voltaggio_batteria_chart, contaore_motore_chart):
    # Salvataggio delle immagini dei grafici
    # Qui potresti implementare il salvataggio delle immagini su disco o su un sistema di archiviazione
    # Per questa implementazione, stiamo utilizzando la generazione di immagini temporanee
    pass

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
    generate_charts(vehicle_id)  # Genera i grafici all'accesso alla pagina
    return render_template('vehicle_history.html', vehicle_id=vehicle_id)

if __name__ == "__main__":
    app.run(debug=True)
