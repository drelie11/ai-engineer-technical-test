import os
import glob
from extractor import extract_receipt
from database import insert_receipt

def process_single_receipt(image_path: str):
    """Extracts data from a single receipt image and stores it in the database."""
    print(f"\n--- Processing: {image_path} ---")
    try:
        data = extract_receipt(image_path)
        print("Extracted Data:")
        print(f"  Merchant: {data.get('merchant_name')}")
        print(f"  Date: {data.get('date')}")
        print(f"  Total: Rp {data.get('total_amount', 0):,}")
        print(f"  Items ({len(data.get('items', []))}):")
        for item in data.get('items', []):
            print(f"    - {item.get('quantity')}x {item.get('item_name')} @ Rp {item.get('price', 0):,}")

        receipt_id = insert_receipt(data)
        if receipt_id:
            print(f" Successfully stored into database with ID: {receipt_id}")
        return receipt_id

    except Exception as e:
        print(f"❌ Failed to process {image_path}: {e}")
        return None

def process_receipts_folder(folder_path: str = "receipt_images"):
    """Scans a folder for receipt images (.jpg, .jpeg, .png) and inserts them all."""
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist. Creating it now...")
        os.makedirs(folder_path)
        print(f"Please place your receipt images inside the '{folder_path}' folder and rerun this script.")
        return

    extensions = ('*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG')
    image_files = set()
    for ext in extensions:
        image_files.update(glob.glob(os.path.join(folder_path, ext)))
    image_files = list(image_files)

    if not image_files:
        print(f"No image files found in '{folder_path}'. Add your receipt images there.")
        return

    print(f"Found {len(image_files)} receipt image(s) to process...")
    for img_path in image_files:
        process_single_receipt(img_path)

if __name__ == "__main__":
    process_receipts_folder("receipt_images")