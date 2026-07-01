# Pandas & NumPy Interview Questions and Answers

## Q1: What is NumPy?
**A:** NumPy (Numerical Python) is a fundamental Python library for numerical computing. It provides: multi-dimensional array objects (`ndarray`), fast vectorized operations, mathematical functions, linear algebra, random number generation, and Fourier transforms. NumPy arrays are more efficient than Python lists for numerical data due to contiguous memory storage and C-level optimizations.

## Q2: What is Pandas?
**A:** Pandas is a Python library for data manipulation and analysis built on top of NumPy. It introduces two core data structures: `Series` (1D labeled array) and `DataFrame` (2D labeled table). Pandas provides powerful tools for reading/writing data (CSV, Excel, SQL, JSON), data cleaning, transformation, aggregation, merging, and time series analysis.

## Q3: What is the difference between NumPy arrays and Python lists?
**A:** NumPy arrays: homogeneous (single dtype), contiguous memory, fast vectorized operations, support broadcasting, consume less memory, provide element-wise operations by default. Python lists: heterogeneous, store object references, slower for numerical operations, no broadcasting, more flexible for mixed data types.

## Q4: What is a NumPy ndarray?
**A:** `ndarray` is the core NumPy object — a multi-dimensional, homogeneous array of fixed-size items. Key attributes: `ndim` (number of dimensions), `shape` (tuple of dimension sizes), `size` (total elements), `dtype` (data type), `itemsize` (bytes per element), `nbytes` (total bytes), `T` (transpose).

## Q5: How do you create NumPy arrays?
**A:** Common methods: `np.array([1, 2, 3])` from list, `np.zeros((3, 4))` all zeros, `np.ones((2, 3))` all ones, `np.full((2, 2), 7)` constant value, `np.eye(3)` identity, `np.arange(0, 10, 2)` range, `np.linspace(0, 1, 5)` evenly spaced, `np.random.rand(3, 3)` uniform random, `np.random.randn()` normal distribution.

## Q6: What is array broadcasting in NumPy?
**A:** Broadcasting allows arithmetic between arrays of different shapes. NumPy "stretches" smaller arrays to match larger ones without copying data. Rules: 1) Trailing dimensions must match or be 1, 2) Arrays are compatible if dimension sizes match or one is 1, 3) 1-sized dimensions are broadcast to match. Example: `(3,1) + (3,) → (3,3) + (3,1) → (3,3)`.

## Q7: What is vectorization in NumPy?
**A:** Vectorization replaces explicit loops with array operations that execute in C. Example: `result = a + b` instead of `for i in range(len(a)): result[i] = a[i] + b[i]`. Benefits: faster execution (10-100x), cleaner code, and utilizes low-level optimizations (SIMD, BLAS). Most NumPy operations and universal functions (ufuncs) are vectorized.

## Q8: What are universal functions (ufuncs) in NumPy?
**A:** Ufuncs are functions that operate element-wise on arrays with broadcasting support. Examples: arithmetic (`np.add`, `np.subtract`, `np.multiply`), trigonometry (`np.sin`, `np.cos`), exponentials (`np.exp`, `np.log`, `np.sqrt`), comparisons (`np.greater`, `np.equal`), and reductions (`np.sum`, `np.mean`, `np.max`). Ufuncs have `reduce()`, `accumulate()`, `outer()` methods.

## Q9: What is the difference between `np.array` and `np.asarray`?
**A:** Both create arrays. `np.array` always creates a new array (copies data). `np.asarray` creates an array from the input; if the input is already an ndarray, it returns it without copying (no copy if possible). Use `np.asarray` for memory efficiency when the input might already be an array.

## Q10: How do you index NumPy arrays?
**A:** Methods: basic indexing `arr[0, 1]`, slicing `arr[1:3, :2]`, fancy indexing `arr[[0, 2], [1, 3]]` (integer arrays), boolean indexing `arr[arr > 5]`, and slicing with steps `arr[::2]`. Slicing returns views (not copies) — modifications affect the original. Fancy and boolean indexing return copies.

## Q11: What is the difference between a view and a copy in NumPy?
**A:** A view shares data with the original array (no memory duplication). A copy has its own memory. Slicing (`arr[1:3]`) returns a view. Fancy indexing (`arr[[0, 1]]`), boolean indexing, and `.copy()` return copies. Use `np.shares_memory(a, b)` to check. Views mutate the original; copies don't. Use `.copy()` to explicitly create a copy.

## Q12: How do you reshape arrays in NumPy?
**A:** `arr.reshape(new_shape)` returns a new view (if contiguous) with the specified shape. `arr.resize(new_shape)` modifies in-place. `np.ravel()` flattens to 1D (returns view if possible). `arr.flatten()` returns a 1D copy. `arr.T` transposes. `np.newaxis` adds a dimension: `arr[:, np.newaxis]`. `np.expand_dims(arr, axis=0)`.

