# 📦 Supply Chain Performance Analysis

“In God we trust. All others must bring data.” — W. Edwards Deming

  

A data analysis project examining 180,519 real supply chain orders from the DataCo Global Supply Chain dataset — built to develop practical analytics skills ahead of an MSc in Engineering Management at the University of Portsmouth London (September 2026).
## 📊 Order Status Breakdown
pie title Order Status Distribution
    "Complete" : 46.1
    "Pending" : 15.7
    "Closed" : 13.4
    "Pending Payment" : 8.5
    "Processing" : 7.8
    "Suspected Fraud" : 4.8
    "On Hold" : 2.4
    "Cancelled" : 1.3
    ## 🔍 Key Findings

📌 Finding 1 — Shipping Mode Risk
First Class shipping has the highest late delivery rate despite being the premium option marketed to customers.
📌 Finding 2 — Profit Concentration
Top 3 product categories drive the majority of total profit — a classic 80/20 distribution pattern.
📌 Finding 3 — Delivery Delays
Average delivery delay across all 180,519 orders is approximately 1.6 days — small individually but significant at scale.
📌 Finding 4 — Systemic Supply Chain Issue
All three customer segments show a late delivery rate of approximately 55% — confirming a systemic problem rather than a segment-specific one.
## 📁 Project Files

- analysis.py — Main Python script
- Supply_Chain_Analysis_Report.xlsx — Excel report with 5 sheets
- chart1_late_delivery.png — Late delivery by shipping mode
- chart2_profit_by_category.png — Top 10 profitable categories
- chart3_order_status.png — Order status breakdown
- chart4_delay_by_segment.png — Delay by customer segment
- ## 🛠️ Tech Stack

- *Python 3.11* — Core language
- *pandas* — Data loading and analysis
- *matplotlib* — Charts and visualisation
- *openpyxl* — Excel report generation
- ## ▶️ How to Run
- pip install pandas matplotlib openpyxl
python analysis.py
## 👤 Author

Ravikumar N
ECE Graduate | MSc Engineering Management Candidate
University of Portsmouth, London Campus — September 2026
📧 ravikumar.n0409@gmail.com
🔗 github.com/ravikumar98
