#pragma once

#include "LedController.h"
#include "AudioController.h"

const int DEFAULT_CONTROL_RATE = 5;
const float MIN_CONTROL_RATE = 0.1;
const float MAX_CONTROL_RATE = 100;
const int CONTROL_RATE_AVERAGE_WINDOW = 5; // How many samples to average over

const float INITIAL_BRIGHTNESS_LIMIT = 0.25;
const float CLOSE_ENOUGH = 0.01;
const int EEPROM_SIZE = 2 + 4 + 1; // 2 for packet offset + 4 for control rate + 1 for use fixed control rate

class AnchorController {
public:
  AnchorController() :
      useFixedControlRate(false),
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
  void setVolume(float volume);
  void setTrack(int track);

  // Misc
  void setPacketOffset(unsigned int newPacketOffset);
  unsigned int getPacketOffset();
  void setUseFixedControlRate(bool useFixed);
  bool usingFixedControlRate();
  void setRate(float newRate);
  float getRate();
  static float getInternalTemperatureCelsius();
private:
  LedController ledController;
  AudioController audioController;

  unsigned int packetOffset;

  bool useFixedControlRate;
  float controlRate;
  float measuredControlRate;

  float lightLimit;
  float lightLimitConfirm;

  float lightTargetPrev;
  float lightTarget;
  unsigned long lightTargetSetTime;
};
