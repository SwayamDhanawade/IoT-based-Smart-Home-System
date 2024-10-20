# Voice-Controlled Smart Home Using Arduino

## Description
This project enables you to control basic home appliances such as lights and a door using voice commands. It combines the power of Arduino and Python to create an interactive, easy-to-use voice-controlled system. By leveraging speech recognition and text-to-speech capabilities, users can control an LED light and a servo motor (which simulates a door) simply by speaking commands like “Light on” or “Door open.”

The system works through a Python script that listens for user commands via a microphone, translates them into text, and sends corresponding instructions to an Arduino board over a serial communication channel. The Arduino, in turn, responds by activating the LED light or rotating the servo motor to simulate opening or closing a door.

This project is beginner-friendly and demonstrates how you can integrate IoT and voice control into your home automation systems. It can be expanded further to control other appliances like fans, heating systems, or security locks.

## Key Features
- **Voice-Activated Control**: Use simple voice commands to control your appliances.
- **LED Lighting**: Turn a light on or off through voice commands.
- **Servo Motor (Door Control)**: Open or close a door using voice control.
- **Simple & Expandable**: Built with easily accessible components and simple software, making it easy to expand with additional devices.

## How It Works
1. The user speaks a command, such as “Light on” or “Door open,” into a microphone.
2. The Python script uses the Google Speech Recognition service to convert the spoken command into text.
3. The script then sends the corresponding instruction to the Arduino via a serial connection.
4. The Arduino reads the command and performs the action:
   - Turning on/off the LED.
   - Moving the servo motor to open/close the door.
5. The system gives feedback by speaking back to the user, acknowledging the action taken.

This project provides a simple and effective foundation for building voice-activated smart home systems. You can add more devices or sensors to it to create a fully functional smart home.