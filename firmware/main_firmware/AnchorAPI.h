#pragma once

#include <HTTPUpdateServer.h>
#include <WebServer.h>

#include "AnchorController.h"

class AnchorAPI {
public:
  void setup(WebServer &server);
  String getHostname();

public:
  void setController(AnchorController *controller) {
    this->controller = controller;
  };

private:
  AnchorController *controller = nullptr;
  HTTPUpdateServer httpUpdater;
};
