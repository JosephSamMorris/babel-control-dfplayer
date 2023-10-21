#!/bin/bash

SOUND_HEADER_DIR="/Users/owentrueblood/Dropbox/Projects/Collaborations/Joseph Morris/Anchorage/Audio/audio_prep/headers"
OUTPUT_DIR=firmwares

mkdir -p "$OUTPUT_DIR"

for sound_header in "$SOUND_HEADER_DIR"/*.h; do
    rm -f sound.h
    rm -f -r build

    lang_name=$(basename "$sound_header" .h)
    echo "Compiling with $lang_name"

    cp "$sound_header" sound.h
    arduino-cli compile --export-binaries --fqbn esp32:esp32:esp32 main_firmware.ino

    cp build/esp32.esp32.esp32/main_firmware.ino.bin "$OUTPUT_DIR/$lang_name.bin"
done

