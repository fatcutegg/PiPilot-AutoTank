#!/usr/bin/env python3
import os
import re
import shutil
import subprocess
import tempfile
from markdown_it import MarkdownIt
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from dotenv import load_dotenv

# Load environmental variables from .env
load_dotenv()

# Configuration
# Smart workspace path detection (checks CWD first, then falls back to parent of the scripts folder)
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_of_script = os.path.dirname(script_dir)

default_workspace = os.getcwd()
if not os.path.exists(os.path.join(default_workspace, "docs")):
    if os.path.exists(os.path.join(parent_of_script, "docs")):
        default_workspace = parent_of_script

WORKSPACE_DIR = os.getenv("WORKSPACE_DIR", default_workspace)
DOCS_DIR = os.getenv("DOCS_DIR", os.path.join(WORKSPACE_DIR, "docs"))
OUTPUT_DIR = os.getenv("OUTPUT_DIR", os.path.join(WORKSPACE_DIR, "docs_pdf"))
CHROME_PATH = os.getenv("CHROME_PATH", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Custom highlighting using Pygments
def highlight_code(code, name, attrs):
    if not name:
        return None
    try:
        lexer = get_lexer_by_name(name)
        # Use nowrap=True so markdown-it-py handles wrapping tags
        return highlight(code, lexer, HtmlFormatter(nowrap=True))
    except Exception:
        return None

# Initialize MarkdownIt parser
md = MarkdownIt('commonmark', {'highlight': highlight_code}).enable('table').enable('strikethrough')

# Generate Pygments CSS for friendly light theme
pygments_css = HtmlFormatter(style='friendly').get_style_defs('pre')

# HTML template with printing optimization
HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{doc_title}</title>
<style>
  @page {{
    size: A4;
    margin: 20mm 15mm 20mm 15mm;
  }}
  
  /* Reset and base styles */
  * {{
    box-sizing: border-box;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Meiryo", sans-serif;
    font-size: 10pt;
    line-height: 1.6;
    color: #2d3748;
    background-color: #fff;
    margin: 0;
    padding: 0;
  }}

  /* Page break rules for clean print */
  h1, h2, h3, h4, h5, h6 {{
    page-break-after: avoid;
    break-after: avoid;
    color: #1a365d;
    font-weight: 700;
  }}
  h1 {{
    font-size: 18pt;
    margin-top: 0;
    margin-bottom: 10pt;
    border-bottom: 2px solid #2b6cb0;
    padding-bottom: 4pt;
  }}
  h2 {{
    font-size: 13pt;
    margin-top: 16pt;
    margin-bottom: 8pt;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 3pt;
  }}
  h3 {{
    font-size: 11pt;
    margin-top: 12pt;
    margin-bottom: 6pt;
  }}
  p {{
    margin-top: 0;
    margin-bottom: 8pt;
    text-align: justify;
  }}
  
  /* Links styling for printing */
  a {{
    color: #2b6cb0;
    text-decoration: underline;
  }}
  
  /* Lists */
  ul, ol {{
    margin-top: 0;
    margin-bottom: 8pt;
    padding-left: 18pt;
  }}
  li {{
    margin-bottom: 3pt;
  }}
  
  /* Code and Pre */
  code {{
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
    font-size: 8.5pt;
    background-color: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 3px;
    padding: 2px 4px;
    color: #c53030;
  }}
  pre {{
    background-color: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 8pt;
    margin-top: 0;
    margin-bottom: 8pt;
    overflow: auto;
  }}
  pre code {{
    background-color: transparent;
    border: none;
    padding: 0;
    color: #2d3748;
    display: block;
    white-space: pre-wrap;
    word-wrap: break-word;
  }}

  /* Pygments syntax highlighting overrides */
  {pygments_css}

  /* Blockquotes */
  blockquote {{
    margin: 0 0 8pt 0;
    padding: 6pt 10pt;
    background-color: #f7fafc;
    border-left: 4px solid #cbd5e0;
    color: #4a5568;
  }}
  blockquote p {{
    margin-bottom: 0;
  }}

  /* Tables */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 10pt;
    page-break-inside: avoid;
    break-inside: avoid;
  }}
  thead {{
    display: table-header-group;
  }}
  tr {{
    page-break-inside: avoid;
    break-inside: avoid;
  }}
  th, td {{
    border: 1px solid #cbd5e0;
    padding: 5pt 7pt;
    text-align: left;
    font-size: 9pt;
  }}
  th {{
    background-color: #f7fafc;
    font-weight: bold;
    color: #2d3748;
  }}
  
  /* Running Header and Footer (Only printed) */
  .header {{
    position: fixed;
    top: -12mm;
    left: 0;
    right: 0;
    height: 8mm;
    font-size: 8.5pt;
    color: #718096;
    border-bottom: 1px solid #e2e8f0;
    line-height: 8mm;
  }}
  .header-left {{
    float: left;
  }}
  .header-right {{
    float: right;
  }}
  .footer {{
    position: fixed;
    bottom: -12mm;
    left: 0;
    right: 0;
    height: 8mm;
    font-size: 8.5pt;
    color: #718096;
    border-top: 1px solid #e2e8f0;
    line-height: 12mm;
    text-align: center;
  }}
  .footer .page-num::after {{
    content: counter(page);
  }}
  
  /* Images */
  img {{
    max-width: 100%;
    height: auto;
    display: block;
    margin: 12pt auto;
    page-break-inside: avoid;
    break-inside: avoid;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }}
