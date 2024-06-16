import time
import requests
import random

# Configurazione del server
server_url = "http://localhost:5000"  # Modifica con l'URL del tuo server se necessario

# Identificativo del veicolo
vehicle_id = "VEH001"

# Funzione per generare coordinate casuali in una certa area
def generate_random_coordinates():
    # Ad esempio, coordinate intorno a Roma
    latitude = 41.9028 + random.uniform(-0.1, 0.1)
    longitude = 12.4964 + random.uniform(-0.1, 0.1)
    return latitude, longitude

# Funzione per inviare la posizione attuale del veicolo al server
def send_location():
    latitude, longitude = generate_random_coordinates()
    data = {
        'vehicle_id': vehicle_id,
        'latitude': latitude,
        'longitude': longitude
    }
    response = requests.post(f"{server_url}/api/update_location", data=data)
    if response.status_code == 200:
        print(f"Posizione inviata: {latitude}, {longitude}")
    else:
        print("Errore nell'invio della posizione")

# Funzione per generare un errore casuale del veicolo
def generate_random_error():
    error_codes = [
        ('P0171', 'System Too Lean'),
        ('P0300', 'Random/Multiple Cylinder Misfire Detected'),
        ('P0420', 'Catalyst System Efficiency Below Threshold'),
        ('P0455', 'Evaporative Emission System Leak Detected'),
        ('P0133', 'Oxygen Sensor Circuit Slow Response')
    ]
    return random.choice(error_codes)

# Funzione per inviare un errore del veicolo al server
def send_error():
    error_code, error_message = generate_random_error()
    data = {
        'vehicle_id': vehicle_id,
        'error_code': error_code,
        'error_message': error_message
    }
    response = requests.post(f"{server_url}/api/report_error", data=data)
    if response.status_code == 200:
        print(f"Errore inviato: {error_code} - {error_message}")
    else:
        print("Errore nell'invio dell'errore")

# Simulazione continua
while True:
    send_location()
    if random.random() < 0.1:  # 10% di probabilità di inviare un errore
        send_error()
    time.sleep(5)  # Attendi 5 secondi prima di inviare la prossima posizione
