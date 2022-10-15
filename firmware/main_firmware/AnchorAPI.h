#pragma once

#include "AnchorController.h"
#include <WebServer.h>

class AnchorAPI {
public:
  AnchorAPI(AnchorController &_controller) : controller(_controller) {}
  void setup(WebServer &server);
  String getHostname();

private:
  AnchorController controller;
};
