
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Introduction to Pandas
# No specific code needed for introduction

# 2. Data Loading and Basic Operations
# Loading Data from CSV
df = pd.read_csv('data.csv')
print(df.head())

# Basic Information and Descriptive Statistics
df.info()
print(df.describe())
print(df['column'].value_counts())

# 3. Handling Missing Values
# Checking and Removing Missing Values
print(df.isnull().sum())
df.dropna(inplace=True)

# Filling Missing Values
df.fillna(0, inplace=True)

# 4. Data Selection and Filtering
# Selecting Columns Based on Data Types
numeric_columns = df.select_dtypes(include=['int', 'float']).columns
print(df[numeric_columns])

# Filtering Rows Based on Multiple Conditions
filtered_df = df[(df['Age'] > 25) & (df['Department'] == 'HR')]
print(filtered_df)

# 5. Data Transformation
# Converting Data Types
df['numeric_column'] = pd.to_numeric(df['numeric_column'])

# String Operations
df['NameLength'] = df['Name'].apply(len)

# Creating New Columns
df['Bonus'] = df['Salary'] * 0.1

# Log Transformation
df['log_column'] = np.log(df['numeric_column'])

# 6. Grouping and Aggregation
# Group by and Aggregate with Multiple Functions
grouped_df = df.groupby('Department').agg({'Salary': ['mean', 'sum'], 'Age': 'max'})
print(grouped_df)

# 7. Merging and Joining DataFrames
# Merging DataFrames on a Specific Column
other_data = {
    'Department': ['HR', 'Finance', 'IT'],
    'Location': ['City1', 'City2', 'City3']
}
other_df = pd.DataFrame(other_data)
merged_df = pd.merge(df, other_df, on='Department', how='left')
print(merged_df)

# 8. Pivot Tables
# Creating a pivot table
pivot_table = df.pivot_table(index='Department', values='Salary', aggfunc='mean')
print(pivot_table)

# 9. Data Visualization
# Basic Plotting with Pandas
plt.hist(df['numeric_column'], bins=10)
plt.xlabel('Numeric Column')
plt.ylabel('Frequency')
plt.show()

plt.scatter(df['feature1'], df['feature2'])
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.show()

# Using Seaborn for Enhanced Visualizations
correlation_matrix = df.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.show()

# 10. Advanced Indexing
# Setting and Using Indexes
df.set_index('Name', inplace=True)
print(df.loc['Alice'])

# Multi-Level Indexing
data = {
    ('Alice', 'Q1'): {'Sales': 300, 'Returns': 30},
    ('Alice', 'Q2'): {'Sales': 350, 'Returns': 35},
    ('Bob', 'Q1'): {'Sales': 200, 'Returns': 20},
    ('Bob', 'Q2'): {'Sales': 250, 'Returns': 25},
    ('Chris', 'Q1'): {'Sales': 400, 'Returns': 40},
    ('Chris', 'Q2'): {'Sales': 450, 'Returns': 45}
}
df_multi = pd.DataFrame.from_dict(data, orient='index')
df_multi.index.names = ['Employee', 'Quarter']
print(df_multi)
