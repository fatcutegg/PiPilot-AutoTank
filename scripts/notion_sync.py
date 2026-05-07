import os
import sys
import argparse
import yaml
from dotenv import load_dotenv
from notion_client import Client

def parse_frontmatter(md_content):
    """Parses YAML frontmatter from markdown and returns dict and the rest of content."""
    lines = md_content.split('\n')
    if not lines or lines[0].strip() != '---':
        return {}, md_content
        
    frontmatter_lines = []
    end_idx = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            end_idx = i
            break
        frontmatter_lines.append(lines[i])
        
    if end_idx == -1:
        return {}, md_content
        
    try:
        frontmatter = yaml.safe_load('\n'.join(frontmatter_lines))
        content = '\n'.join(lines[end_idx+1:])
        return frontmatter or {}, content
    except Exception as e:
        print(f"Warning: Failed to parse frontmatter: {e}")
        return {}, md_content

def markdown_to_notion_blocks(markdown_text):
    """Converts a simple markdown string to Notion block format."""
    blocks = []
    lines = markdown_text.split('\n')
    in_code_block = False
    code_content = []
    code_language = "plain text"

    for line in lines:
        if line.startswith("```"):
            if in_code_block:
                blocks.append({
                    "object": "block",
                    "type": "code",
                    "code": {
                        "rich_text": [{"type": "text", "text": {"content": "\n".join(code_content)}}],
                        "language": code_language
                    }
                })
                in_code_block = False
                code_content = []
            else:
                in_code_block = True
                lang = line[3:].strip()
                if lang == "bash":
                    code_language = "shell"
                elif lang == "python":
                    code_language = "python"
                else:
                    code_language = "plain text"
            continue
            
        if in_code_block:
            code_content.append(line)
            continue
            
        line_stripped = line.strip()
        if not line_stripped:
            continue
            
        if line_stripped.startswith("---"):
            blocks.append({
                "object": "block",
                "type": "divider",
                "divider": {}
            })
        elif line_stripped.startswith("# "):
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {"rich_text": [{"type": "text", "text": {"content": line_stripped[2:]}}]}
            })
        elif line_stripped.startswith("## "):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": line_stripped[3:]}}]}
            })
        elif line_stripped.startswith("### "):
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {"rich_text": [{"type": "text", "text": {"content": line_stripped[4:]}}]}
            })
        elif line_stripped.startswith("- "):
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": line_stripped[2:]}}]}
            })
        elif line_stripped[0].isdigit() and line_stripped[1:3] == ". ":
            blocks.append({
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": line_stripped[3:]}}]}
            })
        elif line_stripped.startswith("![") and "]" in line_stripped and "(" in line_stripped:
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": f"📷 [画像プレースホルダー (Notionで手動アップロードしてください)]: {line_stripped}"}}]}
            })
        else:
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": line_stripped}}]}
            })
            
    return blocks

def blocks_to_markdown(blocks):
    """Converts a list of Notion blocks to a Markdown string."""
    md_lines = []
    for block in blocks:
        b_type = block.get("type")
        if not b_type: continue
        
        if b_type == "paragraph":
            text = "".join([rt["plain_text"] for rt in block["paragraph"]["rich_text"]])
            md_lines.append(text)
        elif b_type == "heading_1":
            text = "".join([rt["plain_text"] for rt in block["heading_1"]["rich_text"]])
            md_lines.append(f"# {text}")
        elif b_type == "heading_2":
            text = "".join([rt["plain_text"] for rt in block["heading_2"]["rich_text"]])
            md_lines.append(f"## {text}")
        elif b_type == "heading_3":
            text = "".join([rt["plain_text"] for rt in block["heading_3"]["rich_text"]])
            md_lines.append(f"### {text}")
        elif b_type == "bulleted_list_item":
            text = "".join([rt["plain_text"] for rt in block["bulleted_list_item"]["rich_text"]])
            md_lines.append(f"- {text}")
        elif b_type == "numbered_list_item":
            text = "".join([rt["plain_text"] for rt in block["numbered_list_item"]["rich_text"]])
            md_lines.append(f"1. {text}") 
        elif b_type == "code":
            text = "".join([rt["plain_text"] for rt in block["code"]["rich_text"]])
            lang = block["code"].get("language", "")
            if lang == "shell": lang = "bash"
            elif lang == "plain text": lang = ""
            md_lines.append(f"```{lang}\n{text}\n```")
        elif b_type == "divider":
            md_lines.append("---")
        elif b_type == "image":
            url = ""
            if "external" in block["image"]:
                url = block["image"]["external"]["url"]
            elif "file" in block["image"]:
                url = block["image"]["file"]["url"]
            md_lines.append(f"![Notion Image]({url})")
            
        if md_lines and md_lines[-1] != "":
            md_lines.append("")
            
    return "\n".join(md_lines)

