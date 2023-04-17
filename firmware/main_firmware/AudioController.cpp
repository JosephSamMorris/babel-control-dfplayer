#include "AudioController.h"

void AudioController::setup() {
  playerSerial.begin(9600, SERIAL_8N1, 27, 14);

  player.begin(playerSerial);
  player.setTimeOut(500); // Serial comms timeout in ms
  player.outputDevice(DFPLAYER_DEVICE_SD);

  player.volume(0); // 0 to 30
  player.loop(1); // Play first song on SD card
}

void AudioController::update() {
  // Nothing to do, update handled by player object
}

void AudioController::setOffsetMillis(unsigned int newOffsetMillis) {
  // Unimplemented
}

void AudioController::setVolume(float rawVolume) {
  float newVolume = 30 * constrain(rawVolume, 0, 1);
  player.volume(newVolume);
}
