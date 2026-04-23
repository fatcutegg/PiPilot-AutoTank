import cv2
import numpy as np
import time
import os
from tensorflow.keras.models import load_model

# --- 1. Load the trained model ---
# --- 1. 学習済みモデルの読み込み ---
print("Loading model...")
model = load_model('./models/model-006.h5', compile=False)
print("✅ Model loaded successfully!")

actions = ["LEFT", "RIGHT", "FORWARD", "BACKWARD", "STOP"]

print("🚀 Starting vision system via rpicam system call...")

try:
    while True:
        # --- 2. Core modification: Capture a single snapshot via system command ---
        # --- 2. 核心的な修正：システムコマンドを使用してスナップショットを1枚キャプチャする ---
        # -n: No preview window / プレビューウィンドウを表示しない
        # -t 1: Minimum delay for fast capture / 高速キャプチャのための最小遅延
        # --width/height: Match the input size of your model to reduce CPU overhead
        # --width/height: CPU負荷を軽減するため、モデルの入力サイズに合わせる
        os.system("rpicam-still -n -t 1 -o snap.jpg --width 160 --height 120 --immediate")
        
        # --- 3. Read the captured image ---
        # --- 3. キャプチャした画像を読み込む ---
        frame = cv2.imread("snap.jpg")
        
        if frame is None:
            print("⚠️ Failed to grab snapshot, retrying...")
            time.sleep(0.1)
            continue
        
        # --- 4. Pre-processing (must match your training pipeline) ---
        # --- 4. 前処理（学習時のパイプラインと一致させる） ---
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_tensor = np.expand_dims(img, axis=0).astype(np.float32) / 255.0
        
        # --- 5. AI Inference ---
        # --- 5. AI 推論 ---
        prediction = model.predict(img_tensor, verbose=0)
        action_idx = np.argmax(prediction)
        confidence = np.max(prediction)
        
        # --- 6. Draw results and save for web/debug viewing ---
        # --- 6. 結果を描画し、デバッグ用に保存する ---
        text = f"{actions[action_idx]} ({confidence:.2f})"
        cv2.putText(frame, text, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.imwrite('debug.jpg', frame)
        
        print(f"Prediction: {text}")

except KeyboardInterrupt:
    print("\nVerification stopped.")