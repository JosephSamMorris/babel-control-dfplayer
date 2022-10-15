#pragma once

const float CLOSE_ENOUGH = 0.01;

class AnchorController {
public:
  AnchorController() : lightLimit(0), lightLimitConfirm(0) {}
  static float getInternalTemperatureCelsius();
  void setLightLimit(float newLimit);
  void confirmLightLimit(float newLimit);
  float getLightLimit();
private:
  float lightLimit;
  float lightLimitConfirm;
};
