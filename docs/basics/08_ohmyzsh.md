---
Notion_Page_ID: 3840fc46-777e-81de-8b07-c9ace488ecff
Notion_Parent_ID: 35a0fc46-777e-81eb-8890-f9cf284b4c5e
---

# 🐚 基礎知識 08：Oh My Zsh でターミナルをもっと使いやすくしよう！

基本的なシェル操作（第2回）を覚えたら、次は「Oh My Zsh（オー・マイ・ズィーシェル）」を使って、ターミナル（コマンドを入力する黒い画面）をもっと使いやすく、カッコよくカスタマイズしてみましょう！

これを入れると、コマンドの入力ミスが減ったり、以前に入力したコマンドを自動で予想してくれたりして、戦車のプログラミングや操作がとても快適になります。

---

## 1. Oh My Zsh をインストールしよう

まずは、Oh My Zsh をインストールするためのスクリプトを実行します。ターミナルを開いて、以下のコマンドをコピーして貼り付け、Enterキーを押してください。

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

> **💡 ヒント（中学生向け）：**
> もしインストール中に「Do you want to change your default shell to zsh? [Y/n]」（標準のシェルを Zsh に変更しますか？）と聞かれたら、キーボードの `Y` を押して Enter を押してください。パスワードを聞かれたら、Raspberry Pi のパスワードを入力してください。

---

## 2. おすすめのプラグイン（拡張機能）をインストールしよう

コマンドの入力を強力にサポートしてくれる2つのプラグインをインストールします。

### ① 過去の履歴から予測する「自動補完」機能（zsh-autosuggestions）
以前に入力したコマンドを覚えておいてくれて、文字を入力し始めると薄いグレーで「次にこれを入れる？」と教えてくれる機能です。キーボードの右矢印キー（`→`）を押すだけで自動入力されます！

```bash
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

### ② 入力間違いを色で教えてくれる「構文ハイライト」機能（zsh-syntax-highlighting）
入力したコマンドが正しいときは「緑色」、スペルミスなどで間違っているときは「赤色」で表示してくれる便利な機能です。実行する前に間違いに気づけるのでとても安心です！

```bash
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

---

## 3. 設定ファイルを書き換えよう

インストールしたプラグインを有効にするために、設定ファイル（`~/.zshrc`）を書き換えます。

1. ターミナルで `nano ~/.zshrc` または `vim ~/.zshrc` を実行して設定ファイルを開きます。
2. `plugins=(git)` と書かれている場所を探します。
3. 以下のように書き換えて、新しく入れたプラグインを追加します：

```bash
plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
```

4. 保存してファイルを閉じます。（nano の場合は `Ctrl + O` の後に `Enter` で保存し、`Ctrl + X` で終了します）
5. 以下のコマンドを実行して、設定を今すぐ反映させましょう：
   ```bash
   source ~/.zshrc
   ```

---

## 4. Conda（コンダ）を自動で有効にしよう

Pythonの環境を管理するツール「Conda」が、Zsh を開いたときにも自動で起動するように設定しておきます。

```bash
conda init zsh
```

これを実行したあとに一度ターミナルを閉じて、新しく開き直すと設定がすべて有効になります！

---

**💡 まとめ：**
使いやすい開発環境を整えることは、素晴らしいロボットやAIを作るための第一歩です。これで、コマンドの入力がぐっと楽しく、スムーズになりましたね！