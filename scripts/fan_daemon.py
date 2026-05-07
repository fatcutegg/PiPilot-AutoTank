import time
import os
import sys

# Try to import RPi.GPIO (will fail on Mac, but we run this on Pi)
try:
    import RPi.GPIO as GPIO
except ImportError:
    print("Warning: RPi.GPIO not found. This script should only run on Raspberry Pi.")
    sys.exit(1)

FAN_PIN = 14
PWM_FREQ = 100
WAIT_TIME = 2

# Temperature Curve Constants
TEMP_START = 48.0  # Temp to turn fan ON
TEMP_STOP = 42.0   # Temp to turn fan OFF (hysteresis)
TEMP_MAX = 60.0    # Temp for 100% speed
PWM_MIN = 40.0
PWM_MAX = 100.0

MODE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fan_mode.txt")

def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = float(f.read()) / 1000.0
        return temp
    except Exception as e:
        print(f"Error reading CPU temp: {e}")
        return 0.0

def get_mode():
    if not os.path.exists(MODE_FILE):
        return "AUTO"
    try:
        with open(MODE_FILE, "r") as f:
            mode = f.read().strip().upper()
            if mode == "":
                return "AUTO"
            return mode
    except Exception:
        return "AUTO"

def calculate_auto_pwm(temp, current_pwm):
    is_on = current_pwm > 0
    
    if not is_on:
        if temp >= TEMP_START:
            is_on = True
        else:
            return 0.0
            
    # If the fan is ON, wait until it drops below TEMP_STOP to turn OFF
    if temp < TEMP_STOP:
        return 0.0
        
    if temp >= TEMP_MAX:
        return 100.0
    
    # Linear interpolation between TEMP_STOP and TEMP_MAX
    fraction = (temp - TEMP_STOP) / (TEMP_MAX - TEMP_STOP)
    pwm = PWM_MIN + fraction * (PWM_MAX - PWM_MIN)
    return min(100.0, max(0.0, pwm))

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN, GPIO.OUT)
    
    pwm = GPIO.PWM(FAN_PIN, PWM_FREQ)
    pwm.start(0)
    
    print("Fan Daemon Started.")
    
    try:
        current_duty_cycle = 0.0
        while True:
            mode = get_mode()
            if mode == "AUTO":
                temp = get_cpu_temp()
                current_duty_cycle = calculate_auto_pwm(temp, current_duty_cycle)
            else:
                try:
                    current_duty_cycle = float(mode)
                    current_duty_cycle = min(100.0, max(0.0, current_duty_cycle))
                except ValueError:
                    current_duty_cycle = 0.0 # Fallback for invalid numeric input
            
            pwm.ChangeDutyCycle(current_duty_cycle)
            time.sleep(WAIT_TIME)
            
    except KeyboardInterrupt:
        print("Stopping Fan Daemon...")
    finally:
        pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
