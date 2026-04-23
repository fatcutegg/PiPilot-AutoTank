import RPi.GPIO as GPIO
import time
import sys
from sshkeyboard import listen_keyboard

# --- BCM Mapping based on your table ---
# --- あなたのテーブルに基づいた BCM マッピング ---
# Pin 19 -> GPIO 10, Pin 21 -> GPIO 9
L_IN1, L_IN2 = 10, 9   
# Pin 22 -> GPIO 25, Pin 23 -> GPIO 11
R_IN1, R_IN2 = 25, 11  

class TankController:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.pins = [L_IN1, L_IN2, R_IN1, R_IN2]
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        
        # Self-test: Spin motors for 0.5s on start
        print("Self-testing motors...")
        self.move("UP")
        time.sleep(0.5)
        self.stop()
        print("--- Ready! Use Arrows to drive, 'q' to quit ---")

    def move(self, direction):
        # IN/IN Logic: One HIGH, One LOW
        if direction == "UP":
            GPIO.output(L_IN1, 1); GPIO.output(L_IN2, 0)
            GPIO.output(R_IN1, 1); GPIO.output(R_IN2, 0)
        elif direction == "DOWN":
            GPIO.output(L_IN1, 0); GPIO.output(L_IN2, 1)
            GPIO.output(R_IN1, 0); GPIO.output(R_IN2, 1)
        # ... Other directions ...

    def stop(self):
        for pin in self.pins: GPIO.output(pin, 0)

car = TankController()

def press(key):
    if key in ["up", "down", "left", "right"]:
        car.move(key.upper())
    elif key == "q":
        car.stop(); GPIO.cleanup(); sys.exit()

def release(key):
    if key in ["up", "down", "left", "right"]:
        car.stop()

listen_keyboard(on_press=press, on_release=release)