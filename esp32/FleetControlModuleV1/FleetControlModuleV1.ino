#include <WiFi.h>
#include <HTTPClient.h>
#include <TinyGPS++.h>

// Configurazione WiFi
const char* ssid = "ninophone";
const char* password = "sapusapunette";

// Configurazione server
const char* serverName = "http://test0000.pythonanywhere.com/api/update_location";

// Configurazione veicolo
const char* vehicle_id = "TestVolante";

// Configurazione GPS
TinyGPSPlus gps;
HardwareSerial gpsSerial(1);

unsigned long previousMillis = 0; // Variabile per memorizzare il tempo precedente
const long interval = 5000; // Intervallo di 5 secondi

void setup() {
  Serial.begin(115200);
  gpsSerial.begin(9600, SERIAL_8N1, 16, 17); // RX=16, TX=17

  // Connessione al Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  // Leggi i dati dal GPS
  while (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
  }

  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    // Variabile per accumulare i messaggi del monitor seriale
    String serialOutput = "";

    // Stampa lo stato del GPS e le coordinate attuali ogni 5 secondi
    if (gps.location.isValid()) {
      String latitudeStr = String(gps.location.lat(), 6);
      String longitudeStr = String(gps.location.lng(), 6);
      serialOutput += "Latitude: " + latitudeStr + "\n";
      serialOutput += "Longitude: " + longitudeStr + "\n";
      Serial.print("Latitude: ");
      Serial.println(latitudeStr);
      Serial.print("Longitude: ");
      Serial.println(longitudeStr);
    } else {
      serialOutput += "GPS location not valid.\n";
      Serial.println("GPS location not valid.");
    }

    if (gps.time.isValid()) {
      String timeStr = String(gps.time.hour()) + ":" + String(gps.time.minute()) + ":" + String(gps.time.second());
      serialOutput += "Time: " + timeStr + "\n";
      Serial.print("Time: ");
      Serial.println(timeStr);
    } else {
      serialOutput += "GPS time not valid.\n";
      Serial.println("GPS time not valid.");
    }

    if (gps.date.isValid()) {
      String dateStr = String(gps.date.day()) + "/" + String(gps.date.month()) + "/" + String(gps.date.year());
      serialOutput += "Date: " + dateStr + "\n";
      Serial.print("Date: ");
      Serial.println(dateStr);
    } else {
      serialOutput += "GPS date not valid.\n";
      Serial.println("GPS date not valid.");
    }

    // Invio dei dati al server
    sendGPSToServer(serialOutput);
  }
}

// Funzione per inviare la richiesta POST
void sendGPSToServer(String serialOutput) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin(serverName);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    // Dati da inviare (sostituire con valori reali)
    float latitude = gps.location.lat();
    float longitude = gps.location.lng();
    unsigned long timestamp = gps.time.value(); // Formato misto, potrebbe dover essere riformattato
    float temp_acqua = 25.0; // esempio
    float pressione_olio = 3.5; // esempio
    float voltaggio_batteria = 12.6; // esempio
    unsigned long contaore_motore = 1200; // esempio
    int errori = 0; // esempio

    String postData = "vehicle_id=" + String(vehicle_id) +
                      "&latitude=" + String(latitude, 6) +
                      "&longitude=" + String(longitude, 6) +
                      "&timestamp=" + String(timestamp) +
                      "&temp_acqua=" + String(temp_acqua, 2) +
                      "&pressione_olio=" + String(pressione_olio, 2) +
                      "&voltaggio_batteria=" + String(voltaggio_batteria, 2) +
                      "&contaore_motore=" + String(contaore_motore) +
                      "&errori=" + String(errori) +
                      "&serial_output=" + serialOutput;

    Serial.println("Sending data:");
    Serial.println(postData); // Stampa i dati per il debug

    int httpResponseCode = http.POST(postData);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("HTTP Response code: " + String(httpResponseCode));
      Serial.println("Server response: " + response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("WiFi Disconnected");
  }
}
