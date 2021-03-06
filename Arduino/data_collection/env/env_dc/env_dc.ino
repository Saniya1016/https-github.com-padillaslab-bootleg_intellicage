#include <ArduinoJson.h>
#include <DHT.h>

#define photo_pin 3
#define DHT_pin 4

DHT dht(DHT_pin, DHT11);

DynamicJsonDocument json(1024);

void setup() {
  // put your setup code here, to run once:
  json["type"] = "env";
  json["ID"] = 0;
  Serial.begin(9600);
  dht.begin();
  pinMode(photo_pin, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly
  delay(60000);
  serialize_data();
}

void serialize_data() {
  json["humidity"] = dht.readHumidity();
  json["temperature"] = dht.readTemperature();
  if(digitalRead(photo_pin)==0) {
    json["photo"] =  1;
  } else {
    json["photo"] =  0;
  }
  serializeJson(json, Serial);
  Serial.println();
}
