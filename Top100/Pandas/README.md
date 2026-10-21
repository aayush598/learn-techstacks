# Pandas Interview Questions and Answers (Top 100)

## Q1: What is Pandas?
**A:** Pandas is a Python library for data manipulation and analysis built on top of NumPy. It introduces two core data structures: `Series` (1D labeled array) and `DataFrame` (2D labeled table). Pandas provides powerful tools for reading/writing data (CSV, Excel, SQL, JSON), data cleaning, transformation, aggregation, merging, and time series analysis.

**Code:**
```python
import pandas as pd

s = pd.Series([1, 2, 3], name="vals")           # 1D labeled array
df = pd.DataFrame({"name": ["A", "B"], "age": [25, 30]})  # 2D labeled table
print(s, df, sep="\n")
```

## Q2: What is a Pandas Series?
**A:** A Series is a 1D labeled array that can hold any data type. It consists of `data` (values) and `index` (labels). Created: `pd.Series([1, 2, 3], index=['a', 'b', 'c'])`. Access by label (`s['a']`), integer position (`s.iloc[0]`), or condition (`s[s > 1]`). Supports vectorized operations like NumPy.

**Code:**
```python
import pandas as pd

s = pd.Series([1, 2, 3], index=["a", "b", "c"])
print(s["a"])        # label access -> 1
print(s.iloc[0])     # positional access -> 1
print(s[s > 1])      # conditional access
```

## Q3: What is a Pandas DataFrame?
**A:** A DataFrame is a 2D labeled data. Rows and columns have labels (index and columns). Created from: dict of Series/arrays, list of dicts, CSV file, SQL query. Key methods: `head()`, `info()`, `describe()`, `shape`, `columns`, `index`, `dtypes`.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"x": [1, 2], "y": ["a", "b"]})
print(df.head(1))
print(df.shape, df.columns.tolist(), df.dtypes.to_dict())
```

## Q4: How do you create a DataFrame from different sources?
**A:** From dict: `pd.DataFrame({'col1': [1,2], 'col2': [3,4]})`. From list of dicts: `pd.DataFrame([{'a': 1}, {'a': 2, 'b': 3}])`. From CSV: `pd.read_csv('file.csv')`. From Excel: `pd.read_excel('file.xlsx')`. From SQL: `pd.read_sql('SELECT * FROM table', connection)`. From JSON: `pd.read_json('file.json')`. From NumPy: `pd.DataFrame(np_array, columns=['a', 'b'])`.

**Code:**
```python
import pandas as pd

from_dict = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
from_list = pd.DataFrame([{"a": 1}, {"a": 2, "b": 3}])
from_csv = pd.read_csv("file.csv")          # needs file.csv on disk
print(from_dict, from_list, sep="\n")
```

## Q5: What are the key methods to explore a DataFrame?
**A:** `df.head(n)` / `df.tail(n)` — preview rows. `df.info()` — column types, non-null counts, memory. `df.describe()` — summary statistics for numeric columns. `df.shape` — dimensions. `df.columns` / `df.index` — axis labels. `df.dtypes` — column data types. `df.value_counts()` — frequency. `df.nunique()` — unique counts. `df.sample(n)` — random sample.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"a": [1, 2, 2], "b": ["x", "y", "y"]})
print(df.head(2))
print(df.shape, df.columns.tolist())
print(df.describe())
print(df["a"].value_counts(), df["b"].nunique())
```

## Q6: How do you select columns in a DataFrame?
**A:** Single column: `df['col']` or `df.col` (returns Series). Multiple columns: `df[['col1', 'col2']]` (returns DataFrame). Select by dtype: `df.select_dtypes(include=['number'])`. Filter columns by name: `df.filter(like='pattern')` or `df.filter(regex='pattern')`.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"age": [20, 30], "name": ["a", "b"], "height_cm": [170, 180]})
print(df["age"])                                    # Series
print(df[["age", "name"]])                          # DataFrame
print(df.select_dtypes(include=["number"]))
print(df.filter(regex="cm$").columns.tolist())
```

## Q7: What is the difference between `loc` and `iloc`?
**A:** `df.loc[row_label, col_label]` uses label-based indexing — inclusive of the endpoint. `df.iloc[row_position, col_position]` uses integer-based positional indexing — exclusive of endpoint. Example: `df.loc['a':'c']` includes 'c', `df.iloc[0:3]` includes rows 0,1,2. `loc` works with bool arrays; `iloc` works with integer arrays.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"v": [1, 2, 3, 4]}, index=["a", "b", "c", "d"])
print(df.loc["a":"c"])    # includes 'c' (label, inclusive)
print(df.iloc[0:3])       # rows 0,1,2 (position, exclusive of 3)
```

## Q8: How do you filter rows conditionally?
**A:** `df[df['col'] > 5]` — boolean indexing. Multiple conditions: `df[(df['col1'] > 5) & (df['col2'] == 'x')]` (use `&`, `|`, `~` — not `and`, `or`, `not`). Query method: `df.query('col1 > 5 & col2 == "x"')`. `df.isin(['a', 'b'])` for membership. `df.between(0, 10)` for range.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"col1": [1, 6, 8], "col2": ["x", "y", "x"]})
print(df[df["col1"] > 5])
print(df[(df["col1"] > 5) & (df["col2"] == "x")])
print(df.query('col1 > 5 & col2 == "x"'))
print(df["col1"].between(0, 7))
```

## Q9: How do you handle missing values in Pandas?
**A:** Detect: `df.isna()` / `df.isnull()` (boolean), `df.isna().sum()`. Drop: `df.dropna()` (rows with any NaN), `df.dropna(axis=1)` (columns), `df.dropna(subset=['col'])` (specific columns). Fill: `df.fillna(value)`, `df.fillna(method='ffill')` (forward fill), `df.fillna(method='bfill')` (backward fill), `df.interpolate()` (linear interpolation).

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"a": [1, None, 3], "b": [4, 5, None]})
print(df.isna().sum())
print(df.dropna())            # drop rows with any NaN
print(df.dropna(axis=1))      # drop columns with any NaN
print(df["a"].fillna(0))      # fill with value
print(df["a"].ffill())        # forward fill
```

## Q10: What is the difference between `isna()` and `isnull()`?
**A:** They are identical — `isnull` is an alias of `isna`. Both return a boolean DataFrame/Series indicating missing values. Similarly, `notna()` and `notnull()` are aliases. The duplicate naming exists for compatibility (R users prefer `is.na`, SQL users prefer `is null`).

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"a": [1, None], "b": [None, 4]})
print(df.isna().equals(df.isnull()))     # True — identical
print(df.notna().equals(df.notnull()))   # True — identical
```

## Q11: How do you rename columns?
**A:** `df.rename(columns={'old_name': 'new_name'}, inplace=True)` or `df.columns = ['new1', 'new2']`. Add prefix/suffix: `df.add_prefix('pre_')`, `df.add_suffix('_suf')`. Replace parts: `df.columns = df.columns.str.replace('old', 'new')`. Use `inplace=True` to modify the original or assign to a new variable.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"old_name": [1, 2]})
print(df.rename(columns={"old_name": "new_name"}))
print(df.add_prefix("pre_").add_suffix("_suf"))
```

## Q12: How do you add and remove columns?
**A:** Add: `df['new_col'] = values`, `df.assign(new_col=values)`. Insert at position: `df.insert(loc, 'col', values)`. Remove: `df.drop('col', axis=1)`, `df.pop('col')` (returns column). Drop by index: `df.drop('col', axis=1, inplace=True)`. Multiple: `df.drop(['col1', 'col2'], axis=1)`.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"a": [1, 2]})
df["b"] = [3, 4]                       # add by assignment
df = df.assign(c=[5, 6])               # add via assign (returns new)
popped = df.pop("b")                   # remove and return column
print(popped, df, sep="\n")
print(df.drop("c", axis=1))
```

## Q13: How do you handle duplicate data in Pandas?
**A:** Detect: `df.duplicated()` (boolean Series, marks duplicates), `df.duplicated(subset=['col1'])` (check specific columns), `df.duplicated(keep='last')` (mark all but last). Remove: `df.drop_duplicates()`, `df.drop_duplicates(subset=['col1'], keep='first')`.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"col1": ["a", "a", "b"], "val": [1, 2, 3]})
print(df.duplicated())                    # [False, True, False]
print(df.duplicated(subset=["col1"]))     # per-subset dupes
print(df.drop_duplicates(subset=["col1"]))
```