## Q13: What is the difference between `ravel`, `flatten`, and `reshape(-1)`?
**A:** `ravel()` returns a 1D view (no copy if possible) of the array — memory efficient. `flatten()` returns a 1D copy — always allocates new memory. `reshape(-1)` is similar to `ravel` — infers the dimension from array size. Prefer `ravel()` or `reshape(-1)` for efficiency; use `flatten()` when you need an independent copy.

## Q14: How do you concatenate and stack arrays?
**A:** `np.concatenate((a, b), axis=0)` joins along existing axis. `np.vstack((a, b))` stacks vertically (row-wise). `np.hstack((a, b))` stacks horizontally (column-wise). `np.dstack((a, b))` depth-wise. `np.stack((a, b), axis=0)` creates new axis. All require same shape except along the concatenation axis.

## Q15: What is the difference between `np.concatenate` and `np.stack`?
**A:** `np.concatenate` joins arrays along an existing axis — no new dimensions created. `np.stack` joins arrays along a new axis — adds a dimension. Example: 2 arrays of shape (3, 4): `concat` → (6, 4), `stack` → (2, 3, 4). Use `concatenate` for extending, `stack` for creating batches/channels.

## Q16: How do you handle missing values in NumPy?
**A:** NumPy uses `np.nan` (Not a Number) for missing float values. Functions: `np.isnan(arr)` detect NaN, `np.nanmean()`, `np.nansum()`, `np.nanmax()` — skip NaN. For non-float types, consider masked arrays (`np.ma.masked_array`) or use Pandas. NaN has properties: `np.nan == np.nan` is False, use `np.isnan()` for detection.

## Q17: What is the difference between NumPy and Pandas?
**A:** NumPy: n-dimensional arrays, homogeneous numeric data, low-level linear algebra, no labeling, no missing data handling in core. Pandas: 2D DataFrames and 1D Series, heterogeneous data, labeled axes (index/columns), rich missing data handling, time series support, SQL-like operations, and I/O for various formats. Pandas is built on NumPy.

## Q18: What is a Pandas Series?
**A:** A Series is a 1D labeled array that can hold any data type. It consists of `data` (values) and `index` (labels). Created: `pd.Series([1, 2, 3], index=['a', 'b', 'c'])`. Access by label (`s['a']`), integer position (`s.iloc[0]`), or condition (`s[s > 1]`). Supports vectorized operations like NumPy.

## Q19: What is a Pandas DataFrame?
**A:** A DataFrame is a 2D labeled data structure with columns of potentially different types. Similar to a spreadsheet or SQL table. Rows and columns have labels (index and columns). Created from: dict of Series/arrays, list of dicts, CSV file, SQL query. Key methods: `head()`, `info()`, `describe()`, `shape`, `columns`, `index`, `dtypes`.

## Q20: How do you create a DataFrame from different sources?
**A:** From dict: `pd.DataFrame({'col1': [1,2], 'col2': [3,4]})`. From list of dicts: `pd.DataFrame([{'a': 1}, {'a': 2, 'b': 3}])`. From CSV: `pd.read_csv('file.csv')`. From Excel: `pd.read_excel('file.xlsx')`. From SQL: `pd.read_sql('SELECT * FROM table', connection)`. From JSON: `pd.read_json('file.json')`. From NumPy: `pd.DataFrame(np_array, columns=['a', 'b'])`.

## Q21: What are the key methods to explore a DataFrame?
**A:** `df.head(n)` / `df.tail(n)` — preview rows. `df.info()` — column types, non-null counts, memory. `df.describe()` — summary statistics for numeric columns. `df.shape` — dimensions. `df.columns` / `df.index` — axis labels. `df.dtypes` — column data types. `df.value_counts()` — frequency. `df.nunique()` — unique counts. `df.sample(n)` — random sample.

## Q22: How do you select columns in a DataFrame?
**A:** Single column: `df['col']` or `df.col` (returns Series). Multiple columns: `df[['col1', 'col2']]` (returns DataFrame). Select by dtype: `df.select_dtypes(include=['number'])`. Filter columns by name: `df.filter(like='pattern')` or `df.filter(regex='pattern')`.

## Q23: What is the difference between `loc` and `iloc`?
**A:** `df.loc[row_label, col_label]` uses label-based indexing — inclusive of the endpoint. `df.iloc[row_position, col_position]` uses integer-based positional indexing — exclusive of endpoint. Example: `df.loc['a':'c']` includes 'c', `df.iloc[0:3]` includes rows 0,1,2. `loc` works with bool arrays; `iloc` works with integer arrays.

## Q24: How do you filter rows conditionally?
**A:** `df[df['col'] > 5]` — boolean indexing. Multiple conditions: `df[(df['col1'] > 5) & (df['col2'] == 'x')]` (use `&`, `|`, `~` — not `and`, `or`, `not`). Query method: `df.query('col1 > 5 & col2 == "x"')`. `df.isin(['a', 'b'])` for membership. `df.between(0, 10)` for range.

## Q25: How do you handle missing values in Pandas?
**A:** Detect: `df.isna()` / `df.isnull()` (boolean), `df.isna().sum()`. Drop: `df.dropna()` (rows with any NaN), `df.dropna(axis=1)` (columns), `df.dropna(subset=['col'])` (specific columns). Fill: `df.fillna(value)`, `df.fillna(method='ffill')` (forward fill), `df.fillna(method='bfill')` (backward fill), `df.interpolate()` (linear interpolation).

