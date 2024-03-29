const int buzzerPin = 13; // Connect the buzzer to pin 8

void setup() {
  Serial.begin(9600); // Initialize serial communication
  pinMode(buzzerPin, OUTPUT); // Set buzzer pin as output
}

void loop() {
  if (Serial.available() > 0) { // If data is available to read
    char command = Serial.read(); // Read the incoming command
    if (command == 'F') { // If the command is 'F' (indicating fall detected)
      tone(buzzerPin, 1000); // Turn on the buzzer at 1000 Hz frequency
      delay(1000); // Keep the buzzer on for 1 second
      noTone(buzzerPin); // Turn off the buzzer
    }
  }
}
