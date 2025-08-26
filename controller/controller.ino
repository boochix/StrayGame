#include <Adafruit_NeoPixel.h>

// ---------------------- CONFIG ----------------------
#define NUM_MODULES 4
#define LEDS_PER_MODULE 8

// Pin definitions
const int buttonPins[4] = {2, 3, 4, 5};
const int joyXPin = A0;
const int joyYPin = A1;
const int pirPin  = 6;
const int neopixelPins[NUM_MODULES] = {7, 8, 9, 10};

// ---------------------- STRUCTS ----------------------
struct InputData {
  bool buttons[4];
  int joyX;
  int joyY;
  bool pir;
};

struct RGB {
  uint8_t r, g, b;
};

struct OutputData {
  RGB colors[NUM_MODULES]; // one RGB per NeoPixel ring
};

// ---------------------- GLOBALS ----------------------
Adafruit_NeoPixel rings[NUM_MODULES] = {
  Adafruit_NeoPixel(LEDS_PER_MODULE, neopixelPins[0], NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(LEDS_PER_MODULE, neopixelPins[1], NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(LEDS_PER_MODULE, neopixelPins[2], NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(LEDS_PER_MODULE, neopixelPins[3], NEO_GRB + NEO_KHZ800)
};

unsigned long lastSend = 0;
const unsigned long sendInterval = 5; // ms → ~200 Hz

// ---------------------- SETUP ----------------------
void setup() {
  Serial.begin(115200);

  for (int i = 0; i < 4; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);
  }
  pinMode(pirPin, INPUT);

  for (int i = 0; i < NUM_MODULES; i++) {
    rings[i].begin();
    rings[i].show(); // clear
  }
}

// ---------------------- HELPERS ----------------------
void sendInputData() {
  InputData data;
  // Read buttons
  for (int i = 0; i < 4; i++) {
    data.buttons[i] = !digitalRead(buttonPins[i]); // active LOW
  }
  // Read joystick
  data.joyX = analogRead(joyXPin);
  data.joyY = analogRead(joyYPin);
  // Read PIR
  data.pir = digitalRead(pirPin);

  // Send raw struct bytes
  Serial.write((uint8_t*)&data, sizeof(data));
}

void applyOutputData(const OutputData& out) {
  for (int i = 0; i < NUM_MODULES; i++) {
    for (int j = 0; j < LEDS_PER_MODULE; j++) {
      rings[i].setPixelColor(j, rings[i].Color(out.colors[i].r, out.colors[i].g, out.colors[i].b));
    }
    rings[i].show();
  }
}

// ---------------------- MAIN LOOP ----------------------
void loop() {
  unsigned long now = millis();

  // Send inputs every 5 ms (~200 Hz)
  if (now - lastSend >= sendInterval) {
    sendInputData();
    lastSend = now;
  }

  // Non-blocking check for new LED data
  while (Serial.available() >= sizeof(OutputData)) {
    OutputData out;
    Serial.readBytes((char*)&out, sizeof(out));
    applyOutputData(out);
  }
}