## Q26: What is the difference between `isna()` and `isnull()`?
**A:** They are identical — `isnull` is an alias of `isna`. Both return a boolean DataFrame/Series indicating missing values. Similarly, `notna()` and `notnull()` are aliases. The duplicate naming exists for compatibility (R users prefer `is.na`, SQL users prefer `is null`).

## Q27: How do you rename columns?
**A:** `df.rename(columns={'old_name': 'new_name'}, inplace=True)` or `df.columns = ['new1', 'new2']`. Add prefix/suffix: `df.add_prefix('pre_')`, `df.add_suffix('_suf')`. Replace parts: `df.columns = df.columns.str.replace('old', 'new')`. Use `inplace=True` to modify the original or assign to a new variable.

## Q28: How do you add and remove columns?
**A:** Add: `df['new_col'] = values`, `df.assign(new_col=values)`. Insert at position: `df.insert(loc, 'col', values)`. Remove: `df.drop('col', axis=1)`, `df.pop('col')` (returns column). Drop by index: `df.drop('col', axis=1, inplace=True)`. Multiple: `df.drop(['col1', 'col2'], axis=1)`.

## Q29: How do you handle duplicate data in Pandas?
**A:** Detect: `df.duplicated()` (boolean Series, marks duplicates), `df.duplicated(subset=['col1'])` (check specific columns), `df.duplicated(keep='last')` (mark all but last). Remove: `df.drop_duplicates()`, `df.drop_duplicates(subset=['col1'], keep='first')`.

## Q30: What is the difference between `apply`, `map`, and `applymap`?
**A:** `df['col'].map(func)` applies function element-wise on a Series (also used for value mapping: `map({'a': 1})`). `df['col'].apply(func)` applies function to each element of a Series (or each row/column of a DataFrame with `axis` parameter). `df.applymap(func)` applies function element-wise to entire DataFrame (deprecated, use `df.map()` in newer versions).

## Q31: How do you group data with `groupby`?
**A:** `df.groupby('col')['value'].mean()` — split by column, apply function, combine results. Multiple groups: `df.groupby(['col1', 'col2'])`. Aggregate multiple functions: `df.groupby('cat').agg({'val1': 'mean', 'val2': 'sum'})`. Named aggs: `df.groupby('cat').agg(avg_val=('val', 'mean'))`. Access groups: `df.groupby('cat').groups`.

## Q32: What aggregation functions are available in groupby?
**A:** Common: `mean()`, `sum()`, `count()`, `size()` (including NaN), `min()`, `max()`, `std()`, `var()`, `median()`, `nunique()`, `first()`, `last()`. Multiple: `df.groupby('cat').agg(['mean', 'std', 'count'])`. Custom: `df.groupby('cat').agg(lambda x: x.max() - x.min())`.

