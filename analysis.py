import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# Load the dataset
df = pd.read_csv("DataCoSupplyChainDataset.csv", encoding="latin-1")

# First look
print("===========================================")
print("DATASET LOADED SUCCESSFULLY")
print("===========================================")
print(f"Total rows    : {df.shape[0]:,}")
print(f"Total columns : {df.shape[1]}")
print("\nColumn names:")
for col in df.columns:
    print(f"  - {col}")
    # ── Select only the columns we need ──────────────────
cols = [
    "Category Name",
    "Customer Segment",
    "Department Name",
    "Order Country",
    "Order Item Quantity",
    "Order Item Total",
    "Order Profit Per Order",
    "Order Status",
    "Shipping Mode",
    "Days for shipping (real)",
    "Days for shipment (scheduled)",
    "Late_delivery_risk"
]

df = df[cols].dropna()

print("\n===========================================")
print("DATA CLEANED")
print("===========================================")
print(f"Rows after cleaning : {df.shape[0]:,}")
print(f"Columns kept        : {df.shape[1]}")
print("\nMissing values remaining:")
print(df.isnull().sum())
# ── ANALYSIS 1: Late Delivery by Shipping Mode ────────
print("\n===========================================")
print("ANALYSIS 1: LATE DELIVERY BY SHIPPING MODE")
print("===========================================")

late_by_mode = df.groupby("Shipping Mode").agg(
    Total_Orders=("Late_delivery_risk", "count"),
    Late_Deliveries=("Late_delivery_risk", "sum")
).reset_index()

late_by_mode["Late_Rate_%"] = (
    late_by_mode["Late_Deliveries"] /
    late_by_mode["Total_Orders"] * 100
).round(1)

late_by_mode = late_by_mode.sort_values(
    "Late_Rate_%", ascending=False
)

print(late_by_mode.to_string(index=False))

# ── Chart 1 ───────────────────────────────────────────
colors = ["#C0392B", "#E67E22", "#F1C40F", "#27AE60"]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(
    late_by_mode["Shipping Mode"],
    late_by_mode["Late_Rate_%"],
    color=colors,
    edgecolor="white",
    linewidth=0.8
)

# Add value labels on top of bars
for bar, val in zip(bars, late_by_mode["Late_Rate_%"]):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        f"{val}%",
        ha="center",
        fontsize=11,
        fontweight="bold",
        color="#1A1A1A"
    )

ax.set_title(
    "Late Delivery Rate by Shipping Mode",
    fontsize=14,
    fontweight="bold",
    pad=15
)
ax.set_ylabel("Late Delivery Rate (%)", fontsize=11)
ax.set_xlabel("Shipping Mode", fontsize=11)
ax.set_ylim(0, max(late_by_mode["Late_Rate_%"]) + 10)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("chart1_late_delivery.png", dpi=150)
plt.show()
print("\nChart 1 saved.")
# ── ANALYSIS 2: PROFIT BY PRODUCT CATEGORY ───────────
print("\n===========================================")
print("ANALYSIS 2: TOP 10 MOST PROFITABLE CATEGORIES")
print("===========================================")

profit_cat = df.groupby("Category Name").agg(
    Total_Profit=("Order Profit Per Order", "sum"),
    Avg_Profit=("Order Profit Per Order", "mean"),
    Total_Orders=("Order Profit Per Order", "count")
).reset_index()

profit_cat = profit_cat.sort_values(
    "Total_Profit", ascending=False
).head(10)

profit_cat["Total_Profit"] = profit_cat["Total_Profit"].round(2)
profit_cat["Avg_Profit"]   = profit_cat["Avg_Profit"].round(2)

print(profit_cat.to_string(index=False))

# ── Chart 2 ───────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))

colors_grad = [
    "#1B3A5C", "#1E4D7A", "#236098", "#2874B6",
    "#3A8DD4", "#5BA5E0", "#7DBDEC", "#A0D2F5",
    "#C2E4FA", "#E0F2FD"
]

bars = ax.barh(
    profit_cat["Category Name"],
    profit_cat["Total_Profit"],
    color=colors_grad,
    edgecolor="white",
    linewidth=0.6
)

