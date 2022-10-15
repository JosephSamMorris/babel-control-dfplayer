#include "AnchorAPI.h"

void AnchorAPI::setup(WebServer &server) {
  httpUpdater.setup(&server); // /update

  // API /hostname - get unique hostname for this device (based on MAC).

  server.on("/hostname", HTTP_GET, [&]() {
    server.send(200, "text/plain", getHostname());
  });

  // API /light/limit - get or set the light intensity limit (0.0% to something
  // less than or equal to 100.0%). Must match limit/confirm value to take
  // effect.

  server.on(
    "/light/limit",
    HTTP_GET,
    [&]() {
      float lightLimit = controller.getLightLimit() * 100.0f;

      char lightLimitStr[8] = {0};
      snprintf(lightLimitStr, sizeof(lightLimitStr), "%.2f", lightLimit);

      String msg = String(lightLimitStr) + "\n";
      server.send(200, "text/plain", msg);
    }
  );
  server.on(
    "/light/limit",
    HTTP_POST,
    [&]() {
      String postBody = server.arg("plain");

      float maybeValue = postBody.toFloat();

      if (maybeValue < 0 || maybeValue > 100) {
        server.send(400, "text/plain", "Limit must be between 0.0 and 100.0\n");
        return;
      }

      controller.setLightLimit(maybeValue / 100.0f);

      server.send(200, "text/plain", "ok\n");
    }
  );

  // API /light/limit/confirm - confirm the light intensity limit. Both max and
  // max/confirm values must match or the LED output is disabled.
  server.on(
    "/light/limit/confirm",
    HTTP_POST,
    [&]() {
      String postBody = server.arg("plain");

      float maybeValue = postBody.toFloat();

      if (maybeValue < 0 || maybeValue > 100) {
        server.send(400, "text/plain", "Limit must be between 0.0 and 100.0\n");
        return;
      }

      controller.confirmLightLimit(maybeValue / 100.0f);

      server.send(200, "text/plain", "ok\n");
    }
  );

  server.on("/temperature", HTTP_GET, [&]() {
    float tempCelsius = controller.getInternalTemperatureCelsius();
    String msg = String(tempCelsius) + " C\n";
    server.send(200, "text/plain", msg);
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
