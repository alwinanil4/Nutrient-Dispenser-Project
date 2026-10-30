// Real-Time Nutrient Dispenser: Arduino side
// Serial '1' = Healthy (Green), '2' = Chlorosis (Yellow),
// '3' = Transpiration Stress (Red), '0' = All OFF

const int GREEN_LED  = 8;
const int YELLOW_LED = 9;
const int RED_LED    = 10;

void allOff() {
  digitalWrite(GREEN_LED, LOW);
  digitalWrite(YELLOW_LED, LOW);
  digitalWrite(RED_LED, LOW);
}

void setup() {
  pinMode(GREEN_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  allOff();

  Serial.begin(9600);
  Serial.println("Arduino ready. Send 0, 1, 2 or 3.");
}

void loop() {
  if (Serial.available() > 0) {
    char signal = Serial.read();

    if (signal == '1') {
      allOff();
      digitalWrite(GREEN_LED, HIGH);
      Serial.println("Healthy -> GREEN");
    }
    else if (signal == '2') {
      allOff();
      digitalWrite(YELLOW_LED, HIGH);
      Serial.println("Chlorosis -> YELLOW");
    }
    else if (signal == '3') {
      allOff();
      digitalWrite(RED_LED, HIGH);
      Serial.println("Transpiration Stress -> RED");
    }
    else if (signal == '0') {
      allOff();
      Serial.println("No leaf -> ALL OFF");
    }
    // anything else is ignored
  }
}