#include "AnchorAPI.h"

void AnchorAPI::setup(WebServer &server) {
  server.on("/temperature", HTTP_GET, [&]() {
    float tempCelsius = controller.getInternalTemperatureCelsius();
    String msg = String(tempCelsius) + " C\n";
    server.send(200, "text/plain", msg);
  });
}
