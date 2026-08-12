# Pandas Interview Questions and Answers (Top 100)

## Q1: What is Pandas?
**A:** Pandas is a Python library for data manipulation and analysis built on top of NumPy. It introduces two core data structures: `Series` (1D labeled array) and `DataFrame` (2D labeled table). Pandas provides powerful tools for reading/writing data (CSV, Excel, SQL, JSON), data cleaning, transformation, aggregation, merging, and time series analysis.

## Q2: What is a Pandas Series?
**A:** A Series is a 1D labeled array that can hold any data type. It consists of `data` (values) and `index` (labels). Created: `pd.Series([1, 2, 3], index=['a', 'b', 'c'])`. Access by label (`s['a']`), integer position (`s.iloc[0]`), or condition (`s[s > 1]`). Supports vectorized operations like NumPy.

## Q3: What is a Pandas DataFrame?
**A:** A DataFrame is a 2D labeled data. Rows and columns have labels (index and columns). Created from: dict of Series/arrays, list of dicts, CSV file, SQL query. Key methods: `head()`, `info()`, `describe()`, `shape`, `columns`, `index`, `dtypes`.

## Q4: How do you create a DataFrame from different sources?
**A:** From dict: `pd.DataFrame({'col1': [1,2], 'col2': [3,4]})`. From list of dicts: `pd.DataFrame([{'a': 1}, {'a': 2, 'b': 3}])`. From CSV: `pd.read_csv('file.csv')`. From Excel: `pd.read_excel('file.xlsx')`. From SQL: `pd.read_sql('SELECT * FROM table', connection)`. From JSON: `pd.read_json('file.json')`. From NumPy: `pd.DataFrame(np_array, columns=['a', 'b'])`.

## Q5: What are the key methods to explore a DataFrame?
**A:** `df.head(n)` / `df.tail(n)` — preview rows. `df.info()` — column types, non-null counts, memory. `df.describe()` — summary statistics for numeric columns. `df.shape` — dimensions. `df.columns` / `df.index` — axis labels. `df.dtypes` — column data types. `df.value_counts()` — frequency. `df.nunique()` — unique counts. `df.sample(n)` — random sample.

## Q6: How do you select columns in a DataFrame?
**A:** Single column: `df['col']` or `df.col` (returns Series). Multiple columns: `df[['col1', 'col2']]` (returns DataFrame). Select by dtype: `df.select_dtypes(include=['number'])`. Filter columns by name: `df.filter(like='pattern')` or `df.filter(regex='pattern')`.

## Q7: What is the difference between `loc` and `iloc`?
**A:** `df.loc[row_label, col_label]` uses label-based indexing — inclusive of the endpoint. `df.iloc[row_position, col_position]` uses integer-based positional indexing — exclusive of endpoint. Example: `df.loc['a':'c']` includes 'c', `df.iloc[0:3]` includes rows 0,1,2. `loc` works with bool arrays; `iloc` works with integer arrays.

## Q8: How do you filter rows conditionally?
**A:** `df[df['col'] > 5]` — boolean indexing. Multiple conditions: `df[(df['col1'] > 5) & (df['col2'] == 'x')]` (use `&`, `|`, `~` — not `and`, `or`, `not`). Query method: `df.query('col1 > 5 & col2 == "x"')`. `df.isin(['a', 'b'])` for membership. `df.between(0, 10)` for range.

## Q9: How do you handle missing values in Pandas?
**A:** Detect: `df.isna()` / `df.isnull()` (boolean), `df.isna().sum()`. Drop: `df.dropna()` (rows with any NaN), `df.dropna(axis=1)` (columns), `df.dropna(subset=['col'])` (specific columns). Fill: `df.fillna(value)`, `df.fillna(method='ffill')` (forward fill), `df.fillna(method='bfill')` (backward fill), `df.interpolate()` (linear interpolation).

## Q10: What is the difference between `isna()` and `isnull()`?
**A:** They are identical — `isnull` is an alias of `isna`. Both return a boolean DataFrame/Series indicating missing values. Similarly, `notna()` and `notnull()` are aliases. The duplicate naming exists for compatibility (R users prefer `is.na`, SQL users prefer `is null`).

## Q11: How do you rename columns?
**A:** `df.rename(columns={'old_name': 'new_name'}, inplace=True)` or `df.columns = ['new1', 'new2']`. Add prefix/suffix: `df.add_prefix('pre_')`, `df.add_suffix('_suf')`. Replace parts: `df.columns = df.columns.str.replace('old', 'new')`. Use `inplace=True` to modify the original or assign to a new variable.

## Q12: How do you add and remove columns?
**A:** Add: `df['new_col'] = values`, `df.assign(new_col=values)`. Insert at position: `df.insert(loc, 'col', values)`. Remove: `df.drop('col', axis=1)`, `df.pop('col')` (returns column). Drop by index: `df.drop('col', axis=1, inplace=True)`. Multiple: `df.drop(['col1', 'col2'], axis=1)`.

