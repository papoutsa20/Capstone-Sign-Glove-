#include <Arduino_LSM9DS1.h>
//#include <stdio.h>
// Change these constants according to your project's design
const int thumbPin = A7;      // Pin connected to voltage divider output flexPin1
const int indexPin = A6;      //flexPin2
const int middlePin = A5;
const int ringPin = A4;
const int pinkyPin = A3;
//const float VCC = 3.3;      // voltage at Ardunio 5V line
//const float R_DIV = 47000.0;  // resistor used to create a voltage divider
float ax, ay, az= 0;

float minVal = -1.0;
float maxVal = 1.0;

bool debug_flag = false;

float initx, inity, initz = 0;

void setup() {
  // put your setup code here, to run once:
  delay(2000);
  Serial.begin(9600);
  pinMode(thumbPin, INPUT);
  pinMode(indexPin, INPUT);
  pinMode(middlePin, INPUT);
  pinMode(ringPin, INPUT);
  pinMode(pinkyPin, INPUT);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
  
  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Acceleration in G's");
  Serial.println("X\tY\tZ");
  

  while (! IMU.accelerationAvailable()) {
    delay(50);
    Serial.println("Not ready yet");
  }
  IMU.readAcceleration(initx, inity, initz);
}

void loop() {
  // put your main code here, to run repeatedly:
  int ADCthumb = analogRead(thumbPin);
  int ADCindex = analogRead(indexPin);
  int ADCmiddle = analogRead(middlePin);
  int ADCring = analogRead(ringPin);
  int ADCpinky = analogRead(pinkyPin);
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(ax, ay, az);
    //to zero out initial value of accelerometer
    ax = ax-initx;
    ay = ay-inity;
    az = az-initz;
  }
  else {
    Serial.print("Gyroscope not available");
  }
  if (debug_flag) {
    //float Vvalue = ADCflex*VCC / 1023;
    Serial.print("Thumb Finger: ");
    Serial.println(ADCthumb);

    Serial.print("Index Finger: ");
    Serial.println(ADCindex);

    Serial.print("Middle Finger: ");
    Serial.println(ADCmiddle);

    Serial.print("Ring Finger: ");
    Serial.println(ADCring);

    Serial.print("Pinky Finger: ");
    Serial.println(ADCpinky);

    int xAng = ax * 90;
    int yAng = ay * 90;
    int zAng = az * 90;
    Serial.print("Acceleration: ");
    Serial.printf("%.5f, %.5f, %.5f\n", ax, ay, az);
    Serial.printf("%d, %d, %d\n", xAng, yAng, zAng);

    Serial.println(" ");
    Serial.println(" ");
  }
  else {
    Serial.printf("%d,%d,%d,%d,%d,%.10f,%.10f,%.10f", ADCthumb, ADCindex, ADCmiddle, ADCring, ADCpinky, ax, ay, az);
    Serial.printf("\n");
  }

  delay(1000);
}
