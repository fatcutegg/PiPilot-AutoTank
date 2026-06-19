# 🚀 PiPilot-AutoTank: SSH接続から自動走行までの完全ガイドライン

このガイドラインは、同一LAN（ローカルネットワーク）内において、パソコン（PC）からSSH接続を用いてRaspberry Pi（ラズベリーパイ）搭載の戦車を操作し、**データ収集、モデル学習、自律走行（自動運転）**までのプロセスをスムーズに実施するための手順書です。

---

## 🛠️ 各種準備とネットワーク設定

パソコンとRaspberry Piが相互通信を行うために、双方が**同じWi-Fiネットワーク**に接続されている必要があります。

### 1. Wi-Fiルーターの設定
*   **同一SSIDへの接続**：パソコンとRaspberry Piを同じWi-Fiルーター（SSID）に接続します。
*   **IPアドレスの固定**：IPアドレスが変動するのを防ぐため、ルーター管理画面でRaspberry PiのMACアドレスに対して固定IPを割り当てることを推奨します。
*   **APアイソレーションの確認**：公共のWi-Fiやモバイルルーターでは「APアイソレーション（プライバシーセパレータ）」機能が有効になっている場合があります。これが有効な場合、同一Wi-Fi内の機器同士の通信が遮断されるため、設定画面で無効にしてください。

---

## 💻 パソコン側のSSHクライアント設定

使用するオペレーティングシステム（OS）に応じて、以下の手順でSSHを設定します。

### 1. Windows 10 & 11
Windowsは標準でOpenSSHをサポートしています。
*   **インストール確認と手順**：
    1.  **設定** -> **システム** -> **オプション機能** を開きます。
    2.  「OpenSSH クライアント」を検索し、未インストールの場合はインストールします。
    3.  インストール完了後、コマンドプロンプトまたはPowerShellを開き、以下のコマンドでインストールを確認します：
        ```cmd
        ssh -V
        ```

### 2. macOS
*   macOSには標準でSSHクライアントが搭載されています。「ターミナル (Terminal)」を起動するだけで、追加の設定なしで使用できます。

### 3. Chromebook
ChromeOSでは、Linux開発環境を有効にすることでターミナルを利用できます。
*   **セットアップ手順**：
    1.  ChromeOSの **設定** -> **詳細** -> **デベロッパー** を開きます。
    2.  **Linux開発環境（Crostini）** を有効にします。
    3.  有効化後、アプリ一覧から **ターミナル（Terminal）** を起動することで、`ssh` コマンドが使用可能になります。

---

## 🍓 Raspberry Pi側のCUI起動およびSSH設定

Raspberry PiのメモリやCPUリソースを節約し、走行制御の応答速度を向上させるため、**CUI（グラフィカルユーザーインターフェースなしのコンソールモード）**での運用を強く推奨します。

### 1. 起動モードをCUI（コンソール）へ変更する
Raspberry Piのターミナルで以下を実行します：
```bash
sudo raspi-config
```
*   **System Options** -> **Boot / Auto Login** の順に選択します。
*   **Console** または **Console Autologin**（自動でログインするコンソールモード）を選択します。
*   設定を保存し、Raspberry Piを再起動します。

### 2. SSHサービスを有効にする
システム起動時にSSHが有効になっていない場合は、`raspi-config` から有効化できます：
*   **Interface Options** -> **SSH** -> **Yes**（有効）を選択します。

### 3. SSH鍵認証によるパスワードなしログインの設定
セキュリティ向上とログイン簡易化のために、SSH鍵認証を設定します。
1.  **パソコン側で鍵ペアを生成**：
    ```bash
    ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519
    ```
2.  **公開鍵をRaspberry Piへ転送**（`username` と `ip` は実際のラズパイのユーザー名とIPに置き換えてください）：
    ```bash
    ssh-copy-id username@192.168.XXX.XXX
    ```
3.  **SSH接続設定の簡略化**：
    パソコン側の `~/.ssh/config` ファイルを編集（または作成）し、以下のように記述します：
    ```text
    Host tank
        HostName 192.168.XXX.XXX
        User username
        IdentityFile ~/.ssh/id_ed25519
    ```
    設定後、パソコンのターミナルで `ssh tank` と入力するだけで、パスワードなしでログインできます。

