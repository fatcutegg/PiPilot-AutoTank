#!/bin/bash
# Mac から 樹莓派 へコードを同期するスクリプト (Rsync Sync Script)
# Type-C OTG で接続されている 'tank' エイリアスを使用します。

echo "Syncing code to Raspberry Pi (tank)..."
rsync -avz --exclude '.git' --exclude '__pycache__' ./ tank:~/tank_project/
echo "Sync completed at $(date)"