## Q13: How do you handle duplicate data in Pandas?
**A:** Detect: `df.duplicated()` (boolean Series, marks duplicates), `df.duplicated(subset=['col1'])` (check specific columns), `df.duplicated(keep='last')` (mark all but last). Remove: `df.drop_duplicates()`, `df.drop_duplicates(subset=['col1'], keep='first')`.

## Q14: What is the difference between `apply`, `map`, and `applymap`?
**A:** `df['col'].map(func)` applies function element-wise on a Series (also used for value mapping: `map({'a': 1})`). `df['col'].apply(func)` applies function to each element of a Series (or each row/column of a DataFrame with `axis` parameter). `df.applymap(func)` applies function element-wise to entire DataFrame (deprecated, use `df.map()` in newer versions).

## Q15: How do you group data with `groupby`?
**A:** `df.groupby('col')['value'].mean()` — split by column, apply function, combine results. Multiple groups: `df.groupby(['col1', 'col2'])`. Aggregate multiple functions: `df.groupby('cat').agg({'val1': 'mean', 'val2': 'sum'})`. Named aggs: `df.groupby('cat').agg(avg_val=('val', 'mean'))`. Access groups: `df.groupby('cat').groups`.

## Q16: What aggregation functions are available in groupby?
**A:** Common: `mean()`, `sum()`, `count()`, `size()` (including NaN), `min()`, `max()`, `std()`, `var()`, `median()`, `nunique()`, `first()`, `last()`. Multiple: `df.groupby('cat').agg(['mean', 'std', 'count'])`. Custom: `df.groupby('cat').agg(lambda x: x.max() - x.min())`.

