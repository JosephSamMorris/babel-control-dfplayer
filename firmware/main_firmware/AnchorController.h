#pragma once

#include "LedController.h"
#include "AudioController.h"

const float CLOSE_ENOUGH = 0.01;

class AnchorController {
public:
  AnchorController() : lightLimit(0), lightLimitConfirm(0) {}
  void setup();
  void update();

  // LED control
  void setLightLimit(float newLimit);
  void confirmLightLimit(float newLimit);
  float getLightLimit();
  void setBrightness(unsigned int ledIndex, float brightness);
  void setBrightnessAll(float brightness);

  // Sound control
  void setVolume(float volume);

  // Misc
  static float getInternalTemperatureCelsius();
private:
  LedController ledController;
  AudioController audioController;

  float lightLimit;
  float lightLimitConfirm;
};
