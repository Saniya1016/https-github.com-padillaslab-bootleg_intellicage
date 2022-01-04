#include <HX711.h>
#include <DHT_U.h>
#include <ArduinoJson.h>
#include <DHT.h>

// instansiating pseudo json capable of holding 5 objects
StaticJsonDocument<JSON_OBJECT_SIZE(5)> json;

// Pins
#define DHT_0_PIN 3
#define PHOTO_PIN 6
#define PIR_0_PIN 4
#define PIR_1_PIN 5
#define HE_0_PIN 7
#define HX_CLK_PIN 8
#define HX_0_PIN 9
#define HX_1_PIN 10

// instantiate dht11
#define DHT_0_TYPE DHT11
DHT dht_0 (DHT_0_PIN,DHT_0_TYPE);

// instantiae PIR
//// PIR 0
volatile int PIR_0_last_read = 0;
volatile int PIR_0_current_read = 0;
volatile int PIR_0_count = 0;
//// PIR 1
volatile int PIR_1_last_read = 0;
volatile int PIR_1_current_read = 0;
volatile int PIR_1_count = 0;

// instantiate hall effect
volatile int HE_0_last_read = 0;
volatile int HE_0_current_read = 0;
volatile int HE_0_count = 0;

// instantiate HX711
HX711 scale_0;
HX711 scale_1;

void setup() {
  // put your setup code here, to run once:
  
  // initializing Serial
  cli();
  Serial.begin(9600);

  //initialize DHT11
  dht_0.begin();

  //initialize photo
  pinMode(PHOTO_PIN, INPUT);
  //initialze PIR
  pinMode(PIR_0_PIN, INPUT);
  pinMode(PIR_1_PIN, INPUT);
  //initialize Hall effect
  pinMode(HE_0_PIN, INPUT);
  //initiate HX711
  scale_0.begin(HX_0_PIN, HX_CLK_PIN);
  scale_0.set_scale(-170);
  scale_0.tare();
  scale_1.begin(HX_1_PIN, HX_CLK_PIN);
  scale_1.set_scale(-170);
  scale_1.tare();
  //initializing timer for PIR_0
  TCCR1A = 0;
  TCCR1B = 0;
  TCCR1B |= B00000100;
  TIMSK1 |= B00000010;
  OCR1A = 6250;
  
  sei();
  delay(5000);
}

void loop() {
  // put your main code here, to run repeatedly:
  cli();
  serialize_data();
  sei();
  delay(5000);
}

void serialize_data() {
  // parsing JSON
  //// parsing DHT11
  json["temperature"] = dht_0.readHumidity();
  json["humidity"] = dht_0.readTemperature();
  //// parsing photo
  json["photo_sensor"] = get_photo(PHOTO_PIN);
  //// parsing PIR
  json["PIR_0_count"] = PIR_0_count;
  PIR_0_count = 0;
  json["PIR_1_count"] = PIR_1_count;
  PIR_1_count = 0;
  ////parsing hall effect
  json["HE_0_count"] = HE_0_count;
  HE_0_count = 0;
  ////parsing scales
  json["scale_0"] = scale_0.get_units();
  json["scale_1"] = scale_1.get_units();
  serializeJson(json, Serial);
  Serial.println();
}

// params <int> pin
// returns <float> photo status
float get_photo(int photo_pin) {
  return digitalRead(photo_pin);
}

// updates PIR count
void read_PIR() {
  // check PIR
  //// PIR 0
  PIR_0_current_read = digitalRead(PIR_0_PIN);
  if(PIR_0_last_read != PIR_0_current_read) {
    PIR_0_count++;
  }
  PIR_0_last_read = PIR_0_current_read;
  //// PIR 1
  PIR_1_current_read = digitalRead(PIR_1_PIN);
  if(PIR_1_last_read != PIR_1_current_read) {
    PIR_1_count++;
  }
  PIR_1_last_read = PIR_1_current_read;
}

void read_HE() {
  // Hall Effect
  HE_0_current_read = digitalRead(HE_0_PIN);
  if(HE_0_last_read != HE_0_current_read) {
    HE_0_count++;
  }
  HE_0_last_read = HE_0_current_read;
}

// ISR to maintain count for PIR_0, PIR_1
ISR(TIMER1_COMPA_vect){
  TCNT1  = 0;
  read_PIR();
  read_HE();
}
