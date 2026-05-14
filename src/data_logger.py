import os
import time
import csv
import cv2
import numpy as np
import subprocess
import threading
import sys
from sshkeyboard import listen_keyboard
from teleop_keyboard import TankController
import config

# --- 設定 (Settings) ---
ACTIVE_MODE = config.ACTIVE_MODE
FPS = 10                     # データ収集の目標フレームレート (10Hz)
DATA_DIR = config.PATHS[ACTIVE_MODE]["dataset_dir"]
IMG_DIR = os.path.join(DATA_DIR, "images")
LOG_FILE = config.PATHS[ACTIVE_MODE]["log_file"]

# ディレクトリの作成
os.makedirs(IMG_DIR, exist_ok=True)

class DataLogger:
    def __init__(self, car):
        self.car = car
        self.recording = False
        self.running = True
        self.frame_count = 0
        self.current_action = "STOP"
        
        # ログファイルの初期化 (Unified Format: path, action, left_pwm, right_pwm)
        file_exists = os.path.isfile(LOG_FILE)
        self.csv_file = open(LOG_FILE, 'a', newline='')
        self.writer = csv.writer(self.csv_file)
        
        if not file_exists:
            # モードに関わらずフルデータを保存するヘッダー
            self.writer.writerow(['image_path', 'action', 'left_pwm', 'right_pwm'])
            
        print(f"=== 統一データロガー (Unified Data Logger) ===")
        print(f"保存先: {DATA_DIR}")
        print("録画中、アクションとPWM値の両方を同時に記録します。")
        print("準備完了: 'r'キーで録画開始/停止, 'q'キーで終了します。")

    def camera_loop(self):
        """rpicam-vid を使用して画像をキャプチャし、録画中なら保存する。"""
        cmd = [
            "rpicam-vid", "-t", "0", "--codec", "mjpeg", 
            "--width", "160", "--height", "120", 
            "--framerate", str(FPS), "-o", "-"
        ]
        
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            bytes_buffer = b''
            
            while self.running:
                chunk = process.stdout.read(1024)
                if not chunk:
                    continue
                    
                bytes_buffer += chunk
                a = bytes_buffer.find(b'\xff\xd8')
                b = bytes_buffer.find(b'\xff\xd9')
                
                if a != -1 and b != -1:
                    jpg = bytes_buffer[a:b+2]
                    bytes_buffer = bytes_buffer[b+2:]
                    
                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    
                    if frame is not None and self.recording:
                        self.save_data(frame)
                        
        except Exception as e:
            print(f"Camera Error: {e}")
        finally:
            process.terminate()
            self.csv_file.close()

    def save_data(self, frame):
        """画像、アクション名、PWM値（L/R）をすべて保存する"""
        timestamp = time.time()
        filename = f"img_{timestamp:.3f}.jpg"
        filepath = os.path.join(IMG_DIR, filename)
        
        # 1. 画像の保存
        cv2.imwrite(filepath, frame)
        
        # 2. データの記録 (Unified Format)
        rel_path = os.path.join("images", filename)
        action = self.current_action
        l_pwm = self.car.current_l
        r_pwm = self.car.current_r
        
        self.writer.writerow([rel_path, action, l_pwm, r_pwm])
        self.csv_file.flush()
        
        self.frame_count += 1
        if self.frame_count % 10 == 0:
            print(f"[REC] {self.frame_count} frames | Action: {action:<5} | PWM: L={l_pwm:>3}, R={r_pwm:>3}")

    def toggle_recording(self):
        self.recording = not self.recording
        if self.recording:
            print("\n[REC START] データ収集を開始しました")
        else:
            print("\n[REC PAUSE] データ収集を一時停止しました")

# === メイン処理 ===
if __name__ == "__main__":
    car = TankController()
    logger = DataLogger(car)
    
    cam_thread = threading.Thread(target=logger.camera_loop, daemon=True)
    cam_thread.start()

    def press(key):
        if key in ["up", "down", "left", "right"]:
            action = key.upper()
            logger.current_action = action
            car.move(action)
        elif key == "r":
            logger.toggle_recording()
        elif key == "q":
            logger.running = False
            car.cleanup()
            sys.exit()

    def release(key):
        if key in ["up", "down", "left", "right"]:
            logger.current_action = "STOP"
            car.stop()

    listen_keyboard(on_press=press, on_release=release)
