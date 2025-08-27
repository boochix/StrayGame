#define BTN_A 2
#define BTN_B 3
#define BTN_C 4
#define BTN_D 5
#define BTN_SPACE 6

void setup() {
  Serial.begin(115200);
  pinMode(BTN_A, INPUT_PULLUP);
  pinMode(BTN_B, INPUT_PULLUP);
  pinMode(BTN_C, INPUT_PULLUP);
  pinMode(BTN_D, INPUT_PULLUP);
  pinMode(BTN_SPACE, INPUT_PULLUP);
}

void loop() {
  if (!digitalRead(BTN_A)) Serial.println("A");
  if (!digitalRead(BTN_B)) Serial.println("B");
  if (!digitalRead(BTN_C)) Serial.println("C");
  if (!digitalRead(BTN_D)) Serial.println("D");
  if (!digitalRead(BTN_SPACE)) Serial.println("SPACE");

  delay(50); // debounce
}
