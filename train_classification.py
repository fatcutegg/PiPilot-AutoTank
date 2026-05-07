import os
import cv2
import csv
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import config

# --- 設定 (Settings) ---
ACTIVE_MODE = "EDUCATION"
DATA_DIR = config.PATHS[ACTIVE_MODE]["dataset_dir"]
LOG_FILE = config.PATHS[ACTIVE_MODE]["log_file"]
MODEL_PATH = config.PATHS[ACTIVE_MODE]["model_path"]

IMG_HEIGHT, IMG_WIDTH = 120, 160

# アクションの定義
ACTIONS = ["STOP", "UP", "DOWN", "LEFT", "RIGHT"]
NUM_CLASSES = len(ACTIONS)

def action_to_id(action_str):
    if action_str in ACTIONS:
        return ACTIONS.index(action_str)
    return 0

def load_data():
    """
    CSVから画像パスとアクションラベル(文字列)を読み込み、前処理を行う。
    """
    images = []
    labels = []
    
    if not os.path.isfile(LOG_FILE):
        print(f"Error: {LOG_FILE} が見つかりません。")
        return None, None

    print(f"=== {ACTIVE_MODE} データの読み込み開始 ===")
    with open(LOG_FILE, 'r') as f:
        reader = csv.reader(f)
        next(reader) # ヘッダーをスキップ
        for row in reader:
            if len(row) < 2:
                continue
                
            img_path = os.path.join(DATA_DIR, row[0])
            action_str = row[1]
            
            img = cv2.imread(img_path)
            if img is None:
                continue
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            action_id = action_to_id(action_str)
            
            images.append(img)
            labels.append(action_id)

    X = np.array(images, dtype=np.float32) / 255.0
    y = np.array(labels, dtype=np.int32)
    
    print(f"合計 {len(X)} 枚の画像を読み込みました。")
    return X, y

def build_classification_model():
    """
    5分類を出力するためのモデル (Classification Model) を構築する。
    教育目的のために構造は非常にシンプルに保つ。
    """
    model = Sequential([
        Input(shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
        
        Conv2D(24, (5, 5), strides=(2, 2), activation='relu'),
        Conv2D(36, (5, 5), strides=(2, 2), activation='relu'),
        Conv2D(48, (5, 5), strides=(2, 2), activation='relu'),
        Conv2D(64, (3, 3), activation='relu'),
        Conv2D(64, (3, 3), activation='relu'),
        
        Flatten(),
        Dense(100, activation='relu'),
        Dropout(0.2),
        Dense(50, activation='relu'),
        
        # 出力層: 5クラス (Softmax)
        Dense(NUM_CLASSES, activation='softmax')
    ])
    
    model.compile(
        optimizer=Adam(learning_rate=0.001), 
        loss='sparse_categorical_crossentropy', 
        metrics=['accuracy']
    )
    return model

if __name__ == "__main__":
    X, y = load_data()
    if X is None or len(X) == 0:
        exit(1)
        
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("\n=== モデルの構築 (Building Model) ===")
    model = build_classification_model()
    model.summary()
    
    print("\n=== 学習開始 (Training) ===")
    model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=20,
        batch_size=32,
        shuffle=True
    )
    
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    model.save(MODEL_PATH)
    print(f"\n✅ 教育用分類モデルの保存が完了しました: {MODEL_PATH}")
