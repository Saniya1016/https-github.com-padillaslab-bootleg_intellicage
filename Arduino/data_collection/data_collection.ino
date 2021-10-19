// DHT library
#include <DHT.h>

// instantiate dht11
#define DHT_0_PIN 4
#define DHT_0_TYPE DHT11
DHT dht_0 (DHT_0_PIN,DHT_0_TYPE);

// instantiae PIR
#define PIR_0_PIN 7
int* PIR_0_last_read = (int*) malloc(sizeof(int));
int* PIR_0_count = (int*) malloc(sizeof(int));

void setup() {
  // put your setup code here, to run once:
  
  // initializing Serial
  cli();
  Serial.begin(9600);

  //initialize up DHT11
  dht_0.begin();

  //initialze PIR
  pinMode(PIR_0_PIN, INPUT);
  *PIR_0_last_read = digitalRead(PIR_0_PIN);
  *PIR_0_count = 0;
  //initializing timer for PIR_0
  TCCR1A = 0;
  TCCR1B = 0;
  TCCR1B |= B00000100;
  TIMSK1 |= B00000010;
  OCR1A = 37500;
  
  sei();
  delay(5000);
}

void loop() {
  // put your main code here, to run repeatedly:
  cli();

  // reset PIR_0 count
  *PIR_0_count = 0;
  
  sei();
  delay(60000);
}

// params <DHT> dht: dht sensor
// returns <float> temperature using DHT11
float get_temperature(DHT dht) {
  return dht.readTemperature();
}

// params <DHT> dht: dht sensor
// returns <float> humidity using DHT11
float get_humidity(DHT dht) {
  return dht.readHumidity();
}

// params
//  PIR_pin <int>
//  last_read <int>
//  current_read <int>: assign using malloc() and free() after use
//  motion_detected <boolean>: assign using malloc() and free() after use
// return: <boolean> motion detected
bool* motion_detection(int PIR_pin, int* last_read, int* current_read, bool* motion_detected) {
  *current_read = digitalRead(PIR_pin);
  *motion_detected = (*current_read > *last_read || *current_read < *last_read);
  *last_read = *current_read;
  return motion_detected;
}

// ISR to maintain count for PIR_0
ISR(TIMER1_COMPA_vect){
  TCNT1  = 0;
  int* current_read = (int*) malloc(sizeof(int));
  bool* motion_detected = (bool*) malloc(sizeof(bool));
  if(*motion_detection(PIR_0_PIN, PIR_0_last_read, current_read, motion_detected)) {
    *PIR_0_count = *PIR_0_count + 1;
  }
  free(current_read);
  free(motion_detected);
}
