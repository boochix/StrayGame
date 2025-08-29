#include <Adafruit_NeoPixel.h>

#define LED_PIN    13      // GPIO pin for NeoPixel
#define LED_COUNT  40      // Number of LEDs

const int btnPins[5] = { 26, 27, 14, 12, 25 }; 
const char keys[5]   = { 'a', 'b', 'c', 'd', 'e' };   

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

unsigned long lastUpdate = 0; 
int rainbowHue = 0;

// Non-blocking rainbow animation
void rainbowStep() {
  for (int i = 0; i < strip.numPixels(); i++) {
    int pixelHue = rainbowHue + (i * 65536L / strip.numPixels());
    strip.setPixelColor(i, strip.gamma32(strip.ColorHSV(pixelHue)));
  }
  strip.show();

  rainbowHue += 256;     // controls speed of rainbow shift
  if (rainbowHue >= 5 * 65536) rainbowHue = 0;
}

void setup() {
  strip.begin();
  strip.show();
  strip.setBrightness(100);

  Serial.begin(115200);
  for (int i = 0; i < 5; i++) {
    pinMode(btnPins[i], INPUT_PULLUP); // buttons to GND
  }
}

void loop() {
  // Handle buttons
  for (int i = 0; i < 5; i++) {
    if (digitalRead(btnPins[i]) == LOW) {
      Serial.println(keys[i]);   
      delay(500); // debounce
    }
  }

  // Update rainbow every 20ms (non-blocking)
  if (millis() - lastUpdate > 20) {
    rainbowStep();
    lastUpdate = millis();
  }
}
