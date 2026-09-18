# Sales Analysis Dashboard Guide

This directory contains two dashboard implementations for the **Sales Data Analysis Dashboard** internship project:

## 1. Power BI Desktop Dashboard (`sales_analysis_dashboard.pbix`)
- **Requirements**: Microsoft Power BI Desktop (Free on Windows Store).
- **How to Open**:
  1. Open Power BI Desktop.
  2. Click **File > Open report** and select `sales_analysis_dashboard.pbix`.
  3. The data model, relationships, measures, and visual cards are pre-configured.

## 2. Standalone Interactive Web Dashboard (`index.html`)
- **Requirements**: Any modern web browser (Google Chrome, Microsoft Edge, Firefox, Safari). Zero dependencies or installations required!
- **Features**:
  - **Live Slicers / Filters**:
    - **Year**: All, 2014, 2015, 2016, 2017
    - **Month**: All, January through December
    - **Region**: All, Central, East, South, West
    - **Category**: All, Furniture, Office Supplies, Technology
    - **Product Search**: Real-time substring filter across all 1,862 catalog products.
  - **Executive KPI Cards**:
    - Total Sales ($)
    - Total Orders
    - Total Quantity
    - Average Order Value ($)
  - **Dynamic Visuals (Chart.js)**:
    - Monthly Sales Trajectory Area Chart
    - Regional Sales Bar Chart
    - Top 10 Best-Selling Products Bar Chart
    - Sales by Category Doughnut Chart
  - **Interactive Data Table**:
    - Filtered transaction row preview with color-coded profit metrics.
  - **Reset Button**: One-click reset to national baseline.

### How to Launch the Web Dashboard:
Simply double-click `index.html` to open it in your default web browser, or run a lightweight local server:
```bash
python -m http.server 8085
```
Then navigate to: `http://localhost:8085/`
