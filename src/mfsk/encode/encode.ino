#define WORDCLK 8  // word load clock
#define FREQUPD 9  // freq update
#define DATA 10
#define RESET 11

#define pulseHigh(pin) \
  { \
    digitalWrite(pin, HIGH); \
    digitalWrite(pin, LOW); \
  }

const double base_freq = 2000000.0;  // 20 MHz to stay well within the 40 MHz clean signal limit of the AD9850
const double spacing = 250.0;        // 250 Hz spacing

const double fsk_freqs[16] = {
  base_freq,
  base_freq + spacing,
  base_freq + (2 * spacing),
  base_freq + (3 * spacing),
  base_freq + (4 * spacing),
  base_freq + (5 * spacing),
  base_freq + (6 * spacing),
  base_freq + (7 * spacing),
  base_freq + (8 * spacing),
  base_freq + (9 * spacing),
  base_freq + (10 * spacing),
  base_freq + (11 * spacing),
  base_freq + (12 * spacing),
  base_freq + (13 * spacing),
  base_freq + (14 * spacing),
  base_freq + (15 * spacing)
};

const byte message[] = { 0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 };
const int message_len = sizeof(message);

const baud = 5;
const symbol_duration = 1000 / baud;  // symbol duration is in ms
const double DDS_CLOCK = 125000000.0; // clock freq of the DDS (not the clock generator)

void setup() {
  // put your setup code here, to run once:
  pinMode(WORDCLK, OUTPUT);
  pinMode(FREQUPD, OUTPUT);
  pinMode(DATA, OUTPUT);
  pinMode(RESET, OUTPUT);


  // Switches ADF9850 from Parallel to Serial Mode
  pulseHigh(RESET);
  pulseHigh(WORDCLK);
  pulseHigh(FREQUPD);
}

void loop() {
  // put your main code here, to run repeatedly:

  for (int i = 0; i < message_len; i++) {
    byte current_symbol = message[i];

    if (current_symbol < 16) {
      sendFrequency(fsk_freqs[current_symbol]);
    }
    delay(symbol_duration);
  }
}

void sendFrequency(double freq) {
  uint32_t tuning_word = freq * 4294967296.0 / DDS_CLOCK;

  for (int b = 0; b < 4; b++, tuning_word >>= 8) {
    tfr_byte(tuning_word & 0xFF); // extracts lowest 8 bits of the 32-bit tuning word
  }

  tfr_byte(0x00);
  pulseHigh(FREQUPD);
  
}
