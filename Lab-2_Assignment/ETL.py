#Stage 1: Business Analyst Task

#Objective: Who are the top 5 doctors by revenue, 
#and how do their patient feedback scores compare?

#Metrics Required:

#treatment_type

#total_revenue = treatment_cost + room_cost

#treatment_count

#yearly_trend (number of treatments per year)

import pandas as pd
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Ensure warehouse directory exists
os.makedirs(f"{CURRENT_DIR}/data_warehouse", exist_ok=True)

# -------------------------------
# 1. Ingestion
# -------------------------------
treatments_df = pd.read_csv(f"{CURRENT_DIR}/raw_data/patients_data_with_doctor.csv")

# -------------------------------
# 2. Cleansing
# -------------------------------

# Convert costs to numeric
treatments_df['treatment_cost'] = pd.to_numeric(treatments_df['treatment_cost'], errors="coerce")
treatments_df['room_cost'] = pd.to_numeric(treatments_df['room_cost'], errors="coerce")

# Convert treatment_date to datetime
treatments_df['treatment_date'] = pd.to_datetime(treatments_df['treatment_date'], errors="coerce")

# Drop duplicates and invalid rows
treatments_df = treatments_df.drop_duplicates()
treatments_df = treatments_df.dropna(subset=['treatment_cost', 'room_cost', 'treatment_date'])

# -------------------------------
# 3. Transformation
# -------------------------------

# Compute revenue
treatments_df['revenue'] = treatments_df['treatment_cost'] + treatments_df['room_cost']

# Group by treatment_type for revenue & counts
summary = (
    treatments_df.groupby("treatment_type")
    .agg(
        total_revenue=("revenue", "sum"),
        treatment_count=("treatment_id", "count")
    )
    .reset_index()
    .sort_values(by="total_revenue", ascending=False)
    .head(5)
)

# Yearly utilization trend
treatments_df['year'] = treatments_df['treatment_date'].dt.year
trend = (
    treatments_df.groupby(["year", "treatment_type"])
    .size()
    .reset_index(name="treatment_count")
)

# -------------------------------
# 4. Loading
# -------------------------------
processed_path = f"{CURRENT_DIR}/data_warehouse/processed_treatments.csv"
treatments_df.to_csv(processed_path, index=False)

summary_path = f"{CURRENT_DIR}/data_warehouse/top5_treatments_summary.csv"
summary.to_csv(summary_path, index=False)

trend_path = f"{CURRENT_DIR}/data_warehouse/treatment_trends.csv"
trend.to_csv(trend_path, index=False)

print(f"Processed data saved to {processed_path}")
print(f"Top 5 treatments summary saved to {summary_path}")
print(f"Treatment trends saved to {trend_path}")
print(summary)
print(trend.head(10))
