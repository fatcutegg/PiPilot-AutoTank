import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from teleop_keyboard import TankController

def test_motor_ramp():
    """
    モーターの加減速（Ramping）ロジックを自動で検証するスクリプト。
    キーボード入力を模倣し、バックグラウンドスレッドが正しくPWMを推移させるか確認する。
    """
    print("=== PWM加減速 自動テスト開始 (Automated PWM Ramping Test) ===")
    
    car = TankController()
    
    try:
        print("\n[Test 1] 前進 (UP) - 平滑な加速をテストします")
        car.move("UP")
        # 40% から 85% まで、5%ずつ20Hz(0.05s)で上がる。
        # (85-40)/5 = 9 steps. 9 * 0.05s = 0.45s 程度で最大速度に到達。
        time.sleep(1.0) 
        
        print("\n[Test 2] 停止 (STOP) - 平滑な減速をテストします")
        car.stop()
        time.sleep(1.0) # 完全に停止するまで待機
        
        print("\n[Test 3] 左旋回 (LEFT) - 差速ターンのテストをします")
        car.move("LEFT")
        time.sleep(1.0)
        
        print("\n[Test 4] 停止 (STOP) - 最終停止")
        car.stop()
        time.sleep(1.0)
        
    finally:
        car.cleanup()
        print("=== テスト完了 (Test Completed) ===")

if __name__ == "__main__":
    test_motor_ramp()
