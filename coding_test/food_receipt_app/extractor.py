import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List
from PIL import Image

load_dotenv() 

try:
    client = genai.Client()
except Exception as e:
    raise ValueError("Failed to initialize GenAI client. Check your GEMINI_API_KEY in .env") from e

class ItemSchema(BaseModel):
    item_name: str = Field(description="Name of the food or drink item.")
    price: int = Field(description="Price per item as a pure integer. Remove 'Rp', dots, and commas. Example: 45000")
    quantity: int = Field(description="Quantity of the item purchased. Default to 1 if not explicitly listed.")

class ReceiptSchema(BaseModel):
    date: str = Field(description="Date on the receipt strictly in YYYY-MM-DD format.")
    merchant_name: str = Field(description="Name of the store or restaurant.")
    total_amount: int = Field(description="Total bill amount as a pure integer. Example: 231440")
    items: List[ItemSchema] = Field(description="List of all purchased items found on the receipt.")

def extract_receipt(image_path: str) -> dict:
    print(f"Analyzing {image_path}...")
    
    try:
        img = Image.open(image_path)
        max_size = (1000, 1000)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
    except Exception as e:
        raise FileNotFoundError(f"Could not open image at {image_path}. Error: {e}")

    prompt = """
    Analyze this Indonesian food receipt.
    Extract the merchant name, transaction date, total amount, and EVERY item purchased.
    
    CRITICAL RULES FOR INDONESIAN RUPIAH (IDR) & DATES:
    - All prices/totals MUST be pure integers without 'Rp', dots, or commas (e.g., 231440).
    - Format date strictly as YYYY-MM-DD.
    - Make sure to populate the 'items' list with every line item you can see.
    """

    response = client.models.generate_content(
        model='gemini-3.5-flash', 
        contents=[prompt, img],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ReceiptSchema,
            temperature=0.0
        ),
    )
    
    return json.loads(response.text)

if __name__ == "__main__":
    test_image = "test_receipt.jpg" 
    
    if os.path.exists(test_image):
        extracted_data = extract_receipt(test_image)
        
        print("\n--- EXTRACTED JSON ---")
        print(json.dumps(extracted_data, indent=2))
    else:
        print(f"Please place '{test_image}' in the directory to test.")