## Q17: What is the difference between `agg` and `transform` in groupby?
**A:** `agg` returns a reduced result (one row per group). `transform` returns a result with the same shape as the original DataFrame (values broadcasted to each group's rows). Example: `df.groupby('cat')['val'].transform('mean')` adds a column with group means. Useful for creating percentage of group total or imputing group means.

## Q18: How do you merge DataFrames?
**A:** `pd.merge(df1, df2, on='key')` — SQL-like join. `how` parameter: 'inner', 'left', 'right', 'outer', 'cross'. Different keys: `left_on='key1', right_on='key2'`. Handle suffix: `suffixes=('_left', '_right')`. Index join: `left_index=True, right_index=True`. Multiple keys: `on=['key1', 'key2']`.

## Q19: What is the difference between `merge` and `join`?
**A:** `merge` is the primary method for database-style joins on columns or indexes. `join` is a convenience method for joining on indexes (simpler but less flexible). `join` is equivalent to `merge(..., left_index=True, right_index=True)` by default. Use `merge` for column-based joins, `join` for index-based joins with simple syntax.

## Q20: How do you concatenate DataFrames?
**A:** `pd.concat([df1, df2])` — stacks vertically (default axis=0). `pd.concat([df1, df2], axis=1)` — side by side horizontally. `ignore_index=True` resets index. `keys=['t1', 't2']` creates hierarchical index. `join='inner'` / `join='outer'` handles column mismatch. `pd.concat` doesn't align on data — it aligns on axes.

## Q21: What is the difference between `concat` and `append`?
**A:** `pd.concat` is the recommended approach for combining DataFrames (vertical or horizontal). `df.append` is deprecated since Pandas 1.4.0, removed in 2.0. Always use `pd.concat`. `append` was a convenience method for vertical stacking but had inconsistent behavior.

## Q22: How do you handle datetime data in Pandas?
**A:** Parse dates: `pd.to_datetime(col)`, `pd.read_csv(..., parse_dates=['col'])`. Extract components: `dt.year`, `dt.month`, `dt.day`, `dt.hour`, `dt.weekday`, `dt.quarter`. Date ranges: `pd.date_range('2024-01-01', periods=10, freq='D')`. Resampling: `df.resample('M').mean()` (monthly mean). Time deltas: `pd.Timedelta(days=5)`.

## Q23: What is the difference between `.loc` and `.iloc` for setting values?
**A:** Both can set values: `df.loc[rows, cols] = value` (by label) and `df.iloc[rows, cols] = value` (by position). The key difference is the access method. When setting with `.loc`, it uses label-based assignment, which can expand the DataFrame if labels don't exist. `.iloc` strictly uses integer positions.

## Q24: How do you apply a function to each row or column?
**A:** Use `df.apply(func, axis=1)` — applies to each row (axis=1) or each column (axis=0). For element-wise operations, use `df.map(func)` (for DataFrames) or `df['col'].map(func)`. For faster row iteration (avoid if possible), use `itertuples()` or `iterrows()`. Vectorized operations are preferred over `apply` for performance.

## Q25: How do you sort DataFrames?
**A:** `df.sort_values('col', ascending=False)` — sort by column values. `df.sort_values(['col1', 'col2'], ascending=[True, False])` — multi-column sort. `df.sort_index()` — sort by index labels. `na_position='first'` or `'last'` controls NaN placement. Use `inplace=True` to modify the original.

## Q26: How do you reset or set the index?
**A:** `df.reset_index()` — reset to default integer index, old index becomes a column. `df.reset_index(drop=True)` — drop old index. `df.set_index('col')` — set column as index. `df.set_index(['col1', 'col2'])` — multi-index. `df.index.name = 'idx_name'` — name the index.

## Q27: What is a MultiIndex (hierarchical index)?
**A:** A MultiIndex has multiple levels of indexing on rows (or columns). Created: `pd.MultiIndex.from_tuples([(1, 'a'), (1, 'b'), (2, 'a')])`. Access: `df.loc[1].loc['a']`, `df.xs(1, level=0)`. Useful for: grouped data, time series with categories, panel data, and pivot tables.

## Q28: How do you pivot and unpivot DataFrames?
**A:** `df.pivot(index='row', columns='col', values='val')` — reshape from long to wide. `df.pivot_table(index='row', columns='col', values='val', aggfunc='mean')` — pivot with aggregation. `pd.melt(df, id_vars=['id'], value_vars=['a', 'b'])` — unpivot from wide to long (gather columns into rows).

## Q29: What is the difference between `pivot` and `pivot_table`?
**A:** `pivot` works with unique index/column combinations (no duplicate entries). If duplicates exist, it raises an error. `pivot_table` handles duplicates by applying an aggregation function (default `mean`), similar to a spreadsheet pivot table. Use `pivot` for simple reshaping, `pivot_table` when you need aggregation.

## Q30: How do you apply SQL-like operations in Pandas?
**A:** SELECT: `df['col']` or `df.filter()`. WHERE: `df[condition]` or `df.query()`. GROUP BY: `df.groupby().agg()`. ORDER BY: `df.sort_values()`. JOIN: `pd.merge()`. UNION: `pd.concat()`. DISTINCT: `df['col'].unique()` or `df.drop_duplicates()`. LIMIT: `df.head(n)`. HAVING: `df.groupby().filter()`.

## Q31: What is the `query` method and when is it useful?
**A:** `df.query('col1 > 5 and col2 == "x"')` filters rows using a string expression. The syntax is cleaner than boolean indexing with `&`/`|`, supports `@variable` interpolation (`df.query('col > @threshold')`), and can be faster for large DataFrames. Supports `in`, `not in`, `==`, `!=`, `>`, `<`, `is null`, `is not null`.

## Q32: How do you handle categorical data?
**A:** `pd.Categorical(values, categories=['a', 'b', 'c'], ordered=True)` — memory efficient (uses integer codes). Convert: `df['col'].astype('category')`. Benefits: smaller memory, faster groupby/sort, ordered categories support `<`/`>` comparisons, and unused category handling. Access codes: `df['col'].cat.codes`. Rename: `df['col'].cat.rename_categories(new_names)`.

## Q33: What is the difference between `str` accessor and regular string operations?
**A:** `df['col'].str.upper()` applies the operation to each string element in the Series. Without `.str`, you'd need a loop or `apply`. The `.str` accessor provides vectorized string operations: `str.contains()`, `str.replace()`, `str.extract()`, `str.split()`, `str.strip()`, `str.startswith()`, `str.len()`, `str.slice()`. Missing values propagate as NaN.

## Q34: How do you handle text data with regex in Pandas?
**A:** `df['col'].str.contains('pattern', regex=True)` — boolean check. `df['col'].str.extract(r'(\d+)')` — capture groups as new column. `df['col'].str.replace('old', 'new', regex=True)` — replace patterns. `df['col'].str.split('\s+', expand=True)` — split into multiple columns. `df['col'].str.findall(r'\w+')` — find all matches.

## Q35: What is the `assign` method?
**A:** `df.assign(new_col=values)` creates a new DataFrame with added columns (doesn't modify original). Useful for method chaining: `df.assign(col2=df['col1'] * 2).query('col2 > 10')`. Can use callable: `df.assign(col2=lambda x: x['col1'] * 2)` where `x` is the DataFrame. Multiple columns: `df.assign(a=1, b=2)`.

## Q36: How do you handle large DataFrames efficiently?
**A:** Strategies: `pd.read_csv(..., chunksize=10000)` for chunked reading, `dtype` parameter to specify types (saves memory), `usecols` to load only needed columns, `pd.read_csv(..., low_memory=False)` for mixed types. For huge data: use Dask, Vaex, PySpark, or database engines. Use categorical dtypes for low-cardinality string columns.

## Q37: What are window functions in Pandas?
**A:** Window functions operate on a sliding window of rows. Rolling: `df['val'].rolling(window=7).mean()` — 7-period moving average. Expanding: `df['val'].expanding().mean()` — cumulative statistics. Exponentially weighted: `df['val'].ewm(span=10).mean()` — weighted average with more weight on recent observations.

## Q38: What is the difference between `rolling` and `expanding` windows?
**A:** `rolling` has a fixed window size that slides across the data — each window contains a fixed number of observations. `expanding` starts from the first observation and grows to include all data up to the current point — cumulative statistics. Both support: `mean()`, `sum()`, `std()`, `min()`, `max()`, `apply(custom_func)`.

## Q39: How do you resample time series data?
**A:** `df.resample('M').mean()` — monthly mean. `df.resample('H').sum()` — hourly sum. `df.resample('Q').agg(['mean', 'sum'])` — quarterly aggregates. Custom: `df.resample('W').apply(custom_func)`. Asfreq: `df.asfreq('D')` — changes frequency without aggregation (fills NaN). Window resampling: `df.rolling('7D').mean()` — time-based rolling.

## Q40: What is the difference between `resample` and `groupby`?
**A:** `resample` is time-based grouping — groups rows by time intervals (hourly, daily, monthly). `groupby` is value-based grouping — groups by column values. `resample` requires a DatetimeIndex. Conceptually, `resample` is temporal `groupby`. Both support `.agg()`, `.transform()`, and `.apply()`.

## Q41: How do you handle time zones in Pandas?
**A:** Localize: `df['col'].dt.tz_localize('UTC')`. Convert: `df['col'].dt.tz_convert('US/Eastern')`. Create timezone-aware: `pd.Timestamp('2024-01-01', tz='UTC')`. Remove timezone: `df['col'].dt.tz_localize(None)`. Use `tz` parameter in `date_range()` and `read_csv()`.

## Q42: What is the difference between `value_counts` and `groupby` + `size`?
**A:** `df['col'].value_counts()` returns frequency counts sorted by descending count. `df.groupby('col').size()` returns counts by group in the order of unique values. `value_counts` provides: `normalize=True` (proportions), `dropna=False` (include NaN), `sort=True/False`, `bins` (for numeric data). `groupby.size` is more flexible for multi-column grouping.

## Q43: How do you create dummy/indicator variables?
**A:** `pd.get_dummies(df['col'], prefix='col')` — converts categorical column to one-hot encoded columns. Parameters: `drop_first=True` (avoid multicollinearity), `dtype=int` (boolean or int), `columns=['col1', 'col2']` for multiple columns. Alternative: `sklearn.preprocessing.OneHotEncoder` for consistent encoding across train/test.

## Q44: What is the difference between `cut` and `qcut`?
**A:** `pd.cut(values, bins=5)` divides into intervals of equal width (bins specified by value ranges). `pd.qcut(values, q=5)` divides into quantiles (each bin has approximately equal number of observations). `cut` for fixed ranges (e.g., age groups 0-18, 18-35), `qcut` for even frequency distribution (e.g., quartiles).

## Q45: How do you handle outliers in Pandas?
**A:** Detect: IQR method — `Q1 = df['col'].quantile(0.25); Q3 = df['col'].quantile(0.75); IQR = Q3 - Q1; outliers = df[(df['col'] < Q1 - 1.5*IQR) | (df['col'] > Q3 + 1.5*IQR)]`. Z-score method: `np.abs(zscore(df['col'])) > 3`. Handle: remove, cap/winsorize (clip to percentiles), or transform (log, Box-Cox).

## Q46: What is the difference between `DataFrame.apply()` and `DataFrame.transform()`?
**A:** `apply` can return any shape (reduced, expanded, or same shape). `transform` must return the same shape as the input (same number of rows). `transform` is more restrictive but guarantees consistent output. Use `apply` for arbitrary operations, `transform` for broadcasting results back to original shape (like group-level statistics).

## Q47: How do you create a correlation matrix?
**A:** `df.corr()` — Pearson correlation between numeric columns. `df.corr(method='spearman')` — Spearman rank correlation. `df.corr(method='kendall')` — Kendall Tau. Visualize with `sns.heatmap(df.corr(), annot=True)` or `df.corr().style.background_gradient()`. Include only numeric columns: `df.select_dtypes(include='number').corr()`.

## Q48: How do you calculate rolling correlations?
**A:** `df['col1'].rolling(30).corr(df['col2'])` — rolling 30-period correlation. For pairwise rolling correlations across DataFrame: `df.rolling(30).corr(df)` returns multi-index DataFrame. Can be used for: time-varying relationships, dynamic portfolio analysis, and regime detection.

## Q49: What are the common I/O operations in Pandas?
**A:** CSV: `pd.read_csv()`, `df.to_csv()`. Excel: `pd.read_excel()`, `df.to_excel()`. JSON: `pd.read_json()`, `df.to_json()`. SQL: `pd.read_sql()`, `df.to_sql()`. HTML: `pd.read_html()` (reads all tables). Parquet: `pd.read_parquet()`, `df.to_parquet()` (fast, compressed). Pickle: `pd.read_pickle()`, `df.to_pickle()`. Clipboard: `pd.read_clipboard()`.

## Q50: What is the difference between `read_csv` default parameters and when to change them?
**A:** Key parameters: `sep=','` (delimiter), `header=0` (row for column names), `index_col=None` (column to use as index), `usecols=None` (columns to read), `dtype=None` (explicit types), `parse_dates=False`, `na_values=None` (additional NaN markers), `skiprows=0`, `nrows=None` (read only N rows), `chunksize=None` (iterator). Adjust for non-standard formats.

## Q51: How do you read a CSV with no header?
**A:** `pd.read_csv('file.csv', header=None)` — assigns integer column names (0, 1, 2...). Then set names: `df.columns = ['a', 'b', 'c']`. Or use `names=['a', 'b', 'c']` parameter in `read_csv()` directly. For skipping a header row: `skiprows=1`.

## Q52: What is the `memory_usage` method?
**A:** `df.memory_usage(deep=True)` returns memory consumption per column in bytes. Useful for optimizing memory: convert object to category, downcast numeric types (`pd.to_numeric(..., downcast='integer')`), and use `df.info(memory_usage='deep')`. Deep=True includes Python object overhead for string columns.

## Q53: How do you chain operations in Pandas?
**A:** Method chaining: `df.sort_values('col').query('val > 5').groupby('cat').agg({'val': 'mean'}).reset_index()`. `pipe()` for custom functions: `df.pipe(custom_func, arg=1)`. `assign()` and `query()` are chain-friendly. Benefits: readable pipeline, avoids intermediate variables, follows functional programming style.

## Q54: What is the difference between `Series` and 1D NumPy array?
**A:** Series has: index (labels), name, richer methods (`value_counts`, `str` accessor, `dt` accessor, `map`, `.isna().sum()`), alignment on operations (matches by index labels), and integration with DataFrame operations. NumPy arrays are faster for pure numerical operations but lack labeling and convenient data analysis methods.

## Q55: How do you handle large text data efficiently?
**A:** Use `df['col'].astype('string')` (StringDtype) instead of object dtype — more consistent NA handling, memory efficiency for some cases. For very large text: use categorical for repeated strings, store in Parquet format, use `pyarrow` backend (`pd.set_option('mode.string_storage', 'pyarrow')`), or use Dask for out-of-core processing.

## Q56: What is the difference between `inplace=True` and reassignment?
**A:** `inplace=True` modifies the original object without creating a copy (some methods support this — `dropna`, `fillna`, `sort_values`, `rename`, `drop`). Reassignment (`df = df.method()`) creates a new object. `inplace` is controversial — it's not consistently supported, can't be chained, and is slightly faster but encourages mutable state. Many experts recommend reassignment for clarity.

## Q57: How do you create a pivot table?
**A:** `pd.pivot_table(df, values='sales', index='region', columns='product', aggfunc='sum', fill_value=0, margins=True)`. Index: row groups. Columns: column groups. Values: aggregated metric. Aggfunc: aggregation function(s). Margins=True adds row/column totals. Multiple values/index/columns are supported.

## Q58: What is the difference between `stack` and `unstack`?
**A:** `stack` pivots columns into rows (rotates from wide to long format). `unstack` pivots rows into columns (rotates from long to wide format). They are inverse operations. Operate on MultiIndex DataFrames. `level` parameter controls which level(s) to pivot. Useful for reshaping between different tabular formats.

## Q59: How do you handle JSON data in Pandas?
**A:** `pd.read_json('file.json')` for basic JSON. `pd.json_normalize(data)` for nested JSON (flattens dicts and lists into columns). Parameters: `record_path` (path to nested records), `meta` (other fields to include), `sep` (nested field separator, default '.'). For deeply nested JSON, use `json_normalize` iteratively or with `record_path` and `meta`.

## Q60: What is the `eval` method in Pandas?
**A:** `df.eval('new_col = col1 + col2')` evaluates a string expression for column operations. Faster than Python evaluation for large DataFrames (uses numexpr). Can also filter: `df.query('col1 > 0')`. Use for: arithmetic expressions, boolean conditions, and assignments. Supports `@` for Python variables: `df.eval('col > @threshold')`.

## Q61: What is the difference between `iterrows()` and `itertuples()`?
**A:** `iterrows()` iterates returning (index, Series) per row — convenient but slow (creates a Series each time and breaks dtype). `itertuples()` returns namedtuples — much faster and preserves dtypes. Avoid both when possible; prefer vectorized operations. If iteration is unavoidable, `itertuples()` is strongly recommended.

## Q62: How do you use `pd.cut` and `pd.qcut` with real data?
**A:** `df['age_group'] = pd.cut(df['age'], bins=[0, 18, 35, 60, 120], labels=['Child', 'Young', 'Adult', 'Senior'])` — category assignment. `df['income_quartile'] = pd.qcut(df['income'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])` — equally populated groups. Returns Categorical Series that can be used in groupby.

## Q63: What is the difference between `pd.merge` and SQL JOINs?
**A:** `pd.merge` supports all SQL JOIN types (inner, left, right, outer, cross). Differences: 1) Pandas merges on index or columns, 2) Supports multiple keys, 3) No support for ON clause conditions beyond equality, 4) Doesn't support non-equi joins (use `df.query()` after cross join), 5) More flexible with overlapping column names via suffixes.

