# -------------
# Identifying High-Value Treatments with K-Means Clustering
# -------------

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load processed treatments
df = pd.read_csv(f"{CURRENT_DIR}/data_warehouse/processed_treatments.csv")

# Aggregate per treatment_type
agg_df = df.groupby('treatment_type').agg(
    avg_revenue=('revenue', 'mean'),
    treatment_count=('treatment_id', 'count')
).reset_index()

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(agg_df[['avg_revenue', 'treatment_count']])

# Cluster into 3 groups
kmeans = KMeans(n_clusters=3, random_state=42)
agg_df['cluster'] = kmeans.fit_predict(X_scaled)

# Label high-value treatments
high_cluster = agg_df.groupby('cluster')['avg_revenue'].mean().idxmax()
agg_df['High_Value_Treatment'] = (agg_df['cluster'] == high_cluster).astype(int)

# Save enriched file
agg_df.to_csv(f"{CURRENT_DIR}/data_warehouse/treatment_segments.csv", index=False)
print(agg_df.head(10))
