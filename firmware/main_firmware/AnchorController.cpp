#include "AnchorController.h"
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif
uint8_t temprature_sens_read();
#ifdef __cplusplus
}
#endif

uint8_t temprature_sens_read();

float AnchorController::getInternalTemperatureCelsius() {
  // Internal temperature sensor has a large random offset between chips
  // so it's only really useful for tracking deltas
  // https://www.esp32.com/viewtopic.php?p=20145&sid=01781d380a7a77ef03b8300fcae1bbc0#p20145
  return (temprature_sens_read() - 32) / 1.8;
}
