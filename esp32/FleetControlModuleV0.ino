#include <WiFi.h>
#include <HTTPClient.h>
#include <TinyGPS++.h>
#include <SoftwareSerial.h>

// Configurazione WiFi
const char* ssid = "ninophone ";
const char* password = "sapusapunette";

// Configurazione server
const char* serverName = "http://test0000.pythonanywhere.com/api/update_location";

// Configurazione veicolo
const char* vehicle_id = "TestVolante";

// Configurazione GPS
TinyGPSPlus gps;
SoftwareSerial ss(16, 17); // RX, TX

void setup() {
  Serial.begin(115200);
  ss.begin(9600);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  if (WiFi.status() == WL_CONNECTED) {
    // Send initial data to the server after connecting to WiFi
    sendGPSToServer();
  }
}

void loop() {
  while (ss.available() > 0) {
    if (gps.encode(ss.read())) {
      if (gps.location.isUpdated()) {
        sendGPSToServer();
      }
    }
  }
}

// Funzione per inviare la richiesta POST
void sendGPSToServer() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    // Dati da inviare (sostituire con valori reali)
    float latitude = gps.location.lat();
    float longitude = gps.location.lng();
    unsigned long timestamp = gps.time.value(); // Formato misto, potrebbe dover essere riformattato
    float temp_acqua = 25.0; // esempio
    float pressione_olio = 3.5; // esempio
    float voltaggio_batteria = 12.6; // esempio
    unsigned long contaore_motore = 1200; // esempio
    int errori = 0; // esempio

    String postData = "{\"vehicle_id\":\"" + String(vehicle_id) + "\",\"latitude\":" + String(latitude, 6) + ",\"longitude\":" + String(longitude, 6) +
                      ",\"timestamp\":" + String(timestamp) + ",\"temp_acqua\":" +     String(temp_acqua, 2) + ",\"pressione_olio\":" + String(pressione_olio, 2) + ",\"voltaggio_batteria\":" + String(voltaggio_batteria, 2) +
                      ",\"contaore_motore\":" + String(contaore_motore) + ",\"errori\":" + String(errori) + "}";

    int httpResponseCode = http.POST(postData);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("WiFi Disconnected");
  }
}