</style>
</head>
<body>
  <div class="header">
    <span class="header-left">{doc_title}</span>
    <span class="header-right">PiPilot AutoTank Manual</span>
  </div>
  <div class="footer">
    <span>Page </span><span class="page-num"></span>
  </div>
  
  <div class="content">
    {content_html}
  </div>
</body>
</html>
"""

def parse_markdown(content):
    """Separate frontmatter and markdown body."""
    frontmatter = {}
    markdown_text = content
    if content.startswith('---'):
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if match:
            frontmatter_text = match.group(1)
            markdown_text = content[match.end():]
            for line in frontmatter_text.split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    frontmatter[key.strip()] = val.strip()
    return frontmatter, markdown_text

def extract_title(markdown_text):
    """Extract document title from the first H1 header."""
    for line in markdown_text.split('\n'):
        line = line.strip()
        if line.startswith('# '):
            # Strip emojis or keep them
            return line[2:].strip()
    return "Documentation"

def render_md_file(md_path, relative_to_docs):
    # Determine target paths
    rel_dir, filename = os.path.split(relative_to_docs)
    base_name, _ = os.path.splitext(filename)
    
    target_dir = os.path.join(OUTPUT_DIR, rel_dir)
    os.makedirs(target_dir, exist_ok=True)
    pdf_filename = f"{base_name}.pdf"
    target_pdf_path = os.path.join(target_dir, pdf_filename)
    
    print(f"Processing: {relative_to_docs} -> docs_pdf/{os.path.join(rel_dir, pdf_filename)}")
    
    # Read Markdown
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    frontmatter, markdown_text = parse_markdown(content)
    doc_title = extract_title(markdown_text)
    
    # Replace links pointing to .md files with .pdf links
    # This allows local document navigation inside PDF viewer
    # E.g. [Next](basics/01_linux.md) -> [Next](basics/01_linux.pdf)
    markdown_text = re.sub(r'\[([^\]]+)\]\(([^)]+)\.md(#([^)]+))?\)', r'[\1](\2.pdf\3)', markdown_text)
    
    # Render Markdown to HTML body
    content_html = md.render(markdown_text)
    
    # Wrap in our HTML template
    full_html = HTML_TEMPLATE.format(
        doc_title=doc_title,
        pygments_css=pygments_css,
        content_html=content_html
    )
    
    # Save temporary HTML file in the SAME directory to preserve relative paths
    temp_html_path = os.path.join(os.path.dirname(md_path), f"__temp_{base_name}.html")
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
        
    # Execute Chrome print-to-pdf
    chrome_profile_dir = tempfile.mkdtemp(prefix="chrome_pdf_profile_")
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--user-data-dir={chrome_profile_dir}",
        f"--print-to-pdf={target_pdf_path}",
        f"file://{temp_html_path}"
    ]
    
    import time
    if os.path.exists(target_pdf_path):
        os.remove(target_pdf_path)

    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Wait for the PDF to be generated (max 30 seconds)
        start_time = time.time()
        success = False
        while time.time() - start_time < 30:
            if os.path.exists(target_pdf_path) and os.path.getsize(target_pdf_path) > 0:
                success = True
                break
            time.sleep(0.1)
            
        # Terminate Chrome immediately to prevent hanging
        try:
            proc.terminate()
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
            
        if not success:
            print(f"Error printing {filename}: PDF was not created or empty.")
    except Exception as e:
        print(f"Exception printing {filename}: {e}")
    finally:
        # Clean up
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)
        if os.path.exists(chrome_profile_dir):
            shutil.rmtree(chrome_profile_dir, ignore_errors=True)

def main():
    # Traverse through docs folder
    print(f"Scanning markdown files in: {DOCS_DIR}")
    for root, dirs, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, DOCS_DIR)
                render_md_file(full_path, rel_path)
    print("Done! All documents rendered to docs_pdf/")

if __name__ == "__main__":
    main()
