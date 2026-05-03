import RPi.GPIO as GPIO
import time
import sys
import threading
from sshkeyboard import listen_keyboard

# --- BCM Mapping (BCMピンマッピング) ---
L_IN1, L_IN2 = 10, 9 
R_IN1, R_IN2 = 25, 11 

class TankController:
    def __init__(self):
        """
        GPIOとPWMの初期化設定を行う。
        将来のAI自律走行（動作推定・模倣学習）を見据え、
        急発進を防ぐための連続的かつ平滑なPWM制御基盤を構築する。
        """
        GPIO.setmode(GPIO.BCM)
        self.pins = [L_IN1, L_IN2, R_IN1, R_IN2]
        
        # 全てのピンで PWM を初期化する (周波数：1000Hz)
        self.pwms = []
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            p = GPIO.PWM(pin, 1000) 
            p.start(0)
            self.pwms.append(p)
            
        # --- 動力制御パラメータ (Power Control Parameters) ---
        self.max_power = 85      # 最大出力 (Maximum target power)
        self.min_power = 40      # 起動トルク用の最小出力 (Minimum power to overcome deadzone)
        self.ramp_step = 5       # 1tickあたりの占空比増加量 (PWM change per tick)
        self.tick_rate = 0.05    # 更新頻度 (秒) (Update frequency: 20Hz)
        
        # 左右のモーターの目標動力と現在動力 (-100 ~ 100, 正は前進、負は後退)
        self.target_l = 0
        self.target_r = 0
        self.current_l = 0
        self.current_r = 0
        
        self.running = True
        
        # モーター動力を非同期で平滑に更新するスレッドを起動
        self.thread = threading.Thread(target=self._motor_update_loop, daemon=True)
        self.thread.start()
        
        print(f"システム初期化完了。最大動力: {self.max_power}%")

    def _update_single_motor_power(self, current, target):
        """
        単一のモーター動力を目標値に向けて1ステップ分更新する計算ロジック。
        死区間(Deadzone)を処理し、滑らかなデータ収集を可能にする。
        """
        if current == target:
            return current
            
        # 停止状態から動き出す場合、死区間(Deadzone)を飛び越えて最小動力を設定する
        if target > 0 and current == 0:
            return self.min_power
        elif target < 0 and current == 0:
            return -self.min_power
            
        # 平滑な加減速 (Ramping up/down)
        if target > current:
            current = min(current + self.ramp_step, target)
        else:
            current = max(current - self.ramp_step, target)
            
        # 停止目標の時、動力が最小起動トルクを下回ったら完全に停止する
        if target == 0 and abs(current) <= self.min_power:
            return 0
            
        return current

    def _apply_pwm(self, power, pwm_in1, pwm_in2):
        """
        計算された動力(-100 ~ 100)をDRV8835(IN/INモード)の実際のPWMピンに適用する。
        """
        if power > 0:
            pwm_in1.ChangeDutyCycle(power)
            pwm_in2.ChangeDutyCycle(0)
        elif power < 0:
            pwm_in1.ChangeDutyCycle(0)
            pwm_in2.ChangeDutyCycle(abs(power))
        else:
            pwm_in1.ChangeDutyCycle(0)
            pwm_in2.ChangeDutyCycle(0)

    def _motor_update_loop(self):
        """
        バックグラウンドで動作し、現在のPWMを目標PWMに徐々に近づける。
        これにより、将来カメラ画像と同期させる動作データ（アクション）が
        連続的かつ微分可能な値となり、学習効率が向上する。
        """
        while self.running:
            old_l, old_r = self.current_l, self.current_r
            
            # 左右の動力を更新
            self.current_l = self._update_single_motor_power(self.current_l, self.target_l)
            self.current_r = self._update_single_motor_power(self.current_r, self.target_r)
            
            # ハードウェアに適用
            self._apply_pwm(self.current_l, self.pwms[0], self.pwms[1])
            self._apply_pwm(self.current_r, self.pwms[2], self.pwms[3])
            
            # 変化があった場合のみログ出力（AIによるリモートデバッグ用）
            if old_l != self.current_l or old_r != self.current_r:
                print(f"[Debug] PWM - Left: {self.current_l:>3}%, Right: {self.current_r:>3}%")
                
            time.sleep(self.tick_rate)

    def move(self, direction):
        """
        キーボード入力に基づき、左右モーターの目標動力(Target Power)を設定する。
        直接PWMを変更せず、目標値を設定するだけで非同期スレッドが追従する。
        """
        if direction == "UP":
            self.target_l = self.max_power
            self.target_r = self.max_power
        elif direction == "DOWN":
            self.target_l = -self.max_power
            self.target_r = -self.max_power
        elif direction == "LEFT":
            self.target_l = -self.max_power
            self.target_r = self.max_power
        elif direction == "RIGHT":
            self.target_l = self.max_power
            self.target_r = -self.max_power

    def stop(self):
        """全てのモーターの目標動力を0に設定し、平滑に停止させる"""
        self.target_l = 0
        self.target_r = 0

    def cleanup(self):
        """プログラム終了時にリソースを解放する (GPIOのクリーンアップ)"""
        self.running = False
        self.stop()
        self.thread.join(timeout=1.0)
        
        for p in self.pwms:
            p.ChangeDutyCycle(0)
            p.stop()
        GPIO.cleanup()
        print("GPIOクリーンアップ完了。システムを終了します。")

# === メイン処理 (Main Execution) ===
if __name__ == "__main__":
    car = TankController()

    def press(key):
        if key in ["up", "down", "left", "right"]:
            car.move(key.upper())
        elif key == "q":
            car.cleanup()
            sys.exit()

    def release(key):
        if key in ["up", "down", "left", "right"]:
            car.stop()

    print("キーボードの方向キーで操作します。'q'で終了します。")
    listen_keyboard(on_press=press, on_release=release)