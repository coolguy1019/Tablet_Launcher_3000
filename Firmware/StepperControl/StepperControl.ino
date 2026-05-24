#include <AccelStepper.h>

int16_t c_stepsToMove_x{0},c_stepsToMove_y{0};
int16_t p_stepsToMove_x{0},p_stepsToMove_y{0};
int xacc{0};
int yacc{0};
uint8_t openess{0};



#define Y_STEP_PIN 2
#define Y_DIR_PIN  5
#define X_STEP_PIN 3
#define X_DIR_PIN  6
#define ENABLE_PIN 8 

AccelStepper xStepper(1,X_STEP_PIN,X_DIR_PIN);
AccelStepper yStepper(1,Y_STEP_PIN,Y_DIR_PIN);

void setup() {
  pinMode(ENABLE_PIN, OUTPUT);
  digitalWrite(ENABLE_PIN, LOW);

  pinMode(12,OUTPUT);
  digitalWrite(12,HIGH);
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

bool coord_retriever(int16_t &x, int16_t &y, uint8_t &openess){
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


void loop() {
  
// just test code to test the serial communication.

 
  
  if(coord_retriever(c_stepsToMove_x,c_stepsToMove_y,openess)){

    c_stepsToMove_y = c_stepsToMove_y + (c_stepsToMove_y - p_stepsToMove_y)*0.02;
    c_stepsToMove_x = c_stepsToMove_x + (c_stepsToMove_x - p_stepsToMove_x)*0.02;
     // if if statment is not used the initial values of x and y can be used causing errors
    
      //Serial.print(c_stepsToMove_x);
      //Serial.print(" ");
      //Serial.print(c_stepsToMove_y);
      //Serial.print(" ");
      //Serial.println(openess);

 




//=================================================================================================================================

  if(abs(c_stepsToMove_x)>5 && abs(c_stepsToMove_x)<90){
    if(xacc != 100){
    xStepper.setAcceleration(50);
    xacc =100;
    }
    if(xStepper.distanceToGo() == 0){ 
      xStepper.move(c_stepsToMove_x);
    }
  }
  
  else if(abs(c_stepsToMove_x)>=0 && abs(c_stepsToMove_x)<=5){}

  else{
    if(xacc != 1000){
    xStepper.setAcceleration(1000);
    xacc = 1000;
    }
    if(xStepper.distanceToGo() == 0){ 
      xStepper.move(c_stepsToMove_x);
    }
  }



    if(abs(c_stepsToMove_y)>5 && abs(c_stepsToMove_y)<90){
    if(yacc != 100){
    yStepper.setAcceleration(50);
    yacc = 100;
    }
    if(yStepper.distanceToGo() == 0){ 
      yStepper.move(c_stepsToMove_y);
    }
  }
  
  else if(abs(c_stepsToMove_y)>=0 && abs(c_stepsToMove_y)<=5){}

  else{
    if(yacc != 1000){
    yStepper.setAcceleration(1000);
    yacc = 1000;
    }
    if(yStepper.distanceToGo() == 0){ 
      yStepper.move(c_stepsToMove_y);
    }
  }
  }

  
  
  




  
xStepper.run();
yStepper.run();
  }





















