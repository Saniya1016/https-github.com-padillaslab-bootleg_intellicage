// DHT library
#include <DHT.h>

// instantiate dht11
#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht0 (DHTPIN,DHTTYPE);

void setup() {
  // put your setup code here, to run once:
  
  // initializing Serial
  Serial.begin(9600);

  //initialize up DHT11
  dht0.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
}

// returns <float> temperature using DHT11
float getTemperature(DHT dht) {
  return dht.readTemperature();
}

// returns <float> humidity using DHT11
float getHumidity(DHT dht) {
  return dht.readHumidity();
}