---

## 👩‍🎓 実習手順 - ログインとプロジェクトの準備

### 1. Raspberry Piへのログイン
パソコンのターミナルを起動し、Raspberry Piに接続します：
```bash
ssh tank
# 或者：ssh username@192.168.XXX.XXX
```

### 2. ディレクトリの作成（CUIコマンド）
ログイン後、データ収集およびプログラム配置用のフォルダを作成します：
```bash
cd ~        # ホームディレクトリに移動
mkdir -p Projects/PiPilot-AutoTank  # プロジェクト用フォルダを作成
cd Projects
```

### 3. Gitのインストール
Gitがインストールされていない場合は、以下のコマンドでインストールします：
```bash
sudo apt update
sudo apt install git -y
```

### 4. GitHubからプロジェクトのダウンロード
自動走行用のソースコード一式をクローンします：
```bash
git clone https://github.com/fatcutegg/PiPilot-AutoTank.git
cd PiPilot-AutoTank
```

### 5. Vimエディタの基本操作の習得
CUI環境でのコード編集には、**Vim（ヴィム）** エディタを使用します。
*   **ファイルを開く**：
    ```bash
    vim src/config.py
    ```
*   **最低限覚えておくべきVimの操作法**：
    1.  **編集モード (Insert Mode)**：キーボードの **`i`** キーを押します。左下に `-- INSERT --` と表示され、文字の入力や編集が可能になります。
    2.  **コマンドモードへの復帰**：キーボードの **`Esc`** キーを押します。
    3.  **保存して終了**：コマンドモードで **`:wq`** と入力し、Enterを押します。**保存せずに強制終了**する場合は **`:q!`** と入力し、Enterを押します。

---

## 🚗 データ収集から自動走行までの実走行フロー

セットアップ完了後、以下の手順に沿って自動運転プロセスを実行します。

### 1. 手動操縦とデータ収集 (Data Collection)
ラズパイ側でデータ収集プログラムを実行します。キーボード操作に合わせて、カメラ映像とモーターのPWM出力データが保存されます：
```bash
# 仮想環境の有効化
source venv/bin/activate
# データ収集プログラムの実行
python src/data_logger.py
```
*   **`r`** キー：データ記録の開始/一時停止。
*   **方向キー (↑ ↓ ← →)**：戦車を手動操作し、コースに沿って走行させます（目標：3000〜5000枚の画像）。
*   **`q`** キー：プログラムを保存して終了。

### 2. データセットのパソコンへの同期
Raspberry PiのCPUは学習処理に向いていないため、収集したデータをパソコンへ転送して学習を行います。
**パソコン（PC）側のターミナル**で以下を実行します：
```bash
# データを戦車からパソコンへ同期
rsync -avz tank:~/PiPilot-AutoTank/dataset/ ./dataset/
```

### 3. パソコン側でのモデル学習 (Model Training)
**パソコン側**の環境で学習スクリプトを実行します：
```bash
# 仮想環境を有効化して学習を開始
conda activate tank_py39
python training/train_regression_model.py
```
学習が正常に完了すると、パソコンの `models/` フォルダ内に `end2end_tank.h5` および `end2end_tank.weights.h5` が生成されます。

### 4. 学習済みモデルの戦車への同期 (Deploy Model)
**パソコン側**のターミナルで以下を実行し、モデルを戦車（Raspberry Pi）に転送します：
```bash
rsync -avz ./models/ tank:~/PiPilot-AutoTank/models/
```

### 5. 自動走行プログラムの起動 (Autonomous Drive)
戦車（Raspberry Pi）側で自律走行プログラムを起動します：
```bash
ssh tank
cd ~/PiPilot-AutoTank
source venv/bin/activate

# 自動走行の実行
python -u src/autonomous_drive.py
```
> [!CAUTION]
> **安全上の警告**：自動走行を開始すると、カメラ画像に基づき戦車が即座に走行を開始します。必ずテスト用コースのスタート地点に配置した状態で起動し、不測の事態に備えてターミナルで `Ctrl + C` を押せる準備（強制終了）を整えておいてください。
