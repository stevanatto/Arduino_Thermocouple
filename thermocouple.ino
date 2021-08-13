#include "max6675.h"

int n;
double valor;
int thermoDO = 2;
int thermoCLK = 3;
int thermoCS1 = 4;
int thermoCS2 = 5;
int thermoCS3 = 6;
int thermoCS4 = 7;
int thermoCS5 = 8;
int thermoCS6 = 9;
int thermoCS7 = 10;
int thermoCS8 = 11;
int thermoCS9 = 12;
int thermoCS0 = 13;
int thermoCSA = 0;
int thermoCSB = 1;
double samplerate_ms = 10000;

MAX6675 thermocouple1(thermoCLK, thermoCS1, thermoDO);
MAX6675 thermocouple2(thermoCLK, thermoCS2, thermoDO);
MAX6675 thermocouple3(thermoCLK, thermoCS3, thermoDO);
MAX6675 thermocouple4(thermoCLK, thermoCS4, thermoDO);
MAX6675 thermocouple5(thermoCLK, thermoCS5, thermoDO);
MAX6675 thermocouple6(thermoCLK, thermoCS6, thermoDO);
MAX6675 thermocouple7(thermoCLK, thermoCS7, thermoDO);
MAX6675 thermocouple8(thermoCLK, thermoCS8, thermoDO);
MAX6675 thermocouple9(thermoCLK, thermoCS9, thermoDO);
MAX6675 thermocouple0(thermoCLK, thermoCS0, thermoDO);
MAX6675 thermocoupleA(thermoCLK, thermoCSA, thermoDO);
MAX6675 thermocoupleB(thermoCLK, thermoCSB, thermoDO);
 
void setup() {
  //Serial.begin(9600);
  Serial.begin(38400);
  
  //Serial.println("MAX6675");
  Serial.println("T1\tT2\tT3\tT4\tT5\tT6\tT7\tT8\tT9\tT0\tTa\tTb"); 
  // wait for MAX chip to stabilize
  delay(500);
}

void loop() {
   //Serial.print(n); 
   //Serial.print(":\t"); 
   valor = thermocouple1.readCelsius(); 
   Serial.print(valor); 
   Serial.print("\t"); 
   valor = thermocouple2.readCelsius(); 
   Serial.print(valor); 
   Serial.print("\t"); 
   valor = thermocouple3.readCelsius(); 
   Serial.print(valor); 
   Serial.print("\t"); 
   valor = thermocouple4.readCelsius(); 
   Serial.print(valor); 
   Serial.print("\t"); 
   valor = thermocouple5.readCelsius(); 
   Serial.print(valor); 
   Serial.print("\t"); 
   valor = thermocouple6.readCelsius(); 
   Serial.print(valor); 
   Serial.print("\t"); 
   valor = thermocouple7.readCelsius(); 
   Serial.print(valor); 
   Serial.print("\t"); 
   valor = thermocouple8.readCelsius(); 
   Serial.print(valor); 
   Serial.print("\t"); 
   valor = thermocouple9.readCelsius(); 
   Serial.print(valor); 
   Serial.print("\t"); 
   valor = thermocouple0.readCelsius(); 
   Serial.print(valor); 
   Serial.print("\t"); 
   valor = thermocoupleA.readCelsius(); 
   Serial.print(valor); 
   Serial.print("\t"); 
   valor = thermocoupleB.readCelsius(); 
   Serial.println(valor); 
   n = n+1;
   delay(samplerate_ms);
}
