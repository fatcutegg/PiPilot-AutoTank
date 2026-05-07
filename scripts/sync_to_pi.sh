#!/bin/bash
# Mac から 樹莓派 へコードを同期するスクリプト (Rsync Sync Script)
# Type-C OTG で接続されている 'tank' エイリアスを使用します。

echo "Syncing code to Raspberry Pi (PiPilot-AutoTank)..."
rsync -avz --exclude '.git' --exclude '__pycache__' --exclude 'dataset' ./ tank:~/PiPilot-AutoTank/
echo "Sync completed at $(date)"
