# NumPy Interview Questions and Answers (Top 100)

## Q1: What is NumPy?
**A:** NumPy (Numerical Python) is a fundamental Python library for numerical computing. It provides: multi-dimensional array objects (`ndarray`), fast vectorized operations, mathematical functions, linear algebra, random number generation, and Fourier transforms. NumPy arrays are more efficient than Python lists for numerical data due to contiguous memory storage and C-level optimizations.
**Code:**
```python
import numpy as np
arr = np.array([1, 2, 3])
print(arr * 2)        # [2 4 6] - vectorized operation
print(arr.sum())      # 6
```

## Q2: What is a NumPy ndarray?
**A:** `ndarray` is the core NumPy object — a multi-dimensional, homogeneous array of fixed-size items. Key attributes: `ndim` (number of dimensions), `shape` (tuple of dimension sizes), `size` (total elements), `dtype` (data type), `itemsize` (bytes per element), `nbytes` (total bytes), `T` (transpose).
**Code:**
```python
import numpy as np
a = np.zeros((3, 4))
print(a.ndim, a.shape, a.size, a.dtype)
print(a.itemsize, a.nbytes, a.T.shape)
```

## Q3: What is the difference between `np.array` and `np.asarray`?
**A:** Both create arrays. `np.array` always creates a new array (copies data). `np.asarray` creates an array from the input; if the input is already an ndarray, it returns it without copying (no copy if possible). Use `np.asarray` for memory efficiency when the input might already be an array.
**Code:**
```python
import numpy as np
x = np.array([1, 2, 3])
a = np.array(x)     # always copies
b = np.asarray(x)   # reuses x, no copy
print(a is x, b is x, np.shares_memory(x, b))
```

## Q4: What is the difference between NumPy arrays and Python lists?
**A:** NumPy arrays: homogeneous (single dtype), contiguous memory, fast vectorized operations, support broadcasting, consume less memory, provide element-wise operations by default. Python lists: heterogeneous, store object references, slower for numerical operations, no broadcasting, more flexible for mixed data types.
**Code:**
```python
import numpy as np
lst = [1, 2, 3, 4]
arr = np.array(lst)
print(arr * 2)          # element-wise: [2 4 6 8]
# lst * 2 would repeat the list, not multiply elements
print(arr.nbytes, lst)
```

## Q5: How do you create NumPy arrays?
**A:** Common methods: `np.array([1, 2, 3])` from list, `np.zeros((3, 4))` all zeros, `np.ones((2, 3))` all ones, `np.full((2, 2), 7)` constant value, `np.eye(3)` identity, `np.arange(0, 10, 2)` range, `np.linspace(0, 1, 5)` evenly spaced, `np.random.rand(3, 3)` uniform random, `np.random.randn()` normal distribution.
**Code:**
```python
import numpy as np
print(np.zeros((2, 2)))
print(np.ones(3), np.full(3, 7), np.eye(2))
print(np.arange(0, 10, 2), np.linspace(0, 1, 5))
```

## Q6: What is the difference between `np.arange` and `np.linspace`?
**A:** `np.arange(start, stop, step)` returns evenly spaced values within an interval defined by a step size (like Python's `range` but returns an array). `np.linspace(start, stop, num)` returns a fixed number of evenly spaced samples over an interval, and by default **includes** the stop value. Use `arange` for integer-like steps; use `linspace` when you need an exact count of points or non-integer spacing.
**Code:**
```python
import numpy as np
print(np.arange(0, 1, 0.25))    # [0.   0.25 0.5  0.75] - step governs
print(np.linspace(0, 1, 5))     # [0.   0.25 0.5  0.75 1.  ] - count governs
```

## Q7: How do you specify and convert data types in NumPy?
**A:** Specify at creation: `np.array([1, 2], dtype=np.float64)`. Convert: `arr.astype(np.int32)`. Common dtypes: `int8/16/32/64`, `float16/32/64`, `complex64/128`, `bool`, `object`, `datetime64`. `astype` always returns a copy (unless the dtype is identical). Use `np.can_cast(from, to)` to check safe casting.
**Code:**
```python
import numpy as np
a = np.array([1, 2], dtype=np.float64)
b = a.astype(np.int32)
print(a.dtype, b.dtype, np.can_cast(a.dtype, b.dtype))
```

## Q8: How do you index NumPy arrays?
**A:** Methods: basic indexing `arr[0, 1]`, slicing `arr[1:3, :2]`, fancy indexing `arr[[0, 2], [1, 3]]` (integer arrays), boolean indexing `arr[arr > 5]`, and slicing with steps `arr[::2]`. Slicing returns views (not copies) — modifications affect the original. Fancy and boolean indexing return copies.
**Code:**
```python
import numpy as np
arr = np.arange(12).reshape(3, 4)
print(arr[0, 1])               # basic
print(arr[1:3, :2])            # slicing
print(arr[[0, 2], [1, 3]])     # fancy
print(arr[arr > 5])            # boolean
print(arr[::2])
```

## Q9: What is the difference between a view and a copy in NumPy?
**A:** A view shares data with the original array (no memory duplication). A copy has its own memory. Slicing (`arr[1:3]`) returns a view. Fancy indexing (`arr[[0, 1]]`), boolean indexing, and `.copy()` return copies. Use `np.shares_memory(a, b)` to check. Views mutate the original; copies don't. Use `.copy()` to explicitly create a copy.
**Code:**
```python
import numpy as np
a = np.arange(5)
view = a[1:3]       # view - shares memory
copy = a[[0, 1]]    # copy
view[0] = 99
print(a, copy, np.shares_memory(a, view))
```

## Q10: What is array broadcasting in NumPy?
**A:** Broadcasting allows arithmetic between arrays of different shapes. NumPy "stretches" smaller arrays to match larger ones without copying data. Rules: 1) Trailing dimensions must match or be 1, 2) Arrays are compatible if dimension sizes match or one is 1, 3) 1-sized dimensions are broadcast to match. Example: `(3,1) + (3,) → (3,3) + (3,1) → (3,3)`.
**Code:**
```python
import numpy as np
a = np.ones((3, 1))
b = np.arange(3)
print(a.shape, b.shape)
print(a + b)          # (3,1) + (3,) -> (3,3)
```

## Q11: What is vectorization in NumPy?
**A:** Vectorization replaces explicit loops with array operations that execute in C. Example: `result = a + b` instead of `for i in range(len(a)): result[i] = a[i] + b[i]`. Benefits: faster execution (10-100x), cleaner code, and utilizes low-level optimizations (SIMD, BLAS). Most NumPy operations and universal functions (ufuncs) are vectorized.
**Code:**
```python
import numpy as np
a = np.arange(1000)
b = np.arange(1000)
result = a + b                      # vectorized, runs in C
print(result.sum())
```

## Q12: What are universal functions (ufuncs) in NumPy?
**A:** Ufuncs are functions that operate element-wise on arrays with broadcasting support. Examples: arithmetic (`np.add`, `np.subtract`, `np.multiply`), trigonometry (`np.sin`, `np.cos`), exponentials (`np.exp`, `np.log`, `np.sqrt`), comparisons (`np.greater`, `np.equal`), and reductions (`np.sum`, `np.mean`, `np.max`). Ufuncs have `reduce()`, `accumulate()`, `outer()` methods.
**Code:**
```python
import numpy as np
x = np.array([1, 4, 9])
print(np.sqrt(x))         # element-wise
print(np.add.reduce(x))   # 14
print(np.multiply.outer([1, 2], [3, 4]))
```

