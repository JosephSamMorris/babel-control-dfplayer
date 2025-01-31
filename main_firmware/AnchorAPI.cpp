#include "AnchorAPI.h"
#include "AnchorReceiver.h"

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
    float lightLimit = controller->getLightLimit() * 100.0f;

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

    controller->setLightLimit(maybeValue / 100.0f);

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

    controller->confirmLightLimit(maybeValue / 100.0f);

    server.send(200, "text/plain", "ok\n");
  }
  );

  // API /light/brightness - set the light intensity between 0.0% and 100.0%.
  // The value is rescaled based on the current active limit.

  // Cannot get brightness for all wings but can set it
  server.on(
    "/light/brightness",
    HTTP_POST,
  [&]() {
    String postBody = server.arg("plain");

    float maybeValue = postBody.toFloat();

    if (maybeValue < 0 || maybeValue > 100) {
      server.send(400, "text/plain", "Brightness must be between 0.0 and 100.0\n");
      return;
    }

    controller->setBrightnessTarget(maybeValue / 100.0f);

    server.send(200, "text/plain", "ok\n");
  }
  );
  

  // API /sound/volume - set the current volume (0.0-100.0%)

  server.on(
    "/sound/volume",
    HTTP_POST,
  [&]() {
    String postBody = server.arg("plain");

    float maybeValue = postBody.toFloat();

    if (maybeValue < 0 || maybeValue > 400) {
      server.send(400, "text/plain", "Volume must be between 0.0 and 400.0\n");
      return;
    }

    controller->setVolume(maybeValue / 100.0f);

    server.send(200, "text/plain", "ok\n");
  }
  );

  // API /sound/track - set the current track

  server.on(
    "/sound/track",
    HTTP_POST,
  [&]() {
    String postBody = server.arg("plain");

    float maybeValue = postBody.toInt();

    if (maybeValue < 0) {
      server.send(400, "text/plain", "track must be greater than 0");
      return;
    }

    controller->setTrack(maybeValue);

    server.send(200, "text/plain", "ok\n");
  }
  );

  // API - /control/offset - get or set offset in UDP broadcasts.

  server.on(
    "/control/offset",
    HTTP_GET,
  [&]() {
    unsigned int offset = controller->getPacketOffset();

    char offsetStr[8] = {0};
    snprintf(offsetStr, sizeof(offsetStr), "%d", offset);

    String msg = String(offsetStr) + "\n";
    server.send(200, "text/plain", msg);
  }
  );
  server.on(
    "/control/offset",
    HTTP_POST,
  [&]() {
    String postBody = server.arg("plain");

    int maybeValue = postBody.toInt();

    if (maybeValue < 0 || maybeValue >= MAX_UNIT_COUNT) {
      server.send(400, "text/plain", "Offset must be between 0 and 179\n");
      return;
    }

    controller->setPacketOffset(maybeValue);

    server.send(200, "text/plain", "ok\n");
  }
  );

  // API - /control/rate - get or set the target control rate,
  // which is used for interpolating animations

  server.on(
    "/control/rate",
    HTTP_GET,
  [&]() {
    float rate = controller->getRate();

    char rateStr[8] = {0};
    snprintf(rateStr, sizeof(rateStr), "%.2f", rate);

    String msg = String(rateStr) + "\n";
    server.send(200, "text/plain", msg);
  }
  );
  server.on(
    "/control/rate",
    HTTP_POST,
  [&]() {
    String postBody = server.arg("plain");

    int maybeValue = postBody.toFloat();

    if (maybeValue <= 0 || maybeValue >= MAX_CONTROL_RATE) {
      server.send(400, "text/plain", "Control rate must be between 0 and 1000\n");
      return;
    }

    controller->setRate(maybeValue);

    server.send(200, "text/plain", "ok\n");
  }
  );

  server.on(
    "/control/rate/fixed",
    HTTP_GET,
  [&]() {
    bool usingFixed = controller->usingFixedControlRate();

    if (usingFixed) {
      server.send(200, "text/plain", "true");
    } else {
      server.send(200, "text/plain", "false");
    }
  }
  );
  server.on(
    "/control/rate/fixed",
    HTTP_POST,
  [&]() {
    String postBody = server.arg("plain");

    int maybeValue = postBody.toInt();

    if (maybeValue != 0 && maybeValue != 1) {
      server.send(400, "text/plain", "Must be 0 (false) or 1 (true)\n");
      return;
    }

    controller->setUseFixedControlRate(maybeValue);

    server.send(200, "text/plain", "ok\n");
  }
  );

  server.on("/temperature", HTTP_GET, [&]() {
    float tempCelsius = controller->getInternalTemperatureCelsius();
    String msg = String(tempCelsius) + " C\n";
    server.send(200, "text/plain", msg);
  });

  server.on("/firmware/version", HTTP_GET, [&]() {
    server.send(200, "text/plain", "3");
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
