#include <AccelStepper.h>

int16_t c_stepsToMove_x{0},c_stepsToMove_y{0};
uint8_t openess{0};
int deadZoneSize{2};

#define Y_STEP_PIN 2
#define Y_DIR_PIN  5
#define X_STEP_PIN 3
#define X_DIR_PIN  6
#define ENABLE_PIN 8 
#define gunPin 12


AccelStepper xStepper(1,X_STEP_PIN,X_DIR_PIN);
AccelStepper yStepper(1,Y_STEP_PIN,Y_DIR_PIN);

void setup() {
  pinMode(ENABLE_PIN, OUTPUT);
  digitalWrite(ENABLE_PIN, LOW);

  pinMode(gunPin, OUTPUT);

  pinMode(gunPin,OUTPUT);
  digitalWrite(gunPin,HIGH);

  Serial.begin(115200);

  // Configure X axis
  xStepper.setMaxSpeed(4000);
  xStepper.setAcceleration(500);
  

  // Configure Y Axis
  yStepper.setMaxSpeed(4000);
  yStepper.setAcceleration(500);

  xStepper.setMinPulseWidth(2);
  yStepper.setMinPulseWidth(2);
  
}

bool coord_retriever(int16_t &x, int16_t &y, uint8_t &openess){//read a fixed amount of bytes everytime, reduces uncertinity.
  if(Serial.available()>=6){
    if(Serial.read()==255){
      uint8_t x_low_byte = Serial.read();
      uint8_t x_high_byte = Serial.read();
      uint8_t y_low_byte = Serial.read();
      uint8_t y_high_byte = Serial.read();
      openess = Serial.read();

      x = x_high_byte << 8 | x_low_byte;
      y = y_high_byte << 8 | y_low_byte; 
    }
    return true;

  }
  else{
    return false;
  }

}

int counter{0};



bool integrator_filter(int openess){//if openess is 1 for 5 times consecutively only then the values will be taken as one.
  if(openess){
    if(counter < 10){
      counter++;
    }
  }else{
    if(counter > 0){
      counter--;
    }
  }

  return counter > 5; 
  }




void loop() {

  if(coord_retriever(c_stepsToMove_x,c_stepsToMove_y,openess)){//retrieve the step values

    if(abs(c_stepsToMove_x)>deadZoneSize){
        xStepper.move(c_stepsToMove_x);
    }


    if(abs(c_stepsToMove_y)>deadZoneSize){
      yStepper.move(c_stepsToMove_y);
    } 
  }

xStepper.run();
yStepper.run();

}




















