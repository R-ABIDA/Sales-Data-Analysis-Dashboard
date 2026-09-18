# Presentation Deck: Sales Data Analysis Dashboard

**Internship Mini Project – Data Analysis**  
**Presentation Title**: Sales Performance & Business Insights  
**Audience**: Internship Evaluators, Mentors & Executive Leadership  
**Format**: 9 Comprehensive Slides (available in PowerPoint `.pptx` & Markdown)  

---

## Slide 1: Title Slide
- **Title**: Sales Data Analysis Dashboard
- **Subtitle**: Sales Performance, Regional Breakdown & Executive Business Insights
- **Track**: Beginner-Level Data Analysis Internship Mini Project (2-Week Duration)
- **Tools**: Python (Pandas, NumPy, Matplotlib, Seaborn), Power BI, Web Dashboard, Excel
- **Dataset**: Superstore Sales Dataset (9,994 Verified Actual Records; 2014–2017)

---

## Slide 2: Project Objectives & 2-Week Roadmap
- **Week 1: Data Understanding, Cleaning & Preprocessing**
  - Acquired authentic 9,994-row retail sales dataset (0 synthetic values).
  - Verified 0 null values, 0 duplicates, and verified all sales/quantity values > 0.
  - Standardized `Order Date` and `Ship Date` into ISO `YYYY-MM-DD`.
  - Standardized postal codes as zero-padded 5-digit strings.
  - Engineered analytical helper columns: `Order Year`, `Order Month`, `Shipping Days`, `Unit Price`.
  - Calculated core business KPIs and exported `cleaned_sales_dataset.xlsx` & `.csv`.

- **Week 2: Visualization, Dashboards & Finalization**
  - Generated 6 publication-quality charts using Matplotlib and Seaborn.
  - Constructed the Power BI Dashboard file (`sales_analysis_dashboard.pbix`).
  - Developed an interactive live web dashboard (`index.html`) with dynamic filters.
  - Derived 7 empirical, evidence-based business insights.
  - Prepared 14-section formal report, executive presentation, and GitHub repository.

---

## Slide 3: Executive Sales KPIs
| Key Performance Indicator (KPI) | Value | Business Meaning |
| :--- | :--- | :--- |
| **Total Sales** | **$2,297,200.65** | Multi-year gross sales revenue |
| **Total Orders** | **5,009** | Distinct commercial transactions |
| **Total Quantity** | **37,873 units** | Physical volume shipped |
| **Average Order Value (AOV)** | **$458.61** | Average revenue per customer order |
| **Unique Products** | **1,862** | Active catalog SKUs |
| **Unique Customers** | **793** | Registered enterprise and consumer clients |
| **Net Profit Margin** | **12.47%** | Healthy overall corporate operating margin |

---

## Slide 4: Monthly Sales Trajectory & Seasonality
- **Continuous Growth**: Monthly sales expanded from ~$40K/month in 2014 to over ~$80K/month by late 2017 (51.4% 4-year growth).
- **All-Time Peak**: **November 2017** recorded **$118,447.80** in sales across 261 orders.
- **Historical Low**: **February 2014** generated **$4,519.92** across 28 orders.
- **Q4 Seasonality**: Between 34% and 38% of annual revenue is concentrated in Q4 (Sept–Dec) driven by corporate budget spend and holiday retail shopping.

---

## Slide 5: Regional Performance & Geographic Distribution
- **West (Market Leader)**: **$725,457.76 (31.58%)** across 1,611 orders.
- **East**: **$678,781.30 (29.55%)** across 1,401 orders.
- **Coastal Concentration**: West + East generate **61.13% ($1.40M)** of total sales.
- **Central**: **$501,239.76 (21.82%)** across 1,175 orders.
- **South (Growth Opportunity)**: **$391,721.83 (17.05%)** across 822 orders—representing untapped potential.

---

## Slide 6: Product Category Dynamics & Top 10 SKUs
- **Category Breakdown**:
  - **Technology**: **$836,154.02 (36.40%)** – Highest revenue and highest unit value.
  - **Furniture**: **$741,999.73 (32.30%)** – High volume, but margin-challenged.
  - **Office Supplies**: **$719,046.90 (31.30%)** – Steady recurring "basket-fillers".
- **Top Product**:
  - **Canon imageCLASS 2200 Advanced Copier** generated **$61,599.83** from only 20 units ($3,080/unit).
  - The top 5 SKUs account for $153,385.69 (6.68% of total catalog sales).

---

## Slide 7: Dual Dashboard Experience
- **Power BI File (`dashboard/sales_analysis_dashboard.pbix`)**:
  - Built for formal enterprise reporting.
  - Contains star-schema data model, relationships, DAX measures, and interactive cross-highlighting.
- **Interactive Live Web Dashboard (`dashboard/index.html`)**:
  - Requires zero installations; runs directly in any browser.
  - Interactive slicers: Year, Month, Region, Category, and live Product search.
  - Real-time recalculation of all 4 KPI cards and 4 dynamic Chart.js visualizations.
  - Searchable transaction table preview for line-item inspection.

---

## Slide 8: Key Business Insights (Empirically Derived)
1. **Coastal Market Strength**: West and East drive over 61% of top-line sales.
2. **Q4 Surge**: Supply chain buffers must be in place before late August to handle November surges.
3. **Technology Hardware Leadership**: Highest gross revenue and margin contribution.
4. **Star SKU Dependency**: Top copier SKU drives outsized revenue and requires priority SLA inventory.
5. **High Repeat Engagement**: Customers average 6.3 orders each with an AOV of $458.61.
6. **Furniture Discounting Risk**: Tables incurred -$17.7K net loss due to discounts exceeding 30%.
7. **Southern Market Gap**: Territory realignment can expand the customer base by 50%+.

---

## Slide 9: Strategic Recommendations & Conclusion
- **Policy Change**: Implement a strict 15% discount cap on Furniture (Tables & Bookcases) to recover an estimated $21K+ in annual margin.
- **Logistics Ramp-up**: Increase safety stock for top 10 SKUs by late August ahead of Q4 rush.
- **Sales Realignment**: Add dedicated commercial sales reps to high-growth Southern metropolitan hubs.
- **B2B Loyalty Program**: Introduce volume rebates on office consumables to raise AOV from $458 to $525+.
- **Conclusion**: The project fulfills all internship requirements, combining data hygiene, statistical rigor, dynamic dashboards, and actionable business strategy.
