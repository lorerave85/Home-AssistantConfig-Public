/*

 This example connects to an unencrypted Wifi network.
 Then it prints the  MAC address of the Wifi module,
 the IP address obtained, and other network details.

 created 13 July 2010
 by dlf (Metodo2 srl)
 modified 31 May 2012
 by Tom Igoe
 */
#include <ESP8266WiFi.h>
#include <SPI.h>
#include <PubSubClient.h>
#include "EmonLib.h" 
#include <Wire.h>
#include <ArduinoJson.h>

#include "arduino_secrets.h"

WiFiClient net;
///////please enter your sensitive data in the Secret tab/arduino_secrets.h
char ssid[] = SECRET_SSID;     
char pass[] = SECRET_PASS;  
char mqtt_user[] = MQTT_USER;
char mqtt_pw[] = MQTT_PW;
char device_name[] = DEV_NAME;
char broker_ip[] = BROKER_IP;
int i=0;
double total = 0;
double media = 0;

EnergyMonitor emon1;

//Inserire la tensione della vostra rete elettrica
int rete = 230.0; // Italia 230V in alcuni paesi 110V 

//Pin del sensore SCT su A1
int pin_sct1 = A0;

void callback(char* topic, byte* payload, unsigned int length) {
  // handle message arrived
}

PubSubClient client(broker_ip, 1883, callback, net);

void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid); 
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected"); 
  Serial.print(WiFi.localIP());
  Serial.println("/"); 
  
  //Burden_resistor = (system_voltage / 2.0) / ((I_RMS * 1.414) / Ratio) = 159
  //system_voltage = 5V - Ratio = 1800 - I_RMS = 20A
  //Pin, calibrazione - Corrente Const= Ratio/Res. Burder. 1800/62 = 29. 
  emon1.current(pin_sct1, 29);
}

void loop() {
  // check the system once every 10 seconds:
  delay(1000);

  //Calcolo della corrente  
  double Irms1 = emon1.calcIrms(1480);
  //Mostra il valore della Corrente
  Serial.print("Corrente 1: ");
  Serial.println(Irms1); // Irms
  total = total + Irms1;
  
  Serial.print("total: ");
  Serial.println(total);
  i=i+1;
  
  if(i==10){
    media = total/10;
    total = 0;
    double power1 = media*220;
    
    StaticJsonDocument<200> doc;
    doc["power_line"] = power1;
    char buffer[512];
    size_t n = serializeJson(doc, buffer);

    Serial.print("Corrente media: ");
    Serial.println(media); // Irms
    
    if (client.connect(device_name, mqtt_user, mqtt_pw)) {
      client.publish("home/power", buffer, n);
    }
    i=0;
  }
}
