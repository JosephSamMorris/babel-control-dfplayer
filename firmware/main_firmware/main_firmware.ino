/*
  To upload through terminal you can use: curl -F "image=@firmware.bin" esp32-webupdate.local/update
*/

#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>
#include <ESPmDNS.h>
#include <HTTPUpdateServer.h>
#include "AnchorController.h"
#include "AnchorAPI.h"
#include "wifi.h"

const char* host = "anchor";
const char* ssid = STASSID;
const char* password = STAPSK;

WebServer httpServer(80);
HTTPUpdateServer httpUpdater;
AnchorController controller;
AnchorAPI api(controller);

void handleRoot() {
  httpServer.send(200, "text/plain", "hello from esp32");
}

void setup(void) {
  Serial.begin(115200);

  Serial.println();
  Serial.println("Booting Sketch...");

  WiFi.mode(WIFI_AP_STA);
  WiFi.begin(ssid, password);

  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    WiFi.begin(ssid, password);
    Serial.println("WiFi failed, retrying.");
  }

  httpServer.on("/", handleRoot);

  api.setup(httpServer);

  httpUpdater.setup(&httpServer);
  httpServer.begin();

  Serial.printf("setup() complete");
}

void loop(void) {
  httpServer.handleClient();
}
