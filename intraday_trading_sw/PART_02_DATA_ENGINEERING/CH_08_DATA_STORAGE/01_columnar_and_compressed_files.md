# 01 — Columnar and Compressed Files

## Purpose
Use column-oriented, compressed file formats for analytic data so backtests and
training read many years of bars quickly with little disk.

## Why columnar
- Read only the columns you need (e.g., close only for some indicators).
- Strong compression (similar values stored together).
- Fast predicates/range scans over millions of rows.

## Practical choices (dependency-minimized)
- **Parquet**: standard columnar format; if your runtime has a library, wrap it
  behind one `DataFrameIO` interface. Alternative: implement your own simple
  columnar format (row-group of fixed-size typed columns + metadata header)
  when you want zero external deps.
- Partitioning: by symbol then by year (typical scan = one file).

## Schema in the file
- Physical columns: ts (int64), open/high/low/close (float64), volume (int64/float64),
  plus optional columns. Store `interval` and `symbol` in file metadata.

## Pseudo-code: self-hosted columnar writer
```
write_row_group(fp, columns):
    header = {col: {dtype, offset, count}}     # fixed at start
    for col in columns: fp.write(col.bytes)    # typed contiguous arrays
    fp.write(index.min_ts); fp.write(index.max_ts)
read_file(fp, needed_cols):
    parse header; seek to each needed col offset; load typed arrays
```

## Steps to adopt
1. Write a writer for validated bars → Parquet/own-columnar, partitioned by
   `symbol/year`.
2. Write a reader that accepts a list of needed columns (column pruning).
3. Add a stats footer (min/max ts, row count) to skip irrelevant files.
4. Test round-trip equality (write → read → same values) in QA (CH_36).

## Rules
- Store metadata (schema version, source, adjustment version) in every file.
- Compress by default; decompression cost is worth the I/O savings.
- Never use columnar files as the live append target — that is the hot tier's job.
