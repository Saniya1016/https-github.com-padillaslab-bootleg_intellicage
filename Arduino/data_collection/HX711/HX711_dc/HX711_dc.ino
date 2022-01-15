#include <ArduinoJson.h>
#include <HX711.h>

#define CAL_FAC 170
#define CLK 12

DynamicJsonDocument json(1024);

HX711 scale0;
HX711 scale1;
HX711 scale2;
HX711 scale3;
HX711 scale4;
HX711 scale5;
HX711 scale6;
HX711 scale7;
HX711 scale8;
HX711 scale9;
HX711 scales[] = {scale0, scale1, scale2, scale3, scale4, scale5, scale6, scale7, scale8, scale9};
int cal_fac[] = {1690, 1690, 470, 1750};

void setup() {
  // put your setup code here, to run once:
  json["type"] = "HX711";
  json["ID"] = 0;
  setup_scales();
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(60000);
  serialize_data();
}

void setup_scales() {
   int i;
   for(i=0; i<=3; i++) {
    scales[i].begin(i+2, 12);
//    if(scale1.wait_ready_timeout(1000)) {
      scales[i].set_scale(cal_fac[i]);
      scales[i].tare();
//    }
   }
}

void serialize_data() {
  int i;
  for(i=0; i <=3; i ++){
//    if(scale1.wait_ready_timeout(1000)) {
      json["data"][i] = scales[i].get_units();
//    } else {
//      json["data"][i] = 0;
//    }
  }
  serializeJson(json, Serial);
  Serial.println();
}
