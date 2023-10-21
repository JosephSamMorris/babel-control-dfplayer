#pragma once

#include "Arduino.h"
#include "DFRobotDFPlayerMini.h"
#include <HardwareSerial.h>

class AudioController {
  public:
    AudioController() : playerSerial(1) {}
    void setup();
    void update();

    void setTrack(int track);
    void setVolume(float newVolume);
  private:
    HardwareSerial playerSerial;
    DFRobotDFPlayerMini player;
};
