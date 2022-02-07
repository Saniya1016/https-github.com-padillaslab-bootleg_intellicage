#include <ArduinoJson.h>

DynamicJsonDocument json(1024);

volatile int PIR_last_read[] = {0,0,0,0,0,0,0,0,0,0};
volatile int PIR_current_read[] = {0,0,0,0,0,0,0,0,0,0};
volatile int PIR_count[] = {0,0,0,0,0,0,0,0,0,0};

void setup() {
  Serial.begin(9600);
  cli();
  json["type"] = "PIR";
  json["ID"] = 0;
  initialize_pins();
  initialize_timer();
  sei();
}

void loop() {
  delay(19000);
  cli();
  serialize_reset_data();
  sei();
}

ISR(TIMER1_COMPA_vect){
  TCNT1  = 0;
  read_PIR();
}

void initialize_timer() {
  TCCR1A = 0;
  TCCR1B = 0;
  TCCR1B |= B00000100;
  TIMSK1 |= B00000010;
  OCR1A = 6250;
}

void initialize_pins() {
  int i;
  for(i = 2; i<=11; i++){
    pinMode(i, INPUT);
  }
}

void read_PIR() {
  int i;
  for(i = 0; i<10; i++) {
    PIR_current_read[i] = digitalRead(i+2);
    if((PIR_last_read[i] == 0) && (PIR_current_read[i] == 1)) {
      PIR_count[i]++;
    }
    PIR_last_read[i] = PIR_current_read[i];
  }
}

void serialize_reset_data() {
  int i = 0;
  for(i=0; i<10; i++){
    json["data"][i] = PIR_count[i];
  }
  serializeJson(json, Serial);
  Serial.println();
  for(i=0; i<10; i++){
    PIR_count[i] = 0;
  }
}
