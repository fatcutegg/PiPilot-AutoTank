import time
import cv2
import numpy as np
import subprocess
import os
import sys
from teleop_keyboard import TankController
from model_factory import load_robust_model
import config

# --- 設定 (Settings) ---
ACTIVE_MODE = config.ACTIVE_MODE
FPS = 10
MODEL_PATH = config.PATHS[ACTIVE_MODE]["model_path"]
ACTIONS = ["STOP", "UP", "DOWN", "LEFT", "RIGHT"]

class AutonomousDriver:
    def __init__(self, car, model):
        self.car = car
        self.model = model
        self.running = True
        print(f"=== AI自律走行モード ({ACTIVE_MODE} Mode) ===")
        print("警告: 動き出します。停止するには Ctrl+C を押してください。")

    def drive_loop(self):
        cmd = [
            "rpicam-vid", "-t", "0", "--codec", "mjpeg", 
            "--width", "160", "--height", "120", 
            "--framerate", str(FPS), "-o", "-"
        ]
        
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            
            # Set the pipe to non-blocking to prevent stale/buffered frames
            import fcntl
            fd = process.stdout.fileno()
            fl = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
            
            bytes_buffer = b''
            print("🚀 カメラ映像ストリームを開始しました。")
            
            while self.running:
                # 1. 蓄積されたバッファをすべて読み出す (Read all available buffered data)
                while True:
                    try:
                        chunk = process.stdout.read(8192)
                        if not chunk:
                            break
                        bytes_buffer += chunk
                    except (IOError, ValueError):
                        break
                
                # 2. バッファから「最新の」完全なJPEGフレームを探す (Find the LATEST complete JPEG frame)
                last_jpg = None
                while True:
                    a = bytes_buffer.find(b'\xff\xd8')
                    b = bytes_buffer.find(b'\xff\xd9')
                    if a != -1 and b != -1 and a < b:
                        last_jpg = bytes_buffer[a:b+2]
                        bytes_buffer = bytes_buffer[b+2:] # 残りのバッファを保持
                    else:
                        break
                
                # 3. 最新フレームが取得できた場合のみ処理を実行 (Process only if a new frame is available)
                if last_jpg is not None:
                    frame = cv2.imdecode(np.frombuffer(last_jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    
                    if frame is not None:
                        # 1. 前処理
                        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        img_tensor = np.expand_dims(img, axis=0).astype(np.float32) / 255.0
                        
                        # 2. モード別推論 (Mode-Specific Inference)
                        t_start = time.time()
                        prediction = self.model.predict(img_tensor, verbose=0)[0]
                        infer_ms = (time.time() - t_start) * 1000
                        
                        if ACTIVE_MODE == "EDUCATION":
                            # 教育モード: 5分類 (Education Mode: 5-class Classification)
                            action_idx = np.argmax(prediction)
                            action = ACTIONS[action_idx]
                            
                            if action == "STOP":
                                self.car.stop()
                            else:
                                self.car.move(action)
                            print(f"[{time.strftime('%H:%M:%S')}] [AI {ACTIVE_MODE}] 予測アクション: {action:<5} (確信度: {prediction[action_idx]:.2f}) | 推論: {infer_ms:.1f}ms")
                            
                        else:
                            # 研究モード: 連続回帰 (Research Mode: Continuous Regression)
                            pred_left = prediction[0]
                            pred_right = prediction[1]
                            
                            raw_l = int(pred_left * 100)
                            raw_r = int(pred_right * 100)
                            
                            # Scale the raw power to overcome the physical deadzone (min_power)
                            def scale_power(power, min_p, max_p):
                                if power == 0:
                                    return 0
                                sign = 1 if power > 0 else -1
                                abs_p = min(max(abs(power), 0), 100)
                                return sign * int(min_p + (abs_p / 100.0) * (max_p - min_p))
                                
                            target_l = scale_power(raw_l, self.car.min_power, self.car.max_power)
                            target_right = scale_power(raw_r, self.car.min_power, self.car.max_power)
                            
                            # Final safety bounds clipping
                            target_l = max(min(target_l, self.car.max_power), -self.car.max_power)
                            target_right = max(min(target_right, self.car.max_power), -self.car.max_power)
                            
                            self.car.target_l = target_l
                            self.car.target_r = target_right
                            
                            print(f"[{time.strftime('%H:%M:%S')}] [AI {ACTIVE_MODE}] Target L: {target_l:>3}% (raw: {raw_l:>3}%), R: {target_right:>3}% (raw: {raw_r:>3}%) | 推論: {infer_ms:.1f}ms")
                        
                        # 操作間に1秒間のウェイトを導入 (Introduce 1s wait between operations)
                        time.sleep(1.0)
                else:
                    # バッファがまだ溜まっていない場合は少し待機してCPU負荷を下げる
                    time.sleep(0.05)
                        
        except KeyboardInterrupt:
            print("\nユーザーによって停止されました。 (Stopped by user.)")
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            process.terminate()
            self.car.stop()
            self.car.cleanup()
            sys.exit(0)

if __name__ == "__main__":
    if not os.path.exists(MODEL_PATH):
        print(f"Error: モデル {MODEL_PATH} が見つかりません。")
        print(f"現在のモードは {ACTIVE_MODE} です。先に学習を完了させてください。")
        sys.exit(1)
        
    print("AIモデルを読み込んでいます... (Loading Model...)")
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
    model = load_robust_model(MODEL_PATH)
    
    car = TankController()
    driver = AutonomousDriver(car, model)
    driver.drive_loop()
