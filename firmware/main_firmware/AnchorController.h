#pragma once

#include "LedController.h"

const float CLOSE_ENOUGH = 0.01;

class AnchorController {
public:
  AnchorController() : lightLimit(0), lightLimitConfirm(0) {}
  void setup();
  static float getInternalTemperatureCelsius();

  // LED control
  void setLightLimit(float newLimit);
  void confirmLightLimit(float newLimit);
  float getLightLimit();
  void setBrightness(unsigned int ledIndex, float brightness);
  void setBrightnessAll(float brightness);
private:
  LedController ledController;

  float lightLimit;
  float lightLimitConfirm;
};
