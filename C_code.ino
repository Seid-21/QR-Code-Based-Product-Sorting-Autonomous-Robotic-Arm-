#include <Servo.h>

Servo s1, s2, s3, s4, s5, s6;

const int SERVO_POS_A = 70;
const int SERVO_POS_B = 130;
const int SERVO_POS_C = 180;
const int SERVO_POS_HOLD = 67;

int x = 100, y = 90, z = 150, p = 60, m = 80, n = 117;
String readString;

void setup() {
  Serial.begin(9600);
  
  s1.attach(3);
  s2.attach(5);
  s3.attach(6);
  s4.attach(9);
  s5.attach(10);
  s6.attach(11);
  
  // Set initial positions
  s1.write(x);
  s2.write(y);
  s3.write(z);
  s4.write(p);
  s5.write(m);
  s6.write(n);
}

void loop() {
  if (Serial.available()) {
    delay(3);
    while (Serial.available()) {
      char c = Serial.read();
      readString += c;
    }

    if (readString.length() > 0) {
      Serial.println(readString);
      if (readString == "ITEM_A") {
        processItemA();
      } else if (readString == "ITEM_B") {
        processItemB();
      }
      readString = "";  // Clear the string after processing
    }
  }
}

void processItemA() {
  moveServos(SERVO_POS_A, SERVO_POS_B, SERVO_POS_C, SERVO_POS_HOLD);
  s1.write(60); delay(2); s1.write(14); delay(2);
  s2.write(95); delay(1000); 
  s5.write(100); delay(1000);
  resetServos();
}

void processItemB() {
  moveServos(SERVO_POS_A, SERVO_POS_B, SERVO_POS_C, SERVO_POS_HOLD);
  s1.write(140); delay(2); s1.write(180); delay(2);
  s2.write(95); delay(1000);
  s5.write(100); delay(1000);
  resetServos();
}

void moveServos(int posA, int posB, int posC, int posHold) {
  s2.write(posA); delay(1000);
  s5.write(posB); delay(1000);
  s3.write(posC); delay(1000);
  s6.write(posHold); delay(1000);
}

void resetServos() {
  s3.write(150); delay(1000);
  s2.write(90); delay(1000);
  s5.write(80); delay(1000);
  s1.write(60); delay(1000);
  s1.write(100); delay(1000);
}
