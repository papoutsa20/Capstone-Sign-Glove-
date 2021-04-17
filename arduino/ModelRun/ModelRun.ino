#include <Arduino_LSM9DS1.h>
#include "TensorFlowLite.h"
#include "tensorflow/lite/micro/kernels/micro_ops.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/version.h"

//Our model
#include "three_model.h"

#define DEBUG 1

// Change these constants according to your project's design
const int thumbPin = A7;      // Pin connected to voltage divider output flexPin1
const int indexPin = A6;      //flexPin2
const int middlePin = A5;
const int ringPin = A4;
const int pinkyPin = A3;

//mins and maxes for normalization
const float mins[8] = {446, 221, 284, 261, 331, -.2823486328, -1.2181396484, -.0247802734};
const float maxs[8] = {654, 544, 585, 587, 610, 1.2548828125, 0.4637541172, 1.3212890625};
float results[26];
//const float VCC = 3.3;      // voltage at Ardunio 5V line
//const float R_DIV = 47000.0;  // resistor used to create a voltage divider
float ax, ay, az= 0;

float minVal = -1.0;
float maxVal = 1.0;

bool debug_flag = false;

float initx, inity, initz = 0;

namespace {
  tflite::ErrorReporter* error_reporter = nullptr;
  const tflite::Model* modelpp = nullptr;
  tflite::MicroInterpreter* interpreter = nullptr;
  TfLiteTensor* model_input = nullptr;
  TfLiteTensor* model_output = nullptr;

  // Create an erea of memory for input output and other Tensorflow arrays.
  // You'll need to adjust this by compiling, running, and looking for errors
  constexpr int kTensorArenaSize = 2  * 1024;
  uint8_t tensor_arena[kTensorArenaSize];
} //namespace


void setup() {

  #if DEBUG
    while(!Serial);
  #endif
  // put your setup code here, to run once:
  delay(2000);
  //Serial.begin(9600);
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

  static tflite::MicroErrorReporter micro_error_reporter;
  error_reporter = &micro_error_reporter;

  //Map the model into a usable data structure
  modelpp = tflite::GetModel(model);
  if (modelpp->version() != TFLITE_SCHEMA_VERSION) {
    error_reporter->Report("Model version no work");
    while(1);
  }

  static tflite::MicroMutableOpResolver<3> micro_mutable_op_resolver; //put this number 4 b/c we found it online, may be a problem

 // micro_mutable_op_resolver.AddBuiltin(
 //   tflite::BuiltInOperator_FULLY_CONNECTED,
 //   tflite::ops::micro::Register_FULLY_CONNECTED(),
 //   1, 3);
  micro_mutable_op_resolver.AddSoftmax();
  micro_mutable_op_resolver.AddRelu();
  micro_mutable_op_resolver.AddFullyConnected();
  

    // Build an interpreter to run the model
    static tflite::MicroInterpreter static_interpreter (
      modelpp, micro_mutable_op_resolver, tensor_arena, kTensorArenaSize,
      error_reporter);
    interpreter = &static_interpreter;

    TfLiteStatus allocate_status = interpreter->AllocateTensors();
    if (allocate_status != kTfLiteOk) {
      error_reporter->Report("AllocateTensors() failed");
      while(1);
    }

    model_input = interpreter->input(0);
    model_output = interpreter->output(0);

#if DEBUG
  Serial.print("Numbers of dimensions: ");
  Serial.println(model_input->dims->size);
  Serial.print("Dim 1 Size:");
  Serial.println(model_input->dims->data[1]);
  Serial.print("output Size:");
  Serial.println(model_output->dims->data[1]);
  Serial.print("Input type: ");
  Serial.println(model_input->type);
#endif  
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

#if DEBUG
  unsigned long start_timestamp = micros();
#endif

float inputs[8] = {ADCthumb, ADCindex, ADCmiddle, ADCring, ADCpinky, ax, ay, az};
  //normalize values before sending to model
  for (int i=0; i<8; i++) {
    inputs[i] = inputs[i]-mins[i];
    inputs[i] = inputs[i] / (maxs[i]-mins[i]);
    model_input->data.f[i] = inputs[i];
  }

  interpreter->Invoke();

  Serial.printf("%f,%f,%f,%f,%f,%f,%f,%f", inputs[0], inputs[1], inputs[2], inputs[3], inputs[4], inputs[5], inputs[6], inputs[7]);
  Serial.printf("\n");

  
  for(int i=0; i<26; i++){
    results[i] = model_output->data.f[i];
    Serial.printf("%c, %f \n", (char)(i+65), results[i]);
  }
 
  TfLiteStatus invoke_status = interpreter->Invoke();
  if (invoke_status != kTfLiteOk) {
    error_reporter->Report("Invoke failed on input");
  }



  Serial.println("             ");
  delay(1000);
}
