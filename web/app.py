from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from collections import deque

app = Flask(__name__)

# Memorizzare le posizioni attuali in una struttura in memoria
current_positions = {}
vehicle_histories = {}

# Massimo numero di punti storici da mantenere per ciascun veicolo
MAX_HISTORY_POINTS = 100

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
        vehicle_histories[vehicle_id] = deque(maxlen=MAX_HISTORY_POINTS)
    vehicle_histories[vehicle_id].appendleft({
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

# Funzione per generare i grafici
def generate_charts(vehicle_id):
    data = list(vehicle_histories.get(vehicle_id, []))

    if not data:
        return None, None, None, None

    timestamps = [entry['timestamp'] for entry in data]
    temp_acqua_values = [entry['temp_acqua'] for entry in data]
    pressione_olio_values = [entry['pressione_olio'] for entry in data]
    voltaggio_batteria_values = [entry['voltaggio_batteria'] for entry in data]
    contaore_motore_values = [entry['contaore_motore'] for entry in data]

    # Grafico per la temperatura dell'acqua
    temp_acqua_chart = generate_chart(timestamps, temp_acqua_values, 'Temperatura Acqua')

    # Grafico per la pressione dell'olio
    pressione_olio_chart = generate_chart(timestamps, pressione_olio_values, 'Pressione Olio')

    # Grafico per il voltaggio della batteria
    voltaggio_batteria_chart = generate_chart(timestamps, voltaggio_batteria_values, 'Voltaggio Batteria')

    # Grafico per il contaore del motore
    contaore_motore_chart = generate_chart(timestamps, contaore_motore_values, 'Contaore Motore')

    return temp_acqua_chart, pressione_olio_chart, voltaggio_batteria_chart, contaore_motore_chart

def generate_chart(x_values, y_values, title):
    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values, marker='o', linestyle='-', color='b')
    plt.title(title)
    plt.xlabel('Timestamp')
    plt.ylabel('Valore')
    plt.xticks(rotation=45)
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

# Pagina di storico delle posizioni di un veicolo
@app.route('/vehicle_history/<vehicle_id>')
def vehicle_history(vehicle_id):
    temp_acqua_chart, pressione_olio_chart, voltaggio_batteria_chart, contaore_motore_chart = generate_charts(vehicle_id)
    vehicle_history_data = list(vehicle_histories.get(vehicle_id, []))
    vehicle_history_data.reverse()  # Inverti l'ordine dei record storici per visualizzare l'ultimo per primo
    return render_template('vehicle_history.html', vehicle_id=vehicle_id, vehicle_history=vehicle_history_data,
                           temp_acqua_chart=temp_acqua_chart, pressione_olio_chart=pressione_olio_chart,
                           voltaggio_batteria_chart=voltaggio_batteria_chart, contaore_motore_chart=contaore_motore_chart)

if __name__ == "__main__":
    app.run(debug=True)