# Value labels
for bar, val in zip(bars, profit_cat["Total_Profit"]):
    ax.text(
        bar.get_width() + 1000,
        bar.get_y() + bar.get_height() / 2,
        f"${val:,.0f}",
        va="center",
        fontsize=9,
        color="#1A1A1A"
    )

ax.set_title(
    "Top 10 Product Categories by Total Profit",
    fontsize=14,
    fontweight="bold",
    pad=15
)
ax.set_xlabel("Total Profit (USD)", fontsize=11)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.invert_yaxis()

plt.tight_layout()
plt.savefig("chart2_profit_by_category.png", dpi=150)
plt.show()
print("\nChart 2 saved.")
# ── ANALYSIS 3: ORDER STATUS BREAKDOWN ───────────────
print("\n===========================================")
print("ANALYSIS 3: ORDER STATUS BREAKDOWN")
print("===========================================")

status_counts = df["Order Status"].value_counts().reset_index()
status_counts.columns = ["Order Status", "Count"]
status_counts["Percentage_%"] = (
    status_counts["Count"] / status_counts["Count"].sum() * 100
).round(1)

print(status_counts.to_string(index=False))

# ── Chart 3 ───────────────────────────────────────────
colors_pie = [
    "#1B3A5C", "#C0392B", "#E67E22",
    "#27AE60", "#8E44AD", "#2980B9"
]

fig, ax = plt.subplots(figsize=(8, 8))

wedges, texts, autotexts = ax.pie(
    status_counts["Count"],
    labels=status_counts["Order Status"],
    autopct="%1.1f%%",
    colors=colors_pie[:len(status_counts)],
    startangle=90,
    pctdistance=0.82,
    wedgeprops={"edgecolor": "white", "linewidth": 2}
)

for text in texts:
    text.set_fontsize(11)
for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_fontweight("bold")
    autotext.set_color("white")

ax.set_title(
    "Order Status Breakdown",
    fontsize=14,
    fontweight="bold",
    pad=20
)

plt.tight_layout()
plt.savefig("chart3_order_status.png", dpi=150)
plt.show()
print("\nChart 3 saved.")
# ── ANALYSIS 4: DELIVERY DELAY DEEP DIVE ─────────────
print("\n===========================================")
print("ANALYSIS 4: DELIVERY DELAY DEEP DIVE")
print("===========================================")

# Calculate delay in days (positive = late, negative = early)
df["Delay_Days"] = (
    df["Days for shipping (real)"] -
    df["Days for shipment (scheduled)"]
)

# Overall delay stats
print("Overall Delivery Performance:")
print(f"  Average delay     : {df['Delay_Days'].mean():.1f} days")
print(f"  Max delay         : {df['Delay_Days'].max():.0f} days")
print(f"  On time or early  : {(df['Delay_Days'] <= 0).sum():,} orders")
print(f"  Late              : {(df['Delay_Days'] > 0).sum():,} orders")

# Delay by Customer Segment
print("\nAverage Delay by Customer Segment:")
seg_delay = df.groupby("Customer Segment").agg(
    Avg_Delay=("Delay_Days", "mean"),
    Total_Orders=("Delay_Days", "count"),
    Late_Orders=("Late_delivery_risk", "sum")
).reset_index()

seg_delay["Avg_Delay"]   = seg_delay["Avg_Delay"].round(2)
seg_delay["Late_Rate_%"] = (
    seg_delay["Late_Orders"] /
    seg_delay["Total_Orders"] * 100
).round(1)

print(seg_delay.to_string(index=False))

# ── Chart 4 ───────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: Average delay by segment
colors_seg = ["#1B3A5C", "#C0392B", "#27AE60"]
bars = axes[0].bar(
    seg_delay["Customer Segment"],
    seg_delay["Avg_Delay"],
    color=colors_seg,
    edgecolor="white",
    linewidth=0.8
)
for bar, val in zip(bars, seg_delay["Avg_Delay"]):
    axes[0].text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.05,
        f"{val} days",
        ha="center",
        fontsize=11,
        fontweight="bold"
    )
axes[0].set_title(
    "Avg Delivery Delay by Customer Segment",
    fontsize=12, fontweight="bold"
)
axes[0].set_ylabel("Average Delay (Days)")
axes[0].spines["top"].set_visible(False)
axes[0].spines["right"].set_visible(False)

