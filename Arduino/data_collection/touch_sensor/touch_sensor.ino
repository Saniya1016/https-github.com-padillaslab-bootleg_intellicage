#include <ArduinoJson.h>
#include <CapacitiveSensor.h>

#define NUM_TOUCH_SENSOR 2
#define RECORD_TIME_FOR_SENSOR 40
#define RECORD_TIME_FOR_ARDUINO_IN_SEC 2
 
DynamicJsonDocument json(1024);
///////////////////////////////// Make the code array independent for UI Demo
CapacitiveSensor ts[] = {CapacitiveSensor(4, 2), CapacitiveSensor(4, 6), CapacitiveSensor(4, 8) ,CapacitiveSensor(4, 10), CapacitiveSensor(4, 12)};
volatile int ts_current[] = {0,0,0,0,0};
volatile int ts_high[] = {0,0,0,0,0};

void setup() {
  // put your setup code here, to run once:
  cli();
  Serial.begin(9600);
  json["type"] = "TS";
  json["ID"] = 0;
  initialize_timer();
  sei();
}

ISR(TIMER1_COMPA_vect){
  read_ts();
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(RECORD_TIME_FOR_ARDUINO_IN_SEC*1000);
  cli();
  serialize_reset_data();
  sei();
}

void serialize_reset_data() {
  int i;
  for(i=0; i<NUM_TOUCH_SENSOR; i++) {
    json["data"][i] = ts_high[i];
    ts_high[i] = 0;
  }
  serializeJson(json, Serial);
  Serial.println();
}

void read_ts() {
  int i;
  for(i=0; i<NUM_TOUCH_SENSOR; i++) {
    ts_current[i] = ts[i].capacitiveSensor(RECORD_TIME_FOR_SENSOR);
    if(ts_current[i] > ts_high[i]) {
      ts_high[i] = ts_current[i];
    }
  }
}

void initialize_timer() {
  TCCR1A = 0;
  TCCR1B = 0;
  TCCR1B |= B00000100;
  TIMSK1 |= B00000010;
  OCR1A = 6250;
}
