import os
import cv2
import csv
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split

# --- 設定 (Settings) ---
DATA_DIR = "dataset"
LOG_FILE = os.path.join(DATA_DIR, "driving_log.csv")
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

# 画像のリサイズ先 (NVIDIA PilotNetに近い比率を保つ)
IMG_HEIGHT, IMG_WIDTH = 120, 160

def load_data():
    """
    CSVから画像パスとPWM値(Labels)を読み込み、
    NumPy配列として前処理(Pre-processing)を行う。
    """
    images = []
    labels = []
    
    if not os.path.isfile(LOG_FILE):
        print(f"Error: {LOG_FILE} が見つかりません。先にPiでデータ収集を行ってください。")
        return None, None

    print("=== データの読み込み開始 (Loading Data) ===")
    with open(LOG_FILE, 'r') as f:
        reader = csv.reader(f)
        next(reader) # ヘッダーをスキップ
        for row in reader:
            if len(row) < 3:
                continue
                
            img_path = os.path.join(DATA_DIR, row[0])
            left_pwm = float(row[1])
            right_pwm = float(row[2])
            
            # 画像の読み込みとRGB変換
            img = cv2.imread(img_path)
            if img is None:
                continue
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # ニューラルネットワークのために、PWMを [-1.0, 1.0] に正規化する
            # 最大電力が100だと仮定して100で割る
            left_label = left_pwm / 100.0
            right_label = right_pwm / 100.0
            
            images.append(img)
            labels.append([left_label, right_label])

    # TensorFlow用に正規化 (0~255 -> 0.0~1.0)
    X = np.array(images, dtype=np.float32) / 255.0
    y = np.array(labels, dtype=np.float32)
    
    print(f"合計 {len(X)} 枚の画像を読み込みました。")
    return X, y

def build_regression_model():
    """
    連続的なPWMを出力するための回帰モデル (Regression Model) を構築する。
    NVIDIAの自動運転モデル(PilotNet)にインスパイアされた軽量CNN構造。
    """
    model = Sequential([
        Input(shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
        
        # 特徴抽出 (Feature Extraction)
        Conv2D(24, (5, 5), strides=(2, 2), activation='relu'),
        Conv2D(36, (5, 5), strides=(2, 2), activation='relu'),
        Conv2D(48, (5, 5), strides=(2, 2), activation='relu'),
        Conv2D(64, (3, 3), activation='relu'),
        Conv2D(64, (3, 3), activation='relu'),
        
        Flatten(),
        
        # 回帰のための全結合層 (Fully Connected Layers)
        Dense(100, activation='relu'),
        Dropout(0.2), # 過学習防止
        Dense(50, activation='relu'),
        Dropout(0.2),
        Dense(10, activation='relu'),
        
        # 出力層: 2ノード (左PWM, 右PWM), tanhで -1.0 ~ 1.0 に収める
        Dense(2, activation='tanh')
    ])
    
    # 損失関数は Mean Squared Error (MSE) を使用する
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])
    return model

if __name__ == "__main__":
    X, y = load_data()
    if X is None or len(X) == 0:
        exit(1)
        
    # 学習用と検証用に分割 (80% Train, 20% Validation)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("\n=== モデルの構築 (Building Model) ===")
    model = build_regression_model()
    model.summary()
    
    print("\n=== 学習開始 (Training) ===")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=30,           # エポック数はデータの複雑さに応じて調整
        batch_size=32,
        shuffle=True
    )
    
    model_save_path = os.path.join(MODEL_DIR, "end2end_tank.h5")
    model.save(model_save_path)
    print(f"\n✅ モデルの保存が完了しました: {model_save_path}")
    print("このモデルを樹莓派にRsyncし、autonomous_drive.pyで推論させます。")
