#pragma once

#include "Arduino.h"

class AudioController {
public:
  AudioController() : lastFilledWord(0), currentSample(0), currentVolume(0) {}
  void setup();
  void update();

  void setVolume(float newVolume);
private:
  const int opcodeCount = 17;
  const int dacTableStart1 = 2048 - 512;
  const int dacTableStart2 = dacTableStart1 - 512;
  const int totalSampleWords = 2048 - 512 - (opcodeCount + 1);
  const int totalSamples = totalSampleWords * 2;
  const int indexAddress = opcodeCount;
  const int bufferStart = indexAddress + 1;

  int lastFilledWord;
  long currentSample;

  float currentVolume;

  unsigned char nextSample();
};