## Q13: How do you reshape arrays in NumPy?
**A:** `arr.reshape(new_shape)` returns a new view (if contiguous) with the specified shape. `arr.resize(new_shape)` modifies in-place. `np.ravel()` flattens to 1D (returns view if possible). `arr.flatten()` returns a 1D copy. `arr.T` transposes. `np.newaxis` adds a dimension: `arr[:, np.newaxis]`. `np.expand_dims(arr, axis=0)`.
**Code:**
```python
import numpy as np
a = np.arange(6)
print(a.reshape(2, 3))
print(a.reshape(-1, 1).shape)     # (6, 1)
print(a.ravel(), a.reshape(2, 3).T)
```

## Q14: What is the difference between `ravel`, `flatten`, and `reshape(-1)`?
**A:** `ravel()` returns a 1D view (no copy if possible) of the array — memory efficient. `flatten()` returns a 1D copy — always allocates new memory. `reshape(-1)` is similar to `ravel` — infers the dimension from array size. Prefer `ravel()` or `reshape(-1)` for efficiency; use `flatten()` when you need an independent copy.
**Code:**
```python
import numpy as np
a = np.arange(6).reshape(2, 3)
r = a.ravel()          # view
f = a.flatten()        # copy
r[0] = 99
print(a[0, 0], f[0], np.shares_memory(a, r), np.shares_memory(a, f))
print(a.reshape(-1))
```

## Q15: How do you transpose and swap axes?
**A:** `arr.T` transposes (reverses axes). `np.transpose(arr)` same as `.T`. `np.swapaxes(arr, axis1, axis2)` swaps two specific axes. For a 2D array `arr.T` is the matrix transpose. For 3D, `.T` reverses all axes; use `swapaxes` or `transpose(perm)` to control ordering.
**Code:**
```python
import numpy as np
a = np.arange(6).reshape(2, 3)
print(a.T)
b = np.arange(24).reshape(2, 3, 4)
print(b.shape, b.swapaxes(0, 2).shape, b.transpose(2, 1, 0).shape)
```

## Q16: How do you concatenate and stack arrays?
**A:** `np.concatenate((a, b), axis=0)` joins along existing axis. `np.vstack((a, b))` stacks vertically (row-wise). `np.hstack((a, b))` stacks horizontally (column-wise). `np.dstack((a, b))` depth-wise. `np.stack((a, b), axis=0)` creates new axis. All require same shape except along the concatenation axis.
**Code:**
```python
import numpy as np
a = np.ones((2, 2)); b = np.zeros((2, 2))
print(np.concatenate((a, b), axis=0).shape)   # (4, 2)
print(np.vstack((a, b)).shape, np.hstack((a, b)).shape)
print(np.stack((a, b), axis=0).shape)         # (2, 2, 2)
```

## Q17: What is the difference between `np.concatenate` and `np.stack`?
**A:** `np.concatenate` joins arrays along an existing axis — no new dimensions created. `np.stack` joins arrays along a new axis — adds a dimension. Example: 2 arrays of shape (3, 4): `concat` → (6, 4), `stack` → (2, 3, 4). Use `concatenate` for extending, `stack` for creating batches/channels.
**Code:**
```python
import numpy as np
a = np.zeros((3, 4)); b = np.ones((3, 4))
print(np.concatenate((a, b), axis=0).shape)   # (6, 4)
print(np.stack((a, b), axis=0).shape)         # (2, 3, 4)
```

## Q18: What is the difference between `vstack`, `hstack`, and `column_stack`?
**A:** `vstack` stacks row-wise (along axis 0), `hstack` stacks column-wise (along axis 1) for 2D arrays. `np.column_stack` stacks 1D arrays as columns into a 2D array (like `hstack` but automatically promotes 1D inputs to columns). `np.c_[a, b]` is a shortcut for `column_stack`. For 1D inputs, `hstack` flattens them — use `column_stack` or `vstack` with `.T` instead.
**Code:**
```python
import numpy as np
a = np.array([1, 2, 3]); b = np.array([4, 5, 6])
print(np.vstack((a, b)))           # [[1 2 3] [4 5 6]]
print(np.hstack((a, b)))           # [1 2 3 4 5 6] - flattened
print(np.column_stack((a, b)))     # [[1 4] [2 5] [3 6]]
```

## Q19: How do you split arrays?
**A:** `np.split(arr, indices)` splits at given indices, `np.hsplit(arr, n)` splits horizontally (columns), `np.vsplit(arr, n)` splits vertically (rows), `np.dsplit` for depth. You can pass an integer (equal sections) or a list of indices. Sections must divide evenly when using an integer count.
**Code:**
```python
import numpy as np
a = np.arange(10)
print(np.split(a, [2, 5]))                 # list of indices
print(np.hsplit(np.arange(8).reshape(2, 4), 2))  # equal columns
```

## Q20: What is the difference between `np.tile` and `np.repeat`?
**A:** `np.tile(arr, reps)` repeats the whole array as a tiling pattern (broadcasts the array block). `np.repeat(arr, n)` repeats each element individually. Example: `repeat([1,2], 2) → [1,1,2,2]`; `tile([1,2], 2) → [1,2,1,2]`.
**Code:**
```python
import numpy as np
print(np.repeat([1, 2], 2))   # [1 1 2 2] - element-wise
print(np.tile([1, 2], 2))     # [1 2 1 2] - whole-array tiling
```

## Q21: How do you use `np.clip`?
**A:** `np.clip(arr, min, max)` limits array values to a range, element-wise. Values below `min` become `min`, above `max` become `max`. Useful for capping outliers, image brightness, and bounding probabilities: `np.clip(probs, 0, 1)`.
**Code:**
```python
import numpy as np
print(np.clip(np.array([-5, 0, 3, 10]), 0, 5))   # [0 0 3 5]
```

