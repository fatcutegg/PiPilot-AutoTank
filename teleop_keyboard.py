import sys
from sshkeyboard import listen_keyboard

# --- Tank Control Class ---
# --- 戦車制御クラス ---
class TankController:
    def __init__(self):
        print("--- Tank Teleop Initialized (SSH Mode) ---")
        print("Use Arrow Keys to drive. Press 'q' to quit.")

    def drive(self, direction):
        # Implementation for movement
        # 移動の実装
        print(f"[DRIVE]: {direction}")

    def stop(self):
        # Implementation for stopping
        # 停止の実装
        print("[DRIVE]: STOP")

car = TankController()

def press(key):
    # Mapping keys to directions
    # キーを方向にマッピングする
    if key == "up":
        car.drive("FORWARD")
    elif key == "down":
        car.drive("BACKWARD")
    elif key == "left":
        car.drive("LEFT")
    elif key == "right":
        car.drive("RIGHT")
    elif key == "q":
        print("Exiting...")
        sys.exit()

def release(key):
    # Stop when the key is released
    # キーが離されたら停止する
    car.stop()

# --- Start listening ---
# --- リスニングを開始する ---
listen_keyboard(on_press=press, on_release=release)