## Q33: What is the difference between `agg` and `transform` in groupby?
**A:** `agg` returns a reduced result (one row per group). `transform` returns a result with the same shape as the original DataFrame (values broadcasted to each group's rows). Example: `df.groupby('cat')['val'].transform('mean')` adds a column with group means. Useful for creating percentage of group total or imputing group means.

## Q34: How do you merge DataFrames?
**A:** `pd.merge(df1, df2, on='key')` — SQL-like join. `how` parameter: 'inner', 'left', 'right', 'outer', 'cross'. Different keys: `left_on='key1', right_on='key2'`. Handle suffix: `suffixes=('_left', '_right')`. Index join: `left_index=True, right_index=True`. Multiple keys: `on=['key1', 'key2']`.

## Q35: What is the difference between `merge` and `join`?
**A:** `merge` is the primary method for database-style joins on columns or indexes. `join` is a convenience method for joining on indexes (simpler but less flexible). `join` is equivalent to `merge(..., left_index=True, right_index=True)` by default. Use `merge` for column-based joins, `join` for index-based joins with simple syntax.

## Q36: How do you concatenate DataFrames?
**A:** `pd.concat([df1, df2])` — stacks vertically (default axis=0). `pd.concat([df1, df2], axis=1)` — side by side horizontally. `ignore_index=True` resets index. `keys=['t1', 't2']` creates hierarchical index. `join='inner'` / `join='outer'` handles column mismatch. `pd.concat` doesn't align on data — it aligns on axes.

## Q37: What is the difference between `concat` and `append`?
**A:** `pd.concat` is the recommended approach for combining DataFrames (vertical or horizontal). `df.append` is deprecated since Pandas 1.4.0, removed in 2.0. Always use `pd.concat`. `append` was a convenience method for vertical stacking but had inconsistent behavior.

## Q38: How do you handle datetime data in Pandas?
**A:** Parse dates: `pd.to_datetime(col)`, `pd.read_csv(..., parse_dates=['col'])`. Extract components: `dt.year`, `dt.month`, `dt.day`, `dt.hour`, `dt.weekday`, `dt.quarter`. Date ranges: `pd.date_range('2024-01-01', periods=10, freq='D')`. Resampling: `df.resample('M').mean()` (monthly mean). Time deltas: `pd.Timedelta(days=5)`.

## Q39: What is the difference between `.loc` and `.iloc` for setting values?
**A:** Both can set values: `df.loc[rows, cols] = value` (by label) and `df.iloc[rows, cols] = value` (by position). The key difference is the access method. When setting with `.loc`, it uses label-based assignment, which can expand the DataFrame if labels don't exist. `.iloc` strictly uses integer positions.

## Q40: How do you apply a function to each row or column?
**A:** Use `df.apply(func, axis=1)` — applies to each row (axis=1) or each column (axis=0). For element-wise operations, use `df.map(func)` (for DataFrames) or `df['col'].map(func)`. For faster row iteration (avoid if possible), use `itertuples()` or `iterrows()`. Vectorized operations are preferred over `apply` for performance.

## Q41: How do you sort DataFrames?
**A:** `df.sort_values('col', ascending=False)` — sort by column values. `df.sort_values(['col1', 'col2'], ascending=[True, False])` — multi-column sort. `df.sort_index()` — sort by index labels. `na_position='first'` or `'last'` controls NaN placement. Use `inplace=True` to modify the original.

## Q42: How do you reset or set the index?
**A:** `df.reset_index()` — reset to default integer index, old index becomes a column. `df.reset_index(drop=True)` — drop old index. `df.set_index('col')` — set column as index. `df.set_index(['col1', 'col2'])` — multi-index. `df.index.name = 'idx_name'` — name the index.

## Q43: What is a MultiIndex (hierarchical index)?
**A:** A MultiIndex has multiple levels of indexing on rows (or columns). Created: `pd.MultiIndex.from_tuples([(1, 'a'), (1, 'b'), (2, 'a')])`. Access: `df.loc[1].loc['a']`, `df.xs(1, level=0)`. Useful for: grouped data, time series with categories, panel data, and pivot tables.

## Q44: How do you pivot and unpivot DataFrames?
**A:** `df.pivot(index='row', columns='col', values='val')` — reshape from long to wide. `df.pivot_table(index='row', columns='col', values='val', aggfunc='mean')` — pivot with aggregation. `pd.melt(df, id_vars=['id'], value_vars=['a', 'b'])` — unpivot from wide to long (gather columns into rows).

## Q45: What is the difference between `pivot` and `pivot_table`?
**A:** `pivot` works with unique index/column combinations (no duplicate entries). If duplicates exist, it raises an error. `pivot_table` handles duplicates by applying an aggregation function (default `mean`), similar to a spreadsheet pivot table. Use `pivot` for simple reshaping, `pivot_table` when you need aggregation.

## Q46: How do you apply SQL-like operations in Pandas?
**A:** SELECT: `df['col']` or `df.filter()`. WHERE: `df[condition]` or `df.query()`. GROUP BY: `df.groupby().agg()`. ORDER BY: `df.sort_values()`. JOIN: `pd.merge()`. UNION: `pd.concat()`. DISTINCT: `df['col'].unique()` or `df.drop_duplicates()`. LIMIT: `df.head(n)`. HAVING: `df.groupby().filter()`.

## Q47: What is the `query` method and when is it useful?
**A:** `df.query('col1 > 5 and col2 == "x"')` filters rows using a string expression. Useful for: cleaner syntax than boolean indexing with `&`/`|`, dynamic queries (string interpolation with `@`), and slightly faster for large DataFrames. Variables: `df.query('col > @threshold')`. Supports `in`, `not in`, `==`, `!=`, `>`, `<`, `is null`, `is not null`.

## Q48: How do you handle categorical data?
**A:** `pd.Categorical(values, categories=['a', 'b', 'c'], ordered=True)` — memory efficient (uses integer codes). Convert: `df['col'].astype('category')`. Benefits: smaller memory, faster groupby/sort, ordered categories support `<`/`>` comparisons, and unused category handling. Access codes: `df['col'].cat.codes`. Rename: `df['col'].cat.rename_categories(new_names)`.

## Q49: What is the difference between `str` accessor and regular string operations?
**A:** `df['col'].str.upper()` applies the operation to each string element in the Series. Without `.str`, you'd need a loop or `apply`. The `.str` accessor provides vectorized string operations: `str.contains()`, `str.replace()`, `str.extract()`, `str.split()`, `str.strip()`, `str.startswith()`, `str.len()`, `str.slice()`. Missing values propagate as NaN.

## Q50: How do you handle text data with regex in Pandas?
**A:** `df['col'].str.contains('pattern', regex=True)` — boolean check. `df['col'].str.extract(r'(\d+)')` — capture groups as new column. `df['col'].str.replace('old', 'new', regex=True)` — replace patterns. `df['col'].str.split('\s+', expand=True)` — split into multiple columns. `df['col'].str.findall(r'\w+')` — find all matches.

## Q51: What is the `assign` method?
**A:** `df.assign(new_col=values)` creates a new DataFrame with added columns (doesn't modify original). Useful for method chaining: `df.assign(col2=df['col1'] * 2).query('col2 > 10')`. Can use callable: `df.assign(col2=lambda x: x['col1'] * 2)` where `x` is the DataFrame. Multiple columns: `df.assign(a=1, b=2)`.

## Q52: How do you handle large DataFrames efficiently?
**A:** Strategies: `pd.read_csv(..., chunksize=10000)` for chunked reading, `dtype` parameter to specify types (saves memory), `usecols` to load only needed columns, `pd.read_csv(..., low_memory=False)` for mixed types. For huge data: use Dask, Vaex, PySpark, or database engines. Use categorical dtypes for low-cardinality string columns.

## Q53: What are window functions in Pandas?
**A:** Window functions operate on a sliding window of rows. Rolling: `df['val'].rolling(window=7).mean()` — 7-period moving average. Expanding: `df['val'].expanding().mean()` — cumulative statistics. Exponentially weighted: `df['val'].ewm(span=10).mean()` — weighted average with more weight on recent observations.

## Q54: What is the difference between `rolling` and `expanding` windows?
**A:** `rolling` has a fixed window size that slides across the data — each window contains a fixed number of observations. `expanding` starts from the first observation and grows to include all data up to the current point — cumulative statistics. Both support: `mean()`, `sum()`, `std()`, `min()`, `max()`, `apply(custom_func)`.

## Q55: How do you resample time series data?
**A:** `df.resample('M').mean()` — monthly mean. `df.resample('H').sum()` — hourly sum. `df.resample('Q').agg(['mean', 'sum'])` — quarterly aggregates. Custom: `df.resample('W').apply(custom_func)`. Asfreq: `df.asfreq('D')` — changes frequency without aggregation (fills NaN). Window resampling: `df.rolling('7D').mean()` — time-based rolling.

## Q56: What is the difference between `resample` and `groupby`?
**A:** `resample` is time-based grouping — groups rows by time intervals (hourly, daily, monthly). `groupby` is value-based grouping — groups by column values. `resample` requires a DatetimeIndex. Conceptually, `resample` is temporal `groupby`. Both support `.agg()`, `.transform()`, and `.apply()`.

## Q57: How do you handle time zones in Pandas?
**A:** Localize: `df['col'].dt.tz_localize('UTC')`. Convert: `df['col'].dt.tz_convert('US/Eastern')`. Create timezone-aware: `pd.Timestamp('2024-01-01', tz='UTC')`. Remove timezone: `df['col'].dt.tz_localize(None)`. Use `tz` parameter in `date_range()` and `read_csv()`.

## Q58: What is the difference between `value_counts` and `groupby` + `size`?
**A:** `df['col'].value_counts()` returns frequency counts sorted by descending count. `df.groupby('col').size()` returns counts by group in the order of unique values. `value_counts` provides: `normalize=True` (proportions), `dropna=False` (include NaN), `sort=True/False`, `bins` (for numeric data). `groupby.size` is more flexible for multi-column grouping.

## Q59: How do you create dummy/indicator variables?
**A:** `pd.get_dummies(df['col'], prefix='col')` — converts categorical column to one-hot encoded columns. Parameters: `drop_first=True` (avoid multicollinearity), `dtype=int` (boolean or int), `columns=['col1', 'col2']` for multiple columns. Alternative: `sklearn.preprocessing.OneHotEncoder` for consistent encoding across train/test.

## Q60: What is the difference between `cut` and `qcut`?
**A:** `pd.cut(values, bins=5)` divides into intervals of equal width (bins specified by value ranges). `pd.qcut(values, q=5)` divides into quantiles (each bin has approximately equal number of observations). `cut` for fixed ranges (e.g., age groups 0-18, 18-35), `qcut` for even frequency distribution (e.g., quartiles).

## Q61: How do you handle outliers in Pandas?
**A:** Detect: IQR method — `Q1 = df['col'].quantile(0.25); Q3 = df['col'].quantile(0.75); IQR = Q3 - Q1; outliers = df[(df['col'] < Q1 - 1.5*IQR) | (df['col'] > Q3 + 1.5*IQR)]`. Z-score method: `np.abs(zscore(df['col'])) > 3`. Handle: remove, cap/winsorize (clip to percentiles), or transform (log, Box-Cox).

## Q62: What is the difference between `DataFrame.apply()` and `DataFrame.transform()`?
**A:** `apply` can return any shape (reduced, expanded, or same shape). `transform` must return the same shape as the input (same number of rows). `transform` is more restrictive but guarantees consistent output. Use `apply` for arbitrary operations, `transform` for broadcasting results back to original shape (like group-level statistics).

## Q63: How do you create a correlation matrix?
**A:** `df.corr()` — Pearson correlation between numeric columns. `df.corr(method='spearman')` — Spearman rank correlation. `df.corr(method='kendall')` — Kendall Tau. Visualize with `sns.heatmap(df.corr(), annot=True)` or `df.corr().style.background_gradient()`. Include only numeric columns: `df.select_dtypes(include='number').corr()`.

## Q64: How do you calculate rolling correlations?
**A:** `df['col1'].rolling(30).corr(df['col2'])` — rolling 30-period correlation. For pairwise rolling correlations across DataFrame: `df.rolling(30).corr(df)` returns multi-index DataFrame. Can be used for: time-varying relationships, dynamic portfolio analysis, and regime detection.

## Q65: What are the common I/O operations in Pandas?
**A:** CSV: `pd.read_csv()`, `df.to_csv()`. Excel: `pd.read_excel()`, `df.to_excel()`. JSON: `pd.read_json()`, `df.to_json()`. SQL: `pd.read_sql()`, `df.to_sql()`. HTML: `pd.read_html()` (reads all tables). Parquet: `pd.read_parquet()`, `df.to_parquet()` (fast, compressed). Pickle: `pd.read_pickle()`, `df.to_pickle()`. Clipboard: `pd.read_clipboard()`.

## Q66: What is the difference between `read_csv` default parameters and when to change them?
**A:** Key parameters: `sep=','` (delimiter), `header=0` (row for column names), `index_col=None` (column to use as index), `usecols=None` (columns to read), `dtype=None` (explicit types), `parse_dates=False`, `na_values=None` (additional NaN markers), `skiprows=0`, `nrows=None` (read only N rows), `chunksize=None` (iterator). Adjust for non-standard formats.

## Q67: How do you read a CSV with no header?
**A:** `pd.read_csv('file.csv', header=None)` — assigns integer column names (0, 1, 2...). Then set names: `df.columns = ['a', 'b', 'c']`. Or use `names=['a', 'b', 'c']` parameter in `read_csv()` directly. For skipping a header row: `skiprows=1`.

## Q68: What is the `memory_usage` method?
**A:** `df.memory_usage(deep=True)` returns memory consumption per column in bytes. Useful for optimizing memory: convert object to category, downcast numeric types (`pd.to_numeric(..., downcast='integer')`), and use `df.info(memory_usage='deep')`. Deep=True includes Python object overhead for string columns.

## Q69: How do you chain operations in Pandas?
**A:** Method chaining: `df.sort_values('col').query('val > 5').groupby('cat').agg({'val': 'mean'}).reset_index()`. `pipe()` for custom functions: `df.pipe(custom_func, arg=1)`. `assign()` and `query()` are chain-friendly. Benefits: readable pipeline, avoids intermediate variables, follows functional programming style.

## Q70: What is the difference between `Series` and 1D NumPy array?
**A:** Series has: index (labels), name, richer methods (`value_counts`, `str` accessor, `dt` accessor, `map`, `.isna().sum()`), alignment on operations (matches by index labels), and integration with DataFrame operations. NumPy arrays are faster for pure numerical operations but lack labeling and convenient data analysis methods.

## Q71: How do you handle large text data efficiently?
**A:** Use `df['col'].astype('string')` (StringDtype) instead of object dtype — more consistent NA handling, memory efficiency for some cases. For very large text: use categorical for repeated strings, store in Parquet format, use `pyarrow` backend (`pd.set_option('mode.string_storage', 'pyarrow')`), or use Dask for out-of-core processing.

## Q72: What is the difference between `inplace=True` and reassignment?
**A:** `inplace=True` modifies the original object without creating a copy (some methods support this — `dropna`, `fillna`, `sort_values`, `rename`, `drop`). Reassignment (`df = df.method()`) creates a new object. `inplace` is controversial — it's not consistently supported, can't be chained, and is slightly faster but encourages mutable state. Many experts recommend reassignment for clarity.

## Q73: How do you create a pivot table?
**A:** `pd.pivot_table(df, values='sales', index='region', columns='product', aggfunc='sum', fill_value=0, margins=True)`. Index: row groups. Columns: column groups. Values: aggregated metric. Aggfunc: aggregation function(s). Margins=True adds row/column totals. Multiple values/index/columns are supported.

## Q74: What is the difference between `stack` and `unstack`?
**A:** `stack` pivots columns into rows (rotates from wide to long format). `unstack` pivots rows into columns (rotates from long to wide format). They are inverse operations. Operate on MultiIndex DataFrames. `level` parameter controls which level(s) to pivot. Useful for reshaping between different tabular formats.

## Q75: How do you handle JSON data in Pandas?
**A:** `pd.read_json('file.json')` for basic JSON. `pd.json_normalize(data)` for nested JSON (flattens dicts and lists into columns). Parameters: `record_path` (path to nested records), `meta` (other fields to include), `sep` (nested field separator, default '.'). For deeply nested JSON, use `json_normalize` iteratively or with `record_path` and `meta`.

## Q76: What is the `eval` method in Pandas?
**A:** `df.eval('new_col = col1 + col2')` evaluates a string expression for column operations. Faster than Python evaluation for large DataFrames (uses numexpr). Can also filter: `df.query('col1 > 0')`. Use for: arithmetic expressions, boolean conditions, and assignments. Supports `@` for Python variables: `df.eval('col > @threshold')`.

## Q77: How do you use NumPy's random module?
**A:** `np.random.rand(3, 3)` — uniform [0,1). `np.random.randn(3, 3)` — standard normal. `np.random.randint(0, 10, size=5)` — integers. `np.random.choice([1,2,3], size=10, p=[0.1, 0.3, 0.6])` — weighted random selection. `np.random.seed(42)` — reproducibility. `np.random.shuffle(arr)` — in-place shuffle. `np.random.permutation(n)` — random order.

## Q78: What is the difference between `np.random.rand` and `np.random.randn`?
**A:** `np.random.rand(d0, d1, ...)` generates samples from a uniform distribution over [0, 1). `np.random.randn(d0, d1, ...)` generates samples from the standard normal distribution (mean=0, variance=1). `rand` is for uniform random values; `randn` is for Gaussian-distributed values.

## Q79: What are linear algebra operations in NumPy?
**A:** `np.dot(a, b)` — matrix multiplication. `np.linalg.inv(m)` — inverse. `np.linalg.det(m)` — determinant. `np.linalg.eig(m)` — eigenvalues/vectors. `np.linalg.svd(m)` — SVD decomposition. `np.linalg.solve(A, b)` — solve linear system Ax = b. `np.linalg.qr(m)` — QR decomposition. `np.linalg.norm(v)` — vector/matrix norm.

## Q80: What is the difference between `np.dot`, `np.matmul`, and `@`?
**A:** `np.dot(a, b)` — scalar, vector, or matrix multiplication (with broadcasting for higher dimensions). `np.matmul(a, b)` — matrix multiplication only, treats last two dimensions as matrix dimensions (batch matrix multiply). `a @ b` is the infix operator for `np.matmul`. For 2D arrays, all three are equivalent.

## Q81: What are NumPy's FFT functions?
**A:** `np.fft.fft(x)` — 1D Fast Fourier Transform. `np.fft.ifft(X)` — inverse. `np.fft.fft2()` — 2D FFT. `np.fft.fftfreq(n, d=1.0)` — frequency bins. `np.fft.fftshift()` — shift zero frequency to center. Used for: signal processing, spectral analysis, convolution acceleration (multiply in frequency domain).

## Q82: How do you use NumPy for image processing?
**A:** Images are 3D arrays (height, width, channels). Operations: cropping `img[50:200, 100:300]`, color channel manipulation `img[:, :, 0] = 0` (zero red), brightness `img = np.clip(img + 50, 0, 255)`, flips `np.fliplr(img)`, rotation `np.rot90(img)`, resizing via interpolation (use skimage or OpenCV for quality resizing).

## Q83: What is the difference between `np.save` and `np.savetxt`?
**A:** `np.save('file.npy', arr)` saves a single array in NumPy's binary `.npy` format (fast, lossless, preserves dtype). `np.savetxt('file.csv', arr, delimiter=',')` saves a 2D array as text (slower, larger files, human-readable). `np.savez('file.npz', a=arr1, b=arr2)` saves multiple arrays in compressed format. `np.load()` loads all formats.

## Q84: How do you use NumPy's polynomial functions?
**A:** `np.polyfit(x, y, deg)` — polynomial regression (least squares). `np.polyval(p, x)` — evaluate polynomial. `np.polyder(p)` — derivative. `np.polyint(p)` — integral. `np.roots(p)` — find roots. `np.polyadd`, `np.polymul`, `np.polydiv` — arithmetic. For modern usage, prefer `np.polynomial.Polynomial` class.

## Q85: What are NumPy masked arrays?
**A:** `np.ma.MaskedArray` is an array with a `mask` boolean array indicating invalid/missing entries. Operations automatically skip masked values. Example: `np.ma.array([1, 2, -999, 4], mask=[False, False, True, False]).mean()` returns 2.33. Useful for: bad data points, missing measurements, invalid sensor readings.

## Q86: How do you compute statistics with NumPy?
**A:** `np.mean(arr)`, `np.median(arr)`, `np.std(arr)`, `np.var(arr)`, `np.min(arr)`, `np.max(arr)`, `np.percentile(arr, 75)`, `np.ptp(arr)` (range), `np.corrcoef(x, y)` (correlation), `np.cov(x, y)` (covariance). All support axis parameter: `np.mean(arr, axis=0)` for column means. `np.nanmean()` and similar skip NaN.

## Q87: What is the purpose of `np.newaxis` and `np.expand_dims`?
**A:** Both add a new dimension to an array. `arr[:, np.newaxis]` adds a dimension at position 1 (shape (3,) → (3, 1)). `np.expand_dims(arr, axis=0)` adds a dimension at position 0 (shape (3,) → (1, 3)). Used for: broadcasting alignment, converting 1D to row/column vector, and adding batch/channel dimensions.

## Q88: How do you compute pairwise distances with NumPy?
**A:** Euclidean: `np.sqrt(((a - b)**2).sum(axis=1))`. Cosine: `1 - np.dot(a, b.T) / (np.linalg.norm(a) * np.linalg.norm(b))`. For many points, use `scipy.spatial.distance.pdist()` or `sklearn.metrics.pairwise_distances()` (more efficient). Broadcasting approach: `np.linalg.norm(a[:, np.newaxis] - b, axis=2)` computes all pairwise distances.

## Q89: What are NumPy's set operations?
**A:** `np.unique(arr)` — sorted unique values. `np.in1d(a, b)` — membership check. `np.intersect1d(a, b)` — intersection. `np.union1d(a, b)` — union. `np.setdiff1d(a, b)` — difference. `np.setxor1d(a, b)` — symmetric difference. All return sorted arrays. `assume_unique=True` for performance if inputs have unique elements.

## Q90: How do you work with structured arrays in NumPy?
**A:** Structured arrays have named fields of different types. Define: `np.dtype([('name', 'U10'), ('age', 'i4'), ('height', 'f8')])`. Create: `np.array([('Alice', 30, 1.7)], dtype=dtype)`. Access: `arr['name']`, `arr['age']`. Filter: `arr[arr['age'] > 25]`. Similar to Pandas DataFrame but lower level and more memory efficient.

## Q91: How do you handle time series data with NumPy?
**A:** NumPy doesn't have native datetime support as rich as Pandas, but: `np.datetime64('2024-01-01')` — datetime scalar. `np.arange('2024-01', '2024-03', dtype='datetime64[D]')` — date range. `np.timedelta64(5, 'D')` — time delta. For complex time series, use Pandas; for simple timestamp arrays or performance-critical code, NumPy is sufficient.

## Q92: What is the difference between `np.any` and `np.all`?
**A:** `np.any(arr)` returns True if any element is truthy. `np.all(arr)` returns True if all elements are truthy. Both support `axis` parameter: `np.any(arr > 0, axis=1)` checks each row. Short-circuit evaluation doesn't apply — the entire array is always evaluated. Use for condition checking in boolean arrays.

## Q93: How do you use `np.where`?
**A:** `np.where(condition)` returns indices where condition is True: `np.where(arr > 5)` returns tuple of arrays (one per dimension). `np.where(condition, x, y)` returns elements from x where True, y where False: `np.where(df['val'] > 0, df['val'], 0)` replaces negative values with 0. Useful for conditional replacement and bulk operations.

## Q94: What is the difference between `np.select` and `np.where`?
**A:** `np.where` handles a single condition (binary if-else). `np.select(condlist, choicelist, default=0)` handles multiple conditions (if-elif-else). Each condition in condlist is a boolean array; the first True condition's choice is selected. Useful for multi-case categorization (e.g., age groups: child, adult, senior).

## Q95: How do you use `pd.cut` and `pd.qcut` with real data?
**A:** `df['age_group'] = pd.cut(df['age'], bins=[0, 18, 35, 60, 120], labels=['Child', 'Young', 'Adult', 'Senior'])` — category assignment. `df['income_quartile'] = pd.qcut(df['income'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])` — equally populated groups. Returns Categorical Series that can be used in groupby.

## Q96: What is the difference between `pd.merge` and SQL JOINs?
**A:** `pd.merge` supports all SQL JOIN types (inner, left, right, outer, cross). Differences: 1) Pandas merges on index or columns, 2) Supports multiple keys, 3) No support for ON clause conditions beyond equality, 4) Doesn't support non-equi joins (use `df.query()` after cross join), 5) More flexible with overlapping column names via suffixes.