# Right: Late rate by segment
bars2 = axes[1].bar(
    seg_delay["Customer Segment"],
    seg_delay["Late_Rate_%"],
    color=colors_seg,
    edgecolor="white",
    linewidth=0.8
)
for bar, val in zip(bars2, seg_delay["Late_Rate_%"]):
    axes[1].text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        f"{val}%",
        ha="center",
        fontsize=11,
        fontweight="bold"
    )
axes[1].set_title(
    "Late Delivery Rate by Customer Segment",
    fontsize=12, fontweight="bold"
)
axes[1].set_ylabel("Late Delivery Rate (%)")
axes[1].spines["top"].set_visible(False)
axes[1].spines["right"].set_visible(False)

plt.suptitle(
    "Delivery Performance by Customer Segment",
    fontsize=14, fontweight="bold", y=1.02
)
plt.tight_layout()
plt.savefig("chart4_delay_by_segment.png", dpi=150, bbox_inches="tight")
plt.show()
print("\nChart 4 saved.")
# ── FINAL: EXPORT SUMMARY REPORT ─────────────────────
print("\n===========================================")
print("EXPORTING SUMMARY REPORT")
print("===========================================")

# ── Sheet 1: Late Delivery by Shipping Mode ───────────
sheet1 = late_by_mode.copy()
sheet1.columns = [
    "Shipping Mode", "Total Orders",
    "Late Deliveries", "Late Rate %"
]

# ── Sheet 2: Top 10 Profitable Categories ─────────────
sheet2 = profit_cat.copy()
sheet2.columns = [
    "Category", "Total Profit ($)",
    "Avg Profit ($)", "Total Orders"
]

# ── Sheet 3: Order Status ─────────────────────────────
sheet3 = status_counts.copy()
sheet3.columns = ["Order Status", "Count", "Percentage %"]

# ── Sheet 4: Delay by Segment ─────────────────────────
sheet4 = seg_delay.copy()
sheet4.columns = [
    "Customer Segment", "Avg Delay (Days)",
    "Total Orders", "Late Orders", "Late Rate %"
]

# ── Sheet 5: Key Findings ─────────────────────────────
findings = {
    "Finding": [
        "Highest late delivery rate shipping mode",
        "Lowest late delivery rate shipping mode",
        "Most profitable product category",
        "Average delivery delay across all orders",
        "Customer segment with highest late rate",
        "Total orders analysed",
        "Overall late delivery rate"
    ],
    "Value": [
        late_by_mode.iloc[0]["Shipping Mode"],
        late_by_mode.iloc[-1]["Shipping Mode"],
        profit_cat.iloc[0]["Category Name"],
        f"{df['Delay_Days'].mean():.1f} days",
        seg_delay.sort_values(
            "Late_Rate_%", ascending=False
        ).iloc[0]["Customer Segment"],
        f"{len(df):,}",
        f"{df['Late_delivery_risk'].mean()*100:.1f}%"
    ]
}
sheet5 = pd.DataFrame(findings)

# ── Write to Excel with multiple sheets ───────────────
output_file = "Supply_Chain_Analysis_Report.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    sheet5.to_excel(writer, sheet_name="Key Findings",    index=False)
    sheet1.to_excel(writer, sheet_name="Late by Shipping", index=False)
    sheet2.to_excel(writer, sheet_name="Profit by Category", index=False)
    sheet3.to_excel(writer, sheet_name="Order Status",    index=False)
    sheet4.to_excel(writer, sheet_name="Delay by Segment", index=False)

print(f"Report saved: {output_file}")
print("\n===========================================")
print("PROJECT COMPLETE")
print("===========================================")
print("Files created:")
print("  analysis.py                        — Python code")
print("  chart1_late_delivery.png           — Chart 1")
print("  chart2_profit_by_category.png      — Chart 2")
print("  chart3_order_status.png            — Chart 3")
print("  chart4_delay_by_segment.png        — Chart 4")
print("  Supply_Chain_Analysis_Report.xlsx  — Excel report")
print("\nReady to push to GitHub.")