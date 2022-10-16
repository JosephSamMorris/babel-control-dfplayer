#pragma once

#include <WiFiUdp.h>

#include "AnchorController.h"

const int MAX_UNIT_COUNT = 180;
const int CMD_DATA_SIZE = 8;
const int PACKET_SIZE = MAX_UNIT_COUNT * CMD_DATA_SIZE;

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

private:
  AnchorController &controller;
  WiFiUDP udp;
  unsigned int udpPort;

  void handleCommand(struct DirectCmdPacket &cmd);
};
