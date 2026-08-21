#include <ESP32Servo.h>
#include <cmath>
#include <WiFi.h>
#include <HTTPClient.h> 

// Constantes para millis()
unsigned long previoMillis = 0;
const long intervalo = 2000; 

// Credenciales para conectarte al Wi-Fi
const char* ssid = "DCore_Explorer1";
const char* pass = "1109666330";

// Cliente HTTP global
HTTPClient http;

int pinAz = 4;
int pinAlt = 3;
int pinV = 2;
int pinVN = 1;
int led = 5;

double tolerance = 0.1;

// Clase para motores
class mountAxis {
  private:
    Servo servo;
    int pin;
    double minAngle;
    double maxAngle;
    double currentAngle;

  public: 
    mountAxis(int p, double mnA, double mxA) : pin(p), minAngle(mnA), maxAngle(mxA), currentAngle(mnA) {}

    void begin() {
      servo.setPeriodHertz(50);
      servo.attach(pin, 1000, 2000);
      servo.write(round(minAngle));
      currentAngle = minAngle;
    }

    void moveTo(double mvt) {
      if (mvt < minAngle) mvt = minAngle;
      if (mvt > maxAngle) mvt = maxAngle;
      servo.write(round(mvt));
      currentAngle = mvt;
    }

    double getPosition() const { return currentAngle; }
    double getMinAngle() const { return minAngle; }
    double getMaxAngle() const { return maxAngle; }
};

// Estructura  8 bytes para recibir az y alt
struct Coordinates {
  float az;
  float alt;
};

struct deltaAngular {
  float az;
  float alt;
};

// Prototipos de funciones
bool get_Coords(Coordinates &dataOut); 
void trackTarget();

// Crear objetos de motores
mountAxis azAxis(pinAz, 0, 180);
mountAxis altAxis(pinAlt, 0, 150);

void setup() {
  Serial.begin(115200);

  // 1. Configuramos el ESP32 como Access Point (Red propia)
  WiFi.softAP(ssid, pass);

  // 2. Imprimimos la IP del ESP32 (Suele ser 192.168.4.1)
  Serial.print("Red AP Creada: ");
  Serial.println(ssid);
  Serial.print("IP del ESP32 (Gateway): ");
  Serial.println(WiFi.softAPIP());

  azAxis.begin();
  altAxis.begin();

  pinMode(pinV, OUTPUT);
  pinMode(led, OUTPUT);
}
void loop() {
  unsigned long actualMillis = millis();

  // Ejecuta la petición y rastreo cada 2 segundos sin congelar el ESP32
  if (actualMillis - previoMillis >= intervalo) { // Corregido: previoMillis
    previoMillis = actualMillis;
    trackTarget(); 
  }
}

// Función que pide las coordenadas y devuelve true/false según el éxito
bool get_Coords(Coordinates &dataOut) {
  http.begin("http://192.168.4.2:8000/api/target");
  int httpCode = http.GET();
  bool verify = false; // Corregido: false
  
  if (httpCode == HTTP_CODE_OK) {
    WiFiClient* stream = http.getStreamPtr();
    if (stream->available() >= sizeof(Coordinates)) {
      // Corregido: uint8_t* en lugar de uint_8*
      stream->readBytes((uint8_t*)&dataOut, sizeof(Coordinates)); 
      verify = true;
    }
  } else {
    Serial.print("Error HTTP: ");
    Serial.println(httpCode);
  }

  http.end(); // Siempre se libera el socket al terminar
  return verify;
}

void trackTarget() {
  Coordinates target;
  deltaAngular delta;
  
  // Corregido: llamada consistente a get_Coords
  if (get_Coords(target)) { 

    delta.az = abs(target.az - azAxis.getPosition());
    delta.alt = abs(target.alt - altAxis.getPosition());
  
    if (delta.az >= tolerance) { 
      azAxis.moveTo(target.az);
    }

    if (delta.alt >= tolerance) {
      if (target.alt < altAxis.getMinAngle() || target.alt > altAxis.getMaxAngle()) {
        Serial.println("Objeto no rastreable (fuera de rango)");
      } else {
        altAxis.moveTo(target.alt);
      }   
    }
  }
}
