#pragma once

#include <stdint.h>
#include "Arduino.h"

const int PIN_LED_IO1 = 12;
const int PIN_LED_IO2 = 13;
const int PIN_LED_IO3 = 14;
const int PIN_LED_IO4 = 15;
const int PIN_LED_IO5 = 16;
const int PIN_LED_IO6 = 17;
const int PIN_LED_IO7 = 21;
const int PIN_LED_IO8 = 22;

// Use 13 bit precision for LEDC timer
const int LEDC_TIMER_13_BIT = 13;

// Needs to be low enough for the current drivers
const int LEDC_BASE_FREQ = 500;

class LedController {
public:
  void setup();
  void setBrightness(unsigned int ledIndex, float brightness);
private:
  void ledcAnalogWrite(uint8_t channel, uint32_t value, uint32_t valueMax);
};
