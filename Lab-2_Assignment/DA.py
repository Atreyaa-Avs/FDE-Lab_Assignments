# -------------------------------
#  Data Analyst Task
# -------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# -------------------------------
# 1. Access processed data
# -------------------------------
processed_path = f"{CURRENT_DIR}/data_warehouse/processed_treatments.csv"
summary_path = f"{CURRENT_DIR}/data_warehouse/top5_treatments_summary.csv"
trend_path = f"{CURRENT_DIR}/data_warehouse/treatment_trends.csv"

df = pd.read_csv(processed_path)
summary_df = pd.read_csv(summary_path)
trend_df = pd.read_csv(trend_path)

# -------------------------------
# 2. Analyse
# -------------------------------

print("\n--- Top 5 Treatment Types by Revenue ---")
print(summary_df)

print("\n--- Yearly Treatment Trends (first 10 rows) ---")
print(trend_df.head(10))

# -------------------------------
# 3. Communicate with Charts
# -------------------------------

# Plot 1: Bar chart of top 5 treatments by total revenue
plt.figure(figsize=(8, 5))
plt.bar(summary_df['treatment_type'], summary_df['total_revenue'], color='skyblue')
plt.title("Top 5 Treatments by Total Revenue")
plt.xlabel("Treatment Type")
plt.ylabel("Total Revenue")
plt.xticks(rotation=30, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# Plot 2: Line plot of treatment utilization trend
plt.figure(figsize=(10, 6))
for ttype in trend_df['treatment_type'].unique():
    subset = trend_df[trend_df['treatment_type'] == ttype]
    plt.plot(subset['year'], subset['treatment_count'], marker="o", label=ttype)

plt.title("Yearly Treatment Utilization Trends")
plt.xlabel("Year")
plt.ylabel("Treatment Count")
plt.legend(title="Treatment Type")
plt.grid(True, linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# -------------------------------
# 4. Feedback to Data Engineer
# -------------------------------

print("\n--- Feedback to Data Engineer ---")
if df['treatment_cost'].isnull().sum() > 0 or df['room_cost'].isnull().sum() > 0:
    print("Some treatment costs are missing. Please verify raw data quality.")
if df['treatment_date'].isnull().sum() > 0:
    print("Some treatment_date entries could not be parsed. Ensure consistent date format.")
if df.duplicated(subset=['treatment_id']).any():
    print("Duplicate treatment_id values detected. Consider deduplication at ingestion step.")
else:
    print("No major data quality issues detected.")
