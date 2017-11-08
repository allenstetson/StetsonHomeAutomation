#include <IRremote.h>
IRsend irsend;
// https://learn.sparkfun.com/tutorials/ir-communication

int incomingByte = 0;
char serialBuffer[10];
String inputString = "";
int IRledPin =  3;

void setup() {
  pinMode(IRledPin, OUTPUT);
  digitalWrite(IRledPin, LOW);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0){
    incomingByte = Serial.read();
    //Serial.println(incomingByte, DEC);
    if(incomingByte == 58){
      Serial.readBytesUntil(58, serialBuffer, 10);
      if(strcmp(serialBuffer,"rpower")==0){
        // Receiver Power
        OnkyoPower();
      } else if(strcmp(serialBuffer,"rinvcr")==0){
        // Receiver Input: VCR/DVR
        OnkyoInVcr();
      } else if(strcmp(serialBuffer,"rincbl")==0){
        // Receiver Input: CBL/SAT
        OnkyoInCbl();
      } else if(strcmp(serialBuffer,"rinaux")==0){
        // Receiver Input: AUX
        OnkyoInAux();
      } else if(strcmp(serialBuffer,"rinmulti")==0){
        // Receiver Input: MULTI CH
        OnkyoInMultiCh();
      } else if(strcmp(serialBuffer,"rindvd")==0){
        // Receiver Input: DVD
        OnkyoInDvd();
      } else if(strcmp(serialBuffer,"rintape")==0){
        // Receiver Input: Tape
        OnkyoInTape();
      } else if(strcmp(serialBuffer,"rintuner")==0){
        // Receiver Input: Tuner
        OnkyoInTuner();
      } else if(strcmp(serialBuffer,"rincd")==0){
        // Receiver Input: CD
        OnkyoInCd();
      }
      memset(serialBuffer, 0, sizeof(serialBuffer));
    }
  }
}



void OnkyoPower(void){ 
  for (int i = 0; i < 3; i++) {
    irsend.sendNEC(0x4B36D32C, 32); // Onkyo Power
    delay(40);
  }
}

void OnkyoInVcr(void){ 
  for (int i = 0; i < 3; i++) {
    irsend.sendNEC(0x4BB6F00F, 32); // Onkyo VCR/DVR
    delay(40);
  }
}

void OnkyoInCbl(void){ 
  for (int i = 0; i < 3; i++) {
    irsend.sendNEC(0x4BB6708F, 32);
    delay(40);
  }
}

void OnkyoInAux(void){ 
  for (int i = 0; i < 3; i++) {
    irsend.sendNEC(0x4BB6F906, 32);
    delay(40);
  }
}

void OnkyoInMultiCh(void){ 
  for (int i = 0; i < 3; i++) {
    irsend.sendNEC(0x4B3620DF, 32);
    delay(40);
  }
}

void OnkyoInDvd(void){ 
  for (int i = 0; i < 3; i++) {
    irsend.sendNEC(0x4B3631CE, 32);
    delay(40);
  }
}

void OnkyoInTape(void){ 
  for (int i = 0; i < 3; i++) {
    irsend.sendNEC(0x4BB610EF, 32);
    delay(40);
  }
}

void OnkyoInTuner(void){ 
  for (int i = 0; i < 3; i++) {
    irsend.sendNEC(0x4BB6D02F, 32);
    delay(40);
  }
}

void OnkyoInCd(void){ 
  for (int i = 0; i < 3; i++) {
    irsend.sendNEC(0x4BB6906F, 32);
    delay(40);
  }
}

