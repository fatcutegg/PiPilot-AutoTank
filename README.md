# 🚀 自動運転スマートタンク・プロジェクト (Smart Tank Project)

このプロジェクトは、Raspberry Pi（ラズベリーパイ）とAI（人工知能）を活用した、自動運転タンクの学習・研究プラットフォームです。
中学生などの初心者向けの「教育モード」から、エンドツーエンドの連続回帰モデルを構築する「研究モード」まで、幅広く対応したデュアルモード設計となっています。

## 📁 プロジェクト構造 (Project Structure)

プロジェクトは、機能ごとにモジュール化されています。

```text
tank_project/
├── src/                # タンクを制御するためのコアプログラム
│   ├── autonomous_drive.py  # AI自動運転のメインロジック
│   ├── teleop_keyboard.py   # キーボードによる手動操縦ロジック
│   ├── data_logger.py       # カメラ画像とPWM値のデータ収集
│   └── config.py            # 全体設定（モード切り替えなど）
├── training/           # AIモデルの学習用スクリプト
│   ├── train_classification.py   # 教育用：5つの離散アクション分類モデル
│   └── train_regression_model.py # 研究用：連続的なPWMを出力する回帰モデル (PilotNet風)
├── scripts/            # ユーティリティ・ツール
│   ├── notion_sync.py       # ローカルMarkdownとNotionの双方向同期ツール
│   └── sync_to_pi.sh        # Raspberry Piへコードやモデルを転送するツール
├── tests/              # テスト・検証用スクリプト
│   ├── test_ramp.py         # モーターの加速・減速テスト
│   └── verify_vision.py     # カメラモジュールとAI推論のテスト
└── docs/               # 教育用マニュアル（日本語）
    ├── 00_index.md          # 目次ページ
    ├── 01_intro.md          # 第1章：スマートタンクを知ろう！
    ├── 02_teleop.md         # 第2章：手動コントロール篇
    └── 03_vision.md         # 第3章：AIビジョン篇
```

---

## 🛠 スクリプトの使い方 (How to Use Scripts)

### 1. Notion 同期ツール (`notion_sync.py`)
ローカルで作成したMarkdownドキュメント（`docs/`内）を、チームのNotionと双方向に同期させることができます。

**準備:**
プロジェクトのルートディレクトリに `.env` ファイルを作成し、Notion APIキーを設定してください。
```env
NOTION_API_KEY=your_notion_api_key_here
```

**MarkdownファイルをNotionへ送信（Push）:**
```bash
# Python仮想環境(例: tank_notion)で実行します
python scripts/notion_sync.py push docs/01_intro.md
```
※ Markdownファイルの先頭に `Notion_Parent_ID` が設定されている場合、Notion上で自動的にサブページが作成され、そのページのIDが自動的にローカルファイルに書き戻されます。

**Notionの変更をローカルへ取得（Pull）:**
```bash
python scripts/notion_sync.py pull docs/01_intro.md
```

### 2. Raspberry Pi への同期 (`sync_to_pi.sh`)
パソコンで開発したコードや学習済みのAIモデルを、Wi-Fi経由でタンク本体（Raspberry Pi）に転送します。
```bash
bash scripts/sync_to_pi.sh
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
