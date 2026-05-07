import sys
import os

MODE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fan_mode.txt")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 set_fan.py [auto | 0-100]")
        print("Examples:")
        print("  python3 set_fan.py auto   # Enable automatic temperature control")
        print("  python3 set_fan.py 0      # Turn off fan completely")
        print("  python3 set_fan.py 100    # Turn on fan at full speed")
        print("  python3 set_fan.py 50     # Turn on fan at 50% speed")
        sys.exit(1)

    mode = sys.argv[1].strip().upper()
    
    if mode != "AUTO":
        try:
            val = float(mode)
            if val < 0 or val > 100:
                print("Error: PWM value must be between 0 and 100.")
                sys.exit(1)
        except ValueError:
            print("Error: Invalid mode. Use 'auto' or a number between 0 and 100.")
            sys.exit(1)
            
    with open(MODE_FILE, "w") as f:
        f.write(mode + "\n")
        
    print(f"✅ Fan mode successfully set to: {mode}")

if __name__ == "__main__":
    main()
