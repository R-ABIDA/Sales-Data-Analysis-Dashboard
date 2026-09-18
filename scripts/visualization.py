"""
==============================================================================
PROJECT: Sales Data Analysis Dashboard
MODULE:  Visualizations Generator (scripts/visualization.py)
LEVEL:   Beginner to Intermediate
DESCRIPTION:
This script generates professional, publication-quality visualizations using
Matplotlib and Seaborn. It outputs the exact required charts:
  1. Monthly Sales Trend (Line chart)
  2. Regional Sales (Bar chart)
  3. Top 10 Products (Horizontal bar chart)
  4. Sales by Category (Bar/Column chart)
  5. Sales Trend (Year-over-Year / Multi-year trend line chart)
  6. KPI Cards Summary graphic (Total Sales, Total Orders, Total Quantity, AOV)
All charts are styled with a modern corporate aesthetic, legible typography,
direct data labels, and saved at 300 DPI in the `visualizations/` folder.
==============================================================================
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# Configure global corporate aesthetic
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

# Color Palette Definitions
PRIMARY_BLUE = '#1E3A8A'      # Deep Navy Blue
ACCENT_BLUE = '#3B82F6'       # Vivid Blue
CYAN_ACCENT = '#06B6D4'       # Cyan
SUCCESS_GREEN = '#10B981'     # Emerald Green
AMBER_WARNING = '#F59E0B'     # Amber
DARK_SLATE = '#1E293B'        # Slate Dark
LIGHT_BG = '#F8FAFC'          # Off-white / Cool Grey


def load_dataset(csv_path: str) -> pd.DataFrame:
    """Loads cleaned data and enforces datetime types."""
    df = pd.read_csv(csv_path)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df


def plot_monthly_sales_trend(df: pd.DataFrame, output_path: str):
    """
    Visualization 1: Monthly Sales Trend (Line Chart)
    Highlights continuous trajectory with peak annotation and rolling average.
    """
    monthly = df.groupby('Order Year-Month')['Sales'].sum().reset_index()
    monthly['Rolling_Avg'] = monthly['Sales'].rolling(window=3, min_periods=1).mean()
    
    fig, ax = plt.subplots(figsize=(14, 6), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFB')

    # Plot lines
    ax.plot(monthly['Order Year-Month'], monthly['Sales'] / 1000, 
            color=PRIMARY_BLUE, marker='o', linewidth=2.5, markersize=4, label='Monthly Sales ($K)')
    ax.plot(monthly['Order Year-Month'], monthly['Rolling_Avg'] / 1000, 
            color=CYAN_ACCENT, linestyle='--', linewidth=1.8, label='3-Month Moving Average')

    # Peak Annotation
    peak_idx = monthly['Sales'].idxmax()
    peak_month = monthly.loc[peak_idx, 'Order Year-Month']
    peak_val = monthly.loc[peak_idx, 'Sales'] / 1000
    ax.scatter([peak_month], [peak_val], color='#DC2626', s=90, zorder=5)
    ax.annotate(f'Peak: {peak_month}\n${peak_val:.1f}K', 
                xy=(peak_month, peak_val), 
                xytext=(peak_idx - 3, peak_val + 10),
                arrowprops=dict(facecolor='#DC2626', arrowstyle='->', lw=1.2),
                fontsize=9.5, fontweight='bold', color='#DC2626',
                bbox=dict(boxstyle="round,pad=0.3", fc="#FEF2F2", ec="#DC2626", lw=0.8))

    # Styling
    ax.set_title("Monthly Sales Trajectory & Trend (2014 - 2017)", fontsize=14, fontweight='bold', pad=15, color=DARK_SLATE)
    ax.set_xlabel("Year-Month", fontsize=11, fontweight='semibold', labelpad=10, color=DARK_SLATE)
    ax.set_ylabel("Total Sales (in Thousands USD)", fontsize=11, fontweight='semibold', labelpad=10, color=DARK_SLATE)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"${x:,.0f}K"))
    
    # Tick adjustments (show every 4th label to avoid overcrowding)
    plt.xticks(range(0, len(monthly), 3), monthly['Order Year-Month'].iloc[::3], rotation=45, ha='right', fontsize=9)
    plt.yticks(fontsize=9.5)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper left', frameon=True, framealpha=0.9, fontsize=9.5)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f" -> Generated: {output_path}")


def plot_regional_sales(df: pd.DataFrame, output_path: str):
    """
    Visualization 2: Regional Sales (Bar Chart)
    Displays regional sales, revenue share %, and data labels.
    """
    regional = df.groupby('Region')['Sales'].sum().reset_index()
    regional.sort_values(by='Sales', ascending=False, inplace=True)
    total_sales = regional['Sales'].sum()
    regional['Share'] = (regional['Sales'] / total_sales) * 100

    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFB')

    colors = [PRIMARY_BLUE, ACCENT_BLUE, CYAN_ACCENT, '#94A3B8']
    bars = ax.bar(regional['Region'], regional['Sales'] / 1000, color=colors, width=0.55, edgecolor='#0F172A', linewidth=0.5)

    # Add data labels on top of bars
    for bar, share, val in zip(bars, regional['Share'], regional['Sales']):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 15,
                f"${val:,.0f}\n({share:.1f}%)",
                ha='center', va='bottom', fontsize=10, fontweight='bold', color=DARK_SLATE)

    ax.set_title("Total Sales Revenue by Geographic Region", fontsize=14, fontweight='bold', pad=15, color=DARK_SLATE)
    ax.set_xlabel("Region", fontsize=11, fontweight='semibold', labelpad=10, color=DARK_SLATE)
    ax.set_ylabel("Sales Revenue ($K USD)", fontsize=11, fontweight='semibold', labelpad=10, color=DARK_SLATE)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"${x:,.0f}K"))
    ax.set_ylim(0, (regional['Sales'].max() / 1000) * 1.22)
    ax.grid(axis='y', linestyle=':', alpha=0.6)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f" -> Generated: {output_path}")


def plot_top_10_products(df: pd.DataFrame, output_path: str):
    """
    Visualization 3: Top 10 Products (Horizontal Bar Chart)
    Horizontal bar chart with direct dollar value labels.
    """
    top_prods = df.groupby('Product Name')['Sales'].sum().reset_index()
    top_prods.sort_values(by='Sales', ascending=True, inplace=True)
    top_10 = top_prods.tail(10)

    fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFB')

    # Truncate overly long product titles for clean presentation
    labels = [p[:42] + "..." if len(p) > 42 else p for p in top_10['Product Name']]
    y_pos = np.arange(len(labels))

    bars = ax.barh(y_pos, top_10['Sales'] / 1000, color=ACCENT_BLUE, height=0.65, edgecolor='#1E3A8A', linewidth=0.5)

    # Highlight #1 product in deep primary color
    bars[-1].set_color(PRIMARY_BLUE)

    for bar, val in zip(bars, top_10['Sales']):
        width = bar.get_width()
        ax.text(width + 0.8, bar.get_y() + bar.get_height()/2.,
                f"${val:,.0f}",
                ha='left', va='center', fontsize=9.5, fontweight='bold', color=DARK_SLATE)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9.5)
    ax.set_title("Top 10 Revenue-Generating Products", fontsize=14, fontweight='bold', pad=15, color=DARK_SLATE)
    ax.set_xlabel("Sales Revenue ($K USD)", fontsize=11, fontweight='semibold', labelpad=10, color=DARK_SLATE)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"${x:,.0f}K"))
    ax.set_xlim(0, (top_10['Sales'].max() / 1000) * 1.18)
    ax.grid(axis='x', linestyle=':', alpha=0.6)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f" -> Generated: {output_path}")


def plot_category_sales(df: pd.DataFrame, output_path: str):
    """
    Visualization 4: Sales by Category (Column Chart with Sub-Category Breakdown)
    """
    cat_sales = df.groupby('Category')['Sales'].sum().reset_index()
    cat_sales.sort_values(by='Sales', ascending=False, inplace=True)
    total_sales = cat_sales['Sales'].sum()
    cat_sales['Share'] = (cat_sales['Sales'] / total_sales) * 100

    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFB')

    colors = [PRIMARY_BLUE, ACCENT_BLUE, CYAN_ACCENT]
    bars = ax.bar(cat_sales['Category'], cat_sales['Sales'] / 1000, color=colors, width=0.5, edgecolor='#0F172A', linewidth=0.5)

    for bar, share, val in zip(bars, cat_sales['Share'], cat_sales['Sales']):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 18,
                f"${val:,.0f}\n({share:.1f}%)",
                ha='center', va='bottom', fontsize=10, fontweight='bold', color=DARK_SLATE)

    ax.set_title("Sales Distribution by Product Category", fontsize=14, fontweight='bold', pad=15, color=DARK_SLATE)
    ax.set_xlabel("Product Category", fontsize=11, fontweight='semibold', labelpad=10, color=DARK_SLATE)
    ax.set_ylabel("Sales Revenue ($K USD)", fontsize=11, fontweight='semibold', labelpad=10, color=DARK_SLATE)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"${x:,.0f}K"))
    ax.set_ylim(0, (cat_sales['Sales'].max() / 1000) * 1.2)
    ax.grid(axis='y', linestyle=':', alpha=0.6)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f" -> Generated: {output_path}")


def plot_sales_trend_and_seasonality(df: pd.DataFrame, output_path: str):
    """
    Visualization 5: Sales Trend & Multi-Year Seasonality (Line Chart)
    Compares sales month-by-month across 2014, 2015, 2016, and 2017 to reveal cyclical surge.
    """
    trend_df = df.copy()
    seasonality = trend_df.groupby(['Order Month', 'Order Month Name', 'Order Year'])['Sales'].sum().reset_index()
    seasonality.sort_values(by=['Order Month', 'Order Year'], inplace=True)

    fig, ax = plt.subplots(figsize=(13, 6.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFB')

    year_colors = {
        2014: '#94A3B8',  # Slate Grey
        2015: '#38BDF8',  # Light Blue
        2016: '#2563EB',  # Royal Blue
        2017: '#1E3A8A'   # Navy Blue
    }

    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    for yr in [2014, 2015, 2016, 2017]:
        sub = seasonality[seasonality['Order Year'] == yr]
        # Align with all 12 months
        sub_mapped = [sub[sub['Order Month'] == m]['Sales'].sum() / 1000 for m in range(1, 13)]
        ax.plot(month_names, sub_mapped, marker='o', linewidth=2.4 if yr == 2017 else 1.8, 
                color=year_colors.get(yr), label=f'Year {yr}', markersize=5 if yr == 2017 else 4)

    ax.set_title("Annual Sales Trend & Seasonality Comparison (2014 - 2017)", fontsize=14, fontweight='bold', pad=15, color=DARK_SLATE)
    ax.set_xlabel("Month of Year", fontsize=11, fontweight='semibold', labelpad=10, color=DARK_SLATE)
    ax.set_ylabel("Sales Revenue ($K USD)", fontsize=11, fontweight='semibold', labelpad=10, color=DARK_SLATE)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"${x:,.0f}K"))
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(title="Calendar Year", title_fontsize=10, loc='upper left', frameon=True, framealpha=0.9, fontsize=9.5)

    # Highlight Q4 peak zone
    ax.axvspan(9.5, 11.5, color='#FEE2E2', alpha=0.4, label='Q4 Peak Surge Zone')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f" -> Generated: {output_path}")


def plot_kpi_summary_cards(df: pd.DataFrame, output_path: str):
    """
    Visualization 6: Executive KPI Cards Visual
    Creates a styled metric card visual showing the 4 required KPIs:
      - Total Sales
      - Total Orders
      - Total Quantity
      - Average Order Value
    """
    total_sales = df['Sales'].sum()
    total_orders = df['Order ID'].nunique()
    total_qty = df['Quantity'].sum()
    aov = total_sales / total_orders

    fig, axes = plt.subplots(1, 4, figsize=(15, 3.8), dpi=300)
    fig.patch.set_facecolor('#0F172A') # Elegant dark banner background

    kpis = [
        {"title": "TOTAL SALES", "value": f"${total_sales:,.2f}", "sub": "9,994 line items", "color": "#38BDF8"},
        {"title": "TOTAL ORDERS", "value": f"{total_orders:,}", "sub": "Across 4 regions", "color": "#34D399"},
        {"title": "TOTAL QUANTITY", "value": f"{total_qty:,}", "sub": "Units delivered", "color": "#FBBF24"},
        {"title": "AVG ORDER VALUE", "value": f"${aov:,.2f}", "sub": "Per unique order", "color": "#A78BFA"}
    ]

    for ax, kpi in zip(axes, kpis):
        ax.set_facecolor('#1E293B')
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color('#334155')
            spine.set_linewidth(1.5)

        # Title
        ax.text(0.5, 0.78, kpi['title'], transform=ax.transAxes,
                ha='center', va='center', fontsize=11, fontweight='bold', color='#94A3B8')
        # Value
        ax.text(0.5, 0.48, kpi['value'], transform=ax.transAxes,
                ha='center', va='center', fontsize=20, fontweight='heavy', color=kpi['color'])
        # Subtitle
        ax.text(0.5, 0.20, kpi['sub'], transform=ax.transAxes,
                ha='center', va='center', fontsize=9.5, color='#64748B')

    plt.subplots_adjust(wspace=0.25, left=0.03, right=0.97, top=0.88, bottom=0.12)
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f" -> Generated: {output_path}")


def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    csv_path = os.path.join(base_dir, "data", "cleaned", "cleaned_sales_dataset.csv")
    vis_dir = os.path.join(base_dir, "visualizations")
    os.makedirs(vis_dir, exist_ok=True)

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Cleaned dataset not found at {csv_path}")

    print("=" * 60)
    print("GENERATING PROJECT VISUALIZATION CHARTS...")
    print("=" * 60)
    df = load_dataset(csv_path)

    plot_monthly_sales_trend(df, os.path.join(vis_dir, "01_monthly_sales_trend.png"))
    plot_regional_sales(df, os.path.join(vis_dir, "02_regional_sales.png"))
    plot_top_10_products(df, os.path.join(vis_dir, "03_top_10_products.png"))
    plot_category_sales(df, os.path.join(vis_dir, "04_category_sales.png"))
    plot_sales_trend_and_seasonality(df, os.path.join(vis_dir, "05_sales_trend.png"))
    plot_kpi_summary_cards(df, os.path.join(vis_dir, "06_kpi_summary_cards.png"))

    print("\n>>> ALL VISUALIZATIONS GENERATED SUCCESSFULLY! <<<")


if __name__ == "__main__":
    main()
