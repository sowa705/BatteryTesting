//set this to your current shunt resistance in ohms
float shuntResistance=1;
//current shunt voltage amplification
float currentGain=1;

float voltageCalibrationData[4] = {1.0,4.0,1.0,4.0};
float amperageCalibrationData[4] = {0.0,4,0.0,4.0};

void setup() {
  Serial.begin(9600);
  pinMode(2,OUTPUT);
}

int readAnalog(int port){
  int total=0;
  for(int i=0;i<3;i++){
    total+=analogRead(port);
    delay(50);
  }
  return total/3;
}

float correct(float val, float* calibrationData){
  return mapf(val,calibrationData[0],calibrationData[1],calibrationData[2],calibrationData[3]);
}

float mapf(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

float readVoltage(){
  float readout=readAnalog(A1)/1024.0*5;
  readout=correct(readout,voltageCalibrationData);
  return readout;
}
float readAmperage(){
  float readout=readAnalog(A0)/1024.0*5/shuntResistance*currentGain;
  readout=correct(readout,amperageCalibrationData);
  return readout;
}

void sendReading(){
  float vbatt=readVoltage();
  float ibatt=readAmperage();
  Serial.print(vbatt, 4);
  Serial.print(",");
  Serial.println(ibatt, 4);
}

void sendCalTable(float* calibrationData){
  Serial.print(calibrationData[0], 4);
  Serial.print(",");
  Serial.print(calibrationData[1], 4);
  Serial.print(",");
  Serial.print(calibrationData[2], 4);
  Serial.print(",");
  Serial.print(calibrationData[3], 4);
  Serial.println(";");
}

void loop() {
  if (Serial.available() > 0) {
    int incomingByte = Serial.read();
    switch(incomingByte){
      case 'r':
        sendReading();
      break;
      case 'e':
        digitalWrite(2,1);
      break;
      case 'd':
        digitalWrite(2,0);
      case 'a':
        sendCalTable(amperageCalibrationData);
        break;
      case 'v':
        sendCalTable(voltageCalibrationData);
        break;
    }
  }
  
 
  delay(50);
}