## Q64: How do you handle `SettingWithCopyWarning`?
**A:** Occurs when modifying a slice of a DataFrame (which might be a view or copy). Fix: 1) Use `.loc` to set values: `df.loc[condition, 'col'] = value`, 2) Explicit copy: `df_slice = df[condition].copy()`, 3) Use `chained_assignment` option: `pd.set_option('mode.chained_assignment', None)` (not recommended — better to fix the code).

## Q65: What are the best practices for Pandas performance?
**A:** 1) Use vectorized operations instead of `apply`/loops, 2) Specify `dtypes` when reading data, 3) Use `category` dtype for low-cardinality strings, 4) Filter early (reduce data before expensive ops), 5) Use `inplace=False` (reassign), 6) Use `.values` or `.to_numpy()` for pure NumPy operations, 7) Use `pd.concat` instead of `df.append`, 8) Avoid `iterrows()` — use `itertuples()` if iteration is necessary.

## Q66: How do you handle memory errors with large datasets?
**A:** 1) Read in chunks: `pd.read_csv(..., chunksize=50000)`, 2) Downcast numeric types: `pd.to_numeric(col, downcast='integer')`, 3) Use `usecols` to load only needed columns, 4) Use `category` dtype, 5) Filter rows during read: `pd.read_csv(..., skiprows=lambda i: i not in rows_to_keep)`, 6) Use PySpark, Dask, or Vaex for truly large data, 7) Store in efficient format (Parquet, Feather).

