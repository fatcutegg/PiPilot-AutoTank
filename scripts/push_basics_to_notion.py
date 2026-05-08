#!/usr/bin/env python3
"""
Push all docs/basics/ files to Notion in the correct order.
1. Push 00_basics_index.md (creates parent page, writes back Notion_Page_ID)
2. Update all child files' Notion_Parent_ID to the actual page ID
3. Push each child file
"""
import os
import re
import subprocess
import sys
import yaml

BASICS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "basics")
INDEX_FILE = os.path.join(BASICS_DIR, "00_basics_index.md")
CHILD_FILES = [
    "01_linux.md",
    "02_shell.md",
    "03_vim.md",
    "04_ssh.md",
    "05_raspi_setup.md",
    "06_git.md",
    "07_python.md",
]
SCRIPT = os.path.join(os.path.dirname(__file__), "notion_sync.py")


def read_frontmatter_page_id(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    lines = content.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    fm_lines = []
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            break
        fm_lines.append(lines[i])
    fm = yaml.safe_load("\n".join(fm_lines)) or {}
    return fm.get("Notion_Page_ID")


def update_parent_id(file_path, parent_id):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Replace placeholder parent ID
    content = re.sub(
        r"(Notion_Parent_ID:\s*)basics_index",
        f"Notion_Parent_ID: {parent_id}",
        content,
    )
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Updated Notion_Parent_ID in {os.path.basename(file_path)}")


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
    print("STEP 1: Push basics index page")
    print("=" * 50)
    push_file(INDEX_FILE)

    # Read the new page ID written back by the script
    parent_id = read_frontmatter_page_id(INDEX_FILE)
    if not parent_id:
        print("❌ Could not read Notion_Page_ID from index file after push.")
        sys.exit(1)
    print(f"\n✅ Basics index page ID: {parent_id}")

    print("\n" + "=" * 50)
    print("STEP 2: Update child files with correct parent ID")
    print("=" * 50)
    for fname in CHILD_FILES:
        fpath = os.path.join(BASICS_DIR, fname)
        if os.path.exists(fpath):
            update_parent_id(fpath, parent_id)
        else:
            print(f"  ⚠️  {fname} not found, skipping.")

    print("\n" + "=" * 50)
    print("STEP 3: Push all child pages")
    print("=" * 50)
    for fname in CHILD_FILES:
        fpath = os.path.join(BASICS_DIR, fname)
        if os.path.exists(fpath):
            push_file(fpath)

    print("\n🎉 All basics pages pushed to Notion successfully!")


if __name__ == "__main__":
    main()
