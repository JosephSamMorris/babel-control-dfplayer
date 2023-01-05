#include "LedController.h"

void LedController::ledcAnalogWrite(uint8_t channel, uint32_t value, uint32_t valueMax = 255) {
  // Calculate duty, 8191 from 2 ^ 13 - 1
  uint32_t duty = (8191 / valueMax) * min(value, valueMax);

  ledcWrite(channel, duty);
}

void LedController::setBrightness(unsigned int ledIndex, float brightness) {
  const uint32_t maxDuty = 8191;
  uint32_t duty = (float)maxDuty * brightness;
  ledcAnalogWrite(ledIndex, duty, maxDuty);
}

void LedController::setup() {
  pinMode(PIN_LED_IO1, OUTPUT);
  pinMode(PIN_LED_IO2, OUTPUT);
  pinMode(PIN_LED_IO3, OUTPUT);
  pinMode(PIN_LED_IO4, OUTPUT);
  pinMode(PIN_LED_IO5, OUTPUT);
  pinMode(PIN_LED_IO6, OUTPUT);
  pinMode(PIN_LED_IO7, OUTPUT);
  pinMode(PIN_LED_IO8, OUTPUT);

  ledcSetup(0, LEDC_BASE_FREQ, LEDC_TIMER_13_BIT);
  ledcAttachPin(PIN_LED_IO1, 0);
  ledcSetup(1, LEDC_BASE_FREQ, LEDC_TIMER_13_BIT);
  ledcAttachPin(PIN_LED_IO3, 1);
  ledcSetup(2, LEDC_BASE_FREQ, LEDC_TIMER_13_BIT);
  ledcAttachPin(PIN_LED_IO7, 2);
  ledcSetup(3, LEDC_BASE_FREQ, LEDC_TIMER_13_BIT);
  ledcAttachPin(PIN_LED_IO5, 3);

  for (int i = 0; i < 4; i++) {
    setBrightness(i, 0);
  }
}