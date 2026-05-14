import os
import cv2
import csv
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import sys
import random

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import config

# --- 設定 (Settings) ---
ACTIVE_MODE = config.ACTIVE_MODE
DATA_DIR = config.PATHS[ACTIVE_MODE]["dataset_dir"]
LOG_FILE = config.PATHS[ACTIVE_MODE]["log_file"]
MODEL_PATH = config.PATHS[ACTIVE_MODE]["model_path"]

IMG_HEIGHT, IMG_WIDTH = 120, 160

# アクションの定義 (Definition of Actions)
ACTIONS = ["STOP", "UP", "DOWN", "LEFT", "RIGHT"]
NUM_CLASSES = len(ACTIONS)

def action_to_id(action_str):
    if action_str in ACTIONS:
        return ACTIONS.index(action_str)
    return 0

def load_data():
    """
    CSVから画像パスとラベルを読み込み、自動的にデータバランスを調整して読み込む。
    統一フォーマット (path, action, L, R) と旧フォーマットの両方に対応。
    """
    if not os.path.isfile(LOG_FILE):
        print(f"Error: {LOG_FILE} が見つかりません。")
        return None, None

    # 1. まずCSVの全データをメモリに読み込む
    all_rows = []
    with open(LOG_FILE, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        
        # 列のインデックスを特定 (統一フォーマット対応)
        try:
            path_idx = header.index('image_path')
            action_idx = header.index('action')
        except ValueError:
            # 旧フォーマットの場合のデフォルト
            path_idx = 0
            action_idx = 1
            
        for row in reader:
            if len(row) > max(path_idx, action_idx):
                all_rows.append((row[path_idx], row[action_idx]))

    # 2. クラスごとにデータを分類する
    data_by_class = {action: [] for action in ACTIONS}
    for row in all_rows:
        img_p, action_str = row
        if action_str in data_by_class:
            data_by_class[action_str].append(row)

    # 3. 動的なサンプリング上限の計算 (Dynamic Balancing)
    other_counts = [len(rows) for action, rows in data_by_class.items() if action != "STOP"]
    max_other = max(other_counts) if other_counts else 0
    stop_limit = int(max_other * 1.5)
    
    print(f"\n--- データバランスの動的調整 (Dynamic Balancing) ---")
    balanced_samples = []
    for action, rows in data_by_class.items():
        if action == "STOP" and len(rows) > stop_limit:
            sampled = random.sample(rows, stop_limit)
            balanced_samples.extend(sampled)
            print(f"  - {action:<5}: {len(rows):>4} -> {len(sampled):>4} (Downsampled)")
        else:
            balanced_samples.extend(rows)
            print(f"  - {action:<5}: {len(rows):>4} (Original)")

    # 4. 画像データの読み込み
    images = []
    labels = []
    
    print(f"\n画像データのロード中...")
    for img_p, action_str in balanced_samples:
        img_full_path = os.path.join(DATA_DIR, img_p)
        img = cv2.imread(img_full_path)
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
        Dense(NUM_CLASSES, activation='softmax')
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

if __name__ == "__main__":
    X, y = load_data()
    if X is None or len(X) == 0:
        exit(1)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    model = build_classification_model()
    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=20, batch_size=32, shuffle=True)
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    model.save(MODEL_PATH)
    print(f"\n✅ 教育用分類モデルの保存が完了しました: {MODEL_PATH}")
