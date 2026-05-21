#include <AccelStepper.h>


int x_coord{0},y_coord{0};

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

  Serial.begin(115200);

  // Configure X axis
  xStepper.setMaxSpeed(4000);
  xStepper.setAcceleration(1000);
  

  // Configure Y Axis
  yStepper.setMaxSpeed(4000);
  yStepper.setAcceleration(1000);

  
}

bool coord_retriever(int &x, int &y){
  if(Serial.available()){
    String input = Serial.readStringUntil(')');
    
    int comma = input.indexOf(',');

    x = input.substring(0, comma).toInt();
    y = input.substring(comma + 1).toInt();
    return true;
  }
  else{
    return false;
  }

}



void loop() {
  
// just test code to test the serial communication.

  if(coord_retriever(x_coord,y_coord)){ // if if statment is not used the initial values of x and y can be used causing errors
      Serial.print(x_coord);
      Serial.print(" ");
      Serial.println(y_coord);
 

//=================================================================================================================================
    

  if(abs(x_coord)>10){
    xStepper.setSpeed(x_coord*2);
  
  }
  else{
    xStepper.setSpeed(0);
  }
  if(abs(y_coord)>10){
    yStepper.setSpeed(y_coord*2);
    
  }else{
    yStepper.setSpeed(0);
  }
xStepper.runSpeed();
yStepper.runSpeed();

}





}