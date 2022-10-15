#pragma once

#include <HTTPUpdateServer.h>
#include <WebServer.h>

#include "AnchorController.h"

class AnchorAPI {
public:
  AnchorAPI(AnchorController &_controller) : controller(_controller) {}
  void setup(WebServer &server);
  String getHostname();

private:
  AnchorController &controller;
  HTTPUpdateServer httpUpdater;
};
