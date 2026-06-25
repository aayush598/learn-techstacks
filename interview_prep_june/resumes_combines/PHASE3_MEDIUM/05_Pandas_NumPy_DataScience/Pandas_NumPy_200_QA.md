# Pandas, NumPy & Data Science - 200+ Interview Q&A

## NumPy (Q1-Q80)

### Q1: What is NumPy? Why use it over Python lists?
**Answer:** NumPy provides N-dimensional arrays. Faster (C implementation, vectorization), memory efficient (contiguous memory), supports broadcasting, has linear algebra functions. Python lists have overhead from dynamic typing and pointers.

### Q2: What is broadcasting in NumPy?
**Answer:** NumPy performs arithmetic on arrays of different shapes by "stretching" smaller array to match larger. Rules: dimensions compared from right, must be equal or 1. Example: (3,1) + (1,4) → (3,4).

### Q3: Difference between np.array vs np.ndarray?
**Answer:** np.array() creates arrays. np.ndarray is the actual class type. Use np.array() for construction.

### Q4: NumPy operations: dot, matmul, multiply?
**Answer:** np.dot: dot product (vectors) or matrix multiplication (2D). np.matmul: matrix multiplication (preferred for >2D). * or np.multiply: element-wise multiplication.

### Q5: Reshape, resize, flatten, ravel differences?
**Answer:** reshape: returns new view (possible). resize: modifies in-place or returns new copy. flatten: always returns copy. ravel: returns view when possible (faster). Use ravel unless you need copy.

## Pandas (Q81-Q180)

### Q6: What is Pandas? Series vs DataFrame?
**Answer:** Pandas provides data structures: Series (1D labeled array) and DataFrame (2D labeled table). Built on NumPy. Labeled axes, missing data handling, group operations, time series.

### Q7: How to handle missing values in Pandas?
**Answer:** dropna() - remove NaN rows/columns. fillna() - fill with value, method (ffill, bfill), or interpolation. isnull(), notnull() for detection. Can fill with mean/median/mode.

### Q8: groupby operations explained?
**Answer:** split-apply-combine: df.groupby('col').agg({'price':'mean', 'qty':'sum'}). Can use multiple aggregations, transform, filter, apply. GroupBy object allows iteration over groups.

### Q9: merge vs join vs concat?
**Answer:** merge: SQL-style joins (how, on, left_on, right_on). join: merges on index. concat: stacks DataFrames along axis (rows=0, columns=1). merge is most flexible.

### Q10: apply vs applymap vs map?
**Answer:** apply: applies function to DataFrame rows/columns. applymap: element-wise on entire DataFrame. map: element-wise on Series only (replacement). For performance, prefer vectorized operations over apply.

## Data Science Workflow (Q181-Q200)

### Q11: Feature engineering techniques?
**Answer:** Numerical: scaling (standard, min-max), binning, polynomial features. Categorical: one-hot encoding, label encoding, target encoding. Text: TF-IDF, count vectorizer. Date: day/month/year, dayofweek, is_holiday.

### Q12: What is the data science workflow?
**Answer:** (1) Problem definition. (2) Data collection. (3) Data cleaning (missing values, outliers, duplicates). (4) EDA (statistics, visualizations). (5) Feature engineering. (6) Model selection. (7) Training & tuning. (8) Evaluation. (9) Deployment. (10) Monitoring.
