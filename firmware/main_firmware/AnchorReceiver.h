#pragma once

#include <WiFiUdp.h>

#include "AnchorController.h"

struct DirectCmdPacket {
  float brightness;
  float offsetMillis;
  float volume;
};

struct BehaviorCmdPacket {
};

class AnchorReceiver {
public:
  AnchorReceiver(AnchorController &_controller, unsigned int port) : controller(_controller), udpPort(port) {}
  void begin();
  void update();
  void setPacketOffset(unsigned int offset);

private:
  AnchorController &controller;
  WiFiUDP udp;
  unsigned int udpPort;

  // Offset in the packet for our command
  unsigned int packetOffset;

  void handleCommand(struct DirectCmdPacket &cmd);
};