## Q22: What are the rounding functions in NumPy?
**A:** `np.round(arr, decimals)` (alias `np.around`) rounds to given decimals. `np.floor` rounds down, `np.ceil` rounds up, `np.trunc` truncates toward zero, `np.rint` rounds to nearest integer. Note: `np.round` uses "round half to even" (banker's rounding), not always round-half-up.
**Code:**
```python
import numpy as np
x = np.array([1.4, 1.5, 2.5, -1.2])
print(np.round(x))        # [1. 2. 2. -1.] (half to even)
print(np.floor(x), np.ceil(x), np.trunc(x), np.rint(x))
```

## Q23: What mathematical functions does NumPy provide?
**A:** `np.exp`, `np.log`, `np.log10`, `np.log2`, `np.sqrt`, `np.square`, `np.power(a, b)`, `np.abs` (absolute value), `np.sign`, `np.reciprocal`, and trigonometric functions `np.sin/cos/tan`, `np.arcsin`, etc. These are all vectorized ufuncs operating element-wise.
**Code:**
```python
import numpy as np
x = np.array([1, 4, 9])
print(np.sqrt(x), np.log(np.array([1, np.e])))
print(np.power(x, 2), np.sin(np.array([0.0, np.pi / 2])))
```

## Q24: How do you compute sums, products, and cumulative operations?
**A:** `np.sum(arr)`, `np.prod(arr)` (product), `np.cumsum(arr)` (cumulative sum), `np.cumprod(arr)` (cumulative product), `np.diff(arr)` (differences between adjacent elements). All support the `axis` parameter for row/column-wise computation.
**Code:**
```python
import numpy as np
a = np.array([[1, 2], [3, 4]])
print(np.sum(a), np.prod(a))          # 10 24
print(np.cumsum(a), np.cumprod(a))    # [1 3 6 10] [1 2 6 24]
print(np.diff(a))
```

## Q25: What does the `axis` parameter mean in NumPy reductions?
**A:** `axis` specifies the dimension along which the operation is performed (and removed from the result). For a 2D array, `axis=0` collapses rows (column-wise result), `axis=1` collapses columns (row-wise result). Omitting `axis` flattens the array first. `keepdims=True` keeps the reduced dimension as size 1 for broadcasting.
**Code:**
```python
import numpy as np
a = np.array([[1, 2, 3], [4, 5, 6]])
print(a.sum(axis=0))           # [5 7 9] - column sums
print(a.sum(axis=1))           # [6 15]  - row sums
print(a.sum())                 # 21 - flattened
print(a.max(axis=1, keepdims=True))
```

## Q26: How do you compute mean, median, and standard deviation?
**A:** `np.mean(arr)`, `np.median(arr)`, `np.std(arr)`, `np.var(arr)`. `std` and `var` use population (ddof=0) by default; pass `ddof=1` for sample standard deviation. All accept `axis`. `np.average(arr, weights=...)` computes a weighted mean.
**Code:**
```python
import numpy as np
x = np.array([1, 2, 3, 4])
print(np.mean(x), np.median(x), np.std(x), np.var(x))
print(np.std(x, ddof=1))
print(np.average(x, weights=[0.1, 0.2, 0.3, 0.4]))
```

## Q27: What is the difference between percentile and quantile?
**A:** `np.percentile(arr, q)` takes q in [0, 100]; `np.quantile(arr, q)` takes q in [0, 1] (quantile = percentile / 100). Both compute cutoff values below which a given fraction of observations fall. `np.median` equals `np.quantile(arr, 0.5)`.
**Code:**
```python
import numpy as np
x = np.arange(1, 101)
print(np.percentile(x, 50))    # 50.5
print(np.quantile(x, 0.5))     # 50.5
print(np.median(x))            # 50.5 - same thing
```

## Q28: How do you find min, max, and their indices?
**A:** `np.min(arr)`, `np.max(arr)`, `np.argmin(arr)` (index of min), `np.argmax(arr)` (index of max). `np.nanargmin`/`np.nanargmax` ignore NaN. For multiple: `np.partition(arr, k)` partially sorts, and `np.argpartition(arr, k)` returns indices of the k smallest — efficient for top-k without full sort.
**Code:**
```python
import numpy as np
a = np.array([[3, 1], [7, 5]])
print(np.min(a), np.max(a), np.argmin(a), np.argmax(a))
print(np.argpartition(a.ravel(), 1)[:2])   # indices of 2 smallest
```

## Q29: How do you sort arrays?
**A:** `np.sort(arr)` returns a sorted copy; `arr.sort()` sorts in place. `np.argsort(arr)` returns indices that would sort the array (use to sort parallel arrays). `np.lexsort(keys)` sorts by multiple keys. `np.partition(arr, k)` places the kth element in its sorted position with smaller to the left — faster than full sort when you only need order statistics.
**Code:**
```python
import numpy as np
a = np.array([3, 1, 2])
print(np.sort(a), a)            # copy; original unchanged
a.sort(); print(a)              # in place
print(np.argsort([3, 1, 2]))    # [1 2 0]
```

## Q30: How do you handle missing values (NaN) in NumPy?
**A:** NumPy uses `np.nan` (Not a Number) for missing float values. Functions: `np.isnan(arr)` detect NaN, `np.nanmean()`, `np.nansum()`, `np.nanmax()` — skip NaN. For non-float types, consider masked arrays (`np.ma.masked_array`) or use Pandas. NaN has properties: `np.nan == np.nan` is False, use `np.isnan()` for detection.
**Code:**
```python
import numpy as np
a = np.array([1.0, np.nan, 3.0])
print(np.isnan(a))
print(np.nanmean(a), np.nansum(a))
```

## Q31: What is the difference between `np.any` and `np.all`?
**A:** `np.any(arr)` returns True if any element is truthy. `np.all(arr)` returns True if all elements are truthy. Both support `axis` parameter: `np.any(arr > 0, axis=1)` checks each row. Short-circuit evaluation doesn't apply — the entire array is always evaluated. Use for condition checking in boolean arrays.
**Code:**
```python
import numpy as np
a = np.array([[1, 0], [0, 0]])
print(np.any(a), np.all(a))
print(np.any(a, axis=1), np.all(a, axis=1))
```

## Q32: What is the difference between `np.allclose` and `np.isclose`?
**A:** `np.isclose(a, b)` returns a boolean array of element-wise closeness (within `rtol`/`atol` tolerances). `np.allclose(a, b)` returns a single boolean — True if all elements are close. Useful for comparing floats where exact equality (`==`) fails due to floating-point error.
**Code:**
```python
import numpy as np
a = np.array([0.1, 0.2]); b = np.array([0.1 + 1e-9, 0.2])
print(np.isclose(a, b))      # [ True  True]
print(np.allclose(a, b))     # True
```

## Q33: How do you detect infinity and finite values?
**A:** `np.isinf(arr)` detects ±infinity, `np.isfinite(arr)` detects finite (non-NaN, non-inf) values, `np.isneginf`/`np.isposinf` for signed infinity. `np.nan_to_num(arr)` replaces NaN with 0 and inf with large finite values (useful before passing to functions that can't handle them).
**Code:**
```python
import numpy as np
x = np.array([1.0, np.inf, -np.inf, np.nan])
print(np.isinf(x), np.isfinite(x))
print(np.nan_to_num(x))
```

## Q34: What are NumPy's set operations?
**A:** `np.unique(arr)` — sorted unique values. `np.in1d(a, b)` — membership check. `np.intersect1d(a, b)` — intersection. `np.union1d(a, b)` — union. `np.setdiff1d(a, b)` — difference. `np.setxor1d(a, b)` — symmetric difference. All return sorted arrays. `assume_unique=True` for performance if inputs have unique elements.
**Code:**
```python
import numpy as np
a = np.array([1, 2, 3, 3]); b = np.array([2, 3, 4])
print(np.unique(a), np.intersect1d(a, b), np.union1d(a, b))
print(np.setdiff1d(a, b), np.setxor1d(a, b), np.isin(a, b))
```

## Q35: What extra outputs does `np.unique` support?
**A:** `np.unique(arr, return_index=True)` returns indices of first occurrences, `return_inverse=True` returns indices to reconstruct the original, `return_counts=True` returns frequency counts. These are handy for label encoding, grouping, and reversing a unique operation.
**Code:**
```python
import numpy as np
u, idx, inv, cnt = np.unique([3, 1, 2, 1], return_index=True,
                             return_inverse=True, return_counts=True)
print(u, idx, inv, cnt)
print(u[inv])      # reconstruct the original array
```

## Q36: How do you use `np.searchsorted`?
**A:** `np.searchsorted(sorted_arr, values)` returns insertion indices that keep `sorted_arr` sorted. Useful for fast lookups, binning, and finding bucket boundaries. `side='left'`/`'right'` controls behavior on ties. Requires the array to be sorted for correct results.
**Code:**
```python
import numpy as np
bins = np.array([10, 20, 30, 40])
print(np.searchsorted(bins, 25))            # 2
print(np.searchsorted(bins, [5, 30, 50]))   # [0 2 4]
```

## Q37: What is `np.digitize` used for?
**A:** `np.digitize(x, bins)` returns the index of the bin each value of `x` falls into, given monotonically increasing `bins`. Returns 0 if below the first bin, `len(bins)` if above the last. Related to `pd.cut` in Pandas, but pure NumPy and returns integer codes.
**Code:**
```python
import numpy as np
bins = np.array([0, 5, 10])
print(np.digitize([1, 6, 12, -2], bins))    # [1 2 3 0]
```

## Q38: How do you compute histograms and counts?
**A:** `np.histogram(arr, bins)` returns (counts, bin_edges). `np.bincount(arr)` counts non-negative integer occurrences (fast, returns array where index = value). `np.bincount` with `weights` computes weighted sums per bin. Use `np.digitize` + `bincount` for custom binning.
**Code:**
```python
import numpy as np
x = np.array([0, 1, 1, 2, 2, 2])
print(np.histogram(x, bins=3))
print(np.bincount(x))                       # [1 2 3]
print(np.bincount(x, weights=np.arange(1, 7)))
```

## Q39: How do you use `np.where`?
**A:** `np.where(condition)` returns indices where condition is True: `np.where(arr > 5)` returns tuple of arrays (one per dimension). `np.where(condition, x, y)` returns elements from x where True, y where False: `np.where(arr > 0, arr, 0)` replaces negative values with 0. Useful for conditional replacement and bulk operations.
**Code:**
```python
import numpy as np
arr = np.array([-1, 2, -3, 4])
print(np.where(arr < 0))            # (array([0, 2]),)
print(np.where(arr < 0, 0, arr))    # [0 2 0 4]
```

## Q40: What is the difference between `np.select` and `np.where`?
**A:** `np.where` handles a single condition (binary if-else). `np.select(condlist, choicelist, default=0)` handles multiple conditions (if-elif-else). Each condition in condlist is a boolean array; the first True condition's choice is selected. Useful for multi-case categorization (e.g., age groups: child, adult, senior).
**Code:**
```python
import numpy as np
ages = np.array([10, 25, 60, 15])
conds = [ages < 18, ages < 60, ages >= 60]
choices = ['child', 'adult', 'senior']
print(np.select(conds, choices, default='unknown'))
```

## Q41: How do you find nonzero and specific indices?
**A:** `np.nonzero(arr)` returns a tuple of indices where arr is nonzero (equivalent to `np.where(arr != 0)`). `np.argwhere(condition)` returns an (N, ndim) array of coordinates. `np.flatnonzero` returns flat indices. These are frequently used to extract positions of matches.
**Code:**
```python
import numpy as np
a = np.array([[1, 0], [0, 3]])
print(np.nonzero(a))
print(np.argwhere(a > 0))
print(np.flatnonzero(a))
```

## Q42: What is the difference between `np.take` and fancy indexing?
**A:** `np.take(arr, indices, axis)` selects elements along an axis using integer indices — often faster and supports out-of-bounds handling via `mode`. Fancy indexing `arr[indices]` is more general (multi-axis) but can be slower. `np.compress(condition, arr, axis)` selects elements where a boolean condition is True along an axis.
**Code:**
```python
import numpy as np
a = np.arange(10)
print(np.take(a, [0, 1, 5]))
print(a[[0, 1, 5]])                       # equivalent fancy indexing
print(np.compress([True, False, True], a[:3]))
```

## Q43: How do you use `np.newaxis` and `np.expand_dims`?
**A:** Both add a new dimension to an array. `arr[:, np.newaxis]` adds a dimension at position 1 (shape (3,) → (3, 1)). `np.expand_dims(arr, axis=0)` adds a dimension at position 0 (shape (3,) → (1, 3)). Used for: broadcasting alignment, converting 1D to row/column vector, and adding batch/channel dimensions.
**Code:**
```python
import numpy as np
a = np.arange(3)
print(a[:, np.newaxis].shape)       # (3, 1)
print(np.expand_dims(a, 0).shape)   # (1, 3)
print((a[:, np.newaxis] + a).shape) # broadcasting demo
```

## Q44: What are `np.atleast_1d/2d/3d`?
**A:** They ensure an array has at least the given number of dimensions by prepending size-1 dimensions. `np.atleast_2d(x)` turns a scalar or 1D array into 2D. Useful in functions that must work with inputs of varying dimensionality without manual shape checks.
**Code:**
```python
import numpy as np
x = 5
print(np.atleast_1d(x).shape, np.atleast_2d(x).shape, np.atleast_3d(x).shape)
print(np.atleast_2d(np.array([1, 2, 3])).shape)   # (1, 3)
```

## Q45: How do you pad an array?
**A:** `np.pad(arr, pad_width, mode)` adds padding. `mode='constant'` (fill with `constant_values`), `'edge'` (repeat edge), `'reflect'`, `'symmetric'`, `'wrap'`. `pad_width` can be a scalar, a (before, after) tuple, or per-axis tuples. Common for image and signal preprocessing.
**Code:**
```python
import numpy as np
a = np.array([1, 2, 3])
print(np.pad(a, (1, 2), mode='constant'))   # [0 1 2 3 0 0]
print(np.pad(a, 2, mode='edge'))            # [1 1 1 2 3 3 3]
```

## Q46: How do you work with diagonals and triangular matrices?
**A:** `np.diag(arr)` extracts or creates a diagonal. `np.trace(arr)` sums the diagonal. `np.tri(n)` creates a lower-triangular matrix of ones. `np.tril(arr)`/`np.triu(arr)` return lower/upper triangular parts. `np.fill_diagonal(arr, val)` sets diagonal values in place.
**Code:**
```python
import numpy as np
a = np.arange(9).reshape(3, 3)
print(np.diag(a), np.trace(a))
print(np.tril(a))
print(np.triu(a))
```

## Q47: What is the difference between `np.eye` and `np.identity`?
**A:** `np.identity(n)` creates an n×n square identity matrix. `np.eye(N, M=None, k=0)` creates an identity-like matrix of shape (N, M) with the diagonal offset by `k`. `eye` is more flexible (non-square, off-diagonal), `identity` is a convenience for square ones.
**Code:**
```python
import numpy as np
print(np.identity(2))
print(np.eye(3))
print(np.eye(2, 3, k=1))   # offset diagonal
```

## Q48: How does NumPy handle linear algebra?
**A:** `np.dot(a, b)` — matrix multiplication. `np.linalg.inv(m)` — inverse. `np.linalg.det(m)` — determinant. `np.linalg.eig(m)` — eigenvalues/vectors. `np.linalg.svd(m)` — SVD decomposition. `np.linalg.solve(A, b)` — solve linear system Ax = b. `np.linalg.qr(m)` — QR decomposition. `np.linalg.norm(v)` — vector/matrix norm.
**Code:**
```python
import numpy as np
A = np.array([[1, 2], [3, 4]]); b = np.array([5, 6])
print(np.linalg.inv(A), np.linalg.det(A))
print(np.linalg.eig(A)[0])            # eigenvalues
print(np.linalg.solve(A, b))          # solves A x = b
print(np.linalg.norm([3, 4]))
```

## Q49: What is the difference between `np.dot`, `np.matmul`, and `@`?
**A:** `np.dot(a, b)` — scalar, vector, or matrix multiplication (with broadcasting for higher dimensions). `np.matmul(a, b)` — matrix multiplication only, treats last two dimensions as matrix dimensions (batch matrix multiply). `a @ b` is the infix operator for `np.matmul`. For 2D arrays, all three are equivalent.
**Code:**
```python
import numpy as np
A = np.ones((2, 3)); B = np.ones((3, 2))
print(np.dot(A, B))          # matrix product
print(np.matmul(A, B))
print(A @ B)                 # infix operator
```

## Q50: What is `np.einsum` and when is it useful?
**A:** `np.einsum` performs tensor operations using Einstein summation notation. Example: `np.einsum('ij,jk->ik', A, B)` is matrix multiplication; `'ii->i'` is the diagonal; `'ij->i'` sums rows. It can express dot, trace, transpose, outer, batch matmul concisely and is often faster than chained calls.
**Code:**
```python
import numpy as np
A = np.arange(6).reshape(2, 3); B = np.arange(6).reshape(3, 2)
print(np.einsum('ij,jk->ik', A, B))   # matmul
print(np.einsum('ii->i', np.arange(4).reshape(2, 2)))  # diagonal
print(np.einsum('ij->i', A))          # row sums
```

## Q51: What are `np.tensordot`, `np.inner`, and `np.cross`?
**A:** `np.tensordot(a, b, axes)` sums over specified axes (generalized dot). `np.inner(a, b)` is the inner (dot) product over the last axis. `np.cross(a, b)` computes the vector cross product (3D). `np.outer(a, b)` computes the outer product. Each targets a different tensor contraction pattern.
**Code:**
```python
import numpy as np
print(np.inner([1, 2], [3, 4]))   # 11
print(np.outer([1, 2], [3, 4]))
print(np.cross([1, 0, 0], [0, 1, 0]))   # [0 0 1]
print(np.tensordot(np.ones((2, 3)), np.ones((3, 4)), axes=1).shape)
```

## Q52: How do you solve linear systems and decompose matrices?
**A:** `np.linalg.solve(A, b)` solves Ax = b directly. `np.linalg.lstsq(A, b)` solves least-squares (overdetermined) systems. `np.linalg.cholesky(m)` Cholesky decomposition. `np.linalg.eigh` for Hermitian matrices. `np.linalg.pinv` computes the Moore-Penrose pseudo-inverse.
**Code:**
```python
import numpy as np
A = np.array([[2, 0], [0, 4]]); b = np.array([8, 16])
print(np.linalg.solve(A, b))                      # [4. 4.]
print(np.linalg.lstsq(A, b, rcond=None)[0])
print(np.linalg.pinv(A))
```

## Q53: What are NumPy's FFT functions?
**A:** `np.fft.fft(x)` — 1D Fast Fourier Transform. `np.fft.ifft(X)` — inverse. `np.fft.fft2()` — 2D FFT. `np.fft.fftfreq(n, d=1.0)` — frequency bins. `np.fft.fftshift()` — shift zero frequency to center. Used for: signal processing, spectral analysis, convolution acceleration (multiply in frequency domain).
**Code:**
```python
import numpy as np
x = np.sin(np.linspace(0, 2 * np.pi, 64))
X = np.fft.fft(x)
print(np.fft.ifft(X).real[:4])       # round-trip with noise at float level
print(np.fft.fftfreq(8, d=0.5))
```

## Q54: How do you use NumPy for image processing?
**A:** Images are 3D arrays (height, width, channels). Operations: cropping `img[50:200, 100:300]`, color channel manipulation `img[:, :, 0] = 0` (zero red), brightness `img = np.clip(img + 50, 0, 255)`, flips `np.fliplr(img)`, rotation `np.rot90(img)`, resizing via interpolation (use skimage or OpenCV for quality resizing).
**Code:**
```python
import numpy as np
img = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
crop = img[10:40, 20:60]                          # cropping
bright = np.clip(img.astype(int) + 50, 0, 255)    # brightness
print(img.shape, crop.shape, np.fliplr(img).shape, np.rot90(img).shape)
```

## Q55: What is the difference between `np.save` and `np.savetxt`?
**A:** `np.save('file.npy', arr)` saves a single array in NumPy's binary `.npy` format (fast, lossless, preserves dtype). `np.savetxt('file.csv', arr, delimiter=',')` saves a 2D array as text (slower, larger files, human-readable). `np.savez('file.npz', a=arr1, b=arr2)` saves multiple arrays in compressed format. `np.load()` loads all formats.
**Code:**
```python
import numpy as np
arr = np.arange(6).reshape(2, 3)
np.save('/tmp/arr.npy', arr)
np.savetxt('/tmp/arr.csv', arr, delimiter=',')
print(np.load('/tmp/arr.npy'))
```

## Q56: What are NumPy's polynomial functions?
**A:** `np.polyfit(x, y, deg)` — polynomial regression (least squares). `np.polyval(p, x)` — evaluate polynomial. `np.polyder(p)` — derivative. `np.polyint(p)` — integral. `np.roots(p)` — find roots. `np.polyadd`, `np.polymul`, `np.polydiv` — arithmetic. For modern usage, prefer `np.polynomial.Polynomial` class.
**Code:**
```python
import numpy as np
x = np.array([0, 1, 2, 3]); y = np.array([0, 1.1, 3.9, 9.1])
p = np.polyfit(x, y, 2)
print(p)
print(np.polyval(p, [0, 1]), np.polyder(p), np.polyint(p))
```

## Q57: What are NumPy masked arrays?
**A:** `np.ma.MaskedArray` is an array with a `mask` boolean array indicating invalid/missing entries. Operations automatically skip masked values. Example: `np.ma.array([1, 2, -999, 4], mask=[False, False, True, False]).mean()` returns 2.33. Useful for: bad data points, missing measurements, invalid sensor readings.
**Code:**
```python
import numpy as np
m = np.ma.array([1, 2, -999, 4], mask=[False, False, True, False])
print(m.mean())
```

## Q58: How do you work with structured arrays in NumPy?
**A:** Structured arrays have named fields of different types. Define: `np.dtype([('name', 'U10'), ('age', 'i4'), ('height', 'f8')])`. Create: `np.array([('Alice', 30, 1.7)], dtype=dtype)`. Access: `arr['name']`, `arr['age']`. Filter: `arr[arr['age'] > 25]`. Similar to Pandas DataFrame but lower level and more memory efficient.
**Code:**
```python
import numpy as np
dtype = np.dtype([('name', 'U10'), ('age', 'i4'), ('height', 'f8')])
arr = np.array([('Alice', 30, 1.7), ('Bob', 20, 1.8)], dtype=dtype)
print(arr['name'], arr['age'])
print(arr[arr['age'] > 25])
```

## Q59: What is a `np.recarray`?
**A:** `np.recarray` is a structured array that allows field access via attribute notation (`rec.name` instead of `rec['name']`). Created with `arr.view(np.recarray)`. Convenient but slightly slower than dict-style access; mostly legacy — modern code usually uses `np.lib.recfunctions` or Pandas.
**Code:**
```python
import numpy as np
dtype = np.dtype([('name', 'U10'), ('age', 'i4')])
rec = np.array([('Alice', 30)], dtype=dtype).view(np.recarray)
print(rec.name, rec.age)
```

## Q60: How do you use `np.vectorize`?
**A:** `np.vectorize(func)` wraps a Python scalar function so it can be applied element-wise to arrays (like a ufunc). It is a convenience loop, not true vectorization — it still calls the function per element. Use for broadcasting custom functions; for performance, prefer writing native ufuncs or Numba.
**Code:**
```python
import numpy as np
f = np.vectorize(lambda x: x ** 2 + 1)
print(f(np.array([1, 2, 3])))    # [2 5 10]
```

## Q61: What is `np.fromfunction`?
**A:** `np.fromfunction(func, shape)` constructs an array by calling `func` with coordinate indices as arguments. Example: `np.fromfunction(lambda i, j: i + j, (3, 3))`. Useful for generating grids and matrices based on position without explicit loops.
**Code:**
```python
import numpy as np
a = np.fromfunction(lambda i, j: i + j, (3, 3))
print(a)
```

## Q62: How do you create meshes and grids?
**A:** `np.meshgrid(x, y)` returns coordinate matrices for vectorized evaluation of functions over a grid (useful for plotting). `np.indices(shape)` returns an array of grid indices. For 1D coordinate arrays, `np.meshgrid` produces 2D broadcasting-friendly coordinates.
**Code:**
```python
import numpy as np
x, y = np.meshgrid([0, 1, 2], [0, 1])
print(x)
print(y)
print(x + y)   # functions evaluated over the grid
```

## Q63: How do you compute gradients and convolutions?
**A:** `np.gradient(f, *varargs)` computes the gradient using central differences (N-dimensional). `np.convolve(a, v, mode)` computes the discrete convolution — used for smoothing and signal filtering. For multi-dimensional convolution use SciPy's `convolve2d`/`convolve`.
**Code:**
```python
import numpy as np
x = np.linspace(0, 1, 5)
print(np.gradient(x ** 2))              # numerical derivative
print(np.convolve([1, 2, 3], [1, 1, 1], mode='same'))
```

## Q64: How do you flip and rotate arrays?
**A:** `np.flip(arr, axis)` reverses element order along an axis. `np.fliplr(arr)`/`np.flipud(arr)` flip left-right / up-down (2D). `np.rot90(arr, k)` rotates 90° counterclockwise k times. These are common in image augmentation and matrix manipulation.
**Code:**
```python
import numpy as np
a = np.arange(6).reshape(2, 3)
print(np.flip(a, axis=1))
print(np.fliplr(a))
print(np.flipud(a))
print(np.rot90(a, 1))
```

## Q65: How do you handle floating-point errors in NumPy?
**A:** `np.seterr(all='warn')` configures behavior for divide-by-zero, overflow, underflow, and invalid operations (options: 'ignore', 'warn', 'raise', 'call'). `np.errstate(divide='ignore', invalid='ignore')` is a context manager for temporary settings. `np.nan`/`np.inf` result from invalid math.
**Code:**
```python
import numpy as np
with np.errstate(divide='ignore', invalid='ignore'):
    print(1 / np.array([0.0, 2.0]))           # inf, 0.5
    print(np.sqrt(np.array([-1.0, 4.0])))     # nan, 2.0
```

## Q66: What is `np.memmap`?
**A:** `np.memmap` maps a binary file on disk to a NumPy array interface, allowing out-of-core processing of arrays larger than RAM. Create with `np.memmap('file.dat', dtype='float64', mode='r+', shape=(n, m))`. Operations are lazy and written to disk. Useful for huge datasets without loading everything into memory.
**Code:**
```python
import numpy as np
m = np.memmap('/tmp/mem.dat', dtype='float64', mode='w+', shape=(4, 4))
m[:] = 1.0
m.flush()
print(np.memmap('/tmp/mem.dat', dtype='float64', mode='r', shape=(4, 4))[0, 0])
```

## Q67: What are array strides and `as_strided`?
**A:** Strides are bytes to step in each dimension to reach the next element. `np.lib.stride_tricks.as_strided(arr, shape, strides)` creates a view with custom strides — enabling tricks like sliding windows without copying. Dangerous if misused (can read invalid memory); prefer `sliding_window_view` in NumPy ≥1.20.
**Code:**
```python
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
a = np.arange(10)
print(sliding_window_view(a, 3)[:3])    # overlapping windows, no copies
```

## Q68: How do you insert, append, and delete elements?
**A:** `np.append(arr, values)` (returns new array, flattens if shape mismatched), `np.insert(arr, index, values)` inserts before index, `np.delete(arr, indices)` removes. All return copies — NumPy arrays are fixed-size, so these allocate new memory. Prefer pre-allocating or `concatenate` for performance.
**Code:**
```python
import numpy as np
a = np.array([1, 2, 3])
print(np.append(a, [4, 5]))       # [1 2 3 4 5]
print(np.insert(a, 1, [8, 9]))    # [1 8 9 2 3]
print(np.delete(a, [0, 2]))       # [2]
```

## Q69: What is `np.put` and `np.putmask`?
**A:** `np.put(arr, indices, values)` sets flat (raveled) indices to values in place. `np.putmask(arr, mask, values)` sets elements where `mask` is True to corresponding `values` (in place). Efficient alternatives to fancy-index assignment for bulk in-place edits.
**Code:**
```python
import numpy as np
a = np.array([1, 2, 3, 4])
np.put(a, [0, 2], [9, 9])
print(a)                    # [9 2 9 4]
np.putmask(a, a % 2 == 0, 0)
print(a)                    # [9 0 9 0]
```

## Q70: How do you copy arrays in NumPy?
**A:** `arr.copy()` creates a deep copy with independent memory. `np.copy(arr)` is equivalent. Shallow "copies" don't exist for ndarray data — slicing creates a view (shared memory), not a copy. Always use `.copy()` when you need to modify an array without affecting its source.
**Code:**
```python
import numpy as np
a = np.array([1, 2, 3])
b = a.copy()
b[0] = 99
print(a, b, np.shares_memory(a, b))
```

## Q71: How do you check memory sharing between arrays?
**A:** `np.shares_memory(a, b)` returns True if the two arrays share any memory (e.g., a view). `np.may_share_memory(a, b)` is a faster, less strict check. `arr.flags.owndata` indicates whether the array owns its data. Use these when debugging unexpected mutation through views.
**Code:**
```python
import numpy as np
a = np.arange(6)
v = a[1:3]
print(np.shares_memory(a, v), np.may_share_memory(a, v), v.flags.owndata)
```

## Q72: What is the memory layout of a NumPy array (C vs Fortran order)?
**A:** `order='C'` stores row-major (last index varies fastest); `order='F'` stores column-major (first index varies fastest). `arr.flags['C_CONTIGUOUS']` / `['F_CONTIGUOUS']` report layout. `np.ascontiguousarray(arr)` returns a C-contiguous copy if needed — important for passing to C/Fortran libraries and for performance.
**Code:**
```python
import numpy as np
a = np.zeros((3, 3), order='F')
print(a.flags['C_CONTIGUOUS'], a.flags['F_CONTIGUOUS'])
c = np.ascontiguousarray(a)
print(c.flags['C_CONTIGUOUS'])
```

## Q73: What is `np.ascontiguousarray` used for?
**A:** It returns the input as a C-contiguous array, copying only if necessary. Many C extensions and BLAS routines require contiguous arrays; passing non-contiguous data forces an implicit copy or raises an error. Use it to guarantee layout before expensive operations.
**Code:**
```python
import numpy as np
a = np.arange(9).reshape(3, 3)[:, ::2]      # strided view
print(a.flags['C_CONTIGUOUS'])
c = np.ascontiguousarray(a)
print(c.flags['C_CONTIGUOUS'], np.shares_memory(a, c))
```

## Q74: How do you use NumPy's random module?
**A:** `np.random.rand(3, 3)` — uniform [0,1). `np.random.randn(3, 3)` — standard normal. `np.random.randint(0, 10, size=5)` — integers. `np.random.choice([1,2,3], size=10, p=[0.1, 0.3, 0.6])` — weighted random selection. `np.random.seed(42)` — reproducibility. `np.random.shuffle(arr)` — in-place shuffle. `np.random.permutation(n)` — random order.
**Code:**
```python
import numpy as np
np.random.seed(42)
print(np.random.rand(2, 2))
print(np.random.randint(0, 10, 5))
print(np.random.choice([1, 2, 3], 5, p=[0.1, 0.3, 0.6]))
```

## Q75: What is the difference between `np.random.rand` and `np.random.randn`?
**A:** `np.random.rand(d0, d1, ...)` generates samples from a uniform distribution over [0, 1). `np.random.randn(d0, d1, ...)` generates samples from the standard normal distribution (mean=0, variance=1). `rand` is for uniform random values; `randn` is for Gaussian-distributed values.
**Code:**
```python
import numpy as np
print(np.random.rand(3))    # uniform [0, 1)
print(np.random.randn(3))   # standard normal, may be negative
```

## Q76: What is the difference between `np.random.seed` and `np.random.default_rng`?
**A:** `np.random.seed(n)` sets the legacy global RandomState — not thread-safe and discouraged. `np.random.default_rng(seed)` returns a modern `Generator` (PCG64 algorithm) that is the recommended API. The `Generator` offers `rng.random()`, `rng.normal()`, `rng.integers()`, `rng.choice()`, and better statistical quality.
**Code:**
```python
import numpy as np
np.random.seed(42)                # legacy global RandomState
rng = np.random.default_rng(42)   # recommended Generator
print(rng.random(3))
print(rng.integers(0, 10, 3))
```

## Q77: What distributions does the `Generator` API provide?
**A:** `rng.normal(loc, scale, size)`, `rng.uniform(a, b)`, `rng.integers(low, high, size)`, `rng.poisson(lam)`, `rng.binomial(n, p)`, `rng.exponential(scale)`, `rng.beta(a, b)`, `rng.gamma(shape)`. The modern API replaces legacy `np.random.*` functions and supports streaming `rng.spawn` for parallel streams.
**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
print(rng.normal(loc=0, scale=1, size=3))
print(rng.uniform(-1, 1, 3))
print(rng.integers(0, 10, 3))
print(rng.poisson(lam=3, size=3))
```

## Q78: How do you compute statistics with NumPy?
**A:** `np.mean(arr)`, `np.median(arr)`, `np.std(arr)`, `np.var(arr)`, `np.min(arr)`, `np.max(arr)`, `np.percentile(arr, 75)`, `np.ptp(arr)` (range), `np.corrcoef(x, y)` (correlation), `np.cov(x, y)` (covariance). All support axis parameter: `np.mean(arr, axis=0)` for column means. `np.nanmean()` and similar skip NaN.
**Code:**
```python
import numpy as np
x = np.array([[1, 2, 3], [4, 5, 6]])
print(np.mean(x), np.median(x), np.std(x), np.ptp(x))
print(np.mean(x, axis=0))
print(np.percentile(x, 75), np.corrcoef([1, 2, 3], [2, 4, 6]))
```

## Q79: What is the difference between `np.corrcoef` and `np.cov`?
**A:** `np.cov(x, y)` computes the covariance matrix (measures joint variability). `np.corrcoef(x, y)` computes the Pearson correlation matrix (normalized covariance in [-1, 1]). Correlation = covariance divided by the product of standard deviations. Both accept row-var or column-var oriented inputs.
**Code:**
```python
import numpy as np
x = np.array([1, 2, 3, 4]); y = np.array([2, 4, 6, 8])
print(np.cov(x, y))
print(np.corrcoef(x, y))
```

## Q80: How do you compute pairwise distances with NumPy?
**A:** Euclidean: `np.sqrt(((a - b)**2).sum(axis=1))`. Cosine: `1 - np.dot(a, b.T) / (np.linalg.norm(a) * np.linalg.norm(b))`. For many points, use `scipy.spatial.distance.pdist()` or `sklearn.metrics.pairwise_distances()` (more efficient). Broadcasting approach: `np.linalg.norm(a[:, np.newaxis] - b, axis=2)` computes all pairwise distances.
**Code:**
```python
import numpy as np
a = np.array([[0, 0], [3, 4]])
b = np.array([1, 1])
print(np.sqrt(((a - b) ** 2).sum(axis=1)))              # [1.414 3.606]
pairwise = np.linalg.norm(a[:, np.newaxis, :] - a[np.newaxis, :, :], axis=2)
print(pairwise)
```

## Q81: What are `np.roll`, `np.cumsum`, and their use in circular operations?
**A:** `np.roll(arr, shift)` circularly shifts elements (wraps around) without changing shape. `np.cumsum`/`np.cumprod` produce running totals/products. `roll` is useful for periodic boundary conditions, lag features, and circular convolution; combined with `np.where` you can build shifted comparisons.
**Code:**
```python
import numpy as np
a = np.array([1, 2, 3, 4])
print(np.roll(a, 1))         # [4 1 2 3] - wraps around
print(np.cumsum(a))          # [1 3 6 10]
print(a - np.roll(a, 1))     # shifted comparison
```

## Q82: How does NumPy handle integer overflow?
**A:** Fixed-size integer dtypes (`int32`, `int64`) wrap around on overflow rather than raising errors (e.g., `np.int8(127) + 1 == -128`). Use larger dtypes or Python `int` (object dtype) for arbitrary precision. `np.errstate` does not catch integer overflow — beware when values can exceed dtype range.
**Code:**
```python
import numpy as np
print(np.int8(127) + np.int8(1))          # -128, wraps around silently
print(np.array([127], dtype=np.int8) + 1)
```

## Q83: What is type promotion in NumPy?
**A:** NumPy promotes operands to a common dtype according to well-defined rules (e.g., `int + float → float`, `float32 + float64 → float64`, `int + complex → complex`). NumPy 2.0 introduced the NEP 50 promotion rules (less surprising upcasting from Python scalars). Use `np.result_type(*arrays)` to predict the result dtype.
**Code:**
```python
import numpy as np
print((np.array([1], dtype=np.int32) + 1.5).dtype)
print((np.array([1], dtype=np.float32) + np.array([1], dtype=np.float64)).dtype)
print(np.result_type(np.int32, np.float64))
```

## Q84: What is the difference between NumPy and Pandas?
**A:** NumPy: n-dimensional arrays, homogeneous numeric data, low-level linear algebra, no labeling, no missing data handling in core. Pandas: 2D DataFrames and 1D Series, heterogeneous data, labeled axes (index/columns), rich missing data handling, time series support, SQL-like operations, and I/O for various formats. Pandas is built on NumPy.
**Code:**
```python
import numpy as np
a = np.array([[1, 2], [3, 4]])     # homogeneous, no labels
print(a, a.dtype, a.shape)
print(a[:, 1])                     # column access by position
```

## Q85: When should you use NumPy vs Pandas?
**A:** Use NumPy for numerical/scientific computing, matrix math, simulations, and homogeneous numeric tensors where labels aren't needed. Use Pandas when you need labeled columns, mixed types, missing-data handling, joins, groupby, and I/O from CSV/SQL/Excel. Pandas DataFrames ultimately store column data in NumPy arrays.
**Code:**
```python
import numpy as np
X = np.random.rand(100, 3)             # numeric tensor, labels unnecessary
print(X.shape, X.mean(axis=0))
```

## Q86: What is the difference between NumPy and SciPy?
**A:** NumPy provides the core array object and basic math/linear algebra/random. SciPy builds on NumPy to provide specialized algorithms: optimization, integration, interpolation, signal/image processing, sparse matrices, stats, and ODE solvers. Import `numpy as np` for arrays; `scipy` for advanced scientific routines.
**Code:**
```python
import numpy as np
A = np.array([[2, 0], [0, 4]])         # NumPy: core arrays + linalg
print(np.linalg.eigvals(A))
```
## Q87: What are the ndarray attributes?
**A:** `ndim`, `shape`, `size`, `dtype`, `itemsize`, `nbytes`, `T`, `real`, `imag`, `flat` (1D iterator), `data` (memory buffer), `flags` (contiguity, owndata, writeable). `arr.shape` returns a tuple; reassigning `arr.shape` reshapes in place if compatible.
**Code:**
```python
import numpy as np
a = np.arange(6).reshape(2, 3)
print(a.ndim, a.shape, a.size, a.dtype, a.itemsize, a.nbytes, a.T.shape)
print(list(a.flat))
a.shape = (3, 2)          # in-place reshape
print(a)
```

## Q88: What is the difference between `shape`, `size`, and `ndim`?
**A:** `ndim` = number of dimensions (e.g., 2). `shape` = tuple of sizes per dimension, e.g., (3, 4). `size` = total number of elements = product of shape (12). `itemsize` = bytes per element; `nbytes` = `size * itemsize` = total bytes.
**Code:**
```python
import numpy as np
a = np.zeros((3, 4))
print(a.ndim)          # 2
print(a.shape)         # (3, 4)
print(a.size)          # 12
print(a.itemsize, a.nbytes)
```

## Q89: What is the difference between `np.loadtxt` and `np.genfromtxt`?
**A:** `np.loadtxt` loads well-formed delimited text into an array (fails on missing values). `np.genfromtxt` is more flexible — handles missing values (NaN), commented lines, multiple dtypes, and named columns via `names=True`. `genfromtxt` is slower but robust for messy data; for large data prefer `pd.read_csv`.
**Code:**
```python
import numpy as np
from io import StringIO
clean = "1 2\n3 4\n"
print(np.loadtxt(StringIO(clean)))
messy = "1,NA,3\n4,5,6\n"
print(np.genfromtxt(StringIO(messy), delimiter=',',
                    missing_values='NA', filling_values=-1))
```

## Q90: How do you read/write raw binary with NumPy?
**A:** `np.fromfile('file.bin', dtype=np.float32)` reads raw binary (no shape/header — you must know the dtype and reshape after). `arr.tofile('file.bin')` writes raw bytes. Use `.npy`/`.npz` (`np.save`/`np.load`) instead for self-describing, portable files that preserve shape and dtype.
**Code:**
```python
import numpy as np
a = np.arange(4, dtype=np.float32)
a.tofile('/tmp/raw.bin')
b = np.fromfile('/tmp/raw.bin', dtype=np.float32)
print(b)
```

## Q91: How do you handle time series data with NumPy?
**A:** NumPy doesn't have native datetime support as rich as Pandas, but: `np.datetime64('2024-01-01')` — datetime scalar. `np.arange('2024-01', '2024-03', dtype='datetime64[D]')` — date range. `np.timedelta64(5, 'D')` — time delta. For complex time series, use Pandas; for simple timestamp arrays or performance-critical code, NumPy is sufficient.
**Code:**
```python
import numpy as np
print(np.datetime64('2024-01-01'))
print(np.arange('2024-01', '2024-03', dtype='datetime64[D]'))
print(np.datetime64('2024-01-10') - np.timedelta64(5, 'D'))
```

## Q92: How do you use `np.testing`?
**A:** `np.testing.assert_array_equal(a, b)` checks exact equality, `assert_array_almost_equal(a, b, decimal=7)` for float tolerance, `assert_allclose` for relative/absolute tolerances. Useful in unit tests to avoid brittle `==` comparisons on floating-point arrays.
**Code:**
```python
import numpy as np
np.testing.assert_array_equal([1, 2], np.array([1, 2]))
np.testing.assert_allclose([0.1], [0.1 + 1e-9], rtol=1e-6)
np.testing.assert_array_almost_equal([0.3], [0.1 + 0.2], decimal=6)
print('all assertions passed')
```

## Q93: What are common NumPy performance pitfalls?
**A:** 1) Growing arrays in a loop (pre-allocate instead), 2) Using `np.vectorize` expecting speed, 3) Allocating many temporaries in chained expressions, 4) Non-contiguous arrays slowing BLAS, 5) Implicit copies through fancy indexing, 6) Python-level loops/`map`. Prefer vectorized ufuncs, `out=` parameter, and views.
**Code:**
```python
import numpy as np
out = np.empty(100)                       # pre-allocate instead of appending
for i in range(100):
    out[i] = i ** 2
print(out.sum())
a = np.arange(100)
b = np.empty(100)
np.square(a, out=b)                       # out= avoids a temporary
print(b.sum())
```

## Q94: Why is NumPy faster than pure Python?
**A:** NumPy operations are implemented in C and operate on contiguous typed memory blocks, enabling: vectorization (no per-element Python overhead), SIMD CPU instructions, BLAS/LAPACK for linear algebra, and avoiding Python object boxing. This yields 10–100x speedups over equivalent Python loops.
**Code:**
```python
import numpy as np
n = 10**6
a = np.arange(n)
print((a * a).sum())          # one vectorized C-level pass
```

## Q95: What are universal function methods beyond reduce?
**A:** Ufuncs provide `reduce(a)` (fold along axis), `accumulate(a)` (running result), `reduceat(a, indices)` (reduced at specified slices), `outer(a, b)` (outer product), and `at(a, indices, b)` (in-place unbuffered operation). Examples: `np.add.reduce(arr)`, `np.add.accumulate(arr)`, `np.multiply.outer(x, y)`.
**Code:**
```python
import numpy as np
x = np.array([1, 2, 3, 4])
print(np.add.reduce(x))         # 10
print(np.add.accumulate(x))     # [1 3 6 10]
print(np.multiply.outer([1, 2], [3, 4]))
print(np.add.reduceat(x, [0, 2]))
```

## Q96: How do you use `np.add.at` (ufunc.at)?
**A:** `np.add.at(arr, indices, values)` performs unbuffered in-place addition at indices (handles duplicates correctly). Unlike `arr[indices] += values` which applies only once per index due to buffering, `at` accumulates. Useful for histogramming and scatter-add operations.
**Code:**
```python
import numpy as np
a = np.zeros(4)
idx = np.array([0, 1, 0, 0])
np.add.at(a, idx, 1)
print(a)                         # [3 1 0 0]
garbage = np.zeros(4)
garbage[[0, 1, 0, 0]] += 1       # buffered: duplicates applied once
print(garbage)                   # [1 1 0 0]
```

## Q97: What is `np.argsort` with `kind` and stable sort?
**A:** `np.argsort(arr, kind='stable')` returns indices that sort the array using a stable algorithm (preserves original order of equal elements). `kind` options: 'quicksort', 'mergesort' (stable), 'heapsort', 'stable'. Stable sort is essential when sorting by multiple keys via successive argsorts or lexsort.
**Code:**
```python
import numpy as np
a = np.array([2, 1, 1, 3])
print(np.argsort(a, kind='stable'))    # [1 2 0 3]
print(np.sort(a, kind='stable'))
first = np.array([1, 1, 2, 2]); second = np.array([0, 1, 0, 1])
order = np.lexsort((second, first))    # sort by first, then second
print(order)
```

## Q98: How do you build arrays from existing ones efficiently?
**A:** Use `np.block` (assemble blocks into one array), `np.vstack`/`hstack`/`dstack`, `np.stack`, `np.tile`/`np.repeat`, and `np.broadcast_to` (creates a read-only view by broadcasting without copying). `np.broadcast_to` is memory-efficient when you only need the broadcasted shape for computation.
**Code:**
```python
import numpy as np
print(np.broadcast_to(np.array([1, 2, 3]), (2, 3)))
print(np.block([[np.ones((1, 2)), np.zeros((1, 2))],
                [np.zeros((1, 2)), np.ones((1, 2))]]))
```

## Q99: What is `np.info` and `np.lookfor`?
**A:** `np.info(obj)` prints documentation/attributes for a NumPy object or function in the console. `np.lookfor('keyword')` searches docstrings across NumPy for a topic and returns matching functions — handy when you know what you want to do but not the exact function name.
**Code:**
```python
import numpy as np
np.info(np.add)                              # prints docstring to console
doc = np.add.__doc__
print('Performs element-wise addition' in (doc or ''))   # docstring lookup
```

## Q100: What are the latest features in modern NumPy (2.0+)?
**A:** NumPy 2.0+: improved string dtype (`np.str_`), faster sorting and copying, enhanced FFT, improved random number generation, cleaner API, better compatibility with the array API standard, NEP 50 type promotion (Python scalars don't upcast arrays unexpectedly), and removal of many long-deprecated aliases. It also improved `numpy.array_api` compliance and `copy=` keyword semantics.
**Code:**
```python
import numpy as np
a = np.array(['a', 'b'], dtype=np.str_)   # 2.0 string dtype
print(np.copy(a), a.dtype)
src = np.array([1.0, 2.0])
print(np.array(src, copy=False))          # copy= keyword semantics
print(src + 1)        # NEP 50: Python scalar does not upcast
```

