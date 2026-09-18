"""
==============================================================================
PROJECT: Sales Data Analysis Dashboard
MODULE:  Data Analysis & KPI Calculation (scripts/data_analysis.py)
LEVEL:   Beginner to Intermediate
DESCRIPTION:
This script performs in-depth statistical and business analysis on the cleaned
sales dataset. It computes core KPIs (Total Sales, Total Orders, Total Quantity,
AOV, etc.), aggregates sales across dimensions (Monthly, Regional, Category,
Product), identifies top and bottom performers, analyzes growth trends, and
outputs structured summaries.
==============================================================================
"""

import os
import json
import pandas as pd
import numpy as np


def load_cleaned_data(filepath: str) -> pd.DataFrame:
    """
    Loads the cleaned sales dataset.
    """
    print(f"[STEP 1] Loading cleaned dataset from: {filepath}")
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)
    
    # Ensure datetime format for temporal operations
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    print(f" -> Loaded {len(df):,} records successfully.")
    return df


def calculate_core_kpis(df: pd.DataFrame) -> dict:
    """
    Calculates executive sales KPIs strictly based on actual dataset columns:
      - Total Sales
      - Total Orders
      - Total Quantity
      - Average Order Value (AOV)
      - Number of Unique Products
      - Number of Unique Customers
      - Average Sales per Order
      - Total Profit & Overall Profit Margin (bonus business context)
    """
    total_sales = float(df['Sales'].sum())
    total_orders = int(df['Order ID'].nunique())
    total_quantity = int(df['Quantity'].sum())
    avg_order_value = float(total_sales / total_orders) if total_orders > 0 else 0.0
    num_products = int(df['Product ID'].nunique())
    num_customers = int(df['Customer ID'].nunique())
    avg_sales_per_order = avg_order_value # Same definition as AOV
    avg_sales_per_item = float(df['Sales'].mean())
    total_profit = float(df['Profit'].sum()) if 'Profit' in df.columns else None
    profit_margin = float((total_profit / total_sales) * 100) if total_profit is not None and total_sales > 0 else None

    kpis = {
        "Total Sales ($)": round(total_sales, 2),
        "Total Orders": total_orders,
        "Total Quantity Sold": total_quantity,
        "Average Order Value ($)": round(avg_order_value, 2),
        "Average Sales per Order ($)": round(avg_sales_per_order, 2),
        "Average Sales per Line Item ($)": round(avg_sales_per_item, 2),
        "Number of Unique Products": num_products,
        "Number of Unique Customers": num_customers,
        "Total Profit ($)": round(total_profit, 2) if total_profit is not None else "N/A",
        "Overall Profit Margin (%)": round(profit_margin, 2) if profit_margin is not None else "N/A"
    }

    print("\n" + "=" * 60)
    print("EXECUTIVE KEY PERFORMANCE INDICATORS (KPIs)")
    print("=" * 60)
    for kpi, val in kpis.items():
        if isinstance(val, (int, float)) and "($)" in kpi:
            print(f" * {kpi:32s}: ${val:,.2f}")
        elif isinstance(val, int):
            print(f" * {kpi:32s}: {val:,}")
        elif isinstance(val, float):
            print(f" * {kpi:32s}: {val:,.2f}%" if "%" in kpi else f" * {kpi:32s}: {val:,.2f}")
        else:
            print(f" * {kpi:32s}: {val}")

    return kpis


def analyze_monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes monthly sales, order counts, and MoM (Month-over-Month) sales growth.
    """
    print("\n" + "=" * 60)
    print("MONTHLY SALES ANALYSIS & TEMPORAL TRENDS")
    print("=" * 60)

    # Group by Year-Month
    monthly = df.groupby('Order Year-Month').agg(
        Total_Sales=('Sales', 'sum'),
        Total_Orders=('Order ID', 'nunique'),
        Total_Quantity=('Quantity', 'sum'),
        Total_Profit=('Profit', 'sum') if 'Profit' in df.columns else ('Sales', 'count')
    ).reset_index()

    monthly['Total_Sales'] = monthly['Total_Sales'].round(2)
    monthly['Total_Profit'] = monthly['Total_Profit'].round(2)
    monthly['MoM_Sales_Growth_%'] = (monthly['Total_Sales'].pct_change() * 100).round(2)

    peak_month = monthly.loc[monthly['Total_Sales'].idxmax()]
    low_month = monthly.loc[monthly['Total_Sales'].idxmin()]

    print(f" * Peak Sales Month  : {peak_month['Order Year-Month']} with ${peak_month['Total_Sales']:,.2f} in sales ({peak_month['Total_Orders']} orders)")
    print(f" * Lowest Sales Month: {low_month['Order Year-Month']} with ${low_month['Total_Sales']:,.2f} in sales ({low_month['Total_Orders']} orders)")
    print(f" * Average Monthly Sales: ${monthly['Total_Sales'].mean():,.2f}")

    return monthly


def analyze_regional_sales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyzes sales, orders, and market share across geographic regions.
    """
    print("\n" + "=" * 60)
    print("REGIONAL SALES PERFORMANCE")
    print("=" * 60)

    total_sales = df['Sales'].sum()
    regional = df.groupby('Region').agg(
        Total_Sales=('Sales', 'sum'),
        Total_Orders=('Order ID', 'nunique'),
        Total_Quantity=('Quantity', 'sum'),
        Total_Profit=('Profit', 'sum') if 'Profit' in df.columns else ('Sales', 'count')
    ).reset_index()

    regional['Total_Sales'] = regional['Total_Sales'].round(2)
    regional['Sales_Share_%'] = ((regional['Total_Sales'] / total_sales) * 100).round(2)
    regional.sort_values(by='Total_Sales', ascending=False, inplace=True)
    regional.reset_index(drop=True, inplace=True)

    for _, row in regional.iterrows():
        print(f" * {row['Region']:10s}: ${row['Total_Sales']:>10,.2f} | Share: {row['Sales_Share_%']:>5.2f}% | Orders: {row['Total_Orders']:>5,}")

    return regional


