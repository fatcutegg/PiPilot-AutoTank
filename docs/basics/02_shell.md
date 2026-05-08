---
Notion_Page_ID: 35a0fc46-777e-81c4-a57e-f04639952a78
Notion_Parent_ID: 35a0fc46-777e-81eb-8890-f9cf284b4c5e
---

# 🐚 Shell コマンド入門：ターミナルを使いこなそう

**Shell（シェル）** はターミナル（黒い画面）でOSに命令を出す仕組みです。
マウスを使わずキーボードだけで操作できると、作業がとても速くなります！

---

## 🤔 Shellって何？

```
あなた → [コマンドを入力] → Shell → Linux OS → 実行結果
```

Shell はあなたとOS（Linux）の間で命令を伝える「通訳者」です。
Raspberry Piでは主に **bash（バッシュ）** というShellが使われています。

---

## 📁 ファイル・ディレクトリの操作

### 現在の場所を確認する

```bash
pwd
# 出力例：/home/pi
```

### ディレクトリの中身を見る

```bash
ls          # ファイル一覧
ls -l       # 詳細表示（権限・サイズ・日時）
ls -la      # 隠しファイルも含めて表示
```

### ディレクトリを移動する

```bash
cd PiPilot-AutoTank   # フォルダに入る
cd ..                  # 一つ上に戻る
cd ~                   # ホームディレクトリに戻る
cd /home/pi/           # 絶対パスで移動
```

### ファイル・フォルダを作る

```bash
mkdir new_folder          # フォルダを作る
touch hello.txt           # 空のファイルを作る
```

### コピー・移動・削除

```bash
cp hello.txt hello_copy.txt    # ファイルをコピー
mv hello.txt renamed.txt       # ファイル名を変更・移動
rm hello.txt                   # ファイルを削除
rm -r new_folder               # フォルダごと削除
```

> ⚠️ `rm` で削除したファイルはゴミ箱に入りません。元に戻せないので注意！

---

## 📄 ファイルの中身を見る

```bash
cat hello.txt          # ファイルの内容を表示
less hello.txt         # 長いファイルをページで表示（q で終了）
head -n 10 hello.txt   # 先頭10行だけ表示
tail -n 10 hello.txt   # 末尾10行だけ表示
```

---

## 🔍 検索する

```bash
# ファイルを探す
find . -name "*.py"

# ファイルの中の文字を検索する
grep "motor" main.py
grep -r "motor" .      # フォルダ内を再帰的に検索
```

---

## ⚡ 便利なショートカット

| ショートカット | 機能 |
|---------------|------|
| `Tab` | コマンド・ファイル名を自動補完 |
| `↑` / `↓` | コマンド履歴を辿る |
| `Ctrl + C` | 実行中のコマンドを中断 |
| `Ctrl + L` | 画面をクリア（`clear` と同じ） |
| `Ctrl + A` | 行の先頭にカーソルを移動 |
| `Ctrl + E` | 行の末尾にカーソルを移動 |

---

## 🔗 パイプとリダイレクト

```bash
# パイプ（|）：前のコマンドの出力を次のコマンドに渡す
ls -l | grep ".py"          # Pythonファイルだけ表示

# リダイレクト（>）：結果をファイルに書き出す
ls > filelist.txt           # ファイル一覧をテキストに保存
echo "Hello" >> log.txt     # ファイルに追記する
```

---

## 📋 よく使うコマンド一覧

| コマンド | 意味 |
|----------|------|
| `pwd` | 今いる場所を表示 |
| `ls` | ファイル一覧を表示 |
| `cd` | ディレクトリを移動 |
| `mkdir` | フォルダを作る |
| `touch` | ファイルを作る |
| `cp` | コピー |
| `mv` | 移動・名前変更 |
| `rm` | 削除 |
| `cat` | ファイルの中身を表示 |
| `grep` | 文字を検索 |
| `echo` | 文字を出力する |
| `sudo` | 管理者権限で実行 |
| `man コマンド` | コマンドの使い方を調べる |

---

## 🎯 ミッション

1. `pwd` で今の場所を確認しよう
2. `mkdir practice && cd practice` でフォルダを作って移動しよう
3. `touch test.txt` でファイルを作って、`echo "Hello" > test.txt` で文字を書き込もう
4. `cat test.txt` で中身を確認しよう
5. `ls -la` で隠しファイルも含めて一覧を見よう

---

👉 次は [⌨️ Vim 入門](https://www.notion.so/35a0fc46777e81748d4cfc9bd24bf3d0) へ