## Q97: How do you handle `SettingWithCopyWarning`?
**A:** Occurs when modifying a slice of a DataFrame (which might be a view or copy). Fix: 1) Use `.loc` to set values: `df.loc[condition, 'col'] = value`, 2) Explicit copy: `df_slice = df[condition].copy()`, 3) Use `chained_assignment` option: `pd.set_option('mode.chained_assignment', None)` (not recommended — better to fix the code).

## Q98: What are the best practices for Pandas performance?
**A:** 1) Use vectorized operations instead of `apply`/loops, 2) Specify `dtypes` when reading data, 3) Use `category` dtype for low-cardinality strings, 4) Filter early (reduce data before expensive ops), 5) Use `inplace=False` (reassign), 6) Use `.values` or `.to_numpy()` for pure NumPy operations, 7) Use `pd.concat` instead of `df.append`, 8) Avoid `iterrows()` — use `itertuples()` if iteration is necessary.

## Q99: How do you handle memory errors with large datasets?
**A:** 1) Read in chunks: `pd.read_csv(..., chunksize=50000)`, 2) Downcast numeric types: `pd.to_numeric(col, downcast='integer')`, 3) Use `usecols` to load only needed columns, 4) Use `category` dtype, 5) Filter rows during read: `pd.read_csv(..., skiprows=lambda i: i not in rows_to_keep)`, 6) Use PySpark, Dask, or Vaex for truly large data, 7) Store in efficient format (Parquet, Feather).

## Q100: What are the latest features in modern Pandas/NumPy?
**A:** Pandas 2.0+: PyArrow backend (`mode.dtype_backend='pyarrow'`), nullable dtypes by default, improved copy-on-write, improved NA support, better Parquet/Feather support, and performance improvements. NumPy 2.0+: improved string dtype, faster sorting, enhanced FFT, improved random number generation, cleaner API, and better compatibility with array API standard.
