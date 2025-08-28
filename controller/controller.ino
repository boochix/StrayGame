// Arduino sketch for paw controller with 5 buttons and 5 NeoPixel strips

#include <Adafruit_NeoPixel.h>

#define NUM_LEDS 8      // Number of LEDs per strip (adjust as needed)
#define NUM_TOES 4      // Number of toe buttons/strips
#define PALM_PIN 9      // Palm NeoPixel data pin
#define PALM_BTN 4      // Palm button pin (space)
#define SCENE_COLOR_COUNT 5

// Toe pins and button pins
const int toeLedPins[NUM_TOES] = {5, 6, 7, 8};   // NeoPixel data pins for toes
const int toeBtnPins[NUM_TOES] = {10, 11, 12, 13}; // Button pins for toes (A,B,C,D)

// NeoPixel objects
Adafruit_NeoPixel toeStrips[NUM_TOES] = {
  Adafruit_NeoPixel(NUM_LEDS, toeLedPins[0], NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(NUM_LEDS, toeLedPins[1], NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(NUM_LEDS, toeLedPins[2], NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(NUM_LEDS, toeLedPins[3], NEO_GRB + NEO_KHZ800)
};
Adafruit_NeoPixel palmStrip(NUM_LEDS, PALM_PIN, NEO_GRB + NEO_KHZ800);

// Scene colors for palm LED
uint32_t sceneColors[SCENE_COLOR_COUNT] = {
  0x00FF00, // start - green
  0x0000FF, // road - blue
  0xFF8000, // market - orange
  0xFFFF00, // sunny - yellow
  0xFF00FF  // stream/ending - magenta
};

String inputString = "";
bool stringComplete = false;

// State variables
String scene = "start";
int lives = 4;
int heartsFlashing = 0;
unsigned long lastFlash = 0;
bool flashState = false;

void setup() {
  Serial.begin(9600);
  inputString.reserve(50);

  // Init NeoPixels
  for (int i = 0; i < NUM_TOES; i++) toeStrips[i].begin();
  palmStrip.begin();

  // Init buttons
  for (int i = 0; i < NUM_TOES; i++) pinMode(toeBtnPins[i], INPUT_PULLUP);
  pinMode(PALM_BTN, INPUT_PULLUP);

  updateLeds();
}

void loop() {
  // Handle serial input
  if (stringComplete) {
    parseInput(inputString);
    inputString = "";
    stringComplete = false;
    updateLeds();
  }

  // Flashing logic
  if (heartsFlashing == 1) {
    unsigned long now = millis();
    if (now - lastFlash > 400) { // Flash every 400ms
      flashState = !flashState;
      flashLeds(flashState);
      lastFlash = now;
    }
  }

  // Button handling (send to Ren'Py)
  for (int i = 0; i < NUM_TOES; i++) {
    if (digitalRead(toeBtnPins[i]) == LOW) {
      Serial.println((char)('a' + i));
      delay(200); // Debounce
    }
  }
  if (digitalRead(PALM_BTN) == LOW) {
    Serial.println("space");
    delay(200);
  }
}

// Parse Ren'Py message: scene,lives,heartsFlashing
void parseInput(String msg) {
  int c1 = msg.indexOf(',');
  int c2 = msg.indexOf(',', c1 + 1);
  if (c1 > 0 && c2 > c1) {
    scene = msg.substring(0, c1);
    lives = msg.substring(c1 + 1, c2).toInt();
    heartsFlashing = msg.substring(c2 + 1).toInt();
  }
}

// Update LEDs for lives and scene
void updateLeds() {
  // Toes: show lives left (on = life, off = lost)
  for (int i = 0; i < NUM_TOES; i++) {
    for (int j = 0; j < NUM_LEDS; j++) {
      if (i < lives)
        toeStrips[i].setPixelColor(j, 0xFF0000); // Red for life
      else
        toeStrips[i].setPixelColor(j, 0x000000); // Off for lost
    }
    toeStrips[i].show();
  }

  // Palm: color by scene
  palmStrip.fill(getSceneColor(scene), 0, NUM_LEDS);
  palmStrip.show();
}

// Flash all LEDs (on/off)
void flashLeds(bool on) {
  uint32_t color = on ? 0xFFFFFF : 0x000000;
  for (int i = 0; i < NUM_TOES; i++) {
    toeStrips[i].fill(color, 0, NUM_LEDS);
    toeStrips[i].show();
  }
  palmStrip.fill(color, 0, NUM_LEDS);
  palmStrip.show();
}

// Map scene name to color
uint32_t getSceneColor(String s) {
  if (s == "start") return sceneColors[0];
  if (s == "road") return sceneColors[1];
  if (s == "market") return sceneColors[2];
  if (s == "sunny") return sceneColors[3];
  if (s == "stream" || s == "ending") return sceneColors[4];
  return 0xFFFFFF; // Default white
}

// Serial event
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      stringComplete = true;
    } else {
      inputString += inChar;
    }
  }
}