def get_page_id_from_file(file_path):
    if not os.path.exists(file_path):
        return None, None, None
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    frontmatter, md_content = parse_frontmatter(content)
    page_id = frontmatter.get("Notion_Page_ID")
    if str(page_id) == "REPLACE_WITH_YOUR_NOTION_PAGE_ID":
        page_id = None
    return page_id, frontmatter, md_content

def push_to_notion(file_path, client):
    page_id, frontmatter, md_content = get_page_id_from_file(file_path)
    parent_id = frontmatter.get("Notion_Parent_ID")
    
    # Extract title from markdown
    title = "Untitled"
    for line in md_content.split('\n'):
        if line.startswith("# "):
            title = line[2:].strip()
            break

    if not page_id:
        if not parent_id or str(parent_id) == "REPLACE_WITH_YOUR_NOTION_PARENT_ID":
            print(f"Error: {file_path} is missing both a valid 'Notion_Page_ID' and 'Notion_Parent_ID'.")
            sys.exit(1)
            
        print(f"Creating new page under parent {parent_id}...")
        new_page = client.pages.create(
            parent={"page_id": parent_id},
            properties={
                "title": [{"text": {"content": title}}]
            }
        )
        page_id = new_page["id"]
        print(f"Created new page with ID: {page_id}")
        
        # Update local file with the new page_id
        frontmatter["Notion_Page_ID"] = page_id
        frontmatter_yaml = yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False).strip()
        final_content = f"---\n{frontmatter_yaml}\n---\n\n{md_content.strip()}"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(final_content)
    else:
        print(f"Pushing {file_path} to Notion Page {page_id}...")
        try:
            client.pages.update(
                page_id=page_id,
                properties={"title": [{"text": {"content": title}}]}
            )
        except Exception as e:
            print(f"Warning: Could not update page title: {e}")

    # 1. Delete existing blocks
    print("Cleaning up existing blocks...")
    existing_blocks = client.blocks.children.list(block_id=page_id).get("results", [])
    for block in existing_blocks:
        if block.get("type") == "child_page":
            continue
        try:
            client.blocks.delete(block_id=block["id"])
        except Exception as e:
            pass 
            
    # 2. Convert and Upload
    print("Parsing Markdown to Notion Blocks...")
    blocks = markdown_to_notion_blocks(md_content)
    
    print(f"Uploading {len(blocks)} blocks...")
    for i in range(0, len(blocks), 100):
        batch = blocks[i:i+100]
        client.blocks.children.append(block_id=page_id, children=batch)
        
    print("✅ Push complete!")

def pull_from_notion(file_path, client):
    page_id, frontmatter, _ = get_page_id_from_file(file_path)
    if not page_id:
        print(f"Error: {file_path} does not have a valid 'Notion_Page_ID' to pull from.")
        sys.exit(1)
        
    print(f"Pulling from Notion Page {page_id} to {file_path}...")
    
    blocks = []
    has_more = True
    start_cursor = None
    while has_more:
        res = client.blocks.children.list(block_id=page_id, start_cursor=start_cursor)
        blocks.extend(res.get("results", []))
        has_more = res.get("has_more", False)
        start_cursor = res.get("next_cursor")
        
    print(f"Downloaded {len(blocks)} blocks. Converting to Markdown...")
    new_md_content = blocks_to_markdown(blocks)
    
    # Keep the original title if missing from blocks (since title is a page property)
    # We'll just fetch the page title
    page = client.pages.retrieve(page_id=page_id)
    title = page["properties"]["title"]["title"][0]["plain_text"] if "title" in page["properties"] and page["properties"]["title"]["title"] else "Untitled"
    if not new_md_content.startswith("# "):
        new_md_content = f"# {title}\n\n{new_md_content}"
        
    frontmatter_yaml = yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False).strip()
    final_content = f"---\n{frontmatter_yaml}\n---\n\n{new_md_content}"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(final_content)
        
    print("✅ Pull complete!")

def main():
    parser = argparse.ArgumentParser(description="Bidirectional sync between local Markdown and Notion.")
    parser.add_argument("action", choices=["push", "pull"], help="Action to perform: push to Notion or pull from Notion.")
    parser.add_argument("file", help="Path to the local markdown file.")
    args = parser.parse_args()

    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    load_dotenv(env_path)
    
    notion_api_key = os.getenv("NOTION_API_KEY")
    if not notion_api_key:
        print("Error: NOTION_API_KEY is missing from .env file.")
        sys.exit(1)

    print("Authenticating with Notion...")
    notion = Client(auth=notion_api_key)
    
    try:
        if args.action == "push":
            push_to_notion(args.file, notion)
        elif args.action == "pull":
            pull_from_notion(args.file, notion)
    except Exception as e:
        print(f"❌ Operation failed: {e}")

if __name__ == "__main__":
    main()
