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

def load_robust_model(model_path):
    """
    Kerasのバージョン互換性問題を回避しつつモデルをロードする。
    .weights.h5 が存在する場合は、モデルを再構築して重みをロードする。
    (Load model while avoiding Keras version compatibility issues.
    If .weights.h5 exists, rebuild the model and load weights.)
    """
    weights_path = model_path.replace(".h5", ".weights.h5")
    
    if os.path.exists(weights_path):
        print(f"Using weight loading mode: {weights_path}")
        model = build_regression_model()
        model.load_weights(weights_path)
        return model
    else:
        print(f"Using standard loading mode: {model_path}")
        return load_model(model_path, compile=False)
