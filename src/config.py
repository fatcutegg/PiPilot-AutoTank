# --- 全局双轨制配置文件 (Global Dual-Mode Configuration) ---
import os

# プロジェクトのルートディレクトリを取得 (Get project root directory)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ACTIVE_MODE を変更することで、データ収集、AI学習、推論のすべての挙動が自動で切り替わります。
# 利用可能なモード:
# "EDUCATION" : 中学生向け。5分類モデル（UP, DOWN, LEFT, RIGHT, STOP）。直感的でわかりやすい。
# "RESEARCH"  : 研究向け。連続空間回帰モデル（Continuous Regression / Transformer）。滑らかな自動運転用。

ACTIVE_MODE = "RESEARCH"  # デフォルトは教育モード

# 各モードに対応する保存先・モデルのパス (Paths for each mode)
PATHS = {
    "EDUCATION": {
        "dataset_dir": os.path.join(ROOT_DIR, "dataset/education"),
        "log_file": os.path.join(ROOT_DIR, "dataset/education/driving_log.csv"),
        "model_path": os.path.join(ROOT_DIR, "models/edu_model.keras")
    },
    "RESEARCH": {
        "dataset_dir": os.path.join(ROOT_DIR, "dataset/research"),
        "log_file": os.path.join(ROOT_DIR, "dataset/research/driving_log.csv"),
        "model_path": os.path.join(ROOT_DIR, "models/end2end_tank.h5")
    }
}