## Q67: What is the difference between `.values` and `.to_numpy()`?
**A:** Both return the underlying data as a NumPy array. `.values` is the older property (may surprise with mixed dtypes by returning object arrays). `.to_numpy()` is the recommended method — it accepts `dtype` and `copy` parameters and is consistent. Prefer `.to_numpy()` for clarity and control.

## Q68: What is the difference between `copy(deep=True)` and `copy(deep=False)`?
**A:** `df.copy(deep=True)` (default) copies both the data and the index/columns. `df.copy(deep=False)` is a shallow copy — a new DataFrame object sharing the same underlying data buffers (modifying data may affect the original). Use deep copies when you need full independence; shallow copies save memory when only metadata changes.

## Q69: How do you use `df.replace`?
**A:** `df.replace({'old': 'new'})` maps values, `df.replace([1, 2], [10, 20])` maps lists positionally, `df.replace(regex={'pat': 'repl'})` uses regex. Unlike `map`, `replace` works on the whole DataFrame and preserves the structure. Use `inplace=True` or reassign. Great for cleaning categorical typos.

## Q70: What is the difference between `df.where` and `df.mask`?
**A:** `df.where(cond, other)` keeps values where `cond` is True and replaces False positions with `other` (default NaN). `df.mask(cond, other)` is the inverse — replaces where `cond` is True. Both are vectorized conditionals that keep the original shape, useful alternatives to `np.where` on DataFrames.

