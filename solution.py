import json
import pandas as pd
import os
import datetime

# --- CONFIGURATION ---
SOURCE_FILE = 'raw_data.json'
OUTPUT_FILE = 'processed_data.csv'

def extract(file_path):
    """Task 1: Doc du lieu JSON tu file."""
    print(f"Extracting data from {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Log dung keyword "Extracted X raw records."
        print(f"Extracted {len(data)} raw records.")
        return data
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON.")
        return None

def validate(data):
    """Task 2: Kiem tra chat luong du lieu."""
    valid_records = []
    error_count = 0

    for record in data:
        record_id = record.get('id', 'Unknown')
        price = record.get('price', 0)
        category = record.get('category')

        # Logic kiem tra
        if price <= 0:
            print(f"  [DROP] Record id={record_id} - price={price} is invalid (price <= 0)")
            error_count += 1
            continue
            
        if not category or not str(category).strip():
            print(f"  [DROP] Record id={record_id} - category is empty")
            error_count += 1
            continue

        valid_records.append(record)

    # Log dung keyword "records kept, X records dropped."
    print(f"Validation complete. Valid: {len(valid_records)} records kept, {error_count} records dropped.")
    return valid_records

def transform(data):
    """Task 3: Ap dung business logic."""
    if not data:
        return None

    df = pd.DataFrame(data)

    # Thuc hien logic
    df['discounted_price'] = df['price'] * 0.9
    df['category'] = df['category'].astype(str).str.title()
    df['processed_at'] = datetime.datetime.now().isoformat()

    # Log dung keyword "records transformed."
    print(f"Transform complete. {len(df)} records transformed.")
    return df

def load(df, output_path):
    """Task 4: Luu DataFrame ra file CSV."""
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    # Dung chinh xac "Data saved to..." nhu trong Option 1
    print(f"Data saved to {output_path}")

# ============================================================
# MAIN PIPELINE
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("ETL Pipeline Started...")
    print("=" * 50)

    # 1. Extract
    raw_data = extract(SOURCE_FILE)

    if raw_data:
        # 2. Validate
        clean_data = validate(raw_data)

        # 3. Transform
        final_df = transform(clean_data)

        # 4. Load
        if final_df is not None:
            load(final_df, OUTPUT_FILE)
            # Log cuoi cung phai khop voi logic Pipeline completed!
            print(f"\nPipeline completed! {len(final_df)} records saved.")
        else:
            print("\nTransform returned None.")
    else:
        print("\nPipeline aborted: No data extracted.")