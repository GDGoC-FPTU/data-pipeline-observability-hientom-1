import json
import pandas as pd
import os
import datetime

# --- CONFIGURATION ---
SOURCE_FILE = 'raw_data.json'
OUTPUT_FILE = 'processed_data.csv'

def extract(file_path):
    """
    Task 1: Đọc dữ liệu JSON từ file.
    """
    print(f"Extracting data from {file_path}...")
    try:
        # Mở và đọc file JSON với encoding utf-8 để tránh lỗi font
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File {file_path} không tồn tại.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Định dạng file JSON không hợp lệ.")
        return None

def validate(data):
    valid_records = []
    error_count = 0
    
    # In ra số lượng record thô ngay từ đầu (giống Option 1)
    print(f"Extracted {len(data)} raw records.")

    for record in data:
        record_id = record.get('id', 'Unknown')
        price = record.get('price', 0)
        category = record.get('category')

        # Kiểm tra điều kiện và in chi tiết lý do Drop
        if price <= 0:
            print(f"  [DROP] Record id={record_id} - price={price} is invalid (price <= 0)")
            error_count += 1
            continue
            
        if not category or not str(category).strip():
            print(f"  [DROP] Record id={record_id} - category is empty")
            error_count += 1
            continue

        valid_records.append(record)

    print(f"Validation complete. Valid: {len(valid_records)} records kept, {error_count} records dropped.")
    return valid_records

def transform(data):
    """
    Task 3: Áp dụng business logic.
    - Giảm giá 10%
    - Chuẩn hóa Category thành Title Case
    - Thêm timestamp xử lý
    """
    if not data:
        return None

    # Tạo DataFrame từ list danh sách các bản ghi hợp lệ
    df = pd.DataFrame(data)

    # 1. Tính giá sau khi giảm 10%
    df['discounted_price'] = df['price'] * 0.9

    # 2. Chuẩn hóa Category (ví dụ: "electronics" -> "Electronics")
    # Đảm bảo cột category là kiểu string trước khi dùng .str.title()
    df['category'] = df['category'].astype(str).str.title()

    # 3. Thêm cột processed_at với thời gian hiện tại
    df['processed_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return df

def load(df, output_path):
    """
    Task 4: Lưu DataFrame ra file CSV.
    """
    try:
        # Lưu file CSV, không lưu cột index mặc định của pandas
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"Data successfully saved to {output_path}")
    except Exception as e:
        print(f"Error saving file: {e}")

# MAIN PIPELINE
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
        if final_df is not None and not final_df.empty:
            load(final_df, OUTPUT_FILE)
            print(f"\nPipeline completed! {len(final_df)} records saved.")
        else:
            print("\nTransform returned empty or None. Check your validate/transform logic.")
    else:
        print("\nPipeline aborted: No data extracted.")