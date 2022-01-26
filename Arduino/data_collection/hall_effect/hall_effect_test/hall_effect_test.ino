#include <ArduinoJson.h>

DynamicJsonDocument json(1024);

volatile int count = 0;

void pctr() {
  count++;
}

void setup() {
  // put your setup code here, to run once:
  json["type"] = "HE";
  json["ID"] = 0;
  Serial.begin(9600);
  pinMode(2, INPUT);
  attachInterrupt(digitalPinToInterrupt(2), pctr, FALLING);
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(5000);
  cli();
  serialize_reset_data();
  sei();
}

void serialize_reset_data() {
  json["count"] = count/2;
  count = 0;
  serializeJson(json, Serial);
  Serial.println();
}
