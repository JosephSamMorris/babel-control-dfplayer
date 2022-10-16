#pragma once

#include "LedController.h"
#include "AudioController.h"

const float INITIAL_BRIGHTNESS_LIMIT = 0.25;
const float CLOSE_ENOUGH = 0.01;

class AnchorController {
public:
  AnchorController() : lightLimit(INITIAL_BRIGHTNESS_LIMIT), lightLimitConfirm(INITIAL_BRIGHTNESS_LIMIT) {}
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