## Q71: How do you use `df.clip`?
**A:** `df.clip(lower=0, upper=100)` caps all values to the range [0, 100] — values below lower become lower, above upper become upper. Works column-wise and along axes. Handy for winsorizing outliers and bounding features without manual masking.

## Q72: What is the difference between `df.diff` and `df.shift`?
**A:** `df.shift(periods=1)` moves values up/down by N positions, leaving NaN where data is unavailable (no computation). `df.diff(periods=1)` computes the difference between current and shifted values (`x - x.shift(1)`). `shift` preserves values; `diff` computes period-over-period change. Related: `df.pct_change()` gives percentage change.

## Q73: How do you compute cumulative operations?
**A:** `df.cumsum()`, `df.cummax()`, `df.cummin()`, `df.cumprod()` compute running totals/extrema/products down each column. Useful for running balances, cumulative revenue, and ranking. Combined with `groupby().cumsum()` you get per-group cumulative sums.

## Q74: What is the difference between `nlargest`/`nsmallest` and `sort_values`?
**A:** `df.nlargest(n, 'col')` / `df.nsmallest(n, 'col')` return the top/bottom n rows by a column efficiently (uses partial sort, faster than full `sort_values`). `sort_values().head(n)` gives the same result but sorts everything. Use `nlargest`/`nsmallest` for quick top-k extraction.

