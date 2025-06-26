import pandas as pd
from sklearn.preprocessing import KBinsDiscretizer

loan_data = pd.read_csv("Task 3 and 4_Loan_Data.csv")

fico_scores = loan_data['fico_score'].values.reshape(-1, 1)

n_buckets = 5

binner = KBinsDiscretizer(n_bins=n_buckets, encode='ordinal', strategy='kmeans')
ratings = binner.fit_transform(fico_scores).astype(int).flatten() + 1

loan_data['fico_rating_mse'] = ratings

result = loan_data.groupby('fico_rating_mse').agg(
    count=('fico_score', 'count'),
    avg_fico=('fico_score', 'mean'),
    default_rate=('default', 'mean')
)

print(result)