## Q14: What is the difference between `apply`, `map`, and `applymap`?
**A:** `df['col'].map(func)` applies function element-wise on a Series (also used for value mapping: `map({'a': 1})`). `df['col'].apply(func)` applies function to each element of a Series (or each row/column of a DataFrame with `axis` parameter). `df.applymap(func)` applies function element-wise to entire DataFrame (deprecated, use `df.map()` in newer versions).

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
print(df["a"].map(lambda v: v * 10))       # series element-wise
print(df["a"].apply(lambda v: v + 1))      # series element-wise
print(df["b"].apply(lambda s: s.sum()))    # df axis=0 -> per column
print(df.map(lambda v: v * 2))             # DataFrame element-wise
```

## Q15: How do you group data with `groupby`?
**A:** `df.groupby('col')['value'].mean()` — split by column, apply function, combine results. Multiple groups: `df.groupby(['col1', 'col2'])`. Aggregate multiple functions: `df.groupby('cat').agg({'val1': 'mean', 'val2': 'sum'})`. Named aggs: `df.groupby('cat').agg(avg_val=('val', 'mean'))`. Access groups: `df.groupby('cat').groups`.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({
    "cat": ["x", "x", "y", "y"],
    "val1": [1, 3, 5, 7],
    "val2": [10, 20, 30, 40],
})
print(df.groupby("cat")["val1"].mean())
print(df.groupby("cat").agg({"val1": "mean", "val2": "sum"}))
print(df.groupby(["cat", "cat"]))
```

## Q16: What aggregation functions are available in groupby?
**A:** Common: `mean()`, `sum()`, `count()`, `size()` (including NaN), `min()`, `max()`, `std()`, `var()`, `median()`, `nunique()`, `first()`, `last()`. Multiple: `df.groupby('cat').agg(['mean', 'std', 'count'])`. Custom: `df.groupby('cat').agg(lambda x: x.max() - x.min())`.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"cat": ["a", "a", "b"], "val": [1, 3, 5]})
print(df.groupby("cat")["val"].agg(["mean", "std", "count"]))
print(df.groupby("cat")["val"].agg(lambda x: x.max() - x.min()))
```

## Q17: What is the difference between `agg` and `transform` in groupby?
**A:** `agg` returns a reduced result (one row per group). `transform` returns a result with the same shape as the original DataFrame (values broadcasted to each group's rows). Example: `df.groupby('cat')['val'].transform('mean')` adds a column with group means. Useful for creating percentage of group total or imputing group means.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"cat": ["a", "a", "b"], "val": [2, 4, 9]})
print(df.groupby("cat")["val"].agg("mean"))                    # 2 rows
df["group_mean"] = df.groupby("cat")["val"].transform("mean")  # same shape
print(df)
df["pct"] = df["val"] / df["group_mean"]
print(df)
```

## Q18: How do you merge DataFrames?
**A:** `pd.merge(df1, df2, on='key')` — SQL-like join. `how` parameter: 'inner', 'left', 'right', 'outer', 'cross'. Different keys: `left_on='key1', right_on='key2'`. Handle suffix: `suffixes=('_left', '_right')`. Index join: `left_index=True, right_index=True`. Multiple keys: `on=['key1', 'key2']`.

**Code:**
```python
import pandas as pd

df1 = pd.DataFrame({"key": [1, 2], "a": ["x", "y"]})
df2 = pd.DataFrame({"key": [2, 3], "b": ["p", "q"]})
print(pd.merge(df1, df2, on="key", how="inner"))
print(pd.merge(df1, df2, on="key", how="outer"))
print(pd.merge(df1, df2, on="key", how="left"))
```

## Q19: What is the difference between `merge` and `join`?
**A:** `merge` is the primary method for database-style joins on columns or indexes. `join` is a convenience method for joining on indexes (simpler but less flexible). `join` is equivalent to `merge(..., left_index=True, right_index=True)` by default. Use `merge` for column-based joins, `join` for index-based joins with simple syntax.

**Code:**
```python
import pandas as pd

left = pd.DataFrame({"k": [1, 2], "a": ["x", "y"]}).set_index("k")
right = pd.DataFrame({"k": [1, 3], "b": ["p", "q"]}).set_index("k")
print(left.join(right))                       # index-based join
print(pd.merge(left, right, left_index=True, right_index=True))  # equivalent
```

## Q20: How do you concatenate DataFrames?
**A:** `pd.concat([df1, df2])` — stacks vertically (default axis=0). `pd.concat([df1, df2], axis=1)` — side by side horizontally. `ignore_index=True` resets index. `keys=['t1', 't2']` creates hierarchical index. `join='inner'` / `join='outer'` handles column mismatch. `pd.concat` doesn't align on data — it aligns on axes.

**Code:**
```python
import pandas as pd

df1 = pd.DataFrame({"a": [1], "b": [2]})
df2 = pd.DataFrame({"a": [3], "b": [4]})
print(pd.concat([df1, df2], ignore_index=True))
print(pd.concat([df1, df2], axis=1))
print(pd.concat([df1, df2], keys=["t1", "t2"]))
```

## Q21: What is the difference between `concat` and `append`?
**A:** `pd.concat` is the recommended approach for combining DataFrames (vertical or horizontal). `df.append` is deprecated since Pandas 1.4.0, removed in 2.0. Always use `pd.concat`. `append` was a convenience method for vertical stacking but had inconsistent behavior.

**Code:**
```python
import pandas as pd

df1 = pd.DataFrame({"a": [1], "b": [2]})
df2 = pd.DataFrame({"a": [3], "b": [4]})
stacked = pd.concat([df1, df2], ignore_index=True)
print(stacked)
```

## Q22: How do you handle datetime data in Pandas?
**A:** Parse dates: `pd.to_datetime(col)`, `pd.read_csv(..., parse_dates=['col'])`. Extract components: `dt.year`, `dt.month`, `dt.day`, `dt.hour`, `dt.weekday`, `dt.quarter`. Date ranges: `pd.date_range('2024-01-01', periods=10, freq='D')`. Resampling: `df.resample('M').mean()` (monthly mean). Time deltas: `pd.Timedelta(days=5)`.

**Code:**
```python
import pandas as pd

s = pd.to_datetime(["2024-01-15", "2024-03-01"])
print(s.dt.year.tolist(), s.dt.month.tolist(), s.dt.quarter.tolist())
print(pd.date_range("2024-01-01", periods=3, freq="D"))
td = pd.Timedelta(days=5)
print(pd.Timestamp("2024-01-01") + td)
```

## Q23: What is the difference between `.loc` and `.iloc` for setting values?
**A:** Both can set values: `df.loc[rows, cols] = value` (by label) and `df.iloc[rows, cols] = value` (by position). The key difference is the access method. When setting with `.loc`, it uses label-based assignment, which can expand the DataFrame if labels don't exist. `.iloc` strictly uses integer positions.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"a": [1, 2], "b": [3, 4]}, index=["r1", "r2"])
df.loc["r1", "b"] = 99      # set by label
df.iloc[1, 0] = 88         # set by position
print(df)
df.loc["r3"] = [5, 6]      # .loc can expand with new labels
print(df)
```

## Q24: How do you apply a function to each row or column?
**A:** Use `df.apply(func, axis=1)` — applies to each row (axis=1) or each column (axis=0). For element-wise operations, use `df.map(func)` (for DataFrames) or `df['col'].map(func)`. For faster row iteration (avoid if possible), use `itertuples()` or `iterrows()`. Vectorized operations are preferred over `apply` for performance.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
print(df.apply(sum, axis=1))                    # row sums
print(df.apply(sum, axis=0))                    # column sums
print(df.map(lambda v: v * 10))                 # element-wise
```

## Q25: How do you sort DataFrames?
**A:** `df.sort_values('col', ascending=False)` — sort by column values. `df.sort_values(['col1', 'col2'], ascending=[True, False])` — multi-column sort. `df.sort_index()` — sort by index labels. `na_position='first'` or `'last'` controls NaN placement. Use `inplace=True` to modify the original.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"col1": [2, 1, 3], "col2": ["b", "a", "c"]})
print(df.sort_values("col1", ascending=False))
print(df.sort_values(["col1", "col2"], ascending=[True, False]))
print(df.sort_index(ascending=False))
```

## Q26: How do you reset or set the index?
**A:** `df.reset_index()` — reset to default integer index, old index becomes a column. `df.reset_index(drop=True)` — drop old index. `df.set_index('col')` — set column as index. `df.set_index(['col1', 'col2'])` — multi-index. `df.index.name = 'idx_name'` — name the index.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"id": [10, 20], "v": [1, 2]}).set_index("id")
print(df.reset_index())            # old index becomes a column
print(df.reset_index(drop=True))   # drop old index
print(df.set_index("v"))
```

