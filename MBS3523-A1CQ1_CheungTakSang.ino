#include <Servo.h>
int potentiometer;

void setup() {
  Serial.begin(9600);
  pinMode(A0, INPUT);  
}

void loop() {
  potentiometer = analogRead(A0);
  Serial.println(potentiometer);
  delay(500);
}
