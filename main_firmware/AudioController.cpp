#include "AudioController.h"

int track;    //the first song on the SD card
int currentTrack; 

void AudioController::setup() {
  playerSerial.begin(9600, SERIAL_8N1, 25, 26);

  player.begin(playerSerial);
  player.setTimeOut(500); // Serial comms timeout in ms
  player.outputDevice(DFPLAYER_DEVICE_SD);

  player.volume(0); // 0 to 30
  player.loop(track); // loop the audio
}

void AudioController::update() {
  // Nothing to do, update handled by player object
}


void AudioController::setTrack(int track) {
  if (track != currentTrack) {
    player.loop(track);
    currentTrack = track;
  }
}

void AudioController::setVolume(float rawVolume) {
  float newVolume = 30 * constrain(rawVolume, 0, 1);
  player.volume(newVolume);
}