## Q27: What is a MultiIndex (hierarchical index)?
**A:** A MultiIndex has multiple levels of indexing on rows (or columns). Created: `pd.MultiIndex.from_tuples([(1, 'a'), (1, 'b'), (2, 'a')])`. Access: `df.loc[1].loc['a']`, `df.xs(1, level=0)`. Useful for: grouped data, time series with categories, panel data, and pivot tables.

**Code:**
```python
import pandas as pd

idx = pd.MultiIndex.from_tuples([(1, "a"), (1, "b"), (2, "a")])
df = pd.DataFrame({"v": [10, 20, 30]}, index=idx)
print(df.loc[1])          # all rows where level-0 == 1
print(df.xs(1, level=0))  # same, by level
print(df.loc[(1, "b")])
```

## Q28: How do you pivot and unpivot DataFrames?
**A:** `df.pivot(index='row', columns='col', values='val')` — reshape from long to wide. `df.pivot_table(index='row', columns='col', values='val', aggfunc='mean')` — pivot with aggregation. `pd.melt(df, id_vars=['id'], value_vars=['a', 'b'])` — unpivot from wide to long (gather columns into rows).

**Code:**
```python
import pandas as pd

df = pd.DataFrame({
    "row": ["r1", "r1", "r2", "r2"],
    "col": ["a", "b", "a", "b"],
    "val": [1, 2, 3, 4],
})
print(df.pivot(index="row", columns="col", values="val"))
wide = pd.DataFrame({"id": [1, 2], "a": [5, 6], "b": [7, 8]})
print(pd.melt(wide, id_vars=["id"], value_vars=["a", "b"]))
```

## Q29: What is the difference between `pivot` and `pivot_table`?
**A:** `pivot` works with unique index/column combinations (no duplicate entries). If duplicates exist, it raises an error. `pivot_table` handles duplicates by applying an aggregation function (default `mean`), similar to a spreadsheet pivot table. Use `pivot` for simple reshaping, `pivot_table` when you need aggregation.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({
    "row": ["r1", "r1", "r2"],
    "col": ["a", "a", "b"],
    "val": [1, 5, 9],
})
print(df.pivot_table(index="row", columns="col", values="val", aggfunc="mean"))
try:  # dupes -> pivot raises
    print(df.pivot(index="row", columns="col", values="val"))
except ValueError as e:
    print("pivot error:", e)
```

## Q30: How do you apply SQL-like operations in Pandas?
**A:** SELECT: `df['col']` or `df.filter()`. WHERE: `df[condition]` or `df.query()`. GROUP BY: `df.groupby().agg()`. ORDER BY: `df.sort_values()`. JOIN: `pd.merge()`. UNION: `pd.concat()`. DISTINCT: `df['col'].unique()` or `df.drop_duplicates()`. LIMIT: `df.head(n)`. HAVING: `df.groupby().filter()`.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"c": ["a", "b", "a"], "v": [1, 2, 3]})
print(df[df["v"] > 1])                                 # WHERE
print(df.groupby("c")["v"].sum())                      # GROUP BY
print(df.sort_values("v", ascending=False).head(2))    # ORDER BY + LIMIT
print(df["c"].unique(), df["c"].drop_duplicates().tolist())  # DISTINCT
```

## Q31: What is the `query` method and when is it useful?
**A:** `df.query('col1 > 5 and col2 == "x"')` filters rows using a string expression. The syntax is cleaner than boolean indexing with `&`/`|`, supports `@variable` interpolation (`df.query('col > @threshold')`), and can be faster for large DataFrames. Supports `in`, `not in`, `==`, `!=`, `>`, `<`, `is null`, `is not null`.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"col1": [1, 6, 9], "col2": ["x", "x", "y"]})
threshold = 2
print(df.query('col1 > 5 and col2 == "x"'))
print(df.query("col1 > @threshold"))
print(df.query("col2 in ['x', 'y']"))
```

## Q32: How do you handle categorical data?
**A:** `pd.Categorical(values, categories=['a', 'b', 'c'], ordered=True)` — memory efficient (uses integer codes). Convert: `df['col'].astype('category')`. Benefits: smaller memory, faster groupby/sort, ordered categories support `<`/`>` comparisons, and unused category handling. Access codes: `df['col'].cat.codes`. Rename: `df['col'].cat.rename_categories(new_names)`.

**Code:**
```python
import pandas as pd

s = pd.Series(["a", "b", "a"]).astype("category").cat.set_categories(
    ["a", "b", "c"], ordered=True
)
print(s.cat.codes.tolist())
print(s < "b")
print(s.cat.rename_categories(["x", "y", "z"]).tolist())
```

## Q33: What is the difference between `str` accessor and regular string operations?
**A:** `df['col'].str.upper()` applies the operation to each string element in the Series. Without `.str`, you'd need a loop or `apply`. The `.str` accessor provides vectorized string operations: `str.contains()`, `str.replace()`, `str.extract()`, `str.split()`, `str.strip()`, `str.startswith()`, `str.len()`, `str.slice()`. Missing values propagate as NaN.

**Code:**
```python
import pandas as pd

s = pd.Series(["  hello  ", "world", None])
print(s.str.upper())
print(s.str.strip().str.len())
print(s.str.contains("o"))
print(s.str.replace("o", "0"))
```

## Q34: How do you handle text data with regex in Pandas?
**A:** `df['col'].str.contains('pattern', regex=True)` — boolean check. `df['col'].str.extract(r'(\d+)')` — capture groups as new column. `df['col'].str.replace('old', 'new', regex=True)` — replace patterns. `df['col'].str.split('\s+', expand=True)` — split into multiple columns. `df['col'].str.findall(r'\w+')` — find all matches.

**Code:**
```python
import pandas as pd

s = pd.Series(["order 42", "order 7", "none"])
print(s.str.contains(r"\d+"))
print(s.str.extract(r"(\d+)"))
print(s.str.replace(r"\d+", "N"))
print(s.str.split(r"\s+", expand=True))
```

## Q35: What is the `assign` method?
**A:** `df.assign(new_col=values)` creates a new DataFrame with added columns (doesn't modify original). Useful for method chaining: `df.assign(col2=df['col1'] * 2).query('col2 > 10')`. Can use callable: `df.assign(col2=lambda x: x['col1'] * 2)` where `x` is the DataFrame. Multiple columns: `df.assign(a=1, b=2)`.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"col1": [3, 8, 12]})
out = df.assign(col2=lambda x: x["col1"] * 2).query("col2 > 10")
print(out)
print(df.assign(a=1, b=2).head(1))
```

## Q36: How do you handle large DataFrames efficiently?
**A:** Strategies: `pd.read_csv(..., chunksize=10000)` for chunked reading, `dtype` parameter to specify types (saves memory), `usecols` to load only needed columns, `pd.read_csv(..., low_memory=False)` for mixed types. For huge data: use Dask, Vaex, PySpark, or database engines. Use categorical dtypes for low-cardinality string columns.

**Code:**
```python
import pandas as pd

# Read in chunks and pool results
dtype = {"id": "int32", "city": "category"}
chunks = [c for c in pd.read_csv("big.csv", chunksize=10000,
                                 usecols=["id", "city"], dtype=dtype)]
df = pd.concat(chunks)
print(df.shape)
```

## Q37: What are window functions in Pandas?
**A:** Window functions operate on a sliding window of rows. Rolling: `df['val'].rolling(window=7).mean()` — 7-period moving average. Expanding: `df['val'].expanding().mean()` — cumulative statistics. Exponentially weighted: `df['val'].ewm(span=10).mean()` — weighted average with more weight on recent observations.

**Code:**
```python
import pandas as pd

s = pd.Series([1, 2, 3, 4, 5, 6, 7, 8])
print(s.rolling(window=3).mean())
print(s.expanding().mean())
print(s.ewm(span=3).mean())
```

## Q38: What is the difference between `rolling` and `expanding` windows?
**A:** `rolling` has a fixed window size that slides across the data — each window contains a fixed number of observations. `expanding` starts from the first observation and grows to include all data up to the current point — cumulative statistics. Both support: `mean()`, `sum()`, `std()`, `min()`, `max()`, `apply(custom_func)`.

