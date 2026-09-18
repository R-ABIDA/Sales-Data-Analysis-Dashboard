"""
==============================================================================
PROJECT: Sales Data Analysis Dashboard
MODULE:  Data Cleaning & Preprocessing (scripts/data_cleaning.py)
LEVEL:   Beginner to Intermediate
DESCRIPTION:
This script loads the raw sales dataset, inspects data quality, performs
standard data cleaning operations (duplicate removal, missing value handling,
date format standardization, data type casting, string cleaning), validates
numerical integrity, adds derived temporal columns, and exports the clean
dataset in both Excel (.xlsx) and CSV (.csv) formats.
==============================================================================
"""

import os
import pandas as pd
import numpy as np

def load_raw_data(filepath: str) -> pd.DataFrame:
    """
    Loads the raw sales dataset with fallback encoding handling.
    """
    print(f"[STEP 1] Loading raw dataset from: {filepath}")
    try:
        # Standard encoding for Superstore datasets is windows-1252 or utf-8
        df = pd.read_csv(filepath, encoding="windows-1252")
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding="utf-8")
    
    print(f" -> Raw Dataset successfully loaded with {df.shape[0]:,} rows and {df.shape[1]} columns.")
    return df


def inspect_raw_data(df: pd.DataFrame) -> None:
    """
    Prints a data understanding summary of the raw dataset.
    """
    print("\n" + "=" * 60)
    print("DATA QUALITY & INTEGRITY INSPECTION (RAW)")
    print("=" * 60)
    print("1. Column Names & Types:")
    for col, dtype in df.dtypes.items():
        print(f"   - {col:20s}: {str(dtype):10s} (Non-null: {df[col].count()})")
    
    print("\n2. Missing Values per Column:")
    nulls = df.isnull().sum()
    if nulls.sum() == 0:
        print("   -> No missing values found in the dataset.")
    else:
        for col, count in nulls[nulls > 0].items():
            print(f"   - {col}: {count} missing values ({count/len(df):.2%})")

    duplicate_count = df.duplicated().sum()
    print(f"\n3. Duplicate Records: {duplicate_count}")


