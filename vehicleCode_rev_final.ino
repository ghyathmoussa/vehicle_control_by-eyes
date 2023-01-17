#include "Arduino.h"
#include <WiFi.h>
#include <WiFiUdp.h>

WiFiUDP Udp;  // Creation of wifi Udp instance

char packetBuffer[255];

unsigned int localPort = 9999;

const char *ssid = "dogu";
const char *password = "123457890";

const int Enable_A = 22;
const int Enable_B = 23;
const int inputA1 = 16;
const int inputA2 = 17;
const int inputB1 = 18;
const int inputB2 = 19;


const int frequency = 500;
const int resolution = 8;
const int pwm_channel_ENB = 0;
const int pwm_channel_ENA = 1;
int flag = 0;

void setup()
{
  definePin();

  Serial.begin(115200);
  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);

  Serial.print("Start To Play");

  WiFi.softAP(ssid, password);  // ESP-32 as access point
  Udp.begin(localPort);
  
}

void motorSpeed(int SpeedENA, int SpeedEnB){
  ledcWrite(pwm_channel_ENA, SpeedENA);
  ledcWrite(pwm_channel_ENB, SpeedEnB);
}


void definePin(){
  pinMode(Enable_A, OUTPUT);
  pinMode(Enable_B, OUTPUT);
  pinMode(inputA1, OUTPUT);
  pinMode(inputA2, OUTPUT);
  pinMode(inputB1, OUTPUT);
  pinMode(inputB2, OUTPUT);

  ledcSetup(pwm_channel_ENA, frequency, resolution);
  ledcSetup(pwm_channel_ENB, frequency, resolution);

  ledcAttachPin(Enable_A, pwm_channel_ENA);
  ledcAttachPin(Enable_B, pwm_channel_ENB);
}

void moveCar(int direction){
  switch(direction)
    {
      case 1: //ileri
        
        digitalWrite(inputA1, HIGH);
        digitalWrite(inputA2, LOW);
        digitalWrite(inputB1 , HIGH);
        digitalWrite(inputB2, LOW);  
        
        if (flag== 1){
          for (int i = 255; i >= 0; --i){
            motorSpeed(i, i);
            delay(2);
          }
        }        


        break;
    
      case 2: //geri
        
        digitalWrite(inputA1, LOW);
        digitalWrite(inputA2, HIGH);
        digitalWrite(inputB1, LOW);
        digitalWrite(inputB2, HIGH);
        
        if (flag== 1){
          for (int i = 255; i >= 0; --i){
            motorSpeed(i, i);
            delay(2);
          }
        }   

        break;
    
      case 3: //sağ

        digitalWrite(inputA1, HIGH);
        digitalWrite(inputA2, LOW); 
        digitalWrite(inputB1, LOW);
        digitalWrite(inputB2, HIGH);

        if (flag== 1){
          for (int i = 225; i >= 0; --i){
            motorSpeed(i, i);
            delay(2);
          }
        }


        break;
    
      case 4: //sol

        digitalWrite(inputA1, LOW);
        digitalWrite(inputA2, HIGH); 
        digitalWrite(inputB1, HIGH);
        digitalWrite(inputB2, LOW);

        if (flag== 1){
          for (int i = 225; i >= 0; --i){
            motorSpeed(i, i);
            delay(2);
          }
        }

        break;
  
      case 5: //dur
        motorSpeed(0, 0);
        break;
    
      default: //dur
        motorSpeed(0, 0);
        break;
    }
  
}


void loop(){
  flag = 0;
  int packetSize = Udp.parsePacket();
  if (packetSize) {
    int len = Udp.read(packetBuffer, 255);
    if (len > 0) packetBuffer[len - 1] = 0;
    Serial.print("Recibido(IP/Size/Data):");
    Serial.print(Udp.remoteIP());
    Serial.print(" / ");
    Serial.print(packetSize);
    Serial.print(" / ");
    Serial.println(packetBuffer);

    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Udp.printf("received: ");
    Udp.printf(packetBuffer);
    Udp.printf("\r\n");
    Udp.endPacket();
  }

  if (!strcmp(packetBuffer, "FW")){
    flag = 1;
    Serial.println("move forward");    
    moveCar(1);
  }
  else if (!strcmp(packetBuffer, "BW")){
    flag = 1;
    Serial.println("move backward");
    moveCar(2);
  }
  else if (!strcmp(packetBuffer, "L")){
    flag = 1;
    Serial.println("move left");
    moveCar(4);
  }
  else if (!strcmp(packetBuffer, "R")){
    flag = 1;
    Serial.println("move right");
    moveCar(3);
  }
  else if (!strcmp(packetBuffer, "ST")){
    flag = 1;
    Serial.println("stop");
    moveCar(5);
  }
  else {
    flag = 1;
    moveCar(5);
  }  

}
