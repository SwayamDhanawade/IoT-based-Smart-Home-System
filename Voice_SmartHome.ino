#include <Servo.h>

const int LED_PIN = 13;  // Pin for LED (lamp)
const int MOTOR_PIN = 9; // Pin for fan (DC motor)
const int SERVO_PIN = 12; // Pin for servo motor (door)

Servo myServo;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Set up LED and motor pins as OUTPUT
  pinMode(LED_PIN, OUTPUT);
  pinMode(MOTOR_PIN, OUTPUT);
  
  // Attach servo to the servo pin and set initial position to 90 (neutral/middle)
  myServo.attach(SERVO_PIN);
  myServo.write(90);
  
  // Initial feedback
  Serial.println("System ready. Awaiting commands...");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();  // Clean command input
    
    // Control the LED
    if (command.equalsIgnoreCase("LED_ON")) {
      digitalWrite(LED_PIN, HIGH);
      Serial.println("LED turned on");
    } else if (command.equalsIgnoreCase("LED_OFF")) {
      digitalWrite(LED_PIN, LOW);
      Serial.println("LED turned off");
      
    // Control the motor (fan)
    } else if (command.equalsIgnoreCase("MOTOR_ON")) {
      analogWrite(MOTOR_PIN, 255);  // Full speed
      Serial.println("Motor (fan) turned on");
    } else if (command.equalsIgnoreCase("MOTOR_OFF")) {
      analogWrite(MOTOR_PIN, 0);  // Turn off motor
      Serial.println("Motor (fan) turned off");
      
    // Control the servo (door)
    } else if (command.equalsIgnoreCase("SERVO_LEFT")) {
      myServo.write(0);  // Move to the left (0 degrees)
      Serial.println("Servo moved left (0 degrees)");
    } else if (command.equalsIgnoreCase("SERVO_RIGHT")) {
      myServo.write(180);  // Move to the right (180 degrees)
      Serial.println("Servo moved right (180 degrees)");
      
    } else {
      Serial.println("Unknown command received. Please try again.");
    }
  }
}
