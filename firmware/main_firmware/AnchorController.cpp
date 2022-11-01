#include <math.h>
#include <stdint.h>
#include <EEPROM.h>
#include "AnchorReceiver.h"

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
  // Read the saved packet offset from EEPROM
  packetOffset = (EEPROM.read(0) << 8) | EEPROM.read(1);

  ledController.setup();
  audioController.setup();
}

void AnchorController::update() {
  audioController.update();
}

// LED API

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

// SOUND API

void AnchorController::setAudioOffset(unsigned int offsetMillis) {
  audioController.setOffsetMillis(offsetMillis);
}

void AnchorController::setVolume(float volume) {
  audioController.setVolume(volume);
}

// MISC API

void AnchorController::setPacketOffset(unsigned int newPacketOffset) {
  if (newPacketOffset >= MAX_UNIT_COUNT) {
    return;
  }

  packetOffset = newPacketOffset;

  // Save the new packet offset to EEPROM
  EEPROM.write(0, packetOffset >> 8);
  EEPROM.write(1, packetOffset & 0xff);
  EEPROM.commit();
}

unsigned int AnchorController::getPacketOffset() {
  return packetOffset;
}

float AnchorController::getInternalTemperatureCelsius() {
  // Internal temperature sensor has a large random offset between chips
  // so it's only really useful for tracking deltas
  // https://www.esp32.com/viewtopic.php?p=20145&sid=01781d380a7a77ef03b8300fcae1bbc0#p20145
  return (temprature_sens_read() - 32) / 1.8;
}