---
Notion_Page_ID: 3840fc46-777e-81ca-af2b-dfe361e1af48
Notion_Parent_ID: 35a0fc46-777e-81eb-8890-f9cf284b4c5e
---

# 🐙 基礎知識 10：GitHub と安全に繋ごう（SSH Key の設定）

戦車のプログラム（コード）をダウンロード（クローン）したり、自分で書き換えたプログラムを保存したりするときに、GitHub（ギットハブ）というウェブサイトを使います。

GitHubと安全に、かつ「パスワードの入力を省略して」通信できるようにするために、**「SSH Key（鍵）」** という仕組みを設定しましょう！

中学生のキミでも、暗号の鍵を作って登録するだけで、カッコいいエンジニアの仲間入りができるよ！

---

## 🔑 SSH Key ってなに？

SSH Keyは、インターネット上の金庫（GitHub）を開けるための**「デジタル合鍵」**です。
パソコンや Raspberry Pi の中で「秘密の鍵（自分だけのもの）」と「公開する鍵（みんなに見せていいもの）」のペアを作り、公開する鍵を GitHub に登録しておくことで、パスワードを何度も入力しなくても「本人であること」を証明してくれます。

---

## 🛠️ 設定の 3 ステップ

### STEP 1：自分の鍵（キーペア）を作ろう
ターミナルを開いて、以下のコマンドを実行します。

```bash
# 鍵を作るコマンド（メールアドレスの部分は、GitHubに登録した自分のメールアドレスに変えてね！）
ssh-keygen -t ed25519 -C "your_email@example.com"
```

実行すると、いくつか質問されますが、**すべて何も入力せずに Enter キーを押して** 進めて大丈夫です！

```text
Enter file in which to save the key (/home/pi/.ssh/id_ed25519): (Enterを押す)
Enter passphrase (empty for no passphrase): (Enterを押す)
Enter same passphrase again: (Enterを押す)
```

これで、`~/.ssh/` というフォルダの中に、以下の2つのファイル（鍵）が作られました！
- `id_ed25519`：秘密鍵（絶対に他の人に見せてはいけない、自分だけの鍵）
- `id_ed25519.pub`：公開鍵（GitHub などの相手に渡す、公開用の鍵）

---

### STEP 2：公開鍵をコピーして GitHub に登録しよう

1. 作成した公開鍵（`.pub` がついている方）の中身を表示します。
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
2. 画面に `ssh-ed25519 AAAA...` から始まる長い文字列が表示されるので、それを**すべてコピー**します。
3. ブラウザで [GitHub](https://github.com/) にログインし、右上の自分のアイコンをクリックして **「Settings（設定）」** を開きます。
4. 左メニューから **「SSH and GPG keys」** をクリックします。
5. **「New SSH key」** ボタンをクリックします。
6. 設定を入力します：
   - **Title**: どのパソコンで作ったか分かりやすい名前（例: `My Laptop` や `Raspi Zero`）
   - **Key**: 先ほどコピーした公開鍵の文字列をそのまま貼り付けます。
7. **「Add SSH key」** ボタンを押して登録完了です！

---

### STEP 3：正しく接続できるかテストしてみよう

登録できたら、ターミナルで以下のテストコマンドを実行します：

```bash
ssh -T git@github.com
```

初めて接続するときは、以下のような質問が表示されます：
`Are you sure you want to continue connecting (yes/no/[fingerprint])?`
このときは、キーボードで **`yes`** と入力して Enter キーを押してください。

最後に、以下のようなウェルカムメッセージが表示されれば設定は大成功です！ 🎉
`Hi username! You've successfully authenticated, but GitHub does not provide shell access.`

---

**💡 まとめ：**
これで GitHub とあなたの環境が「合鍵」で安全に繋がりました！
これからは、GitHub からプログラムをダウンロードするときに、パスワードを入力せずに素早く `git clone` などのコマンドが使えるようになります。