def clean_sales_data(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Performs data cleaning operations:
      1. Preserves original data by working on an explicit copy.
      2. Deduplicates records.
      3. Standardizes date columns (Order Date, Ship Date) into datetime objects.
      4. Standardizes postal code format.
      5. Strips leading/trailing whitespace and normalizes string casing.
      6. Checks and validates numerical fields (Sales > 0, Quantity > 0).
      7. Engineers business helper columns (Order Year, Order Month, Year-Month,
         Shipping Duration in Days, Unit Price).
    """
    print("\n" + "=" * 60)
    print("[STEP 2] Commencing Data Cleaning Pipeline...")
    print("=" * 60)

    # 1. Create a deep copy to never mutate original raw data
    df = df_raw.copy()

    # 2. Check and remove duplicate rows
    initial_rows = len(df)
    df.drop_duplicates(inplace=True)
    rows_after_dedup = len(df)
    print(f" -> Deduplication: Removed {initial_rows - rows_after_dedup} duplicate rows. Remaining: {rows_after_dedup:,}")

    # 3. Handle missing values (if any)
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            if df[col].dtype in ['float64', 'int64']:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                print(f" -> Imputed missing values in '{col}' with median: {median_val}")
            else:
                mode_val = df[col].mode()[0]
                df[col] = df[col].fillna(mode_val)
                print(f" -> Imputed missing values in '{col}' with mode: {mode_val}")

    # 4. Standardize Date formats
    print(" -> Standardizing Date fields ('Order Date', 'Ship Date')...")
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed', dayfirst=False)
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='mixed', dayfirst=False)

    # Format dates as ISO string YYYY-MM-DD for consistency
    df['Order Date Formatted'] = df['Order Date'].dt.strftime('%Y-%m-%d')
    df['Ship Date Formatted'] = df['Ship Date'].dt.strftime('%Y-%m-%d')

    # 5. Correct and Standardize Postal Code (preserve 5-digit US ZIP code format)
    if 'Postal Code' in df.columns:
        df['Postal Code'] = df['Postal Code'].fillna(0).astype(int).astype(str).str.zfill(5)
        print(" -> Standardized 'Postal Code' to 5-digit string format.")

    # 6. Standardize Categorical and Text Columns
    text_cols = ['Customer Name', 'Segment', 'Country', 'City', 'State', 'Region', 'Category', 'Sub-Category', 'Product Name']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # 7. Identify and handle invalid sales or quantity values
    invalid_sales = df[df['Sales'] <= 0]
    invalid_qty = df[df['Quantity'] <= 0]
    print(f" -> Integrity Check: Invalid Sales (<=0): {len(invalid_sales)}, Invalid Quantity (<=0): {len(invalid_qty)}")
    
    if len(invalid_sales) > 0:
        df = df[df['Sales'] > 0]
        print(f"    -> Filtered out {len(invalid_sales)} records with non-positive sales.")
    if len(invalid_qty) > 0:
        df = df[df['Quantity'] > 0]
        print(f"    -> Filtered out {len(invalid_qty)} records with non-positive quantity.")

    # 8. Feature Engineering / Derived Columns for Analytics
    print(" -> Engineering temporal and analytical helper columns...")
    df['Order Year'] = df['Order Date'].dt.year
    df['Order Month'] = df['Order Date'].dt.month
    df['Order Month Name'] = df['Order Date'].dt.strftime('%b')
    df['Order Year-Month'] = df['Order Date'].dt.to_period('M').astype(str)
    df['Order Quarter'] = df['Order Date'].dt.to_period('Q').astype(str)
    df['Order Day of Week'] = df['Order Date'].dt.day_name()
    
    # Calculate Shipping Duration (in days)
    df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days
    
    # Calculate Unit Price (Sales / Quantity) rounded to 2 decimal places
    df['Unit Price'] = (df['Sales'] / df['Quantity']).round(2)
    
    # Round numerical metrics to 2 decimal places
    df['Sales'] = df['Sales'].round(2)
    if 'Profit' in df.columns:
        df['Profit'] = df['Profit'].round(2)
    if 'Discount' in df.columns:
        df['Discount'] = df['Discount'].round(2)

    # Sort records chronologically
    df.sort_values(by=['Order Date', 'Row ID' if 'Row ID' in df.columns else 'Order ID'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    print(f" -> Cleaning complete! Final cleaned dataset contains {df.shape[0]:,} rows and {df.shape[1]} columns.")
    return df


def export_cleaned_dataset(df_clean: pd.DataFrame, output_dir: str) -> None:
    """
    Exports the cleaned dataset to Excel (.xlsx) as required, and CSV (.csv) for fast reading.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    excel_path = os.path.join(output_dir, "cleaned_sales_dataset.xlsx")
    csv_path = os.path.join(output_dir, "cleaned_sales_dataset.csv")

    print("\n" + "=" * 60)
    print(f"[STEP 3] Exporting Cleaned Dataset to: {output_dir}")
    print("=" * 60)

    # Export to Excel (.xlsx) - Requirement 4
    print(f" -> Writing Excel file: {excel_path} (this may take a few seconds)...")
    # Date formatting in Excel
    df_export = df_clean.copy()
    # Save with openpyxl engine
    df_export.to_excel(excel_path, index=False, engine='openpyxl')
    print(f"    -> Successfully generated: {excel_path}")

    # Also export to CSV for ultra-fast performance in downstream scripts & web dashboard
    print(f" -> Writing CSV file: {csv_path}...")
    df_export.to_csv(csv_path, index=False)
    print(f"    -> Successfully generated: {csv_path}")


def main():
    # Resolve relative paths relative to repository structure
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    raw_path = os.path.join(base_dir, "data", "original", "Sample - Superstore.csv")
    cleaned_dir = os.path.join(base_dir, "data", "cleaned")

    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw dataset not found at {raw_path}")

    # Execute cleaning workflow
    df_raw = load_raw_data(raw_path)
    inspect_raw_data(df_raw)
    df_cleaned = clean_sales_data(df_raw)
    export_cleaned_dataset(df_cleaned, cleaned_dir)

    print("\n>>> DATA CLEANING WORKFLOW COMPLETED SUCCESSFULLY! <<<")


if __name__ == "__main__":
    main()
