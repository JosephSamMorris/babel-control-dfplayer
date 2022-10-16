#include <math.h>
#include <stdint.h>

#include "AnchorController.h"

#ifdef __cplusplus
extern "C" {
#endif
uint8_t temprature_sens_read();
#ifdef __cplusplus
}
#endif

uint8_t temprature_sens_read();

void AnchorController::setup() {
  ledController.setup();
}

float AnchorController::getInternalTemperatureCelsius() {
  // Internal temperature sensor has a large random offset between chips
  // so it's only really useful for tracking deltas
  // https://www.esp32.com/viewtopic.php?p=20145&sid=01781d380a7a77ef03b8300fcae1bbc0#p20145
  return (temprature_sens_read() - 32) / 1.8;
}

void AnchorController::setLightLimit(float newLimit) {
  if (newLimit < 0 || newLimit > 1) {
    return;
  }

  lightLimit = newLimit;
}

void AnchorController::confirmLightLimit(float newLimit) {
  if (newLimit < 0 || newLimit > 1) {
    return;
  }

  lightLimitConfirm = newLimit;
}

float AnchorController::getLightLimit() {
  bool confirmed = fabs(lightLimit - lightLimitConfirm) < CLOSE_ENOUGH;

  if (!confirmed) {
    // Limit and confirmation value don't match
    return 0;
  } else {
    return lightLimit;
  }
}

void AnchorController::setBrightness(unsigned int ledIndex, float brightness) {
  float adjustedBrightness = getLightLimit() * brightness;
  ledController.setBrightness(ledIndex, adjustedBrightness);
}

void AnchorController::setBrightnessAll(float brightness) {
  for (int i = 0; i < 4; i++) {
    setBrightness(i, brightness);
  }
}
