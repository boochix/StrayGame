#include <Adafruit_NeoPixel.h>

#define LED_PIN    13      // GPIO pin for NeoPixel
#define LED_COUNT  40      // Number of LEDs

const int btnPins[5] = { 26, 27, 14, 12, 25 }; 
const char keys[5]   = { 'a', 'b', 'c', 'd', '' };   

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();
  strip.setBrightness(100);
  strip.show();

  Serial.begin(115200);
  for (int i = 0; i < 5; i++) {
    pinMode(btnPins[i], INPUT_PULLUP); // buttons to GND
  }

  // Turn all LEDs red
  for (int i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, strip.Color(255, 0, 0)); // Red, Green, Blue
  }
  strip.show();
}

void loop() {
  // Handle buttons
  for (int i = 0; i < 5; i++) {
    if (digitalRead(btnPins[i]) == LOW) {
      Serial.println(keys[i]);   
      delay(200); // debounce
    }
  }
}