**Code:**
```python
import pandas as pd

s = pd.Series([1, 2, 3, 4, 5])
print(s.rolling(2).mean())     # fixed window of 2 -> NaN, 1.5, 2.5, ...
print(s.expanding().mean())    # grows -> 1, 1.5, 2, 2.5, 3
print(s.rolling(3).sum())
```

## Q39: How do you resample time series data?
**A:** `df.resample('M').mean()` — monthly mean. `df.resample('H').sum()` — hourly sum. `df.resample('Q').agg(['mean', 'sum'])` — quarterly aggregates. Custom: `df.resample('W').apply(custom_func)`. Asfreq: `df.asfreq('D')` — changes frequency without aggregation (fills NaN). Window resampling: `df.rolling('7D').mean()` — time-based rolling.

**Code:**
```python
import pandas as pd

idx = pd.date_range("2024-01-01", periods=60, freq="D")
df = pd.DataFrame({"v": range(60)}, index=idx)
print(df.resample("W").mean())
print(df.resample("M").agg(["mean", "sum"]))
print(df.asfreq("D").head(3))
```

## Q40: What is the difference between `resample` and `groupby`?
**A:** `resample` is time-based grouping — groups rows by time intervals (hourly, daily, monthly). `groupby` is value-based grouping — groups by column values. `resample` requires a DatetimeIndex. Conceptually, `resample` is temporal `groupby`. Both support `.agg()`, `.transform()`, and `.apply()`.

**Code:**
```python
import pandas as pd

idx = pd.date_range("2024-01-01", periods=5, freq="D")
df = pd.DataFrame({"cat": ["a", "b", "a", "b", "a"], "v": [1, 2, 3, 4, 5]},
                  index=idx)
print(df.resample("W").sum())          # time-based grouping
print(df.groupby("cat")["v"].sum())    # value-based grouping
```

## Q41: How do you handle time zones in Pandas?
**A:** Localize: `df['col'].dt.tz_localize('UTC')`. Convert: `df['col'].dt.tz_convert('US/Eastern')`. Create timezone-aware: `pd.Timestamp('2024-01-01', tz='UTC')`. Remove timezone: `df['col'].dt.tz_localize(None)`. Use `tz` parameter in `date_range()` and `read_csv()`.

**Code:**
```python
import pandas as pd

ts = pd.Series(pd.to_datetime(["2024-01-01 10:00"]))
utc = ts.dt.tz_localize("UTC")
print(utc)
print(utc.dt.tz_convert("US/Eastern"))
print(utc.dt.tz_localize(None))
```

## Q42: What is the difference between `value_counts` and `groupby` + `size`?
**A:** `df['col'].value_counts()` returns frequency counts sorted by descending count. `df.groupby('col').size()` returns counts by group in the order of unique values. `value_counts` provides: `normalize=True` (proportions), `dropna=False` (include NaN), `sort=True/False`, `bins` (for numeric data). `groupby.size` is more flexible for multi-column grouping.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"col": ["b", "a", "b", "a", "b"]})
print(df["col"].value_counts())                 # sorted by count desc
print(df["col"].value_counts(normalize=True))   # proportions
print(df.groupby("col").size())                 # order of unique values
print(df.groupby("col").size(normalize=True))
```

## Q43: How do you create dummy/indicator variables?
**A:** `pd.get_dummies(df['col'], prefix='col')` — converts categorical column to one-hot encoded columns. Parameters: `drop_first=True` (avoid multicollinearity), `dtype=int` (boolean or int), `columns=['col1', 'col2']` for multiple columns. Alternative: `sklearn.preprocessing.OneHotEncoder` for consistent encoding across train/test.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"col": ["a", "b", "a"], "v": [1, 2, 3]})
print(pd.get_dummies(df["col"], prefix="col", dtype=int))
print(pd.get_dummies(df["col"], prefix="col", drop_first=True, dtype=int))
print(pd.get_dummies(df, columns=["col"], dtype=int))
```

## Q44: What is the difference between `cut` and `qcut`?
**A:** `pd.cut(values, bins=5)` divides into intervals of equal width (bins specified by value ranges). `pd.qcut(values, q=5)` divides into quantiles (each bin has approximately equal number of observations). `cut` for fixed ranges (e.g., age groups 0-18, 18-35), `qcut` for even frequency distribution (e.g., quartiles).

**Code:**
```python
import pandas as pd

ages = [10, 18, 30, 50, 80]
print(pd.cut(ages, bins=[0, 18, 35, 60, 120]).tolist())   # equal-width ranges
print(pd.qcut(ages, q=4).tolist())                        # equal counts
```

## Q45: How do you handle outliers in Pandas?
**A:** Detect: IQR method — `Q1 = df['col'].quantile(0.25); Q3 = df['col'].quantile(0.75); IQR = Q3 - Q1; outliers = df[(df['col'] < Q1 - 1.5*IQR) | (df['col'] > Q3 + 1.5*IQR)]`. Z-score method: `np.abs(zscore(df['col'])) > 3`. Handle: remove, cap/winsorize (clip to percentiles), or transform (log, Box-Cox).

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"col": [1, 2, 3, 4, 5, 100]})
q1, q3 = df["col"].quantile(0.25), df["col"].quantile(0.75)
iqr = q3 - q1
outliers = df[(df["col"] < q1 - 1.5 * iqr) | (df["col"] > q3 + 1.5 * iqr)]
print(outliers)                                  # 100 flagged
df["col_clipped"] = df["col"].clip(q1, q3)       # winsorize
print(df["col_clipped"].tolist())
```

## Q46: What is the difference between `DataFrame.apply()` and `DataFrame.transform()`?
**A:** `apply` can return any shape (reduced, expanded, or same shape). `transform` must return the same shape as the input (same number of rows). `transform` is more restrictive but guarantees consistent output. Use `apply` for arbitrary operations, `transform` for broadcasting results back to original shape (like group-level statistics).

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
print(df.apply(lambda c: c.max() - c.min()))             # reduced shape ok
print(df.transform(lambda c: c - c.min()))               # same shape only
```

## Q47: How do you create a correlation matrix?
**A:** `df.corr()` — Pearson correlation between numeric columns. `df.corr(method='spearman')` — Spearman rank correlation. `df.corr(method='kendall')` — Kendall Tau. Visualize with `sns.heatmap(df.corr(), annot=True)` or `df.corr().style.background_gradient()`. Include only numeric columns: `df.select_dtypes(include='number').corr()`.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({
    "a": [1, 2, 3, 4],
    "b": [2, 4, 6, 8],
    "c": [9, 1, 4, 2],
})
print(df.select_dtypes(include="number").corr())
print(df.corr(method="spearman"))
```

## Q48: How do you calculate rolling correlations?
**A:** `df['col1'].rolling(30).corr(df['col2'])` — rolling 30-period correlation. For pairwise rolling correlations across DataFrame: `df.rolling(30).corr(df)` returns multi-index DataFrame. Can be used for: time-varying relationships, dynamic portfolio analysis, and regime detection.

**Code:**
```python
import pandas as pd

x = pd.Series(range(10))
y = pd.Series([v + v % 2 for v in range(10)])
print(x.rolling(3).corr(y).round(2))
df = pd.DataFrame({"x": x, "y": y})
print(df.rolling(3).corr(df).round(2))
```

## Q49: What are the common I/O operations in Pandas?
**A:** CSV: `pd.read_csv()`, `df.to_csv()`. Excel: `pd.read_excel()`, `df.to_excel()`. JSON: `pd.read_json()`, `df.to_json()`. SQL: `pd.read_sql()`, `df.to_sql()`. HTML: `pd.read_html()` (reads all tables). Parquet: `pd.read_parquet()`, `df.to_parquet()` (fast, compressed). Pickle: `pd.read_pickle()`, `df.to_pickle()`. Clipboard: `pd.read_clipboard()`.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
df.to_csv("/tmp/df.csv", index=False)
df.to_json("/tmp/df.json")
print(pd.read_csv("/tmp/df.csv"))
print(pd.read_json("/tmp/df.json"))
```

## Q50: What is the difference between `read_csv` default parameters and when to change them?
**A:** Key parameters: `sep=','` (delimiter), `header=0` (row for column names), `index_col=None` (column to use as index), `usecols=None` (columns to read), `dtype=None` (explicit types), `parse_dates=False`, `na_values=None` (additional NaN markers), `skiprows=0`, `nrows=None` (read only N rows), `chunksize=None` (iterator). Adjust for non-standard formats.

