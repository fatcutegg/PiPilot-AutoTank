---
Notion_Page_ID: 35a0fc46-777e-81ce-a35b-d49b97628fae
Notion_Parent_ID: 35a0fc46-777e-81eb-8890-f9cf284b4c5e
---

# 🐙 Git 入門：コードを安全に管理しよう

**Git** は「コードの変更履歴を記録するツール」です。
ミスをしても昔の状態に戻せるので、安心してコードを書けます！

---

## 🤔 Gitって何？

Gitは**バージョン管理システム**です。
たとえば、ゲームのセーブデータのように、好きなタイミングでコードの状態を保存できます。

```
プロジェクト/
├── main.py       ← 今のコード
└── .git/         ← 変更履歴がここに記録されている
```

---

## 🚀 基本コマンド

### 1. リポジトリをコピーする（clone）

```bash
git clone https://github.com/fatcutegg/PiPilot-AutoTank.git
```

> GitHubにあるプロジェクトを自分のパソコンに持ってくるコマンドです。

---

### 2. 変更を記録する（add → commit）

```bash
# 変更したファイルを「ステージング」する
git add main.py

# 変更内容にメモをつけて保存する
git commit -m "モーターの速度を調整した"
```

---

### 3. GitHubに送る（push）

```bash
git push origin main
```

---

### 4. 最新版を取得する（pull）

```bash
git pull
```

---

## 📋 よく使うコマンド一覧

| コマンド | 意味 |
|----------|------|
| `git status` | 今どんな変更があるか確認する |
| `git log` | これまでの変更履歴を見る |
| `git diff` | 変更した内容の差分を見る |
| `git add .` | 全ての変更をステージングする |
| `git commit -m "メッセージ"` | コミット（保存）する |
| `git push` | GitHubに送る |
| `git pull` | GitHubから最新版を取得する |

---

## 🎯 ミッション

1. `git clone` でPiPilotのコードをダウンロードしよう
2. ファイルを編集して `git status` で変更を確認しよう
3. `git add` → `git commit` → `git push` を一通り体験しよう

---

👉 次は [🐍 Python 入門](https://www.notion.so/35a0fc46777e816eba15f4a3eb922cbd) へ