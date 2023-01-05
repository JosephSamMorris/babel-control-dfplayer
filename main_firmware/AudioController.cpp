#include <esp32/ulp.h>
#include <driver/rtc_io.h>
#include <driver/dac.h>
#include <soc/rtc.h>

#include "sound.h"
#include "AudioController.h"

void AudioController::setup() {
  // Based on https://github.com/bitluni/ULPSoundESP32

  // Calculate the actual ULP clock
  unsigned long rtc_8md256_period = rtc_clk_cal(RTC_CAL_8MD256, 1000);

  Serial.print("rtc_clk_cal ");
  Serial.println(rtc_8md256_period);

  // HACK: we only have to do this because rtc_clk_cal returns zero after a
  // software reset. We should figure out why that happens and fix the root.
  if (rtc_8md256_period == 0) {
    rtc_8md256_period = 15744985;
    Serial.println("Falling back to hardcoded rtc_8md256_period");
  }

  unsigned long rtc_fast_freq_hz =
      1000000ULL * (1 << RTC_CLK_CAL_FRACT) * 256 / rtc_8md256_period;

  // Initialize DACs
  dac_output_enable(DAC_CHANNEL_1);
  dac_output_enable(DAC_CHANNEL_2);
  dac_output_voltage(DAC_CHANNEL_1, 128);
  dac_output_voltage(DAC_CHANNEL_2, 128);

  const int retAddress1 = 13;

  const int loopCycles = 84;
  const int dt = (rtc_fast_freq_hz / samplingRate) - loopCycles;
  if (dt < 0) {
    Serial.println("Sampling rate too high");
  }

  const ulp_insn_t mono[] = {
      // Reset offset register
      I_MOVI(R3, 0),
      // Delay to get the right sampling rate
      I_DELAY(dt), // 6 + dt
      // Reset sample index
      I_MOVI(R0, 0), // 6
      // Write the index back to memory for the main CPU
      I_ST(R0, R3, indexAddress), // 8
      // Divide index by two since we store two samples in each dword
      I_RSHI(R2, R0, 1), // 6
      // Load the samples
      I_LD(R1, R2, bufferStart), // 8
      // Get if odd or even sample
      I_ANDI(R2, R0, 1), // 6
      // Multiply by 8
      I_LSHI(R2, R2, 3), // 6
      // Shift the bits to have the right sample in the lower 8 bits
      I_RSHR(R1, R1, R2), // 6
      // Mask the lower 8 bits
      I_ANDI(R1, R1, 255), // 6
      // Multiply by 2
      I_LSHI(R1, R1, 1), // 6
      // Add start position
      I_ADDI(R1, R1, dacTableStart1), // 6
      // Jump to the DAC opcode
      I_BXR(R1), // 4
      // Here we get back from writing a sample
      // increment the sample index
      I_ADDI(R0, R0, 1), // 6
      // If reached end of the buffer, jump relative to index reset
      I_BGE(-13, totalSamples), // 4
      // Wait to get the right sample rate (2 cycles more to compensate the
      // index reset)
      I_DELAY((unsigned int)dt + 2), // 8 + dt
      // If not, jump absolute to where index is written to memory
      I_BXI(3) // 4
  };
  // Write io and jump back another 12 + 4

  size_t load_addr = 0;
  size_t size = sizeof(mono) / sizeof(ulp_insn_t);
  ulp_process_macros_and_load(load_addr, mono, &size);
  //  this is how to get the opcodes
  //  for(int i = 0; i < size; i++)
  //    Serial.println(RTC_SLOW_MEM[i], HEX);

  // Create DAC opcode tables
  for (int i = 0; i < 256; i++) {
    RTC_SLOW_MEM[dacTableStart1 + i * 2] = 0x1D4C0121 | (i << 10); // dac0
    RTC_SLOW_MEM[dacTableStart1 + 1 + i * 2] = 0x80000000 + retAddress1 * 4;
  }

  // Set all samples to 128 (silence)
  for (int i = 0; i < totalSampleWords; i++) {
    RTC_SLOW_MEM[bufferStart + i] = 0x8080;
  }

  // Start
  RTC_SLOW_MEM[indexAddress] = 0;
  ulp_run(0);
  while (RTC_SLOW_MEM[indexAddress] == 0) {
    delay(1);
  }
}

void AudioController::update() {
  const int currentSample = RTC_SLOW_MEM[indexAddress] & 0xffff;
  const int currentWord = currentSample >> 1;

  while (lastFilledWord != currentWord) {
    unsigned int w = nextSample();
    w |= nextSample() << 8;

    RTC_SLOW_MEM[bufferStart + lastFilledWord] = w;

    lastFilledWord++;

    if (lastFilledWord == totalSampleWords) {
      lastFilledWord = 0;
    }
  }
}

void AudioController::setOffsetMillis(unsigned int newOffsetMillis) {
  int offsetInSamples = newOffsetMillis * samplingRate / 1000;

  // Wrap if beyond the end of the audio
  lastFilledWord = offsetInSamples;
  lastFilledWord %= totalSampleWords;
}

void AudioController::setVolume(float newVolume) {
  currentVolume = constrain(newVolume, 0, 4);
}

unsigned char AudioController::nextSample() {
  static long pos = 0;

  if (pos >= sampleCount) {
    pos = 0;
  }

  return (unsigned char)((int)(currentVolume * samples[pos++]) + 128);
}