**Code:**
```python
import pandas as pd

df = pd.read_csv("data.tsv", sep="\t", index_col=0, parse_dates=["date"],
                 na_values=["NULL", ""], usecols=["id", "date", "amt"],
                 dtype={"id": "int32"})
print(df.head())
```

## Q51: How do you read a CSV with no header?
**A:** `pd.read_csv('file.csv', header=None)` — assigns integer column names (0, 1, 2...). Then set names: `df.columns = ['a', 'b', 'c']`. Or use `names=['a', 'b', 'c']` parameter in `read_csv()` directly. For skipping a header row: `skiprows=1`.

**Code:**
```python
import pandas as pd

print(pd.read_csv("no_header.csv", header=None))
df = pd.read_csv("no_header.csv", header=None, names=["a", "b", "c"])
print(df[["a", "b"]])
print(pd.read_csv("with_header.csv", skiprows=1, header=None))
```

## Q52: What is the `memory_usage` method?
**A:** `df.memory_usage(deep=True)` returns memory consumption per column in bytes. Useful for optimizing memory: convert object to category, downcast numeric types (`pd.to_numeric(..., downcast='integer')`), and use `df.info(memory_usage='deep')`. Deep=True includes Python object overhead for string columns.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"id": [1, 2, 3], "name": ["alice", "bob", "carol"]})
print(df.memory_usage())
print(df.memory_usage(deep=True))
df["id"] = pd.to_numeric(df["id"], downcast="integer")
print(df.memory_usage(deep=True))
```

## Q53: How do you chain operations in Pandas?
**A:** Method chaining: `df.sort_values('col').query('val > 5').groupby('cat').agg({'val': 'mean'}).reset_index()`. `pipe()` for custom functions: `df.pipe(custom_func, arg=1)`. `assign()` and `query()` are chain-friendly. Benefits: readable pipeline, avoids intermediate variables, follows functional programming style.

**Code:**
```python
import pandas as pd

def tag_small(df, thresh):
    return df.assign(flag=df["val"] < thresh)

df = pd.DataFrame({"cat": ["a", "b", "a", "b"], "val": [9, 3, 7, 1]})
result = (df.sort_values("val")
            .query("val > 5")
            .pipe(tag_small, thresh=8)
            .reset_index(drop=True))
print(result)
```

## Q54: What is the difference between `Series` and 1D NumPy array?
**A:** Series has: index (labels), name, richer methods (`value_counts`, `str` accessor, `dt` accessor, `map`, `.isna().sum()`), alignment on operations (matches by index labels), and integration with DataFrame operations. NumPy arrays are faster for pure numerical operations but lack labeling and convenient data analysis methods.

**Code:**
```python
import numpy as np
import pandas as pd

arr = np.array([10, 20, 30, 40])
s = pd.Series([10, 20, 30, 40], index=["a", "b", "c", "d"], name="vals")
print(s * 2)                    # labeled, like NumPy vectorized ops
print(s + pd.Series([1, 1, 1, 1], index=["a", "b", "c", "d"]))  # aligns by label
print(s.value_counts(), s.isna().sum())
```

## Q55: How do you handle large text data efficiently?
**A:** Use `df['col'].astype('string')` (StringDtype) instead of object dtype — more consistent NA handling, memory efficiency for some cases. For very large text: use categorical for repeated strings, store in Parquet format, use `pyarrow` backend (`pd.set_option('mode.string_storage', 'pyarrow')`), or use Dask for out-of-core processing.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"col": ["foo", "bar"] * 100})
df["col"] = df["col"].astype("string")          # StringDtype
print(df.dtypes)
low_card = df["col"].astype("category")         # repeated strings -> category
print(low_card.dtype, low_card.memory_usage(deep=True))
```

## Q56: What is the difference between `inplace=True` and reassignment?
**A:** `inplace=True` modifies the original object without creating a copy (some methods support this — `dropna`, `fillna`, `sort_values`, `rename`, `drop`). Reassignment (`df = df.method()`) creates a new object. `inplace` is controversial — it's not consistently supported, can't be chained, and is slightly faster but encourages mutable state. Many experts recommend reassignment for clarity.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"a": [1, None, 3]})
df.fillna(0, inplace=True)     # mutates original, returns None
print(df)

df2 = pd.DataFrame({"a": [1, None, 3]})
df2 = df2.fillna(0)            # reassignment creates new object
print(df2)
```

## Q57: How do you create a pivot table?
**A:** `pd.pivot_table(df, values='sales', index='region', columns='product', aggfunc='sum', fill_value=0, margins=True)`. Index: row groups. Columns: column groups. Values: aggregated metric. Aggfunc: aggregation function(s). Margins=True adds row/column totals. Multiple values/index/columns are supported.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({
    "region": ["N", "N", "S", "S"],
    "product": ["A", "B", "A", "B"],
    "sales": [100, 200, 150, 50],
})
table = pd.pivot_table(df, values="sales", index="region",
                       columns="product", aggfunc="sum",
                       fill_value=0, margins=True)
print(table)
```

## Q58: What is the difference between `stack` and `unstack`?
**A:** `stack` pivots columns into rows (rotates from wide to long format). `unstack` pivots rows into columns (rotates from long to wide format). They are inverse operations. Operate on MultiIndex DataFrames. `level` parameter controls which level(s) to pivot. Useful for reshaping between different tabular formats.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({
    "A": [1, 2], "B": [3, 4],
}, index=pd.MultiIndex.from_tuples([("x", "i"), ("x", "ii")]))
stacked = df.stack()       # wide -> long
print(stacked)
unstacked = stacked.unstack()  # long -> wide (inverse)
print(unstacked)
```

## Q59: How do you handle JSON data in Pandas?
**A:** `pd.read_json('file.json')` for basic JSON. `pd.json_normalize(data)` for nested JSON (flattens dicts and lists into columns). Parameters: `record_path` (path to nested records), `meta` (other fields to include), `sep` (nested field separator, default '.'). For deeply nested JSON, use `json_normalize` iteratively or with `record_path` and `meta`.

**Code:**
```python
import pandas as pd

data = [{"id": 1, "info": {"city": "NYC"}, "orders": [{"amount": 10}]},
        {"id": 2, "info": {"city": "SF"}, "orders": [{"amount": 20}]}]
print(pd.json_normalize(data, record_path="orders", meta=["id", ["info", "city"]]))
```

## Q60: What is the `eval` method in Pandas?
**A:** `df.eval('new_col = col1 + col2')` evaluates a string expression for column operations. Faster than Python evaluation for large DataFrames (uses numexpr). Can also filter: `df.query('col1 > 0')`. Use for: arithmetic expressions, boolean conditions, and assignments. Supports `@` for Python variables: `df.eval('col > @threshold')`.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"col1": [1, 2], "col2": [10, 20]})
df.eval("new_col = col1 + col2", inplace=True)
print(df)

threshold = 5
print(df.query("new_col > @threshold"))   # filter, @ for Python vars
```

## Q61: What is the difference between `iterrows()` and `itertuples()`?
**A:** `iterrows()` iterates returning (index, Series) per row — convenient but slow (creates a Series each time and breaks dtype). `itertuples()` returns namedtuples — much faster and preserves dtypes. Avoid both when possible; prefer vectorized operations. If iteration is unavoidable, `itertuples()` is strongly recommended.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"a": [1, 2], "b": [3.5, 4.5]})
for idx, row in df.iterrows():       # row is a Series
    print(idx, row["a"] * row["b"])
for row in df.itertuples():          # namedtuple, faster, keeps dtypes
    print(row.a + row.b)
```

## Q62: How do you use `pd.cut` and `pd.qcut` with real data?
**A:** `df['age_group'] = pd.cut(df['age'], bins=[0, 18, 35, 60, 120], labels=['Child', 'Young', 'Adult', 'Senior'])` — category assignment. `df['income_quartile'] = pd.qcut(df['income'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])` — equally populated groups. Returns Categorical Series that can be used in groupby.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"age": [10, 25, 40, 70], "income": [20, 80, 50, 120]})
df["age_group"] = pd.cut(df["age"], bins=[0, 18, 35, 60, 120],
                         labels=["Child", "Young", "Adult", "Senior"])
df["income_quartile"] = pd.qcut(df["income"], q=4,
                                labels=["Q1", "Q2", "Q3", "Q4"])
print(df)
print(df.groupby("age_group", observed=False)["income"].mean())
```

## Q63: What is the difference between `pd.merge` and SQL JOINs?
**A:** `pd.merge` supports all SQL JOIN types (inner, left, right, outer, cross). Differences: 1) Pandas merges on index or columns, 2) Supports multiple keys, 3) No support for ON clause conditions beyond equality, 4) Doesn't support non-equi joins (use `df.query()` after cross join), 5) More flexible with overlapping column names via suffixes.

