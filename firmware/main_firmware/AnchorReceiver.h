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
  AnchorReceiver(unsigned int port) : udpPort(port) {}
  void begin();
  void update();

public:
  void setController(AnchorController *controller) {
    this->controller = controller;
  }

private:
  AnchorController *controller = nullptr;
  WiFiUDP udp;
  unsigned int udpPort;

  void handleCommand(struct DirectCmdPacket &cmd);
};
