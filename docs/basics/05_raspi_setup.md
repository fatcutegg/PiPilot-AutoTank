---
Notion_Page_ID: 35a0fc46-777e-81cb-9d09-d156c75ed481
Notion_Parent_ID: 35a0fc46-777e-81eb-8890-f9cf284b4c5e
---

# 🍓 Raspberry Pi セットアップ：ゼロからはじめる！

Raspberry Piを箱から出して、タンクを動かせる状態にするまでの手順をステップバイステップで説明します。

---

## 📦 用意するもの

| アイテム | 説明 |
|----------|------|
| Raspberry Pi Zero 2 W | タンクの頭脳。このプロジェクトで使うモデル |
| microSDカード（16GB以上） | OSを書き込むストレージ |
| microSDカードリーダー | パソコンにSDカードを挿すために必要 |
| パソコン（Mac/Win） | セットアップ作業用 |
| Wi-Fi環境 | Raspberry PiをWi-Fiに繋ぐため |

---

## 🖥️ STEP 1：Raspberry Pi Imager をインストール

**Raspberry Pi Imager** はOSを書き込む公式ツールです。

1. [https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/) にアクセス
2. 自分のOSに合ったImagerをダウンロード
3. インストールして起動する

---

## 💾 STEP 2：OSを書き込む

1. Imagerを起動する
2. **「デバイスを選択」** → `Raspberry Pi Zero 2 W` を選ぶ
3. **「OSを選択」** → `Raspberry Pi OS Lite (64-bit)` を選ぶ  
   ※ デスクトップ不要・軽量版
4. **「ストレージを選択」** → SDカードを選ぶ
5. **歯車アイコン（⚙️）** をクリックして以下を設定：

   | 設定項目 | 設定値 |
   |----------|--------|
   | ホスト名 | `pizero.local` |
   | SSHを有効にする | ✅ チェック |
   | ユーザー名 | `pi` |
   | パスワード | 任意（忘れずに！） |
   | Wi-Fi設定 | SSIDとパスワードを入力 |
   | ロケール | `Asia/Tokyo` |

6. **「書き込む」** をクリック → 数分待つ

---

## 🔌 STEP 3：起動する

1. SDカードをRaspberry Piに挿す
2. 電源を繋ぐ（USBケーブル）
3. 1〜2分待つ（初回起動は少し時間がかかる）

---

## 💻 STEP 4：SSH接続して確認

自分のパソコンのターミナルで：

```bash
ssh pi@pizero.local
```

以下のような表示が出れば成功！

```
pi@pizero:~ $
```

---

## 📦 STEP 5：基本パッケージのインストール

接続後、以下を実行してシステムを最新状態にする：

```bash
# システムを更新する
sudo apt update && sudo apt upgrade -y

# Pythonとpipをインストール
sudo apt install -y python3-pip python3-venv git

# インストール確認
python3 --version
git --version
```

---

## 🤖 STEP 6：PiPilotプロジェクトをセットアップ

```bash
# リポジトリをクローン
git clone https://github.com/fatcutegg/PiPilot-AutoTank.git
cd PiPilot-AutoTank

# Python仮想環境を作成
python3 -m venv venv
source venv/bin/activate

# 必要なライブラリをインストール
pip install -r requirements.txt
```

---

## ✅ セットアップ完了チェックリスト

- [ ] Raspberry Pi Imager でOSを書き込んだ
- [ ] Wi-FiとSSHの設定をした
- [ ] SSH接続に成功した（`ssh pi@pizero.local`）
- [ ] `sudo apt update` を実行した
- [ ] PiPilotリポジトリをクローンした

---

## 🎯 ミッション

全部のチェックリストにチェックを入れて、Raspberry Piを使える状態にしよう！

---

👉 次は [🐙 Git 入門](https://www.notion.so/35a0fc46777e81cea35bd49b97628fae) へ