#include "AnchorAPI.h"

void AnchorAPI::setup(WebServer &server) {
  httpUpdater.setup(&server); // /update

  server.on("/temperature", HTTP_GET, [&]() {
    float tempCelsius = controller.getInternalTemperatureCelsius();
    String msg = String(tempCelsius) + " C\n";
    server.send(200, "text/plain", msg);
  });

  server.on("/hostname", HTTP_GET, [&]() {
    server.send(200, "text/plain", getHostname());
  });
}

String AnchorAPI::getHostname() {
  char mac[16] = {0};
  sprintf(mac, "%012llx", ESP.getEfuseMac());

  String hostname = "anchor-";
  hostname += mac;
  hostname += "\n";

  return hostname;
}
