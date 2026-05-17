import os
import tensorflow as tf
try:
    import tf_keras as keras
except ImportError:
    import tensorflow.keras as keras
from keras.models import Sequential, load_model
from keras.layers import Conv2D, Flatten, Dense, Dropout, Input, BatchNormalization, Activation

def build_regression_model(img_height=120, img_width=160):
    """
    連続的なPWMを出力するための回帰モデル (Regression Model) を構築する。
    (Build a regression model to output continuous PWM.)
    """
    model = Sequential([
        Conv2D(24, (5, 5), strides=(2, 2), padding="same", use_bias=False, input_shape=(img_height, img_width, 3)),
        BatchNormalization(),
        Activation('relu'),
        
        Conv2D(36, (5, 5), strides=(2, 2), padding="same", use_bias=False),
        BatchNormalization(),
        Activation('relu'),
        
        Conv2D(48, (5, 5), strides=(2, 2), padding="same", use_bias=False),
        BatchNormalization(),
        Activation('relu'),
        
        Conv2D(64, (3, 3), padding="valid", use_bias=False),
        BatchNormalization(),
        Activation('relu'),
        
        Conv2D(64, (3, 3), padding="valid", use_bias=False),
        BatchNormalization(),
        Activation('relu'),
        
        Flatten(),
        
        Dense(100, activation='relu'),
        Dropout(0.3),
        Dense(50, activation='relu'),
        Dropout(0.2),
        Dense(10, activation='relu'),
        
        Dense(2, activation='tanh')
    ])
    
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

def build_classification_model(img_height=120, img_width=160, num_classes=5):
    """
    5分類を出力するためのモデル (Classification Model) を構築する。
    (Build a classification model to output 5 classes.)
    """
    model = Sequential([
        Input(shape=(img_height, img_width, 3)),
        Conv2D(24, (5, 5), strides=(2, 2), activation='relu'),
        Conv2D(36, (5, 5), strides=(2, 2), activation='relu'),
        Conv2D(48, (5, 5), strides=(2, 2), activation='relu'),
        Conv2D(64, (3, 3), activation='relu'),
        Conv2D(64, (3, 3), activation='relu'),
        Flatten(),
        Dense(100, activation='relu'),
        Dropout(0.2),
        Dense(50, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

def load_robust_model(model_path):
    """
    Kerasのバージョン互換性問題を回避しつつモデルをロードする。
    .weights.h5 が存在する場合は、モデルを再構築して重みをロードする。
    エラー発生時は自動的にモデル構造を再定義して重みを直接読み込む。
    (Load model while avoiding Keras version compatibility issues.
    If .weights.h5 exists, rebuild the model and load weights.
    On failure, automatically reconstruct the architecture and load weights.)
    """
    # 1. .weights.h5 ファイルが明示的に存在する場合 (Explicit weights file)
    weights_path = model_path.replace(".h5", ".weights.h5")
    if os.path.exists(weights_path):
        print(f"Using weight loading mode: {weights_path}")
        model = build_regression_model()
        model.load_weights(weights_path)
        return model
        
    # 2. 教育用分類モデルの場合 (Classification model)
    if "edu_model" in model_path:
        try:
            print(f"Using standard loading mode for classification: {model_path}")
            return load_model(model_path, compile=False)
        except Exception as e:
            print(f"Standard load failed ({e}). Rebuilding architecture & loading weights directly...")
            model = build_classification_model()
            model.load_weights(model_path)
            return model
            
    # 3. 一般的な回帰モデルの場合 (Regression model)
    try:
        print(f"Using standard loading mode: {model_path}")
        return load_model(model_path, compile=False)
    except Exception as e:
        print(f"Standard load failed ({e}). Rebuilding architecture & loading weights directly...")
        model = build_regression_model()
        model.load_weights(model_path)
        return model
