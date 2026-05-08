---
Notion_Page_ID: 35a0fc46-777e-8191-ae66-d0a8d888c6ae
Notion_Parent_ID: 35a0fc46-777e-81eb-8890-f9cf284b4c5e
---

# 🔐 SSH 入門：ネットワーク越しにRaspberry Piをさわろう

**SSH（Secure Shell）** は、別のパソコンにネットワーク経由で安全に接続するための技術です。
Raspberry Piにはモニターやキーボードを繋がなくても、自分のパソコンから操作できます！

---

## 🤔 SSHって何？

```
あなたのパソコン  ──── WiFi ────  Raspberry Pi
    (Mac/Win)         SSH接続        (タンクの頭脳)
```

SSHを使うと、Raspberry Piが手元になくても、Wi-Fi経由でコマンドを送れます。

---

## 🍓 Raspberry PiのSSHを有効にする

Raspberry Pi Imagerでイメージを書き込む際に設定できます。

1. Raspberry Pi Imagerを開く
2. 歯車アイコン（⚙️）をクリック
3. 「SSHを有効にする」にチェック
4. ユーザー名とパスワードを設定する

> すでにセットアップ済みの場合は、ターミナルで以下を実行：
> ```bash
> sudo systemctl enable ssh
> sudo systemctl start ssh
> ```

---

## 🚀 SSH接続の手順

### 1. Raspberry PiのIPアドレスを調べる

Raspberry Pi側のターミナルで：
```bash
hostname -I
```

例：`192.168.1.42` と表示されたとする。

---

### 2. 自分のパソコンからSSH接続する

```bash
ssh pi@192.168.1.42
```

または、ホスト名で接続：

```bash
ssh pi@pizero.local
```

> 初回接続時に「接続しますか？(yes/no)」と聞かれたら `yes` と入力。

---

### 3. パスワードを入力する

設定したパスワードを入力（入力しても画面に表示されない）→ `Enter`

接続成功すると以下のような表示になります：

```
pi@raspberrypi:~ $
```

---

## 🔑 SSH鍵認証（パスワード不要にする方法）

毎回パスワードを入力するのが面倒なら、SSH鍵を設定しよう。

```bash
# 自分のパソコンで鍵を生成する
ssh-keygen -t rsa -b 4096

# 公開鍵をRaspberry Piに送る
ssh-copy-id pi@pizero.local
```

これで次回からパスワードなしで接続できます！

---

## 📋 よく使うコマンド

| コマンド | 意味 |
|----------|------|
| `ssh ユーザー@IPアドレス` | SSH接続する |
| `exit` | SSH接続を終了する |
| `scp ファイル pi@IP:パス` | ファイルをRaspberry Piに転送する |
| `ssh-keygen` | SSH鍵ペアを生成する |
| `ssh-copy-id pi@IP` | 公開鍵を送る |

---

## 🎯 ミッション

1. Raspberry PiのSSHを有効にしよう
2. `hostname -I` でIPアドレスを確認しよう
3. 自分のパソコンから `ssh pi@<IPアドレス>` で接続しよう
4. `ls` コマンドでファイル一覧を確認しよう
5. `exit` で接続を終了しよう

---

👉 次は [🍓 Raspberry Pi セットアップ](https://www.notion.so/35a0fc46777e81cb9d09d156c75ed481) へ