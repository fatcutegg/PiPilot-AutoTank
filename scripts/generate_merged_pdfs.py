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

# Define the files in each group (relative to DOCS_DIR)
MAIN_FILES = [
    "00_index.md",
    "01_intro.md",
    "02_teleop.md",
    "03_vision.md"
]

BASICS_FILES = [
    "basics/00_basics_index.md",
    "basics/01_linux.md",
    "basics/02_shell.md",
    "basics/03_vim.md",
    "basics/04_ssh.md",
    "basics/05_raspi_setup.md",
    "basics/06_git.md",
    "basics/07_python.md",
    "basics/08_ohmyzsh.md"
]

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Custom highlighting using Pygments
def highlight_code(code, name, attrs):
    if not name:
        return None
    try:
        lexer = get_lexer_by_name(name)
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
  
  .page-break {{
    page-break-before: always;
    break-before: always;
  }}
</style>
</head>
<body>
  <div class="header">
    <span class="header-left">{doc_title}</span>
    <span class="header-right">{manual_name}</span>
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
    markdown_text = content
    if content.startswith('---'):
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if match:
            markdown_text = content[match.end():]
    return markdown_text

def resolve_links(markdown_text, current_file_rel, current_group):
    """Rewrite links to point to local anchors or cross-document targets."""
    current_dir = os.path.dirname(current_file_rel)
    
    def replacer(match):
        text = match.group(1)
        target_path = match.group(2)
        anchor = match.group(3) or ""
        
        # Clean up path
        normalized_target = os.path.normpath(os.path.join(current_dir, target_path))
        
        # Check if the target is in the current group
        in_current_group = False
        target_base = ""
        for group_file in current_group:
            if normalized_target == group_file:
                in_current_group = True
                target_base = os.path.splitext(os.path.basename(group_file))[0]
                break
                
        if in_current_group:
            # Anchor to section inside the same PDF
            return f"[{text}](#chapter_{target_base})"
        else:
            # Link to the other PDF file
            if normalized_target in MAIN_FILES:
                target_base = os.path.splitext(os.path.basename(normalized_target))[0]
                return f"[{text}](main_manual.pdf#chapter_{target_base})"
            elif normalized_target in BASICS_FILES:
                target_base = os.path.splitext(os.path.basename(normalized_target))[0]
                return f"[{text}](basics_guide.pdf#chapter_{target_base})"
            else:
                # Return original match for external/absolute links
                return match.group(0)
                
    # Regex matching [text](path.md#anchor) or [text](path.md)
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\.md(#([^)]+))?\)', replacer, markdown_text)

def generate_merged_pdf(files, manual_name, output_filename, temp_html_dir):
    """Merge files and print to PDF using headless Chrome."""
    print(f"\nGenerating: {output_filename}")
    
    chapters_html = []
    
    for i, file_rel in enumerate(files):
        full_path = os.path.join(DOCS_DIR, file_rel)
        base_name = os.path.splitext(os.path.basename(file_rel))[0]
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        markdown_text = parse_markdown(content)
        # Rewrite links for correct PDF behavior
        markdown_text = resolve_links(markdown_text, file_rel, files)
        
        # Parse MD to HTML
        chapter_html = md.render(markdown_text)
        
        # Add page break before every chapter (except the first one)
        page_break_prefix = '<div class="page-break"></div>\n' if i > 0 else ''
        
        # Wrap each chapter inside a div with anchor id
        chapters_html.append(
            f'{page_break_prefix}<div id="chapter_{base_name}" class="chapter-content">\n{chapter_html}\n</div>'
        )
        
    combined_content = "\n\n".join(chapters_html)
    
    # Render final HTML page
    full_html = HTML_TEMPLATE.format(
        doc_title=manual_name,
        manual_name=manual_name,
        pygments_css=pygments_css,
        content_html=combined_content
    )
    
    # Save temp HTML in the specified folder (docs/ or docs/basics/) to resolve images relative path
    temp_html_filename = f"__temp_merged_{os.path.splitext(output_filename)[0]}.html"
    temp_html_path = os.path.join(temp_html_dir, temp_html_filename)
    
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
        
    target_pdf_path = os.path.join(OUTPUT_DIR, output_filename)
    if os.path.exists(target_pdf_path):
        os.remove(target_pdf_path)
        
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
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Wait up to 30s
        start_time = time.time()
        success = False
        while time.time() - start_time < 30:
            if os.path.exists(target_pdf_path) and os.path.getsize(target_pdf_path) > 0:
                success = True
                break
            time.sleep(0.1)
            
        # Clean up Chrome process immediately
        try:
            proc.terminate()
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
            
        if success:
            print(f"Success! Generated {output_filename} ({os.path.getsize(target_pdf_path)} bytes)")
        else:
            print(f"Error printing {output_filename}: PDF was not created or empty.")
    except Exception as e:
        print(f"Exception printing {output_filename}: {e}")
    finally:
        # Clean up temp files
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)
        if os.path.exists(chrome_profile_dir):
            shutil.rmtree(chrome_profile_dir, ignore_errors=True)

def main():
    # 1. Generate Main Handbook
    # Temp HTML dir is DOCS_DIR so that intro.md images relative path 'assets/...' works
    generate_merged_pdf(
        files=MAIN_FILES,
        manual_name="PiPilot AutoTank 自動運転マニュアル (手動/AI運転篇)",
        output_filename="main_manual.pdf",
        temp_html_dir=DOCS_DIR
    )
    
    # 2. Generate Basics Guide
    # Temp HTML dir is docs/basics/ so that relative links match basics/ directory
    generate_merged_pdf(
        files=BASICS_FILES,
        manual_name="PiPilot AutoTank 🛠️ 基礎知識ガイド",
        output_filename="basics_guide.pdf",
        temp_html_dir=os.path.join(DOCS_DIR, "basics")
    )
    
    print("\nMerge complete! Merged PDFs are saved in docs_pdf/")

if __name__ == "__main__":
    main()
