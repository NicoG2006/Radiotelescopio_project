#include<ESP32Servo.h>
#include<cmath>
#include<WiFi.h>

//Const for IP
const char* name = "R_ESP_CONECTION";
const char* pass = "Nico_2006";

//Create server and client
WiFiServer server(8080);
WiFiClient client;

int pinAz = 4;
int pinAlt = 3;
int pinV = 2;
int pinVN = 1;
int led = 5;
//unsigned long lastTime = 0;
double tolerance = 0.1;

//Class for each axis motor
class mountAxis{
  private:
  //atributes class
    Servo servo; //For this prototype use a servo
    int pin; //Pin for Motor
    double minAngle;
    double maxAngle;
    double currentAngle;
  public: 
    mountAxis(int p, double mnA, double mxA) //inicialite the atributes
    :
      pin(p),
      minAngle(mnA),
      maxAngle(mxA),
      currentAngle(mnA)
    {}

    void begin(){ //start the motor from begin -> motor's setup
      servo.setPeriodHertz(50);
      servo.attach(pin, 1000,2000);
      servo.write(round(minAngle));
      currentAngle = minAngle;
    }

    void moveTo(double mvt){ //Move the motor order
      if(mvt<minAngle){
        mvt=minAngle;
      }
      if(mvt>maxAngle){
        mvt=maxAngle;
      }
      servo.write(round(mvt));
      currentAngle=mvt;
    }

    double getPosition() const{ //Get the last position
      return currentAngle;
    }

    double getMinAngle(){
      return minAngle;
    }

    double getMaxAngle(){
      return maxAngle;
    }
};

//Struct coords azAlt
struct Coordinates{
  double az;
  double alt;
  bool valid;
};

//Struct for angular diference on Azimut or Altitude
struct deltaAngular{
  double az;
  double alt;
};

//Protoype function 
  //Astropy send coords -> ESP32-C3 mini get the coords
Coordinates get_Coords();
  //return an object client if client conected
WiFiClient getClient();
  //Calculate angularError:
void trackTarget();


//Create the axis objects
mountAxis azAxis(pinAz,0,180);
mountAxis altAxis(pinAlt,30,150);

void setup(){
  Serial.begin(115200);//start serial comunication
  WiFi.softAP(name, pass); //Set name and pass for local conection (Set esp as ACCSESS POINT)
  server.begin(); //INIZIALITE server
  azAxis.begin(); //sart the axis motor Azimut
  altAxis.begin(); //sart the axis motor altitude
  pinMode(pinV, OUTPUT);
  pinMode(led,OUTPUT);
  //Print IP address for socket clients
  Serial.print("IP address: ");
  Serial.println(WiFi.softAPIP());
}

void loop(){  
  trackTarget();
}

//Build the get function
Coordinates get_Coords(){
  //Create a struct objetct data
  Coordinates target;
  target.valid=false; //Inicializate valid bool
  client = getClient(); 
  if(client.connected()){
    if(client.available()){
      String data = client.readStringUntil('\n');
      int comma = data.indexOf(',');

      digitalWrite(pinV, HIGH);
      digitalWrite(led,HIGH);

      if (comma != -1){
        String azStr = data.substring(0, comma);
        String altStr = data.substring(comma + 1);

        target.az = azStr.toFloat();
        target.alt = altStr.toFloat();

        target.valid = true;
      }
    } else {
      digitalWrite(led, LOW);
    }
  }
  return target;
}

void trackTarget(){
  Coordinates target = get_Coords();
  deltaAngular delta;
  
  //Calculate delta angular for exactly position, and the actually position 
  if (target.valid){

    delta.az = abs(target.az - azAxis.getPosition()); //Diference angular position on azimuth magnitude
    delta.alt = abs(target.alt - altAxis.getPosition()); //Diference angular position on Altitude magnitude
  
    //If delta angular superate the tolerance, the axis AZ need move to the new position
    if(delta.az >=tolerance){ 

      azAxis.moveTo(target.az);

    }

    //If delta angular superate the tolerance, the axis ALT need move to the new position
    if(delta.alt >= tolerance){
      //If coords outs range dont move the AltAxis
      if(target.alt < altAxis.getMinAngle()  || target.alt > altAxis.getMaxAngle()){
        Serial.print("Objeto no rastreable");
      }else{
        altAxis.moveTo(target.alt);
      }  

    }
  }else{
    return;
  }
}

WiFiClient getClient(){
  if (!client || !client.connected()) {
    client = server.available();
  }
  if (client) {
    Serial.println("Device connected!");
  }

  return client;
}
