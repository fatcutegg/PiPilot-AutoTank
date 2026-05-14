import os
import csv
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Dropout, Input, BatchNormalization
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import sys
import random

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import config

# --- 設定 (Settings) ---
ACTIVE_MODE = config.ACTIVE_MODE
RES_DATA_DIR = config.PATHS["RESEARCH"]["dataset_dir"]
RES_LOG_FILE = config.PATHS["RESEARCH"]["log_file"]
EDU_DATA_DIR = config.PATHS["EDUCATION"]["dataset_dir"]
EDU_LOG_FILE = config.PATHS["EDUCATION"]["log_file"]

MODEL_PATH = config.PATHS["RESEARCH"]["model_path"]

IMG_HEIGHT, IMG_WIDTH = 120, 160
BATCH_SIZE = 32

def parse_data():
    """
    統一フォーマット (path, action, left_pwm, right_pwm) からデータを読み込む。
    PWM値が記録されている場合はそれを使用し、なければaction名からマッピングする。
    """
    image_paths = []
    labels = []
    
    # 読み込むログファイルの決定
    if os.path.isfile(RES_LOG_FILE):
        log_file = RES_LOG_FILE
        data_dir = RES_DATA_DIR
    elif os.path.isfile(EDU_LOG_FILE):
        log_file = EDU_LOG_FILE
        data_dir = EDU_DATA_DIR
    else:
        print("Error: ログファイルが見つかりません。")
        return None, None

    print(f"=== {log_file} を読み込み中 ===")

    # 1. データの読み込み
    all_rows = []
    header = []
    with open(log_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if len(row) >= 2:
                all_rows.append(row)

    # 列インデックスの特定
    try:
        path_idx = header.index('image_path')
        action_idx = header.index('action')
        # PWM値があるか確認
        l_idx = header.index('left_pwm')
        r_idx = header.index('right_pwm')
        has_real_pwm = True
    except ValueError:
        path_idx = 0
        action_idx = 1
        has_real_pwm = False

    # 2. クラスごとの分類 (平衡化のためaction名を使用)
    data_by_action = {}
    for row in all_rows:
        action = row[action_idx]
        if action not in data_by_action:
            data_by_action[action] = []
        data_by_action[action].append(row)

    # 3. 動的バランシング
    if "STOP" in data_by_action:
        other_counts = [len(v) for k, v in data_by_action.items() if k != "STOP"]
        max_other = max(other_counts) if other_counts else 0
        stop_limit = int(max_other * 1.5)
        
        print(f"--- データバランスの動的調整 (Dynamic Balancing) ---")
        balanced_rows = []
        for action, rows in data_by_action.items():
            if action == "STOP" and len(rows) > stop_limit:
                sampled = random.sample(rows, stop_limit)
                balanced_rows.extend(sampled)
            else:
                balanced_rows.extend(rows)
    else:
        balanced_rows = all_rows

    # 4. PWM値への変換
    EDU_PWM_MAP = {
        "STOP":  [0.0, 0.0],
        "UP":    [0.85, 0.85],
        "DOWN":  [-0.85, -0.85],
        "LEFT":  [-0.85, 0.85],
        "RIGHT": [0.85, -0.85]
    }

    for row in balanced_rows:
        img_p = row[path_idx]
        img_full_path = os.path.join(data_dir, img_p)
        if not os.path.exists(img_full_path):
            continue
            
        if has_real_pwm:
            # 実際のPWM値が記録されている場合はそれを使用
            pwm = [float(row[l_idx]) / 100.0, float(row[r_idx]) / 100.0]
        else:
            # アクション名からマッピング
            pwm = EDU_PWM_MAP.get(row[action_idx], [0.0, 0.0])
            
        image_paths.append(img_full_path)
        labels.append(pwm)

    print(f"合計 {len(image_paths)} 件のデータを読み込みました。")
    return image_paths, labels

def process_path(file_path, label):
    img = tf.io.read_file(file_path)
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.resize(img, [IMG_HEIGHT, IMG_WIDTH])
    img = img / 255.0
    return img, label

def create_dataset(image_paths, labels, batch_size=BATCH_SIZE, shuffle=True):
    ds = tf.data.Dataset.from_tensor_slices((image_paths, labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(image_paths))
    ds = ds.map(process_path, num_parallel_calls=tf.data.AUTOTUNE)
    ds = ds.batch(batch_size)
    ds = ds.prefetch(tf.data.AUTOTUNE)
    return ds

def build_regression_model():
    model = Sequential([
        Input(shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
        Conv2D(24, (5, 5), strides=(2, 2), activation='relu'),
        BatchNormalization(),
        Conv2D(36, (5, 5), strides=(2, 2), activation='relu'),
        BatchNormalization(),
        Conv2D(48, (5, 5), strides=(2, 2), activation='relu'),
        BatchNormalization(),
        Conv2D(64, (3, 3), activation='relu'),
        Conv2D(64, (3, 3), activation='relu'),
        Flatten(),
        Dense(100, activation='relu'),
        Dropout(0.3),
        Dense(50, activation='relu'),
        Dense(10, activation='relu'),
        Dense(2, activation='tanh')
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])
    return model

if __name__ == "__main__":
    image_paths, labels = parse_data()
    if image_paths is None or len(image_paths) == 0:
        exit(1)
    train_paths, val_paths, train_labels, val_labels = train_test_split(image_paths, labels, test_size=0.2, random_state=42)
    train_dataset = create_dataset(train_paths, train_labels, shuffle=True)
    val_dataset = create_dataset(val_paths, val_labels, shuffle=False)
    model = build_regression_model()
    model.fit(train_dataset, validation_data=val_dataset, epochs=30)
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    model.save(MODEL_PATH, save_format='h5')
    print(f"\n✅ 研究用回帰モデルの保存が完了しました: {MODEL_PATH}")
