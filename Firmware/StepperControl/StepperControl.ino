#include <AccelStepper.h>

int16_t x_coord{0},y_coord{0};
uint8_t openess{0};
int xcurrent{0};
int xprevious{0};
int ycurrent{0};
int yprevious{0};
int shot{0};

unsigned long currt;
unsigned long elapsed_time;
unsigned long prevt;


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
 
  

  // Configure Y Axis
  yStepper.setMaxSpeed(4000);
  

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

  if(openess == 0){
    digitalWrite(12,HIGH);
  }
 
  
  if(coord_retriever(x_coord,y_coord,openess)){
    
     // if if statment is not used the initial values of x and y can be used causing errors
    /*
      Serial.print(x_coord);
      Serial.print(" ");
      Serial.print(y_coord);
      Serial.print(" ");
      Serial.println(openess);
 */
//=================================================================================================================================
  
  if(abs(x_coord)>5 && abs(x_coord)<50){
    xStepper.setSpeed(x_coord);
    xStepper.runSpeed();
    if(openess==1){
      
      
      digitalWrite(12,LOW);
      delay(100);
      
      
    }
    
    
  
  }else if(abs(x_coord)<=5 && abs(x_coord)>=0){
    
  }else{
    xcurrent = x_coord/abs(x_coord);
    if(xcurrent != xprevious && xcurrent ==1){
    xStepper.setSpeed(4000);
    xprevious = xcurrent;
    }else if(xcurrent != xprevious && xcurrent ==-1){
      xStepper.setSpeed(-4000);
      xprevious = xcurrent;
    }
    xStepper.runSpeed();
  }
  
  if(abs(y_coord)>5 && abs(y_coord)<50){
    yStepper.setSpeed(y_coord);
    yStepper.runSpeed();
    
    
  }else if(abs(y_coord)<=5 && abs(y_coord)>=0){
    
    
    }else{
    ycurrent = y_coord/abs(y_coord);;
    if(ycurrent != yprevious && ycurrent ==1){
    yStepper.setSpeed(4000);
    yprevious = ycurrent;
    }else if(ycurrent != yprevious && ycurrent ==-1){
      yStepper.setSpeed(-4000);
      yprevious = ycurrent;
    }
    yStepper.runSpeed();
  }

  }else{
    digitalWrite(12,HIGH);
  }
  
}