**Code:**
```python
import pandas as pd

emp = pd.DataFrame({"dept": ["a", "a", "b"], "name": ["x", "y", "z"]})
dept = pd.DataFrame({"dept": ["a", "b", "c"], "floor": [1, 2, 3]})
inner = pd.merge(emp, dept, on="dept", how="inner")     # SQL INNER JOIN
print(inner)
cross = emp.assign(k=1).merge(dept.assign(k=1), on="k")  # cross join
print(cross.drop(columns="k"))
```

## Q64: How do you handle `SettingWithCopyWarning`?
**A:** Occurs when modifying a slice of a DataFrame (which might be a view or copy). Fix: 1) Use `.loc` to set values: `df.loc[condition, 'col'] = value`, 2) Explicit copy: `df_slice = df[condition].copy()`, 3) Use `chained_assignment` option: `pd.set_option('mode.chained_assignment', None)` (not recommended — better to fix the code).

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"a": [1, 2, 3], "b": [0, 0, 0]})

# BAD: chained assignment triggers SettingWithCopyWarning
# df[df["a"] > 1]["b"] = 5

# GOOD: set via .loc on the original
df.loc[df["a"] > 1, "b"] = 5
# or modify an explicit copy
sub = df[df["a"] > 1].copy()
sub["b"] = 7
print(df, sub, sep="\n")
```

## Q65: What are the best practices for Pandas performance?
**A:** 1) Use vectorized operations instead of `apply`/loops, 2) Specify `dtypes` when reading data, 3) Use `category` dtype for low-cardinality strings, 4) Filter early (reduce data before expensive ops), 5) Use `inplace=False` (reassign), 6) Use `.values` or `.to_numpy()` for pure NumPy operations, 7) Use `pd.concat` instead of `df.append`, 8) Avoid `iterrows()` — use `itertuples()` if iteration is necessary.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"cat": ["a", "b"] * 50, "v": range(100)})
df["cat"] = df["cat"].astype("category")          # low-cardinality string
df = df.query("v > 10")                           # filter early
feature = df["v"] / df["v"].max()                 # vectorized, no loop
print(feature.head())
```

## Q66: How do you handle memory errors with large datasets?
**A:** 1) Read in chunks: `pd.read_csv(..., chunksize=50000)`, 2) Downcast numeric types: `pd.to_numeric(col, downcast='integer')`, 3) Use `usecols` to load only needed columns, 4) Use `category` dtype, 5) Filter rows during read: `pd.read_csv(..., skiprows=lambda i: i not in rows_to_keep)`, 6) Use PySpark, Dask, or Vaex for truly large data, 7) Store in efficient format (Parquet, Feather).

**Code:**
```python
import pandas as pd

parts = []
for chunk in pd.read_csv("big.csv", chunksize=50000,
                         usecols=["id", "cat"], dtype={"id": "int32"}):
    chunk["cat"] = chunk["cat"].astype("category")
    parts.append(chunk)
df = pd.concat(parts, ignore_index=True)
print(df.dtypes)
```

## Q67: What is the difference between `.values` and `.to_numpy()`?
**A:** Both return the underlying data as a NumPy array. `.values` is the older property (may surprise with mixed dtypes by returning object arrays). `.to_numpy()` is the recommended method — it accepts `dtype` and `copy` parameters and is consistent. Prefer `.to_numpy()` for clarity and control.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"a": [1, 2], "b": [3.5, 4.5]})
print(df.values)                      # legacy property
print(df.to_numpy())                 # recommended
print(df.to_numpy(dtype="float64"))  # with explicit dtype
print(df.to_numpy(copy=True))
```

## Q68: What is the difference between `copy(deep=True)` and `copy(deep=False)`?
**A:** `df.copy(deep=True)` (default) copies both the data and the index/columns. `df.copy(deep=False)` is a shallow copy — a new DataFrame object sharing the same underlying data buffers (modifying data may affect the original). Use deep copies when you need full independence; shallow copies save memory when only metadata changes.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"a": [1, 2]})
deep = df.copy(deep=True)
deep.iloc[0, 0] = 99
print(df.iloc[0, 0])                 # unchanged -> 1

shallow = df.copy(deep=False)
shallow.iloc[0, 0] = 42               # may affect df (shared buffer)
print(df.iloc[0, 0])
```

## Q69: How do you use `df.replace`?
**A:** `df.replace({'old': 'new'})` maps values, `df.replace([1, 2], [10, 20])` maps lists positionally, `df.replace(regex={'pat': 'repl'})` uses regex. Unlike `map`, `replace` works on the whole DataFrame and preserves the structure. Use `inplace=True` or reassign. Great for cleaning categorical typos.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"x": ["nyc", "SFO", "nyc"], "v": [1, 2, 1]})
print(df.replace({"nyc": "NYC", "SFO": "SF"}))
print(df.replace([1, 2], [10, 20]))
print(df.replace(regex={"y$": "Y"}))
```

## Q70: What is the difference between `df.where` and `df.mask`?
**A:** `df.where(cond, other)` keeps values where `cond` is True and replaces False positions with `other` (default NaN). `df.mask(cond, other)` is the inverse — replaces where `cond` is True. Both are vectorized conditionals that keep the original shape, useful alternatives to `np.where` on DataFrames.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"a": [1, 2, 3]})
print(df.where(df["a"] > 1, -1))    # keep True, else -1
print(df.mask(df["a"] > 1, -1))     # inverse: replace True with -1
```

## Q71: How do you use `df.clip`?
**A:** `df.clip(lower=0, upper=100)` caps all values to the range [0, 100] — values below lower become lower, above upper become upper. Works column-wise and along axes. Handy for winsorizing outliers and bounding features without manual masking.

**Code:**
```python
import pandas as pd

s = pd.Series([-5, 10, 150])
print(s.clip(lower=0, upper=100).tolist())          # [0, 10, 100]
df = pd.DataFrame({"a": [1, 200], "b": [-3, 300]})
print(df.clip(lower=0, upper=100))                  # per column
```

## Q72: What is the difference between `df.diff` and `df.shift`?
**A:** `df.shift(periods=1)` moves values up/down by N positions, leaving NaN where data is unavailable (no computation). `df.diff(periods=1)` computes the difference between current and shifted values (`x - x.shift(1)`). `shift` preserves values; `diff` computes period-over-period change. Related: `df.pct_change()` gives percentage change.

**Code:**
```python
import pandas as pd

s = pd.Series([10, 15, 21])
print(s.shift(1).tolist())     # [NaN, 10, 15]
print(s.diff(1).tolist())      # [NaN, 5, 6]
print(s.pct_change().tolist()) # [NaN, 0.5, 0.4]
```

## Q73: How do you compute cumulative operations?
**A:** `df.cumsum()`, `df.cummax()`, `df.cummin()`, `df.cumprod()` compute running totals/extrema/products down each column. Useful for running balances, cumulative revenue, and ranking. Combined with `groupby().cumsum()` you get per-group cumulative sums.

**Code:**
```python
import pandas as pd

s = pd.Series([1, 2, 3, 4])
print(s.cumsum().tolist())
print(s.cummax().tolist(), s.cumprod().tolist())
df = pd.DataFrame({"cat": ["a", "a", "b", "b"], "v": [1, 2, 3, 4]})
df["cum"] = df.groupby("cat")["v"].cumsum()
print(df)
```

## Q74: What is the difference between `nlargest`/`nsmallest` and `sort_values`?
**A:** `df.nlargest(n, 'col')` / `df.nsmallest(n, 'col')` return the top/bottom n rows by a column efficiently (uses partial sort, faster than full `sort_values`). `sort_values().head(n)` gives the same result but sorts everything. Use `nlargest`/`nsmallest` for quick top-k extraction.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"v": [5, 1, 9, 3]})
print(df.nlargest(2, "v"))
print(df.nsmallest(2, "v"))
print(df.sort_values("v", ascending=False).head(2))  # equivalent, full sort
```

## Q75: What is `df.crosstab`?
**A:** `pd.crosstab(index=df['a'], columns=df['b'])` computes a frequency contingency table (counts) of two or more factors. Supports `aggfunc`, `margins=True`, `normalize=True` (row/col/total proportions). Conceptually similar to `pivot_table` with a count aggregation but optimized for categorical cross-tabulation.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"a": ["x", "x", "y", "y"], "b": ["p", "q", "p", "p"]})
print(pd.crosstab(index=df["a"], columns=df["b"], margins=True))
print(pd.crosstab(index=df["a"], columns=df["b"], normalize="index"))
```

