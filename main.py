import speech_recognition as sr
import pyttsx3
import serial
import time
import csv
import boto3
import os
from datetime import datetime

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set up the serial connection to Arduino
arduino = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)  # Wait for the connection to establish

# CSV file to log the commands
csv_file = "command_log.csv"

# AWS S3 Configuration
s3_bucket_name = "smart-home-system"
s3 = boto3.client('s3')

# Function to create an S3 bucket if it doesn't exist
def create_s3_bucket(bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} already exists.")
    except s3.exceptions.ClientError:
        # Bucket does not exist, so create it
        try:
            s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
                'LocationConstraint': 'us-west-1'})  # Adjust region as needed
            print(f"Bucket {bucket_name} created successfully.")
        except Exception as e:
            print(f"Failed to create bucket {bucket_name}: {e}")

# Function to upload the CSV file to S3
def upload_to_s3(file_name, bucket_name):
    try:
        s3.upload_file(file_name, bucket_name, file_name)
        print(f"Uploaded {file_name} to S3 bucket {bucket_name}")
    except Exception as e:
        print(f"Failed to upload {file_name} to S3: {e}")

# Function to log the command to a CSV file
def log_command(command):
    # Check if the file exists to decide whether to write the header
    file_exists = os.path.isfile(csv_file)
    
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write the header only if the file is new
        if not file_exists:
            writer.writerow(['Timestamp', 'Command'])
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([timestamp, command])
        print(f"Logged command: {command}")

# Function to speak a message
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for voice commands
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        print("Sorry, there was an error with the speech recognition service.")
        return ""

# Function to send command to Arduino
def send_command(command):
    arduino.write(command.encode())
    time.sleep(0.1)
    response = arduino.readline().decode().strip()
    print(f"Arduino response: {response}")

# Main function to control the smart home system
def main():
    speak("Welcome to your voice-controlled smart home.")
    
    # Create S3 bucket if it doesn't exist
    create_s3_bucket(s3_bucket_name)
    
    # Initialize the CSV file (header will be handled in the log_command function)
    
    while True:
        command = listen()
        
        # Handling light commands
        if "light on" in command:
            send_command("LED_ON")
            speak("Light turned on.")
            log_command("Light ON")
        elif "light off" in command:
            send_command("LED_OFF")
            speak("Light turned off.")
            log_command("Light OFF")
        
        # Handling fan commands
        elif "fan on" in command:
            send_command("MOTOR_ON")
            speak("Fan turned on.")
            log_command("Fan ON")
        elif "fan off" in command:
            send_command("MOTOR_OFF")
            speak("Fan turned off.")
            log_command("Fan OFF")
        
        # Handling door commands
        elif any(phrase in command for phrase in ["door open", "dor open", "store open"]):
            send_command("SERVO_LEFT")
            speak("Door opened.")
            log_command("Door OPEN")
        elif "door close" in command:
            send_command("SERVO_RIGHT")
            speak("Door closed.")
            log_command("Door CLOSE")
        
        # Exit command
        elif "exit" in command:
            speak("Goodbye!")
            log_command("System EXIT")
            break
        
        else:
            speak("Sorry, I didn't understand that command.")
            log_command("Unknown Command")
    
    # Upload the CSV log file to S3 after exiting
    upload_to_s3(csv_file, s3_bucket_name)

if __name__ == "__main__":
    main()
