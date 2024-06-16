import mysql.connector
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configura la connessione al database MySQL
db_config = {
    'user': 'test0000',
    'password': 'gino',  # Sostituisci con la tua password
    'host': 'test0000.mysql.pythonanywhere-services.com',
    'database': 'test0000$flotta_testdb'
}

db = mysql.connector.connect(**db_config)

@app.route('/api/report_error', methods=['POST'])
def report_error():
    vehicle_id = request.form['vehicle_id']
    error_code = request.form['error_code']
    error_message = request.form['error_message']

    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO vehicle_errors (vehicle_id, error_code, error_message)
        VALUES (%s, %s, %s)
    """, (vehicle_id, error_code, error_message))
    db.commit()
    cursor.close()

    send_telegram_alert(vehicle_id, error_code, error_message)
    return "Error reported successfully", 200

def send_telegram_alert(vehicle_id, error_code, error_message):
    bot_token = 'YOUR_BOT_TOKEN'
    chat_id = 'YOUR_CHAT_ID'
    message = f"Error in vehicle {vehicle_id}: {error_code} - {error_message}"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message}
    requests.post(url, data=payload)

@app.route('/api/get_errors/<vehicle_id>', methods=['GET'])
def get_errors(vehicle_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT error_code, error_message, timestamp FROM vehicle_errors WHERE vehicle_id = %s ORDER BY timestamp DESC", (vehicle_id,))
    errors = cursor.fetchall()
    cursor.close()
    return jsonify(errors)

@app.route('/api/current_locations', methods=['GET'])
def get_current_locations():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT vehicle_id, latitude, longitude, MAX(timestamp) as last_seen FROM vehicle_locations GROUP BY vehicle_id")
    locations = cursor.fetchall()
    cursor.close()
    return jsonify(locations)

@app.route('/api/vehicle_history/<vehicle_id>', methods=['GET'])
def get_vehicle_history(vehicle_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT latitude, longitude, timestamp FROM vehicle_locations WHERE vehicle_id = %s ORDER BY timestamp", (vehicle_id,))
    history = cursor.fetchall()
    cursor.close()
    return jsonify(history)

if __name__ == "__main__":
    app.run()
