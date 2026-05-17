import os
import sys
import numpy as np
import time
import tensorflow as tf

# Include src directory in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from model_factory import load_robust_model, build_regression_model

def test_model(model_path, is_classification=False):
    print(f"\n--------------------------------------------------")
    print(f"Testing model: {model_path}")
    if not os.path.exists(model_path):
        print(f"❌ Error: File not found at {model_path}")
        return False
        
    try:
        t_start = time.time()
        # Load model
        if model_path.endswith(".weights.h5"):
            print("Weight-only file detected. Rebuilding model architecture...")
            model = build_regression_model()
            model.load_weights(model_path)
        else:
            model = load_robust_model(model_path)
            
        load_time = (time.time() - t_start) * 1000
        print(f"✅ Successfully loaded in {load_time:.1f}ms")
        
        # Display model summary info
        input_shape = model.input_shape
        output_shape = model.output_shape
        print(f"Input Shape:  {input_shape}")
        print(f"Output Shape: {output_shape}")
        
        # Test inference with dummy image
        dummy_input = np.random.rand(1, 120, 160, 3).astype(np.float32)
        t_infer_start = time.time()
        prediction = model.predict(dummy_input, verbose=0)
        infer_time = (time.time() - t_infer_start) * 1000
        
        print(f"⚡ Inference successful! Time: {infer_time:.2f}ms")
        print(f"Raw Output: {prediction}")
        
        # Verify output formats
        if is_classification:
            predicted_class = np.argmax(prediction[0])
            confidence = np.max(prediction[0])
            ACTIONS = ["STOP", "UP", "DOWN", "LEFT", "RIGHT"]
            print(f"Interpretation (Classification): Action = {ACTIONS[predicted_class]} ({confidence*100:.1f}%)")
        else:
            pred_left = prediction[0][0]
            pred_right = prediction[0][1]
            print(f"Interpretation (Regression): Left Motor = {pred_left*100:.1f}%, Right Motor = {pred_right*100:.1f}%")
            
        return True
    except Exception as e:
        print(f"❌ Failed to load/test model: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("==================================================")
    print("        PiPilot-AutoTank Model Tester             ")
    print("==================================================")
    print(f"TensorFlow Version: {tf.__version__}")
    
    models_to_test = [
        ("models/edu_model.h5", True),
        ("models/end2end_tank.h5", False),
        ("models/end2end_tank.keras", False),
        ("models/end2end_tank.weights.h5", False)
    ]
    
    success_count = 0
    for path, is_class in models_to_test:
        if test_model(path, is_class):
            success_count += 1
            
    print(f"\n==================================================")
    print(f"Test Finished. Success: {success_count}/{len(models_to_test)}")
    print("==================================================")
    
if __name__ == "__main__":
    main()
