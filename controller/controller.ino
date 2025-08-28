#include <Adafruit_NeoPixel.h>

// ---------------- CONFIG ----------------
#define PIN_STRIP 12           // NeoPixel data pin
#define NUM_LEDS 40            // 5 segments × 8 LEDs each
#define SEGMENT_SIZE 8

// Button pins
int buttonPins[5] = {32, 33, 25, 26, 27}; // A, B, C, D, Space

Adafruit_NeoPixel strip(NUM_LEDS, PIN_STRIP, NEO_GRB + NEO_KHZ800);

// Game state (from Ren’Py)
int lives = 5;
bool heartsFlashing = false;

// Button debounce
unsigned long lastPress[5] = {0};
const unsigned long debounceDelay = 200;

// Flash timer
unsigned long lastFlash = 0;
bool flashOn = false;

void setup() {
  Serial.begin(115200);
  strip.begin();
  strip.show();
  for (int i = 0; i < 5; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);
  }
}

void loop() {
  // 1. Check buttons
  for (int i = 0; i < 5; i++) {
    if (digitalRead(buttonPins[i]) == LOW) {
      unsigned long now = millis();
      if (now - lastPress[i] > debounceDelay) {
        lastPress[i] = now;
        // Send button letter
        if (i == 4) Serial.println("SPACE");
        else Serial.println(String(char('A' + i)));
      }
    }
  }

  // 2. Read incoming serial from Ren’Py
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    parseState(line);
  }

  // 3. Update LEDs
  updateLEDs();
}

void parseState(String line) {
  line.trim();
  if (line.length() == 0) return;

  int comma = line.indexOf(',');
  if (comma == -1) return;

  lives = line.substring(0, comma).toInt();
  heartsFlashing = (line.substring(comma + 1).toInt() == 1);
}

void updateLEDs() {
  strip.clear();

  // --- Toes (A-D) = lives ---
  for (int i = 0; i < 4; i++) {
    if (i < lives) {
      setSegmentColor(i, strip.Color(255, 0, 0)); // Red = life
    }
  }

  // --- Palm (Space) = always white (may flash) ---
  if (heartsFlashing) {
    unsigned long now = millis();
    if (now - lastFlash > 500) {
      flashOn = !flashOn;
      lastFlash = now;
    }
    if (flashOn) setSegmentColor(4, strip.Color(255, 255, 255));
  } else {
    setSegmentColor(4, strip.Color(255, 255, 255));
  }

  strip.show();
}

// Helper: set one segment
void setSegmentColor(int segment, uint32_t color) {
  int start = segment * SEGMENT_SIZE;
  for (int i = 0; i < SEGMENT_SIZE; i++) {
    strip.setPixelColor(start + i, color);
  }
}
