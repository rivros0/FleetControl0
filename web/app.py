from flask import Flask, render_template, request, jsonify
from datetime import datetime
from OBDerrors import error_codes  # Importa il dizionario degli errori

app = Flask(__name__)

# Memorizza lo storico degli errori in una struttura in memoria
error_history = {}

# Funzione per aggiungere un errore allo storico
def add_error_to_history(error_code, timestamp):
    if error_code not in error_history:
        error_history[error_code] = []
    error_history[error_code].append(timestamp)

# Endpoint per aggiungere un errore
@app.route('/api/add_error', methods=['POST'])
def add_error():
    error_code = request.form['error_code']
    timestamp = request.form['timestamp']

    add_error_to_history(error_code, timestamp)
    
    return "Errore aggiunto con successo", 200

# Endpoint per ottenere i dettagli di un errore specifico
@app.route('/error_detail/<error_code>', methods=['GET'])
def error_detail(error_code):
    if error_code not in error_codes:
        return "Codice errore non trovato", 404

    if error_code not in error_history or len(error_history[error_code]) == 0:
        timestamps = []
    else:
        timestamps = error_history[error_code]

    error_info = error_codes[error_code]

    return render_template('error_detail.html', error_code=error_code, error_info=error_info, timestamps=timestamps)

if __name__ == '__main__':
    app.run(debug=True)
