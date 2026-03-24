# Skill: data_analysis

## Purpose
Perform data analysis tasks — statistics, visualization, transformation, and reporting using Python (pandas, matplotlib, seaborn).

## When to use
- Analyzing CSV, JSON, Excel, or database data
- Computing statistics, correlations, or trends
- Creating charts and visualizations
- Cleaning, transforming, or merging datasets
- Generating data-driven reports

## How to execute

**Load and inspect data:**
```bash
pip install pandas --quiet && python3 -c "
import pandas as pd

df = pd.read_csv('./data/input.csv')
print('Shape:', df.shape)
print('\nColumns:', list(df.columns))
print('\nData types:')
print(df.dtypes)
print('\nFirst 5 rows:')
print(df.head())
print('\nBasic stats:')
print(df.describe())
"
```

**Load JSON data:**
```bash
python3 -c "
import pandas as pd, json

with open('./data/input.json') as f:
    data = json.load(f)
df = pd.DataFrame(data)
print(df.info())
print(df.head())
"
```

**Filter and aggregate:**
```bash
python3 -c "
import pandas as pd

df = pd.read_csv('./data/sales.csv')

# Filter
high_value = df[df['amount'] > 1000]
print(f'High value transactions: {len(high_value)}')

# Group by
summary = df.groupby('category').agg(
    count=('amount', 'count'),
    total=('amount', 'sum'),
    average=('amount', 'mean'),
    median=('amount', 'median')
).round(2).sort_values('total', ascending=False)

print('\nBy category:')
print(summary.to_string())
"
```

**Create visualizations:**
```bash
pip install matplotlib seaborn --quiet && python3 -c "
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

df = pd.read_csv('./data/sales.csv')

# Bar chart
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Chart 1: Category totals
cat_totals = df.groupby('category')['amount'].sum().sort_values(ascending=False)
cat_totals.plot(kind='bar', ax=axes[0], color='steelblue')
axes[0].set_title('Revenue by Category')
axes[0].set_ylabel('Total Revenue')

# Chart 2: Monthly trend
df['date'] = pd.to_datetime(df['date'])
monthly = df.resample('M', on='date')['amount'].sum()
monthly.plot(ax=axes[1], marker='o', color='coral')
axes[1].set_title('Monthly Revenue Trend')
axes[1].set_ylabel('Revenue')

plt.tight_layout()
os.makedirs('./output', exist_ok=True)
plt.savefig('./output/analysis_charts.png', dpi=150)
print('Charts saved to ./output/analysis_charts.png')
"
```

**Correlation analysis:**
```bash
python3 -c "
import pandas as pd

df = pd.read_csv('./data/metrics.csv')
numeric_cols = df.select_dtypes(include='number')
corr = numeric_cols.corr().round(3)
print('Correlation matrix:')
print(corr.to_string())

# Find strong correlations
import numpy as np
pairs = []
for i in range(len(corr.columns)):
    for j in range(i+1, len(corr.columns)):
        val = corr.iloc[i, j]
        if abs(val) > 0.7:
            pairs.append((corr.columns[i], corr.columns[j], val))

if pairs:
    print('\nStrong correlations (|r| > 0.7):')
    for a, b, r in sorted(pairs, key=lambda x: abs(x[2]), reverse=True):
        print(f'  {a} ↔ {b}: {r}')
"
```

**Clean data:**
```bash
python3 -c "
import pandas as pd

df = pd.read_csv('./data/raw.csv')
print(f'Before: {len(df)} rows')

# Remove duplicates
df = df.drop_duplicates()

# Handle missing values
print(f'Missing values: {df.isnull().sum().to_dict()}')
df = df.dropna(subset=['required_field'])  # Drop rows missing required fields
df['optional_field'] = df['optional_field'].fillna('N/A')  # Fill optional

# Standardize text
df['name'] = df['name'].str.strip().str.title()

# Fix data types
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

print(f'After: {len(df)} rows')
df.to_csv('./data/cleaned.csv', index=False)
print('Saved to ./data/cleaned.csv')
"
```

**Merge datasets:**
```bash
python3 -c "
import pandas as pd

users = pd.read_csv('./data/users.csv')
orders = pd.read_csv('./data/orders.csv')

# Join on user_id
merged = pd.merge(users, orders, on='user_id', how='left')
print(f'Users: {len(users)}, Orders: {len(orders)}, Merged: {len(merged)}')

# User summary
user_summary = merged.groupby('user_id').agg(
    name=('name', 'first'),
    order_count=('order_id', 'count'),
    total_spent=('amount', 'sum')
).sort_values('total_spent', ascending=False)

print(user_summary.head(10).to_string())
"
```

**Export analysis results:**
```bash
python3 -c "
import pandas as pd, json, os

df = pd.read_csv('./data/sales.csv')

# Build summary
summary = {
    'total_records': len(df),
    'total_revenue': round(df['amount'].sum(), 2),
    'average_order': round(df['amount'].mean(), 2),
    'median_order': round(df['amount'].median(), 2),
    'top_category': df.groupby('category')['amount'].sum().idxmax(),
}

os.makedirs('./output', exist_ok=True)
with open('./output/summary.json', 'w') as f:
    json.dump(summary, f, indent=2)
print('Summary:', json.dumps(summary, indent=2))
"
```

## Output contract
- stdout: analysis results, statistics, or confirmation
- exit_code 0: success
- exit_code 1: file not found, parse error, or library missing

## Evaluate output
If KeyError: inspect columns with `df.columns` first.
If memory issues: use `chunksize` parameter for large files.
Always inspect data shape and types before analysis.
Charts require `matplotlib.use('Agg')` for headless environments.
