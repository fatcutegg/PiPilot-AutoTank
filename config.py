# --- 全局双轨制配置文件 (Global Dual-Mode Configuration) ---

# ACTIVE_MODE を変更することで、データ収集、AI学習、推論のすべての挙動が自動で切り替わります。
# 利用可能なモード:
# "EDUCATION" : 中学生向け。5分類モデル（UP, DOWN, LEFT, RIGHT, STOP）。直感的でわかりやすい。
# "RESEARCH"  : 研究向け。連続空間回帰モデル（Continuous Regression / Transformer）。滑らかな自動運転用。

ACTIVE_MODE = "EDUCATION"  # デフォルトは教育モード

# 各モードに対応する保存先・モデルのパス
PATHS = {
    "EDUCATION": {
        "dataset_dir": "dataset/education",
        "log_file": "dataset/education/driving_log.csv",
        "model_path": "models/edu_model.h5"
    },
    "RESEARCH": {
        "dataset_dir": "dataset/research",
        "log_file": "dataset/research/driving_log.csv",
        "model_path": "models/end2end_tank.h5"
    }
}
