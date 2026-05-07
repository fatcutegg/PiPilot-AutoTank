import os
from dotenv import load_dotenv
from notion_client import Client

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    notion_api_key = os.getenv("NOTION_API_KEY")
    page_id = os.getenv("NOTION_PAGE_ID")
    
    if not notion_api_key or not page_id:
        print("Error: NOTION_API_KEY or NOTION_PAGE_ID is missing from .env file.")
        print("Please configure them based on .env.example")
        return

    print("Authenticating with Notion...")
    notion = Client(auth=notion_api_key)
    
    try:
        # Verify connection by fetching the page
        page = notion.pages.retrieve(page_id=page_id)
        page_title = page["properties"]["title"]["title"][0]["plain_text"] if "title" in page["properties"] else "Unknown Title"
        print(f"✅ Successfully connected to Notion Page: {page_title}")
        
        # Example: Append a simple text block to the page
        print("Appending a test block to the page...")
        notion.blocks.children.append(
            block_id=page_id,
            children=[
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": "This is an automated publish test from the Tank Project!"
                                }
                            }
                        ]
                    }
                }
            ]
        )
        print("✅ Test block appended successfully!")
        
    except Exception as e:
        print(f"❌ Failed to communicate with Notion API: {e}")

if __name__ == "__main__":
    main()
