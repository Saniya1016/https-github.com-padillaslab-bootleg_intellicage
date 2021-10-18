// DHT library
#include <DHT.h>

// instantiate dht11
#define DHT_0_PIN 4
#define DHT_0_TYPE DHT11
DHT dht_0 (DHT_0_PIN,DHT_0_TYPE);

// instantiae PIR
#define PIR_0_PIN 7
#define reading

void setup() {
  // put your setup code here, to run once:
  
  // initializing Serial
  Serial.begin(9600);

  //initialize up DHT11
  dht_0.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
}

// returns <float> temperature using DHT11
float get_temperature(DHT dht) {
  return dht.readTemperature();
}

// returns <float> humidity using DHT11
float get_humidity(DHT dht) {
  return dht.readHumidity();
}
