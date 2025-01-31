#include "AnchorReceiver.h"

void AnchorReceiver::handleCommand(struct DirectCmdPacket &cmd) {
  controller->setBrightnessTarget(cmd.brightness);
  controller->setVolume(cmd.volume);
  controller->setTrack(cmd.track);
}

void AnchorReceiver::begin() {
  udp.begin(udpPort);
}

bool AnchorReceiver::update() {
  int packetSize = udp.parsePacket();

  if (packetSize == 0) {
    // Nothing to process
    return false;
  }

  uint8_t packet[PACKET_SIZE] = {0};
  const int len = udp.read(packet, sizeof(packet));

  if (len != PACKET_SIZE) {
    // Invalid or not for us
    return false;
  }

  unsigned int packetOffset = controller->getPacketOffset();
  uint8_t *cmdData = &packet[packetOffset * CMD_DATA_SIZE];

  uint8_t mode = cmdData[0];

  if (mode == 0) {
    struct DirectCmdPacket cmd = {
      .brightness = (float)((cmdData[1] << 8) | cmdData[2]) / 0xffff,
      .track = (cmdData[3] << 8) | cmdData[4],
      .volume = (float)((cmdData[5] << 8) | cmdData[6]) / 0xffff,
    };

    handleCommand(cmd);
  } else if (mode == 1) {
    // TODO: implement behavior commands
  }

  return true;
}
