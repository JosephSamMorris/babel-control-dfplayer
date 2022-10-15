#pragma once

#include <WebServer.h>
#include "AnchorController.h"

class AnchorAPI {
public:
    AnchorAPI(AnchorController &_controller) : controller(_controller) {}
    void setup(WebServer &server);

private:
    AnchorController controller;
};
