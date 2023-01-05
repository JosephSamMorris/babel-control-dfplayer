#!/bin/bash

PORT=/dev/cu.usbserial-AC01N5OB
FIRMWARE="$1"

ESP32_PKG=/Users/owentrueblood/Library/Arduino15/packages/esp32
ESP32_TOOL=$ESP32_PKG/tools/esptool_py/4.2.1/esptool
ESP32_BOOTAPP=$ESP32_PKG/hardware/esp32/2.0.5/tools/partitions/boot_app0.bin
ESP32_BOOTLOADER=$ESP32_PKG/hardware/esp32/2.0.5/tools/sdk/esp32/bin/bootloader_qio_80m.bin

"$ESP32_TOOL" --chip esp32 --port "$PORT" --baud 921600 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 80m --flash_size detect 0xe000 "$ESP32_BOOTAPP" 0x1000 "$ESP32_BOOTLOADER" 0x10000 "$FIRMWARE"
