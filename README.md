# 🚀 PiPilot-AutoTank: 樹莓派自動運転タンク

このプロジェクトは、Raspberry Pi（ラズベリーパイ）とAI（人工知能）を活用した、自動運転タンクの学習・研究プラットフォームです。
中学生などの初心者向けの「教育モード」から、エンドツーエンドの連続回帰モデルを構築する「研究モード」まで、幅広く対応したデュアルモード設計となっています。

マニュアルはすべて中学生向けにわかりやすく翻訳・整理され、Notion とも双方向に同期可能です。

---

## 📁 プロジェクト構造 (Project Structure)

プロジェクトは、機能ごとにモジュール化されています。

```text
pipilot-autotank/
├── src/                      # タンクを制御するためのコアプログラム
│   ├── autonomous_drive.py    # AI自動運転のメインロジック
│   ├── teleop_keyboard.py     # キーボードによる手動操縦ロジック
│   ├── data_logger.py         # カメラ画像とPWM値のデータ収集
│   └── config.py              # 全体設定（モード切り替えなど）
├── training/                 # AIモデルの学習用スクリプト
│   ├── train_classification.py   # 教育用：5つの離散アクション分類モデル
│   └── train_regression_model.py # 研究用：連続的なPWMを出力する回帰モデル (PilotNet风)
├── scripts/                  # ユーティリティ・ツール
│   ├── notion_sync.py         # ローカルMarkdownとNotionの双方向同期ツール（リンク自動解決機能付き）
│   ├── push_main_to_notion.py # メインガイドを一括プッシュするスクリプト
│   ├── push_basics_to_notion.py # 基礎知識ガイドを一括プッシュするスクリプト
│   └── sync_to_pi.sh          # Raspberry Piへコードやモデルを転送するツール
├── tests/                    # テスト・検証用スクリプト
│   ├── test_ramp.py           # モーターの加速・減速テスト
│   └── verify_vision.py       # カメラモジュールとAI推論 of テスト
└── docs/                     # 教育用マニュアル（中学生向け・日本語）
    ├── 00_index.md            # メインガイドの目次（アンカーリンク解決済み）
    ├── 01_intro.md            # 第1章：スマートタンクを知ろう！
    ├── 02_ssh_setup.md        # 第2章：戦車にSSH免密接続しよう
    ├── 03_env_setup.md        # 第3章：Python環境とプログラムの準備
    ├── 04_teleop.md           # 第4章：キミがドライバーだ！(手動コントロール篇)
    ├── 05_vision.md           # 第5章：タンクに「視力」をあたえよう (AIビジョン篇)
    ├── 06_data_collection.md  # 第6章：キーボード操縦でデータを集めよう
    ├── 07_model_learning.md   # 第7章：データを提出してAIモデルを作ろう
    ├── 08_autonomous_drive.md # 第8章：自動走行をスタートさせよう！
    ├── assets/                # 画像などのメディアアセット
    └── basics/                # パソコンやツールなどの基礎知識ガイド
        ├── 00_basics_index.md      # 基礎知識の目次
        ├── 01_linux.md             # 第1回：Linux 入門
        ├── 02_shell.md             # 第2回：Shell コマンド入門
        ├── 03_vim.md               # 第3回：Vim 入門
        ├── 04_ssh.md               # 第4回：SSH 入門
        ├── 05_raspi_setup.md       # 第5回：Raspberry Pi セットアップ
        ├── 06_git.md               # 第6回：Git 入門
        ├── 07_python.md            # 第7回：Python 入門
        ├── 08_ohmyzsh.md           # 第8回：Oh My Zsh 入門
        ├── 09_chromebook_setup.md  # 第9回：Chromebook Linux セットアップ
        ├── 10_github_ssh.md        # 第10回：GitHub SSHの設定（アカウント作成手順付き）
        └── 11_scp.md               # 第11回：SCP コマンド入門
```

---

## 🛠 スクリプトの使い方 (How to Use Scripts)

### 1. Notion 同期ツール (`notion_sync.py`)
ローカルのMarkdownマニュアルを、Notion上の共有ワークスペースと双方向に同期できます。
同期時に、ファイル間の相対リンク（`01_intro.md` など）は自動的に対応する Notion ページの絶対 URL に置換されて流し込まれます。

