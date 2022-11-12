#pragma once

#include "LedController.h"
#include "AudioController.h"

const int MAX_CONTROL_RATE = 1000;
const int DEFAULT_CONTROL_RATE = 5;
const float INITIAL_BRIGHTNESS_LIMIT = 0.25;
const float CLOSE_ENOUGH = 0.01;
const int EEPROM_SIZE = 6; // 2 for packet offset + 4 for control rate

class AnchorController {
public:
  AnchorController() :
      controlRate(DEFAULT_CONTROL_RATE),
      lightLimit(INITIAL_BRIGHTNESS_LIMIT),
      lightLimitConfirm(INITIAL_BRIGHTNESS_LIMIT)
      {}
  void setup();
  void update();

  // LED control
  void setLightLimit(float newLimit);
  void confirmLightLimit(float newLimit);
  float getLightLimit();
  void setBrightness(unsigned int ledIndex, float brightness);
  void setBrightnessAll(float brightness);
  void setBrightnessTarget(float target);

  // Sound control
  void setAudioOffset(unsigned int offsetMillis);
  void setVolume(float volume);

  // Misc
  void setPacketOffset(unsigned int newPacketOffset);
  unsigned int getPacketOffset();
  void setRate(float newRate);
  float getRate();
  static float getInternalTemperatureCelsius();
private:
  LedController ledController;
  AudioController audioController;

  unsigned int packetOffset;
  float controlRate;

  float lightLimit;
  float lightLimitConfirm;

  float lightTargetPrev;
  float lightTarget;
  unsigned long lightTargetSetTime;
};
