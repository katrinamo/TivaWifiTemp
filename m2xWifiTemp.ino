/* 
   LaunchPadWiFiButtonPost.ino 

   Author: Mark Easley
   This code example released to the public domain.
*/

#include <aJSON.h>
#include "SPI.h"
#include "WiFi.h"

#include "M2XStreamClient.h"

char ssid[] = "<SSID>"; //  your network SSID (name)
char pass[] = "<PASSWORD>";    // your network password (use for WPA, or use as key for WEP)
int keyIndex = 0;            // your network key Index number (needed only for WEP)

int status = WL_IDLE_STATUS;

char deviceId[] = "<DEVICE ID>"; // Device you want to push to
char streamName1[] = "<STREAM NAME>"; // Stream you want to push to
char streamName2[] = "<STREAM NAME>"; // Stream you want to push to
char m2xKey[] = "<KEY>"; // Your M2X access key


int changedTemp;

//Temp read and then the value
int readTemp;
int TempF;

WiFiClient client;
M2XStreamClient m2xClient(&client, m2xKey);

void setup() {

    Serial.begin(9600);

    
    // attempt to connect to Wifi network:
    Serial.print("Attempting to connect to Network named: ");
    // print the network name (SSID);
    Serial.println(ssid); 
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    WiFi.begin(ssid, pass);
    while ( WiFi.status() != WL_CONNECTED) {
      // print dots while we wait to connect
      Serial.print(".");
      delay(300);
    }
  
    Serial.println("\nYou're connected to the network");
    Serial.println("Waiting for an ip address");
  
    while (WiFi.localIP() == INADDR_NONE) {
      // print dots while we wait for an ip addresss
      Serial.print(".");
      delay(300);
    }

    Serial.println("\nIP Address obtained");
  
    // you're connected now, so print out the status  
    printWifiStatus();

    analogRead(TEMPSENSOR);

}

void loop() {
  readTemp =analogRead(TEMPSENSOR);
  TempF = ((1475 - ((2475*readTemp)/4096))/10);
  TempF = (TempF*(9000));
  TempF = (int)(TempF/5000 + 32);


  Serial.print("temp: ");
  Serial.println(TempF);



  int response = m2xClient.updateStreamValue(deviceId, streamName1, TempF);
  Serial.print("M2X client response code: ");
  Serial.println(response);

  aJsonObject *object = NULL;
  int response2 = m2xClient.listStreamValues(deviceId, streamName2, NULL, &object);

  if (response == -1)
    while (1)
      ;
  if (response2 == -1)
    while (1)
      ;

 if (object) {
    aJsonObject *values = aJson.getObjectItem(object, "values");
    for (unsigned char i = 0; i < aJson.getArraySize(values); i++) {
      aJsonObject *item = aJson.getArrayItem(values, i);
      aJsonObject *timestamp = aJson.getObjectItem(item, "timestamp");
      aJsonObject *val = aJson.getObjectItem(item, "value");

      Serial.print("Found a data point, index: ");
      Serial.println(i);
      Serial.print("Timestamp: ");
      Serial.println(timestamp->valuestring);
      Serial.print("Value: ");
      switch (val->type) {
        case aJson_Int:
          Serial.println(val->valueint);
          break;
        case aJson_Float:
          Serial.println(val->valuefloat);
          break;
        case aJson_String:
          Serial.println(val->valuestring);
          break;
        default:
          Serial.println("(Unknown format)");
          break;
      }
    }
    aJson.deleteItem(object);
  }

  delay(3000);
}

void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
}
