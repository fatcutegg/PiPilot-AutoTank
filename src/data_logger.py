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
        self.current_action = "STOP" # EDUCATIONモード用
        
        # ログファイルの初期化
        file_exists = os.path.isfile(LOG_FILE)
        self.csv_file = open(LOG_FILE, 'a', newline='')
        self.writer = csv.writer(self.csv_file)
        
        if not file_exists:
            if ACTIVE_MODE == "EDUCATION":
                self.writer.writerow(['image_path', 'action_label'])
            else:
                self.writer.writerow(['image_path', 'left_pwm', 'right_pwm'])
            
        print(f"=== 双軌制 データロガー (Dual-Mode Data Logger) ===")
        print(f"現在のモード: {ACTIVE_MODE}")
        print("準備完了: 'r'キーで録画開始/停止, 'q'キーで終了します。")

    def camera_loop(self):
        """rpicam-vid (libcamera) を使用して、メモリ上でMJPEGストリームを高速に読み取る。"""
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
        """画像とモードに応じたラベル（カテゴリ or PWM）をペアとして保存する"""
        timestamp = time.time()
        filename = f"img_{timestamp:.3f}.jpg"
        filepath = os.path.join(IMG_DIR, filename)
        
        # 1. 画像の保存
        cv2.imwrite(filepath, frame)
        
        # パスは相対パスで記録
        rel_path = os.path.join("images", filename)
        
        # 2. モードに基づくCSVへの記録
        if ACTIVE_MODE == "EDUCATION":
            self.writer.writerow([rel_path, self.current_action])
            log_msg = f"Action: {self.current_action}"
        else:
            current_l = self.car.current_l
            current_r = self.car.current_r
            self.writer.writerow([rel_path, current_l, current_r])
            log_msg = f"PWM: L={current_l}%, R={current_r}%"
            
        self.csv_file.flush() # データの即時書き込みを保証
        
        self.frame_count += 1
        if self.frame_count % 10 == 0:
            print(f"[Recording] 記録済みフレーム: {self.frame_count} ({log_msg})")

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
    
    # カメラスレッドの起動
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
