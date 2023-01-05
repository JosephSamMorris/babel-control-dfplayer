#include <math.h>
#include <stdint.h>
#include <Arduino.h>
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
  EEPROM.begin(EEPROM_SIZE);

  // Read the saved packet offset from EEPROM
  uint16_t maybePacketOffset = (EEPROM.read(0) << 8) | EEPROM.read(1);
  if (maybePacketOffset != 0xffff) {
    packetOffset = maybePacketOffset;
  }

  Serial.print("Packet offset is ");
  Serial.println(packetOffset);

  // Read the saved control rate from EEPROM
  uint32_t maybeFixedControlRate = (EEPROM.read(2) << 24)
    | (EEPROM.read(3) << 16)
    | (EEPROM.read(4) << 8)
    | EEPROM.read(5);

  if (maybeFixedControlRate != 0 && maybeFixedControlRate != 0xffffffff) {
    controlRate = (float)maybeFixedControlRate / 1000;
  }

  useFixedControlRate = EEPROM.read(6);

  if (useFixedControlRate) {
    Serial.print("Control rate is fixed at ");
    Serial.println(controlRate);
  } else {
    Serial.println("Control rate is adaptive");
  }

  ledController.setup();
  audioController.setup();
}

float lerp(float a, float b, float p) {
  return (b - a) * p + a;
}

float min(float a, float b) {
  if (a < b) {
    return a;
  }

  return b;
}

float max(float a, float b) {
  if (a > b) {
    return a;
  }

  return b;
}

void AnchorController::update() {
  // Interpolate LEDs
  unsigned int lerpPeriod = 1000 / getRate();
  unsigned int timeSinceTargetSet = millis() - lightTargetSetTime;
  float periodPortion = min((float)timeSinceTargetSet / lerpPeriod, 1);

  setBrightnessAll(lerp(lightTargetPrev, lightTarget, periodPortion));

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

void AnchorController::setBrightnessTarget(float target) {
  if (target < 0 || target > 1.0) {
    return;
  }

  unsigned long now = millis();

  // Measure actual rate
  float timeSinceLast = now - lightTargetSetTime;
  lightTargetSetTime = now;
  float rateNow = 1000.0f / timeSinceLast;
  
  if (rateNow > MIN_CONTROL_RATE && rateNow < MAX_CONTROL_RATE) {
    // Update average
    float avg = measuredControlRate;
    avg -= avg / CONTROL_RATE_AVERAGE_WINDOW;
    avg += rateNow / CONTROL_RATE_AVERAGE_WINDOW;

    measuredControlRate = avg;

    // Serial.print(timeSinceLast);
    // Serial.print("\t");
    // Serial.print(rateNow);
    // Serial.print("\t");
    // Serial.println(measuredControlRate);
  }

  // Update target
  lightTargetPrev = lightTarget;
  lightTarget = target;
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

void AnchorController::setUseFixedControlRate(bool useFixed) {
  useFixedControlRate = useFixed;

  EEPROM.write(6, useFixed);
  EEPROM.commit();
}

bool AnchorController::usingFixedControlRate() {
  return useFixedControlRate;
}

void AnchorController::setRate(float newRate) {
  if (newRate > MAX_CONTROL_RATE) {
    return;
  }

  controlRate = newRate;

  // Save the new control rate to EEPROM
  uint32_t fixedControlRate = controlRate * 1000;
  EEPROM.write(2, (fixedControlRate >> 24) & 0xff);
  EEPROM.write(3, (fixedControlRate >> 16) & 0xff);
  EEPROM.write(4, (fixedControlRate >> 8) & 0xff);
  EEPROM.write(5, fixedControlRate & 0xff);
  EEPROM.commit();
}

float AnchorController::getRate() {
  float rawRate = useFixedControlRate ? controlRate : measuredControlRate;
  return min(max(rawRate, MIN_CONTROL_RATE), MAX_CONTROL_RATE);
}

float AnchorController::getInternalTemperatureCelsius() {
  // Internal temperature sensor has a large random offset between chips
  // so it's only really useful for tracking deltas
  // https://www.esp32.com/viewtopic.php?p=20145&sid=01781d380a7a77ef03b8300fcae1bbc0#p20145
  return (temprature_sens_read() - 32) / 1.8;
}