## Q76: What is `df.melt` used for?
**A:** `pd.melt(df, id_vars=['id'], value_vars=['a','b'], var_name='metric', value_name='value')` unpivots wide data into long format — turning columns into rows. Inverse of `pivot`/`pivot_table`. Essential for tidy data preparation before plotting (e.g., with `seaborn`) and time-series reshaping.

**Code:**
```python
import pandas as pd

wide = pd.DataFrame({"id": [1, 2], "a": [5, 6], "b": [7, 8]})
long = pd.melt(wide, id_vars=["id"], value_vars=["a", "b"],
               var_name="metric", value_name="value")
print(long)
print(long.pivot(index="id", columns="metric", values="value"))  # inverse
```

## Q77: How do you use `groupby` with `filter`?
**A:** `df.groupby('cat').filter(lambda g: len(g) > 5)` keeps only groups satisfying a condition (returns a DataFrame with the same columns). Unlike `agg`/`transform`, `filter` returns original rows, not aggregates. Useful for removing small groups or selecting groups by a computed property.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"cat": ["a"] * 6 + ["b"] * 2, "v": range(8)})
print(df.groupby("cat").filter(lambda g: len(g) > 3))
print(df.groupby("cat").filter(lambda g: g["v"].mean() > 2))
```

## Q78: What is the difference between `groupby` and `resample` for time series?
**A:** `groupby` groups by arbitrary column values (including time buckets you compute manually). `resample` groups by fixed calendar/clock frequencies ('D', 'M', 'H') on a DatetimeIndex — it's essentially a time-aware groupby. `resample` is more convenient for evenly spaced temporal aggregation and supports `.rolling` after.

**Code:**
```python
import pandas as pd

idx = pd.date_range("2024-01-01", periods=6, freq="D")
df = pd.DataFrame({"v": [1, 2, 3, 4, 5, 6]}, index=idx)
print(df.resample("W").sum())                        # calendar buckets
df["cat"] = ["a", "a", "b", "b", "a", "b"]
print(df.groupby(pd.Grouper(freq="W"))["v"].sum())    # same via Grouper
```

## Q79: How do you use `df.pipe`?
**A:** `df.pipe(func, *args, **kwargs)` applies a function to the DataFrame as its first argument, enabling clean method chaining with functions that aren't DataFrame methods. Example: `df.pipe(clean_data, drop_cols=['x']).pipe(add_features)`. Reads left-to-right and composes reusable transforms.

**Code:**
```python
import pandas as pd

def add_feature(df, col="a"):
    return df.assign(a2=lambda d: d[col] * 2)

def drop_small(df, thresh=5):
    return df.query("a > @thresh")

df = pd.DataFrame({"a": [1, 6, 8]})
out = (df.pipe(add_feature).pipe(drop_small, thresh=5))
print(out)
```

## Q80: What is `df.explode`?
**A:** `df.explode('col')` transforms each list-like element in a column into a separate row, replicating the other column values. Useful for normalizing JSON/list columns into one-element-per-row form. Inverse of an aggregation that produced lists.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"id": [1, 2], "tags": [["a", "b"], ["c"]]})
print(df.explode("tags").reset_index(drop=True))
```

## Q81: What is the difference between `df.combine_first` and `df.update`?
**A:** `df.combine_first(other)` fills missing values in `df` with values from `other` (returns a new DataFrame, non-destructive). `df.update(other)` modifies `df` in place, overwriting existing values (not just NaN) with `other`'s values where indexes align. Use `combine_first` for safe fill; `update` for overwrite.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"a": [1, None], "b": [3, 4]})
other = pd.DataFrame({"a": [99, 100]})
print(df.combine_first(other))          # fills NaN from other, returns new
df2 = pd.DataFrame({"a": [1, None], "b": [3, 4]})
df2.update(pd.DataFrame({"a": [99, 100]}))  # mutates in place, overwrites
print(df2)
```

## Q82: How do you use `df.reindex`?
**A:** `df.reindex(new_index)` conforms the DataFrame to a new index, introducing NaN for missing labels and dropping unmatched ones. Supports `columns=` to reindex columns, `method='ffill'/'bfill'` to fill, and `fill_value`. Useful for aligning two datasets to a common axis before operations.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"v": [1, 2]}, index=["a", "b"])
print(df.reindex(["a", "b", "c"]))                    # c -> NaN
print(df.reindex(["a", "b", "c"], method="ffill"))    # forward fill
print(df.reindex(columns=["v", "w"]))                 # w -> NaN
```

## Q83: What is the difference between `df.align` and `df.reindex`?
**A:** `df.align(other, join='outer')` returns a tuple of both objects reindexed to a common index/columns (non-destructive, aligns both). `reindex` changes only the calling object to a specified index. `align` is convenient when you need both frames on the same axes for arithmetic.

**Code:**
```python
import pandas as pd

a = pd.DataFrame({"v": [1, 2]}, index=["x", "y"])
b = pd.DataFrame({"v": [10, 20]}, index=["y", "z"])
a2, b2 = a.align(b, join="outer")
print(a2, b2, sep="\n")          # both share index x, y, z
print(a.reindex(b.index))        # only reindexes a to b's index
```

## Q84: How do you handle mixed dtypes with `convert_dtypes`?
**A:** `df.convert_dtypes()` infers and converts columns to the best nullable dtype (e.g., `Int64`, `string`, `boolean`, `Float64`) that supports `<NA>` instead of object/NaN. This gives proper type support for missing values and is recommended after reading messy CSV/JSON data.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({
    "a": [1, None, 3],
    "b": [True, None, False],
    "c": ["x", "y", None],
})
print(df.convert_dtypes().dtypes)
```

## Q85: What is the difference between `astype('category')` and `astype('string')`?
**A:** `astype('category')` converts to a Categorical storing integer codes + a category list — best for low-cardinality repetitive string columns (memory + speed). `astype('string')` converts to the new `StringDtype` for proper NA-aware string handling — best for free-text or high-cardinality columns. Choose based on cardinality.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"s": ["a", "b"] * 10})
df["cat"] = df["s"].astype("category")
df["str"] = df["s"].astype("string")
print(df.dtypes)
print(df["cat"].memory_usage(deep=True), df["str"].memory_usage(deep=True))
```

## Q86: How do you use `df.style`?
**A:** `df.style` returns a Styler for conditional formatting in Jupyter: `df.style.background_gradient(cmap='coolwarm')`, `.highlight_max()`, `.format('{:.2f}')`, `.bar()`. Output is HTML/CSS for notebooks and can be exported via `df.to_html()` or `df.style.to_excel()`. Not for data transformation — presentation only.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"a": [1.234, 2.5], "b": [3.0, 0.5]})
styled = (df.style.background_gradient(cmap="coolwarm")
            .highlight_max(color="yellow")
            .format("{:.2f}"))
html = styled.to_html()
print("style obj:", styled, "| rendered chars:", len(html))
```

## Q87: How do you plot directly from a DataFrame?
**A:** `df.plot()` (uses matplotlib) produces line plots; `df.plot.bar()`, `.hist()`, `.box()`, `.scatter(x, y)`, `.area()` for others. `df.plot(kind='...')` selects the type. Requires matplotlib installed. For interactive plots prefer Plotly/`df.plot()` with the Plotly backend. Great for quick EDA.

**Code:**
```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({"x": [1, 2, 3], "y": [3, 1, 4]})
ax = df.plot.line(x="x", y="y", title="Trend")
df[["x", "y"]].plot.bar()
plt.close("all")   # close figures in scripted context
```

## Q88: What is the difference between `df.to_csv` parameters `index` and `header`?
**A:** `index=False` avoids writing the row index to the file (set True to keep it). `header=False` avoids writing column names. Other useful params: `sep`, `encoding='utf-8'`, `na_rep='NaN'`, `compression='gzip'`, `quoting`, `float_format`. Always set `index=False` when the index isn't meaningful to avoid extra columns on reload.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]}, index=["i1", "i2"])
df.to_csv("/tmp/out.csv", index=False, header=True, sep=",")
df.to_csv("/tmp/out_no_header.csv", header=False, index=False)
print(open("/tmp/out.csv").read())
print(open("/tmp/out_no_header.csv").read())
```

