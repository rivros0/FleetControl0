import matplotlib.pyplot as plt
from flask import Flask, render_template, jsonify
import io
import base64
import random
import time

app = Flask(__name__)

# Dati iniziali dei veicoli
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

# Funzione per generare i grafici
def generate_charts(vehicle_id):
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    charts = {
        'temp_acqua': axs[0, 0],
        'pressione_olio': axs[0, 1],
        'voltaggio_batteria': axs[1, 0],
        'contaore_motore': axs[1, 1]
    }

    for chart_name, ax in charts.items():
        ax.plot([entry[0] for entry in vehicle_data[vehicle_id][chart_name]],
                [entry[1] for entry in vehicle_data[vehicle_id][chart_name]])
        ax.set_title(chart_name.replace("_", " ").title())
        ax.set_xlabel('Timestamp')
        ax.set_ylabel('Value')

    # Convertire il grafico in un'immagine base64
    img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return img_base64

# Funzione per aggiornare i dati e generare i grafici
def update_data_and_charts():
    while True:
        # Simulazione di aggiornamento dati dai veicoli (da sostituire con dati reali)
        for vehicle_id in vehicle_data.keys():
            # Simulazione di dati casuali (sostituire con i dati reali provenienti dai veicoli)
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            temp_acqua = random.uniform(60, 100)
            pressione_olio = random.uniform(10, 100)
            voltaggio_batteria = random.uniform(11, 14)
            contaore_motore = random.randint(1000, 5000)
            errori = random.randint(0, 5)

            # Aggiornare i dati per il veicolo selezionato
            vehicle_data[vehicle_id]['temp_acqua'].append((timestamp, temp_acqua))
            vehicle_data[vehicle_id]['pressione_olio'].append((timestamp, pressione_olio))
            vehicle_data[vehicle_id]['voltaggio_batteria'].append((timestamp, voltaggio_batteria))
            vehicle_data[vehicle_id]['contaore_motore'].append((timestamp, contaore_motore))
            vehicle_data[vehicle_id]['errori'].append((timestamp, errori))

            # Mantieni solo gli ultimi 10 dati per ogni tipo
            for key in vehicle_data[vehicle_id].keys():
                vehicle_data[vehicle_id][key] = vehicle_data[vehicle_id][key][-10:]

            # Genera i grafici per il veicolo
            img_base64 = generate_charts(vehicle_id)
            vehicle_data[vehicle_id]['img_base64'] = img_base64

        time.sleep(5)

# Avvia il thread per aggiornare i dati e generare i grafici
import threading
update_thread = threading.Thread(target=update_data_and_charts)
update_thread.daemon = True
update_thread.start()

# Endpoint per visualizzare la pagina vehicle_history
@app.route('/vehicle_history/<vehicle_id>')
def vehicle_history(vehicle_id):
    return render_template('vehicle_history.html', vehicle_id=vehicle_id, vehicle_data=vehicle_data[vehicle_id])

if __name__ == "__main__":
    app.run(debug=True)
