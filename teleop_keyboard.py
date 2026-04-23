import RPi.GPIO as GPIO
import time
import sys
from sshkeyboard import listen_keyboard

# --- BCM Mapping ---
L_IN1, L_IN2 = 10, 9 
R_IN1, R_IN2 = 25, 11 

class TankController:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.pins = [L_IN1, L_IN2, R_IN1, R_IN2]
        
        # Initialize PWM on all pins
        # 全てのピンで PWM を初期化する
        self.pwms = []
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            # Frequency: 1000Hz (Reduces high-pitched noise)
            # 周波数：1000Hz（高周波ノイズを低減）
            p = GPIO.PWM(pin, 1000) 
            p.start(0)
            self.pwms.append(p)
        
        # --- ADJUST POWER HERE (0 to 100) ---
        # --- ここでパワーを調整する (0 から 100) ---
        self.power = 85  # Higher value to overcome stall torque / 起動トルクを確保するため高めに設定
        
        print(f"Self-testing motors at {self.power}% power...")
        self.move("UP")
        time.sleep(0.5)
        self.stop()
        print(f"--- Ready! Power: {self.power}% ---")

    def move(self, direction):
        """Execute movement logic with PWM / PWMで移動ロジックを実行"""
        # IN/IN Logic: PWM on one pin, 0 on the other
        # IN/IN ロジック：一方のピンに PWM、他方のピンに 0
        if direction == "UP":
            self.pwms[0].ChangeDutyCycle(self.power); self.pwms[1].ChangeDutyCycle(0)
            self.pwms[2].ChangeDutyCycle(self.power); self.pwms[3].ChangeDutyCycle(0)
        elif direction == "DOWN":
            self.pwms[0].ChangeDutyCycle(0); self.pwms[1].ChangeDutyCycle(self.power)
            self.pwms[2].ChangeDutyCycle(0); self.pwms[3].ChangeDutyCycle(self.power)
        elif direction == "LEFT":
            self.pwms[0].ChangeDutyCycle(0); self.pwms[1].ChangeDutyCycle(self.power)
            self.pwms[2].ChangeDutyCycle(self.power); self.pwms[3].ChangeDutyCycle(0)
        elif direction == "RIGHT":
            self.pwms[0].ChangeDutyCycle(self.power); self.pwms[1].ChangeDutyCycle(0)
            self.pwms[2].ChangeDutyCycle(0); self.pwms[3].ChangeDutyCycle(self.power)

    def stop(self):
        """Stop all PWM output / 全ての PWM 出力を停止"""
        for p in self.pwms:
            p.ChangeDutyCycle(0)

    def cleanup(self):
        """Clean up GPIO / GPIO をクリーンアップ"""
        self.stop()
        for p in self.pwms:
            p.stop()
        GPIO.cleanup()

car = TankController()

def press(key):
    if key in ["up", "down", "left", "right"]:
        car.move(key.upper())
    elif key == "q":
        car.cleanup()
        sys.exit()

def release(key):
    if key in ["up", "down", "left", "right"]:
        car.stop()

listen_keyboard(on_press=press, on_release=release)