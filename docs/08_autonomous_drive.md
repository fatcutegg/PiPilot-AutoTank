---
Notion_Page_ID: 3840fc46-777e-81fd-9c87-c9c43e15ec60
Notion_Parent_ID: 3590fc46777e80cea840f8f9b4833418
---

# 🏎️ 第8章：自動走行をスタートさせよう！

配布された学習済みモデルを使って、いよいよ自動走行を行います！

---

## 1. 学習済みモデルを戦車に転送する

パソコン側のターミナルで、届いたモデルファイル（`end2end_tank.h5`）を戦車の `models` フォルダに転送します：

```bash
# モデル用のフォルダを作り、そこへ転送します
ssh tank "mkdir -p ~/Projects/PiPilot-AutoTank/models"
scp end2end_tank.h5 tank:~/Projects/PiPilot-AutoTank/models/
```

---

## 2. 自律走行プログラムの起動

戦車側（`ssh tank`）のターミナルでプログラムを実行します：

```bash
cd ~/Projects/PiPilot-AutoTank

# 仮想環境が有効であることを確認して実行
conda activate tank_py39  # または source ~/venv_tank/bin/activate

# 自動走行の実行
python -u src/autonomous_drive.py
```

---

## ⚠️ 【重要】安全上の警告

自動走行プログラムを起動すると、カメラが画像を捉えた瞬間から**戦車が即座に走り出します**。

必ずテスト用コースのスタートラインにセットした状態で起動し、暴走したときに備えていつでもキーボードの **`Ctrl + C`**（強制終了）を押せる準備をしておいてください！