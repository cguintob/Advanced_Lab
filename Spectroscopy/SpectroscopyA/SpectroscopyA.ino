float startP=350;   //scan start wavelength
float stopP=700;    //stop wavelength 
float currentP=900;  //current wavelength

int readySpeed=10;       //moving speed to the scan start
int scanSpeed=20/6;       //scan speed
int readSpeed=20;       //data taking speed

int Step=3;     //Arduino pin #4 to the direction pin of A4988#3 to the setp pin of A4988
int Dir=4;      //Arduino pin 
int Relay=7;    //a relay switch of the motor power supply
int sensor=1;   //analog input at A1 to read light intensity

int Reading[10];        //10 element array to store light intensity reading
int dropVal,dropIndex;  //parameters to identify get min and max
int Ydata;            //intensity average (of 6 middle values)

int stepCounter=(int)((stopP-startP)/0.125);    //motor step numbers for the scan
int moveCounter=(int)((startP-currentP)/0.125); //step numbers to move to startP
int inByte=0;   //a parameter used for hand shaking with Processing

void setup() {
  Serial.begin(9600);   //initiate serial communication
  while(!Serial){ }     //wait until the communication is established
  firstContact();       //wait for a character sent by Processing
  Serial.write(((int)(startP*10))/256);
  Serial.write(((int)(startP*10))%256);
  Serial.write(((int)(stopP*10))/256);
  Serial.write(((int)(stopP*10))%256);
  delay(100);

  pinMode(Dir,OUTPUT);
  pinMode(Step,OUTPUT);
  pinMode(Relay,OUTPUT);
  pinMode(sensor,INPUT);
  
  digitalWrite(Relay,HIGH);   //connect the power supply
  if(currentP>startP){
    digitalWrite(Dir,LOW);    //set the motor spin direction to CCW
    moveCounter=-moveCounter; //to make the parameter a positive number
  } else {
    digitalWrite(Dir,HIGH);   
  }
  for (int counter=0; counter<moveCounter; counter++){  //move the startP
    digitalWrite(Step,HIGH);
    delay(readySpeed);
    digitalWrite(Step,LOW);
    delay(readySpeed);
    digitalWrite(Step,HIGH);
    delay(readySpeed);
    digitalWrite(Step,LOW);
    delay(readySpeed);
  }
  if (startP>stopP){
    digitalWrite(Dir,LOW);    //set the motor direction to CCW
    stepCounter=-stepCounter; //to make the parameter a positive number
  } else {
    digitalWrite(Dir,HIGH);   //sets the motor direction to CW
  }
}

void loop() {
  if(Serial.available()>0){ //see if there is a character sent by Processing
    inByte=Serial.read();   //read the character sent by Processing
    for (int count=0; count<stepCounter; count++){
      digitalWrite(Step,HIGH);
      delay(scanSpeed);                
      digitalWrite(Step,LOW);
      delay(scanSpeed); 
      digitalWrite(Step,HIGH);
      delay(scanSpeed);                
      digitalWrite(Step,LOW);
      
      for (int i=0;i<10;i++){
        Reading[i]=analogRead(sensor);
        delay(readSpeed);
      }
      Ydata=10000*getYdata(Reading);
      Serial.write(count/256);
      Serial.write(count%256);
      Serial.write(Ydata/256);
      Serial.write(Ydata%256);
    }
  }
  digitalWrite(Relay,LOW);    //disconnect the power supply
  while(1){ }                 //an infinite loop
}

float getYdata(int A[10]){
  dropVal=min(min(min(min(min(min(min(min(min(A[0],A[1]),A[2]),A[3]),A[4]),A[5]),A[6]),A[7]),A[8]),A[9]);
  for (int i=0;i<10;i++){
    if(dropVal==A[i]){dropIndex=i;}
  }
  for (int i=dropIndex;i<10;i++){
    A[i]=A[i+1];
  }

  dropVal=min(min(min(min(min(min(min(min(A[0],A[1]),A[2]),A[3]),A[4]),A[5]),A[6]),A[7]),A[8]);
  for (int i=0;i<9;i++){
    if(dropVal==A[i]){dropIndex=i;}
  }
  for(int i=dropIndex;i<9;i++){
    A[i]=A[i+1];
  }

  dropVal=max(max(max(max(max(max(max(A[0],A[1]),A[2]),A[3]),A[4]),A[5]),A[6]),A[7]);
  for (int i=0;i<8;i++){
    if(dropVal==A[i]){dropIndex=i;}
  }
  for(int i=dropIndex;i<8;i++){
    A[i]=A[i+1];
  }

  dropVal=max(max(max(max(max(max(A[0],A[1]),A[2]),A[3]),A[4]),A[5]),A[6]);
  for (int i=0;i<7;i++){
    if(dropVal==A[i]){dropIndex=i;}
  }
  for(int i=dropIndex;i<7;i++){
    A[i]=A[i+1];
  }

  int Sum=0;
  for(int i=0;i<6;i++){
    Sum+=A[i];
  }
  float Avg=((float)Sum)/(6*212);
  return Avg;
}

void firstContact(){
  while(Serial.available() <=0) { //wait until Processing to send a character
    Serial.print("A");            //while waiting, keep sending "A"
    delay(300);
  }
}
