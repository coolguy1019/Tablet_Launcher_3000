int x_coord{0},y_coord{0};

void setup() {
  Serial.begin(115200);
  
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
 // if(coord_retriever(x_coord,y_coord)){ // if if statment is not used the initial values of x and y can be used causing errors
 //     Serial.print(x_coord);
 //     Serial.print(" ");
 //     Serial.println(y_coord);
 //}
  

}