#include <ArduinoJson.h>
#include <DHT.h>

#define photo_pin 3
#define DHT_pin 2

DHT dht(DHT_pin, DHT11);

DynamicJsonDocument json(1024);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  dht.begin();
  pinMode(3, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly
  json["humidity"] = dht.readHumidity();
  json["temperature"] = dht.readTemperature();
  if(digitalRead(photo_pin)==0) {
    json["photo"] =  1;
  } else {
    json["photo"] =  0;
  }
  
  serializeJson(json, Serial);
  Serial.println();

  delay(10000);
}
