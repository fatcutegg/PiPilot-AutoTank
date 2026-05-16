import os
import csv
import numpy as np
import tensorflow as tf
try:
    import tf_keras as keras
except ImportError:
    import tensorflow.keras as keras
from keras.models import Sequential
from keras.layers import Conv2D, Flatten, Dense, Dropout, Input, BatchNormalization, Activation
from keras.layers import RandomBrightness, RandomContrast
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from model_factory import build_regression_model
import config

# --- 設定 (Settings) ---
ACTIVE_MODE = "RESEARCH"
DATA_DIR = config.PATHS[ACTIVE_MODE]["dataset_dir"]
LOG_FILE = config.PATHS[ACTIVE_MODE]["log_file"]
MODEL_PATH = config.PATHS[ACTIVE_MODE]["model_path"]

# 画像のリサイズ先 (NVIDIA PilotNetに近い比率を保つ)
IMG_HEIGHT, IMG_WIDTH = 120, 160
BATCH_SIZE = 32

def parse_csv():
    """
    CSVから画像パスとPWM値(Labels)をリストとして読み込む。
    (Read image paths and PWM values from CSV as lists.)
    """
    image_paths = []
    labels = []
    
    if not os.path.isfile(LOG_FILE):
        print(f"Error: {LOG_FILE} が見つかりません。先にPiでデータ収集を行ってください。")
        return None, None

    print(f"=== {ACTIVE_MODE} データのパスを読み込み開始 ===")
    with open(LOG_FILE, 'r') as f:
        reader = csv.reader(f)
        next(reader) # ヘッダーをスキップ
        for row in reader:
            # 新フォーマット: [image_path, action_label, left_pwm, right_pwm]
            if len(row) < 4:
                continue
                
            img_path = os.path.join(DATA_DIR, row[0]) 
            if not os.path.exists(img_path):
                # print(f"Warning: {img_path} not found")
                continue
                
            left_pwm = float(row[2])
            right_pwm = float(row[3])
            
            # ニューラルネットワークのために、PWMを [-1.0, 1.0] に正規化する
            left_label = left_pwm / 100.0
            right_label = right_pwm / 100.0
            
            image_paths.append(img_path)
            labels.append([left_label, right_label])

    print(f"合計 {len(image_paths)} 件のデータを読み込みました。")
    return image_paths, labels

def process_path(file_path, label):
    """
    ファイルパスから画像を読み込み、前処理を行う関数。
    tf.data.Dataset.map で使用される。
    (Load image from file path and perform pre-processing. Used in tf.data.Dataset.map.)
    """
    # ファイルを読み込む
    img = tf.io.read_file(file_path)
    # JPEGとしてデコードし、RGBチャンネルを持つテンソルに変換
    img = tf.image.decode_jpeg(img, channels=3)
    # 160x120 にリサイズ
    img = tf.image.resize(img, [IMG_HEIGHT, IMG_WIDTH])
    # 正規化 (0.0~1.0)
    img = img / 255.0
    return img, label

def create_dataset(image_paths, labels, batch_size=BATCH_SIZE, shuffle=True):
    """
    効率的なデータローダー (tf.data.Dataset) を作成する。
    (Create an efficient data loader using tf.data.Dataset.)
    """
    ds = tf.data.Dataset.from_tensor_slices((image_paths, labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(image_paths))
    
    # 並列処理で画像を読み込み
    ds = ds.map(process_path, num_parallel_calls=tf.data.AUTOTUNE)
    ds = ds.batch(batch_size)
    ds = ds.prefetch(tf.data.AUTOTUNE)
    return ds


if __name__ == "__main__":
    image_paths, labels = parse_csv()
    if image_paths is None or len(image_paths) == 0:
        print("Error: No data found.")
        exit(1)
        
    # 学習用と検証用に分割 (80% Train, 20% Validation)
    train_paths, val_paths, train_labels, val_labels = train_test_split(
        image_paths, labels, test_size=0.2, random_state=42
    )
    
    train_dataset = create_dataset(train_paths, train_labels, shuffle=True)
    val_dataset = create_dataset(val_paths, val_labels, shuffle=False)
    
    print("\n=== モデルの構築 (Building Model) ===")
    model = build_regression_model()
    model.summary()
    
    print("\n=== 学習開始 (Training) ===")
    history = model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=30,
    )
    
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    model.save(MODEL_PATH)
    
    # また、互換性のために重みだけを保存する (Also save weights only for compatibility)
    weights_path = MODEL_PATH.replace(".h5", ".weights.h5")
    model.save_weights(weights_path)
    
    print(f"\n✅ 最適化されたモデルの保存が完了しました: {MODEL_PATH}")
    print(f"✅ 重みファイルの保存が完了しました: {weights_path}")
    print("このモデル/重みを樹莓派にRsyncし、autonomous_drive.pyで推論させます。")