## Q89: How do you write to Parquet and why?
**A:** `df.to_parquet('file.parquet')` and `pd.read_parquet('file.parquet')` use the columnar Parquet format — fast, compressed, and preserving dtypes (including categorical and datetime) far better than CSV. Requires `pyarrow` or `fastparquet`. Preferred for large datasets and ML pipelines.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({
    "a": [1, 2],
    "dt": pd.to_datetime(["2024-01-01", "2024-01-02"]),
    "c": pd.Categorical(["x", "y"]),
})
df.to_parquet("/tmp/data.parquet")
back = pd.read_parquet("/tmp/data.parquet")
print(back, back.dtypes, sep="\n")
```

## Q90: What is `pd.to_datetime` and parsing pitfalls?
**A:** `pd.to_datetime(series)` converts to datetime; `errors='coerce'` turns unparseable values into NaT. Pitfalls: ambiguous day-first formats — set `format='%d/%m/%Y'` or `dayfirst=True`. For mixed formats use `format='mixed'`. UTC: pass `utc=True` to return timezone-aware UTC. `infer_datetime_format` was removed in 2.0 — always specify `format` for speed.

**Code:**
```python
import pandas as pd

print(pd.to_datetime(["01/02/2024"], dayfirst=True))       # Feb 1
print(pd.to_datetime(["garbage"], errors="coerce"))        # NaT
print(pd.to_datetime(["2024-01-01"], utc=True))            # tz-aware
print(pd.to_datetime(["01/02/2024", "2024-03-01"], format="mixed", dayfirst=True))
```

## Q91: How do you extract components from datetime columns?
**A:** Via the `.dt` accessor: `dt.year`, `dt.month`, `dt.day`, `dt.hour`, `dt.minute`, `dt.second`, `dt.dayofweek`/`dt.weekday`, `dt.dayofyear`, `dt.quarter`, `dt.is_leap_year`, `dt.days_in_month`, `dt.day_name()`, `dt.month_name()`, `dt.date`, `dt.time`, `dt.floor('D')`. All vectorized on datetime Series.

**Code:**
```python
import pandas as pd

s = pd.to_datetime(["2024-02-29 14:30"])
print(s.dt.year.tolist(), s.dt.month.tolist(), s.dt.day.tolist())
print(s.dt.quarter.tolist(), s.dt.dayofyear.tolist())
print(s.dt.day_name().tolist(), s.dt.is_leap_year.tolist())
```

## Q92: What is the difference between `df.fillna` with method and `interpolate`?
**A:** `fillna(method='ffill')` copies the last valid value forward (or `bfill` backward) — flat steps. `df.interpolate()` estimates missing values by linear (or other) interpolation between neighbors — smoother and more realistic for numeric/time series. Use `interpolate` for trends; `ffill/bfill` for categorical/status data.

**Code:**
```python
import pandas as pd

s = pd.Series([1.0, None, None, 4.0])
print(s.ffill().tolist())          # [1, 1, 1, 4]
print(s.interpolate().tolist())    # [1, 2, 3, 4]
print(s.interpolate(method="quadratic").round(2).tolist())
```

## Q93: How do you use `df.groupby` with multiple aggregation levels (`NamedAgg`)?
**A:** `df.groupby('cat').agg(avg=('val', 'mean'), total=('val', 'sum'), n=('val', 'size'))` produces columns named `avg`, `total`, `n` via `NamedAgg`. Cleaner than passing a dict of lists and easier to read. Supports any valid aggregation string or callable. Available since Pandas 0.25.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"cat": ["a", "a", "b"], "val": [1, 3, 5]})
out = df.groupby("cat").agg(
    avg=("val", "mean"),
    total=("val", "sum"),
    n=("val", "size"),
)
print(out)
```

## Q94: What is the difference between `df.drop` and `df.pop`?
**A:** `df.drop('col', axis=1)` removes columns (or rows via `axis=0`) and returns a new DataFrame by default (or in place with `inplace=True`). `df.pop('col')` removes and returns the column as a Series in one operation (mutates the DataFrame). Use `pop` when you need the removed column's values.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"a": [1], "b": [2], "c": [3]})
print(df.drop("b", axis=1))          # returns new DataFrame
b = df.pop("b")                      # removes and returns Series
print(b, df, sep="\n")
```

## Q95: How do you apply a function element-wise with `applymap`/`map` on a DataFrame?
**A:** `df.map(func)` (Pandas 2.1+, replaces deprecated `applymap`) applies `func` to every element. `df['col'].map(func)` applies to a Series. For row/column-wise (not element-wise) use `df.apply(func, axis=...)`. For performance, prefer vectorized operations (e.g., `df * 2`) over `map`.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
print(df.map(lambda v: v ** 2))       # element-wise on whole DataFrame
print(df["a"].map(lambda v: v + 1))   # element-wise on a Series
print(df * 2)                         # vectorized, preferable
```

## Q96: What is copy-on-write (CoW) and how does it affect Pandas 3.0?
**A:** Copy-on-write is a mode (default in Pandas 3.0) where chained assignments no longer trigger `SettingWithCopyWarning` because operations like slicing return true copies lazily. It makes behavior predictable: `df2 = df[mask]` won't reflect later mutations to `df`. Enable with `pd.set_option('mode.copy_on_write', True)` in 2.x.

**Code:**
```python
import pandas as pd

pd.set_option("mode.copy_on_write", True)   # default in 3.0, opt-in in 2.x

df = pd.DataFrame({"v": [1, 2, 3]})
df2 = df[df["v"] > 1]          # CoW: lazy copy, independent
df2.loc[0, "v"] = 99           # no SettingWithCopyWarning
print(df)                      # original unchanged
```

## Q97: How do you handle duplicate index values?
**A:** Duplicate index labels are allowed in Pandas. `df.loc['dup']` returns a DataFrame/series for all matches. To find: `df.index.duplicated()`. To make unique: `df[~df.index.duplicated()]` (keep first) or `df.reset_index()`. Be careful: `loc` with duplicate labels can be ambiguous — prefer unique indexes or `reset_index(drop=True)`.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"v": [1, 2, 3]}, index=["dup", "dup", "x"])
print(df.loc["dup"])                       # all matching rows
print(df.index.duplicated().tolist())      # marks 2nd 'dup'
print(df[~df.index.duplicated()])          # keep first occurrence
print(df.reset_index(drop=True))
```

## Q98: What is the difference between `df.compare` and subtraction?
**A:** `df.compare(other)` returns a DataFrame showing only the differing cells with `self`/`other` columns (clear diff view). Plain subtraction `df - other` returns element-wise differences (NaN where both NaN). `compare` is for auditing changes between two aligned DataFrames; subtraction is for numeric deltas.

**Code:**
```python
import pandas as pd

a = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
b = pd.DataFrame({"x": [1, 9], "y": [3, 2]})
print(a.compare(b))          # only differing cells, self/other views
print(a - b)                 # element-wise numeric difference
```

## Q99: How do you set display options for large DataFrames?
**A:** `pd.set_option('display.max_rows', 100)`, `'display.max_columns'`, `'display.width'`, `'display.max_colwidth'`, `'display.float_format'`. Reset with `pd.reset_option('all')`. Useful in notebooks/CLIs to preview full frames without truncation. Also `df.head()`/`pd.option_context(...)` for temporary changes.

**Code:**
```python
import pandas as pd

pd.set_option("display.max_rows", 5)
pd.set_option("display.max_columns", 10)
pd.set_option("display.float_format", lambda v: f"{v:.2f}")
df = pd.DataFrame({"a": range(20), "b": [1 / 3] * 20})
print(df.head(20))           # truncated to max_rows
with pd.option_context("display.max_rows", 100):   # temporary scope
    print(df)
```

## Q100: What are the latest features in modern Pandas (2.0+)?
**A:** Pandas 2.0+: PyArrow backend (`mode.dtype_backend='pyarrow'`), nullable dtypes by default, improved copy-on-write, improved NA support, better Parquet/Feather support, and performance improvements. Also: `df.map` for element-wise DataFrame ops, `StringDtype` storage options, `convert_dtypes`, `pd.read_csv(..., dtype_backend='pyarrow')`, and deprecation of `append`. Pandas 3.0 makes copy-on-write the default.

**Code:**
```python
import pandas as pd

df = pd.DataFrame({"a": [1, None], "b": ["x", None]})
df2 = df.convert_dtypes()                              # nullable dtypes
print(df2.dtypes)
print(df.map(lambda v: str(v)))                        # element-wise, 2.1+
print(pd.read_csv("file.csv", dtype_backend="pyarrow").dtypes)
```