def analyze_category_sales(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Analyzes sales by Category and Sub-Category.
    """
    print("\n" + "=" * 60)
    print("SALES BY PRODUCT CATEGORY & SUB-CATEGORY")
    print("=" * 60)

    total_sales = df['Sales'].sum()
    category = df.groupby('Category').agg(
        Total_Sales=('Sales', 'sum'),
        Total_Orders=('Order ID', 'nunique'),
        Total_Quantity=('Quantity', 'sum'),
        Total_Profit=('Profit', 'sum') if 'Profit' in df.columns else ('Sales', 'count')
    ).reset_index()

    category['Total_Sales'] = category['Total_Sales'].round(2)
    category['Sales_Share_%'] = ((category['Total_Sales'] / total_sales) * 100).round(2)
    category.sort_values(by='Total_Sales', ascending=False, inplace=True)

    print("--- Category Level Breakdown ---")
    for _, row in category.iterrows():
        print(f" * {row['Category']:18s}: ${row['Total_Sales']:>10,.2f} ({row['Sales_Share_%']:>5.2f}% of total sales)")

    sub_category = df.groupby(['Category', 'Sub-Category']).agg(
        Total_Sales=('Sales', 'sum'),
        Total_Quantity=('Quantity', 'sum'),
        Total_Profit=('Profit', 'sum') if 'Profit' in df.columns else ('Sales', 'count')
    ).reset_index()
    sub_category['Total_Sales'] = sub_category['Total_Sales'].round(2)
    sub_category.sort_values(by='Total_Sales', ascending=False, inplace=True)

    return category, sub_category


def analyze_product_performance(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Identifies Top 10 Best-Selling Products and Lowest-Performing Products.
    """
    print("\n" + "=" * 60)
    print("PRODUCT PERFORMANCE: TOP 10 & LOWEST PERFORMERS")
    print("=" * 60)

    prod_perf = df.groupby(['Product ID', 'Product Name', 'Category', 'Sub-Category']).agg(
        Total_Sales=('Sales', 'sum'),
        Units_Sold=('Quantity', 'sum'),
        Total_Profit=('Profit', 'sum') if 'Profit' in df.columns else ('Sales', 'count')
    ).reset_index()

    prod_perf['Total_Sales'] = prod_perf['Total_Sales'].round(2)
    prod_perf.sort_values(by='Total_Sales', ascending=False, inplace=True)

    top_10 = prod_perf.head(10).copy().reset_index(drop=True)
    bottom_10 = prod_perf.tail(10).copy().reset_index(drop=True)

    print("--- Top 10 Revenue-Generating Products ---")
    for idx, row in top_10.iterrows():
        name_trunc = (row['Product Name'][:45] + '...') if len(row['Product Name']) > 48 else row['Product Name']
        print(f" {idx+1:2d}. {name_trunc:48s} | ${row['Total_Sales']:>9,.2f} | Units: {row['Units_Sold']:>3d}")

    print("\n--- 10 Lowest-Performing Products (by Sales Volume) ---")
    for idx, row in bottom_10.iterrows():
        name_trunc = (row['Product Name'][:45] + '...') if len(row['Product Name']) > 48 else row['Product Name']
        print(f" {idx+1:2d}. {name_trunc:48s} | ${row['Total_Sales']:>9,.2f} | Units: {row['Units_Sold']:>3d}")

    return top_10, bottom_10


def run_full_analysis(df: pd.DataFrame, output_dir: str = None) -> dict:
    """
    Orchestrates the entire analytical calculations and returns all tables.
    """
    kpis = calculate_core_kpis(df)
    monthly_sales = analyze_monthly_sales(df)
    regional_sales = analyze_regional_sales(df)
    category_sales, subcategory_sales = analyze_category_sales(df)
    top_10_products, bottom_10_products = analyze_product_performance(df)

    results = {
        "kpis": kpis,
        "monthly_sales": monthly_sales,
        "regional_sales": regional_sales,
        "category_sales": category_sales,
        "subcategory_sales": subcategory_sales,
        "top_10_products": top_10_products,
        "bottom_10_products": bottom_10_products
    }

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        # Save KPI json
        with open(os.path.join(output_dir, "kpi_summary.json"), "w") as f:
            json.dump(kpis, f, indent=4)
        # Save CSV summaries
        monthly_sales.to_csv(os.path.join(output_dir, "monthly_sales_summary.csv"), index=False)
        regional_sales.to_csv(os.path.join(output_dir, "regional_sales_summary.csv"), index=False)
        category_sales.to_csv(os.path.join(output_dir, "category_sales_summary.csv"), index=False)
        top_10_products.to_csv(os.path.join(output_dir, "top_10_products.csv"), index=False)

    return results


def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    cleaned_csv = os.path.join(base_dir, "data", "cleaned", "cleaned_sales_dataset.csv")
    output_dir = os.path.join(base_dir, "insights")

    if not os.path.exists(cleaned_csv):
        raise FileNotFoundError(f"Cleaned dataset not found at {cleaned_csv}. Run data_cleaning.py first.")

    df = load_cleaned_data(cleaned_csv)
    run_full_analysis(df, output_dir)
    print("\n>>> DATA ANALYSIS WORKFLOW COMPLETED SUCCESSFULLY! <<<")


if __name__ == "__main__":
    main()
