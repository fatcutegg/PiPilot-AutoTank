#!/usr/bin/env python3
"""
Push all docs/ main files (00 to 08) to Notion.
1. Push 00_index.md (which is the master page)
2. Push each child file
"""
import os
import subprocess
import sys

DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs")
INDEX_FILE = os.path.join(DOCS_DIR, "00_index.md")
CHILD_FILES = [
    "01_intro.md",
    "02_ssh_setup.md",
    "03_env_setup.md",
    "04_teleop.md",
    "05_vision.md",
    "06_data_collection.md",
    "07_model_learning.md",
    "08_autonomous_drive.md",
]
SCRIPT = os.path.join(os.path.dirname(__file__), "notion_sync.py")


def push_file(file_path):
    rel = os.path.relpath(file_path, os.path.join(os.path.dirname(__file__), ".."))
    print(f"\n→ Pushing {rel} ...")
    result = subprocess.run(
        [sys.executable, SCRIPT, "push", file_path],
        capture_output=False,
    )
    if result.returncode != 0:
        print(f"❌ Failed to push {rel}")
        sys.exit(1)


def main():
    print("=" * 50)
    print("STEP 1: Push main index page")
    print("=" * 50)
    push_file(INDEX_FILE)

    print("\n" + "=" * 50)
    print("STEP 2: Push all main chapter pages")
    print("=" * 50)
    for fname in CHILD_FILES:
        fpath = os.path.join(DOCS_DIR, fname)
        if os.path.exists(fpath):
            push_file(fpath)
        else:
            print(f"  ⚠️  {fname} not found, skipping.")

    print("\n🎉 All main pages pushed to Notion successfully!")


if __name__ == "__main__":
    main()