## Q75: What is `df.crosstab`?
**A:** `pd.crosstab(index=df['a'], columns=df['b'])` computes a frequency contingency table (counts) of two or more factors. Supports `aggfunc`, `margins=True`, `normalize=True` (row/col/total proportions). Conceptually similar to `pivot_table` with a count aggregation but optimized for categorical cross-tabulation.

## Q76: What is `df.melt` used for?
**A:** `pd.melt(df, id_vars=['id'], value_vars=['a','b'], var_name='metric', value_name='value')` unpivots wide data into long format — turning columns into rows. Inverse of `pivot`/`pivot_table`. Essential for tidy data preparation before plotting (e.g., with `seaborn`) and time-series reshaping.

## Q77: How do you use `groupby` with `filter`?
**A:** `df.groupby('cat').filter(lambda g: len(g) > 5)` keeps only groups satisfying a condition (returns a DataFrame with the same columns). Unlike `agg`/`transform`, `filter` returns original rows, not aggregates. Useful for removing small groups or selecting groups by a computed property.

## Q78: What is the difference between `groupby` and `resample` for time series?
**A:** `groupby` groups by arbitrary column values (including time buckets you compute manually). `resample` groups by fixed calendar/clock frequencies ('D', 'M', 'H') on a DatetimeIndex — it's essentially a time-aware groupby. `resample` is more convenient for evenly spaced temporal aggregation and supports `.rolling` after.

## Q79: How do you use `df.pipe`?
**A:** `df.pipe(func, *args, **kwargs)` applies a function to the DataFrame as its first argument, enabling clean method chaining with functions that aren't DataFrame methods. Example: `df.pipe(clean_data, drop_cols=['x']).pipe(add_features)`. Reads left-to-right and composes reusable transforms.

## Q80: What is `df.explode`?
**A:** `df.explode('col')` transforms each list-like element in a column into a separate row, replicating the other column values. Useful for normalizing JSON/list columns into one-element-per-row form. Inverse of an aggregation that produced lists.

## Q81: What is the difference between `df.combine_first` and `df.update`?
**A:** `df.combine_first(other)` fills missing values in `df` with values from `other` (returns a new DataFrame, non-destructive). `df.update(other)` modifies `df` in place, overwriting existing values (not just NaN) with `other`'s values where indexes align. Use `combine_first` for safe fill; `update` for overwrite.

## Q82: How do you use `df.reindex`?
**A:** `df.reindex(new_index)` conforms the DataFrame to a new index, introducing NaN for missing labels and dropping unmatched ones. Supports `columns=` to reindex columns, `method='ffill'/'bfill'` to fill, and `fill_value`. Useful for aligning two datasets to a common axis before operations.

## Q83: What is the difference between `df.align` and `df.reindex`?
**A:** `df.align(other, join='outer')` returns a tuple of both objects reindexed to a common index/columns (non-destructive, aligns both). `reindex` changes only the calling object to a specified index. `align` is convenient when you need both frames on the same axes for arithmetic.

## Q84: How do you handle mixed dtypes with `convert_dtypes`?
**A:** `df.convert_dtypes()` infers and converts columns to the best nullable dtype (e.g., `Int64`, `string`, `boolean`, `Float64`) that supports `<NA>` instead of object/NaN. This gives proper type support for missing values and is recommended after reading messy CSV/JSON data.

## Q85: What is the difference between `astype('category')` and `astype('string')`?
**A:** `astype('category')` converts to a Categorical storing integer codes + a category list — best for low-cardinality repetitive string columns (memory + speed). `astype('string')` converts to the new `StringDtype` for proper NA-aware string handling — best for free-text or high-cardinality columns. Choose based on cardinality.

## Q86: How do you use `df.style`?
**A:** `df.style` returns a Styler for conditional formatting in Jupyter: `df.style.background_gradient(cmap='coolwarm')`, `.highlight_max()`, `.format('{:.2f}')`, `.bar()`. Output is HTML/CSS for notebooks and can be exported via `df.to_html()` or `df.style.to_excel()`. Not for data transformation — presentation only.

## Q87: How do you plot directly from a DataFrame?
**A:** `df.plot()` (uses matplotlib) produces line plots; `df.plot.bar()`, `.hist()`, `.box()`, `.scatter(x, y)`, `.area()` for others. `df.plot(kind='...')` selects the type. Requires matplotlib installed. For interactive plots prefer Plotly/`df.plot()` with the Plotly backend. Great for quick EDA.

## Q88: What is the difference between `df.to_csv` parameters `index` and `header`?
**A:** `index=False` avoids writing the row index to the file (set True to keep it). `header=False` avoids writing column names. Other useful params: `sep`, `encoding='utf-8'`, `na_rep='NaN'`, `compression='gzip'`, `quoting`, `float_format`. Always set `index=False` when the index isn't meaningful to avoid extra columns on reload.

