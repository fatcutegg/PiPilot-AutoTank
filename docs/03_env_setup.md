---
Notion_Page_ID: 3840fc46-777e-8117-9bcc-f20dc7ae411c
Notion_Parent_ID: 3590fc46777e80cea840f8f9b4833418
---

# 🐍 第3章：Python環境とプログラムの準備

戦車を制御するプログラムを動かすために、Python の「仮想環境」を作ります。これによって、システム全体の環境を汚さずに必要なライブラリを追加できます。

---

## 1. Pythonの実行環境を作ろう（Conda または venv）

### 選択肢 A：Conda（Miniconda）を使う方法
もし Conda が問題なく動く場合は、以下のコマンドで戦車側（Raspberry Pi）に Miniconda をセットアップします：

```bash
# インストーラのダウンロードとインストール
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -p ~/miniconda3
~/miniconda3/bin/conda init zsh   # zshを使っている場合（またはbash）
# 一度ターミナルを閉じて開き直す

# 仮想環境を作成して有効化
conda create -n tank_py39 python=3.9 -y
conda activate tank_py39
```

### 選択肢 B：予備プラン（venv）を使う方法
「Conda を入れるのにメモリが足りない」「ダウンロードに失敗する」といった場合は、Raspberry Pi 標準の **`venv`（ブイエンブ）** を使うのが最もおすすめです。軽快で確実に動作します。

```bash
# 必要なシステムパッケージをインストール
sudo apt update
sudo apt install -y python3-pip python3-venv

# 仮想環境を「venv_tank」という名前で作る
python3 -m venv ~/venv_tank

# 仮想環境を有効にする
source ~/venv_tank/bin/activate
```
※ 仮想環境が有効になると、プロンプトの左側に `(venv_tank)` のように表示されます。

---

## 2. プログラムをダウンロードしよう（Git Clone）

戦車のプログラムコードを GitHub からダウンロードします。

> ⚠️ **前提条件**：事前に GitHub の SSH Key 設定を完了させておいてください。設定方法は [🐙 基礎知識 10：GitHub SSHの設定](basics/10_github_ssh.md) を確認してください。

戦車に SSH 接続（`ssh tank`）した状態で、以下のコマンドを実行します：

```bash
# プロジェクトフォルダを作成して移動
mkdir -p ~/Projects && cd ~/Projects

# SSH URLを使ってクローン（ダウンロード）
git clone git@github.com:fatcutegg/PiPilot-AutoTank.git
cd PiPilot-AutoTank

# ライブラリ（依存関係）をまとめてインストール
pip install -r requirements.txt
```

---

👉 次は [第4章：キミがドライバーだ！ (手動コントロール篇)](04_teleop.md) へ