**準備:**
プロジェクトルートに `.env` ファイルを作成し、Notion APIキーを設定します。
```env
NOTION_API_KEY=your_notion_api_key_here
```

**実行環境の準備:**
プロジェクトルートに配置された仮想環境の Conda（`.conda/`）を使用します。
```bash
# 依存関係のインストール（必要な場合）
.conda/bin/pip install -r requirements_notion.txt
```

**MarkdownファイルをNotionへ送信（Push）:**
```bash
# 特定のファイルをプッシュする
.conda/bin/python scripts/notion_sync.py push docs/01_intro.md

# 一括でメインガイドをプッシュする
.conda/bin/python scripts/push_main_to_notion.py

# 一括で基礎知識ガイドをプッシュする
.conda/bin/python scripts/push_basics_to_notion.py
```

**Notionの変更をローカルへ取得（Pull）:**
```bash
.conda/bin/python scripts/notion_sync.py pull docs/01_intro.md
```

### 2. Raspberry Pi への同期 (`sync_to_pi.sh`)
パソコンで開発したコードや学習済みのAIモデルを、Wi-Fi経由でタンク本体（Raspberry Pi）に転送します。
```bash
bash scripts/sync_to_pi.sh
```

---

## 📊 データ収集とAIモデル学習 (Data Collection & Training)

自動運転AIを動かすまでの基本的なワークフローは以下の通りです。

### 1. 手動操縦によるデータ収集 (Data Collection)
PC側のキーボードを使ってタンクを手動操縦し、自動運転に必要な「教師データ（カメラ映像と操作ログのペア）」を収集します。

1. タンクにSSH接続した状態で、データ収集プログラムを起動します：
   ```bash
   python src/data_logger.py
   ```
2. キーボードで操縦します：
   - `r` キー: データの記録を開始 / 一時停止（記録がオンの時、映像とPWM値がペアで保存されます）
   - 方向キー（`↑` `↓` `←` `→`）: タンクを操作
   - `q` キー: データを安全に保存して終了
3. 収集されたデータは `dataset/` ディレクトリに保存されます。（目安として 3000〜5000枚 程度収集します）

### 2. AIモデルの学習 (AI Model Training)
Raspberry PiのCPUは小さいため、PCや学習用サーバーにデータを送信してAIモデルを作成（学習）します。

1. 収集したデータをPCに転送するか、PC/学習用サーバー上で以下を実行してAIモデルを学習させます：
   * **分類モデルの学習（教育用・5つの離散アクション）**:
     ```bash
     python training/train_classification.py
     ```
   * **回帰モデルの学習（研究用・スムーズな走行）**:
     ```bash
     python training/train_regression_model.py
     ```
2. 学習が完了すると、モデルファイル（例: `models/end2end_tank.h5`）が出力されます。

### 3. モデルの転送と自律走行の実行 (Deployment & Autonomous Drive)
1. 作成されたモデルをタンクへ転送します（モデルフォルダに配置）：
   ```bash
   scp models/end2end_tank.h5 pi@192.168.1.xxx:~/PiPilot-AutoTank/models/
   ```
2. タンク側で自律走行プログラムを起動します：
   ```bash
   python src/autonomous_drive.py
   ```

---

## 🤖 AIモデルと走行モード (AI Modes)

`src/config.py` で `ACTIVE_MODE` を切り替えることで、2つの異なるAIを体験できます。

1. **EDUCATION (教育モード)**:
   - シンプルな画像分類AI (CNN) を使用。
   - `STOP`, `UP`, `DOWN`, `LEFT`, `RIGHT` の5つのコマンドでタンクを動かします。AIの基本を学ぶのに最適です。
2. **RESEARCH (研究モード)**:
   - より高度な回帰モデルを使用（`tf.data.Dataset`による非同期読み込み、Data Augmentation、BatchNormalizationを実装）。
   - 左右のキャタピラ(モーター)の出力を `-1.0` から `1.0` の間で滑らかに予測し、まるで本物の自動運転車のようにスムーズなカーブを描いて走行します。