## Q89: How do you write to Parquet and why?
**A:** `df.to_parquet('file.parquet')` and `pd.read_parquet('file.parquet')` use the columnar Parquet format — fast, compressed, and preserving dtypes (including categorical and datetime) far better than CSV. Requires `pyarrow` or `fastparquet`. Preferred for large datasets and ML pipelines.

## Q90: What is `pd.to_datetime` and parsing pitfalls?
**A:** `pd.to_datetime(series)` converts to datetime; `errors='coerce'` turns unparseable values into NaT. Pitfalls: ambiguous day-first formats — set `format='%d/%m/%Y'` or `dayfirst=True`. For mixed formats use `format='mixed'`. UTC: pass `utc=True` to return timezone-aware UTC. `infer_datetime_format` was removed in 2.0 — always specify `format` for speed.

## Q91: How do you extract components from datetime columns?
**A:** Via the `.dt` accessor: `dt.year`, `dt.month`, `dt.day`, `dt.hour`, `dt.minute`, `dt.second`, `dt.dayofweek`/`dt.weekday`, `dt.dayofyear`, `dt.quarter`, `dt.is_leap_year`, `dt.days_in_month`, `dt.day_name()`, `dt.month_name()`, `dt.date`, `dt.time`, `dt.floor('D')`. All vectorized on datetime Series.

## Q92: What is the difference between `df.fillna` with method and `interpolate`?
**A:** `fillna(method='ffill')` copies the last valid value forward (or `bfill` backward) — flat steps. `df.interpolate()` estimates missing values by linear (or other) interpolation between neighbors — smoother and more realistic for numeric/time series. Use `interpolate` for trends; `ffill/bfill` for categorical/status data.

## Q93: How do you use `df.groupby` with multiple aggregation levels (`NamedAgg`)?
**A:** `df.groupby('cat').agg(avg=('val', 'mean'), total=('val', 'sum'), n=('val', 'size'))` produces columns named `avg`, `total`, `n` via `NamedAgg`. Cleaner than passing a dict of lists and easier to read. Supports any valid aggregation string or callable. Available since Pandas 0.25.

## Q94: What is the difference between `df.drop` and `df.pop`?
**A:** `df.drop('col', axis=1)` removes columns (or rows via `axis=0`) and returns a new DataFrame by default (or in place with `inplace=True`). `df.pop('col')` removes and returns the column as a Series in one operation (mutates the DataFrame). Use `pop` when you need the removed column's values.

## Q95: How do you apply a function element-wise with `applymap`/`map` on a DataFrame?
**A:** `df.map(func)` (Pandas 2.1+, replaces deprecated `applymap`) applies `func` to every element. `df['col'].map(func)` applies to a Series. For row/column-wise (not element-wise) use `df.apply(func, axis=...)`. For performance, prefer vectorized operations (e.g., `df * 2`) over `map`.

## Q96: What is copy-on-write (CoW) and how does it affect Pandas 3.0?
**A:** Copy-on-write is a mode (default in Pandas 3.0) where chained assignments no longer trigger `SettingWithCopyWarning` because operations like slicing return true copies lazily. It makes behavior predictable: `df2 = df[mask]` won't reflect later mutations to `df`. Enable with `pd.set_option('mode.copy_on_write', True)` in 2.x.

## Q97: How do you handle duplicate index values?
**A:** Duplicate index labels are allowed in Pandas. `df.loc['dup']` returns a DataFrame/series for all matches. To find: `df.index.duplicated()`. To make unique: `df[~df.index.duplicated()]` (keep first) or `df.reset_index()`. Be careful: `loc` with duplicate labels can be ambiguous — prefer unique indexes or `reset_index(drop=True)`.

## Q98: What is the difference between `df.compare` and subtraction?
**A:** `df.compare(other)` returns a DataFrame showing only the differing cells with `self`/`other` columns (clear diff view). Plain subtraction `df - other` returns element-wise differences (NaN where both NaN). `compare` is for auditing changes between two aligned DataFrames; subtraction is for numeric deltas.

## Q99: How do you set display options for large DataFrames?
**A:** `pd.set_option('display.max_rows', 100)`, `'display.max_columns'`, `'display.width'`, `'display.max_colwidth'`, `'display.float_format'`. Reset with `pd.reset_option('all')`. Useful in notebooks/CLIs to preview full frames without truncation. Also `df.head()`/`pd.option_context(...)` for temporary changes.

## Q100: What are the latest features in modern Pandas (2.0+)?
**A:** Pandas 2.0+: PyArrow backend (`mode.dtype_backend='pyarrow'`), nullable dtypes by default, improved copy-on-write, improved NA support, better Parquet/Feather support, and performance improvements. Also: `df.map` for element-wise DataFrame ops, `StringDtype` storage options, `convert_dtypes`, `pd.read_csv(..., dtype_backend='pyarrow')`, and deprecation of `append`. Pandas 3.0 makes copy-on-write the default.
