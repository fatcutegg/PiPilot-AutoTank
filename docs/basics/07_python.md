---
Notion_Page_ID: 35a0fc46-777e-816e-ba15-f4a3eb922cbd
Notion_Parent_ID: 35a0fc46-777e-81eb-8890-f9cf284b4c5e
---

# 🐍 Python 入門：タンクを動かすプログラミング言語

このプロジェクトでは **Python（パイソン）** を使ってタンクを制御します。
シンプルで読みやすく、AIや機械学習にも広く使われている言語です！

---

## 🤔 Pythonって何？

```python
# これがPythonのコード。読みやすい！
print("こんにちは、タンク！")

speed = 100
if speed > 50:
    print("速い！")
```

Pythonの特徴：
- **シンプル**：英語に近い文法で読みやすい
- **万能**：Web・AI・ロボット制御など何でもできる
- **豊富なライブラリ**：便利な機能がすぐ使える

---

## 🐍 基本文法

### 変数と型

```python
name = "PiPilot"        # 文字列（str）
speed = 100             # 整数（int）
angle = 45.5            # 小数（float）
is_running = True       # 真偽値（bool）

print(name, speed)      # PiPilot 100
```

### 条件分岐（if）

```python
speed = 80

if speed > 100:
    print("速すぎ！")
elif speed > 50:
    print("ちょうどいい速さ")
else:
    print("ゆっくり走行中")
```

### 繰り返し（for / while）

```python
# forループ
for i in range(5):
    print(f"カウント: {i}")   # 0, 1, 2, 3, 4

# whileループ
count = 0
while count < 3:
    print("回転中...")
    count += 1
```

### 関数（def）

```python
def move_tank(direction, speed):
    print(f"方向: {direction}, 速度: {speed}")

move_tank("前進", 80)
move_tank("右折", 50)
```

---

## 📦 ライブラリ（pip）

Pythonには便利な **ライブラリ（外部パッケージ）** が豊富にあります。

```bash
# ライブラリをインストール
pip install opencv-python

# インストール済みのライブラリ一覧
pip list

# ライブラリを削除
pip uninstall opencv-python
```

---

## 🌏 仮想環境とは？

**仮想環境（Virtual Environment）** は、プロジェクトごとに独立したPython環境を作る仕組みです。

```
PC全体
├── Python 3.11（システム）
├── 🗂️ PiPilot-AutoTank環境
│   ├── opencv 4.8
│   └── numpy 1.24
└── 🗂️ 別プロジェクト環境
    ├── opencv 4.5（古いバージョン）
    └── tensorflow 2.0
```

> 仮想環境がないと、プロジェクトAのライブラリがプロジェクトBに干渉してしまいます。

---

## 🐊 Conda で環境管理する（推奨）

**Conda（コンダ）** はパッケージ管理ツールで、仮想環境の作成・切り替えが簡単です。
開発マシン（Mac）での作業に特におすすめです。

### インストール（Miniforge を推奨）

```bash
# Miniforgeをダウンロードしてインストール（Mac）
brew install miniforge

# または公式サイトからインストーラーをダウンロード
# https://github.com/conda-forge/miniforge
```

### 基本的な使い方

```bash
# 新しい環境を作る（Python 3.11を指定）
conda create -n pipilot python=3.11

# 環境を有効にする
conda activate pipilot

# 環境の中でライブラリをインストール
conda install numpy
pip install opencv-python    # condaにない場合はpipも使える

# 現在の環境を確認
conda info --envs

# 環境を無効にする（元に戻る）
conda deactivate
```

### PiPilot用の環境セットアップ

```bash
# PiPilot専用の環境を作る
conda create -n pipilot python=3.11 -y
conda activate pipilot

# プロジェクトのライブラリを一括インストール
cd PiPilot-AutoTank
pip install -r requirements.txt

# 正しい環境か確認
which python     # → /opt/homebrew/Caskroom/miniforge/base/envs/pipilot/bin/python
python --version # → Python 3.11.x
```

### よく使うコマンド一覧

| コマンド | 意味 |
|----------|------|
| `conda create -n 名前 python=3.11` | 新しい環境を作る |
| `conda activate 名前` | 環境を有効にする |
| `conda deactivate` | 環境を無効にする |
| `conda info --envs` | 全環境の一覧を見る |
| `conda remove -n 名前 --all` | 環境を削除する |
| `conda list` | インストール済みパッケージを表示 |

---

## 🍓 Raspberry Pi での Python 環境

Raspberry Pi（Raspberry Pi OS）では **venv** を使います。  
※ Raspberry Pi OS は `conda` が使えないため。

```bash
# venvで仮想環境を作る
python3 -m venv venv

# 有効にする
source venv/bin/activate

# ライブラリをインストール
pip install -r requirements.txt

# 無効にする
deactivate
```

> 💡 **開発マシン（Mac）では conda**、**Raspberry Piでは venv** と使い分けよう。

---

## 🎯 ミッション

1. `conda create -n pipilot python=3.11 -y` で環境を作ろう
2. `conda activate pipilot` で環境を有効にしよう
3. `pip install -r requirements.txt` で必要なライブラリをインストールしよう
4. `python -c "print('タンク起動準備完了！')"` を実行しよう
5. Raspberry Piでも `venv` で同じことをやってみよう

---

👉 基礎知識コンプリート！[メインガイドへ戻る](https://www.notion.so/3590fc46777e80cea840f8f9b4833418) でタンクを動かしはじめよう！🎉