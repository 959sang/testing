#include <Servo.h>
Servo myServo_1;
Servo myServo_2;

int servoPin_1 = 9;     // y-axis or vertical
int servoPin_2 = 10;    // x-axis or horizontal

String servoPos_1;
String servoPos_2;

int pos_1;
int pos_2;

void setup() {
  Serial.begin(9600);
  myServo_1.attach(servoPin_1);
  myServo_2.attach(servoPin_2);
  myServo_1.write(50);
  myServo_2.write(90);
}

void loop() {
  if (Serial.available() != 0) {  
    servoPos_1 = Serial.readStringUntil('\r');
    servoPos_2 = Serial.readStringUntil('\n');
    pos_1 = servoPos_1.toInt();
    pos_2 = servoPos_2.toInt();
    myServo_1.write(pos_1);
    myServo_2.write(pos_2);
    delay(80);
  }
}
