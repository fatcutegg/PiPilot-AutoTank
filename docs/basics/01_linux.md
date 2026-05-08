---
Notion_Page_ID: 35a0fc46-777e-813a-9e90-c9ade95a1671
Notion_Parent_ID: 35a0fc46-777e-81eb-8890-f9cf284b4c5e
---

# 🐧 Linux 入門：Raspberry Piを動かすOSを知ろう

Raspberry Piは **Linux（リナックス）** というOSで動いています。
WindowsやmacOSと似ていますが、ちょっと違います。一緒に見ていきましょう！

---

## 🤔 Linuxって何？

**OS（オペレーティングシステム）** とは、コンピュータ全体を管理するソフトウェアです。

| OS | 使われる場所 |
|----|-------------|
| Windows | 家庭用PC |
| macOS | Mac |
| **Linux** | サーバー・Raspberry Pi・スーパーコンピュータなど |

Linuxは **無料・オープンソース** で、世界中のサーバーやIoTデバイスで使われています。

---

## 🗂️ Linuxのファイルシステム

Linuxのファイルは「ツリー構造」で管理されています。

```
/                    ← ルート（全ての起点）
├── home/
│   └── pi/          ← あなたのホームディレクトリ
│       ├── PiPilot-AutoTank/
│       └── test.txt
├── etc/             ← 設定ファイル
├── usr/             ← プログラム本体
└── tmp/             ← 一時ファイル
```

> `~`（チルダ）は `/home/pi` の省略形です。`cd ~` でホームに戻れます。

---

## 👤 ユーザーと権限

Linuxには **ユーザー権限** という概念があります。

| 権限 | 説明 |
|------|------|
| 一般ユーザー (`pi`) | 普段の作業はこれ |
| スーパーユーザー (`root`) | システム全体を変更できる管理者 |

`sudo` をコマンドの前につけると、一時的に管理者権限で実行できます。

```bash
sudo apt update   ← 管理者権限でパッケージリストを更新
```

> ⚠️ `sudo` は強力です。何をするか理解してから使いましょう！

---

## 📦 パッケージ管理（apt）

Linuxでは **apt（エーピーティー）** でソフトウェアをインストールします。
スマホのApp Storeのようなものです。

```bash
# パッケージリストを最新にする
sudo apt update

# ソフトウェアをインストールする
sudo apt install python3

# インストール済みのソフトを更新する
sudo apt upgrade

# ソフトウェアを削除する
sudo apt remove python3
```

---

## 🎯 ミッション

1. SSH接続したRaspberry Piで `ls /` を実行してルートディレクトリを確認しよう
2. `ls ~` でホームディレクトリの中身を見よう
3. `sudo apt update` を実行してみよう

---

👉 次は [🐚 Shell コマンド入門](https://www.notion.so/35a0fc46777e81c4a57ef04639952a78) へ