const int GREEN_PIN = 8;
const int YELLOW_PIN = 9;
const int RED_PIN = 10;

void setup() {
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(YELLOW_PIN, OUTPUT);
  pinMode(RED_PIN, OUTPUT);
  digitalWrite(GREEN_PIN, LOW);
  digitalWrite(YELLOW_PIN, LOW);
  digitalWrite(RED_PIN, LOW);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char signal = Serial.read();
    digitalWrite(GREEN_PIN, LOW);
    digitalWrite(YELLOW_PIN, LOW);
    digitalWrite(RED_PIN, LOW);
    if (signal == 'G') {
      digitalWrite(GREEN_PIN, HIGH);
    } else if (signal == 'Y') {
      digitalWrite(YELLOW_PIN, HIGH);
    } else if (signal == 'R') {
      digitalWrite(RED_PIN, HIGH);
    }
  }
}
