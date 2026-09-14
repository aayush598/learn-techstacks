# SQL — Master Interview Resource (45 files · 4,500 Q&A)

One-stop, deeply organized SQL interview prep built for senior/principal-level loops at top companies (FAANG, MAANG, Tesla, Samsung, Nvidia, Infosys, and more). Every file contains exactly **100 scenario-based questions**, answered with runnable SQL, and typically **multiple alternative queries** (different dialect, technique, or approach) per question.

**How to use this resource**
1. Start at `01_sql_fundamentals` and work bottom-up. Do not read file 2 before file 1.
2. For every question: cover the answer, write your own SQL, then compare. The `**Alt1:**` variants are the real interview signal — they are the alternative solutions senior engineers are expected to know.
3. When timing an interview, do `05_interview_scenario_playbook/...` rounds as mock sprints.
4. Dialects are mixed (MySQL 8+, PostgreSQL, SQL Server, Oracle, SQLite) and marked with `-- MySQL`, `-- PostgreSQL`, etc. Prefer standard SQL where possible; know the vendor-specific syntax for the company you are interviewing with.

---

## 01 — SQL Fundamentals (11 files, 1,100 Q&A)

### 01_select_and_filter
| File | Covers |
|---|---|
| `01_basic_select.md` | SELECT columns, aliases, DISTINCT, expressions, computed fields, row-limiting |
| `02_where_and_operators.md` | Comparison/boolean logic, IN/BETWEEN/LIKE/NULL, operator precedence, ANY/ALL/EXISTS |
| `03_sorting_and_pagination.md` | ORDER BY patterns, NULL ordering, custom sorts, LIMIT/OFFSET vs keyset pagination, TOP/ROWNUM |

### 02_joins
| File | Covers |
|---|---|
| `01_inner_and_self_joins.md` | INNER JOIN, explicit vs implicit, compound keys, SELF JOIN families (pairs, managers, duplicates) |
| `02_outer_and_cross_joins.md` | LEFT/RIGHT/FULL OUTER, CROSS JOIN, anti-joins, ON vs WHERE traps, emulations |
| `03_multi_table_join_scenarios.md` | 3+ table business joins, fan-out control, 2-hop graphs, many roles of one table |

### 03_aggregation
| File | Covers |
|---|---|
| `01_group_by_and_having.md` | GROUP BY, WHERE vs HAVING, ROLLUP/GROUPING SETS, bucket grouping, group filters |
| `02_aggregate_functions.md` | COUNT/SUM/AVG/MIN/MAX semantics, NULL traps, conditional aggregation, median/mode, STRING_AGG |

### 04_subqueries_and_ctes
| File | Covers |
|---|---|
| `01_subqueries.md` | Scalar/derived/IN/EXISTS/ANY/ALL subqueries, NULL pitfalls, two-step nesting |
| `02_correlated_subqueries.md` | Correlated SELECT/WHERE/HAVING, per-group top rows without windows, rewrites |
| `03_ctes.md` | CTE anatomy, chained/multiple CTEs, pipeline architecture, CTE in DML |

## 02 — Advanced SQL (8 files, 800 Q&A)

### 01_window_functions
| File | Covers |
|---|---|
| `01_ranking_window_functions.md` | ROW_NUMBER/RANK/DENSE_RANK/NTILE, top-N-per-group with ties, distribution ranks |
| `02_lag_lead_and_value_windows.md` | LAG/LEAD, FIRST/LAST/NTH_VALUE, framing, day-over-day deltas, backfill |
| `03_running_totals_and_moving_averages.md` | Cumulative sums, moving/weighted averages, expanding/trailing frames, window-over-window traps |

### 02_string_date_case_logic
| File | Covers |
|---|---|
| `01_string_manipulation.md` | CONCAT/SUBSTR/TRIM/REPLACE/SPLIT/regex, string parsing, GROUP_CONCAT |
| `02_date_time_functions.md` | Date arithmetic, extraction, truncation, timezones, date ranges, business days, date series |
| `03_case_conditional_logic.md` | CASE both forms, conditional aggregation, IF/IIF/DECODE, bucketing, order-by logic |

### 03_set_operations_and_nulls
| File | Covers |
|---|---|
| `01_union_intersect_except.md` | UNION/UNION ALL, INTERSECT/EXCEPT/MINUS across dialects, ALL-variants, table diffing |
| `02_nulls_and_coalesce.md` | Three-valued logic, NULL traps in every context, COALESCE/IFNULL/NVL/NULLIF |

## 03 — Schema & Database Design (8 files, 800 Q&A)

### 01_ddl_and_constraints
| File | Covers |
|---|---|
| `01_creating_tables_and_constraints.md` | CREATE/ALTER, data types, defaults, identities/sequences, CTAS, engines |
| `02_primary_foreign_and_unique_keys.md` | PK/UNIQUE/FK semantics, ON DELETE actions, composite keys, deferrable cycles, surrogate vs natural |

### 02_normalization_and_design
| File | Covers |
|---|---|
| `01_normalization_and_denormalization.md` | 1NF-5NF/BCNF, functional dependencies, decomposition, star/snowflake, SCD-2, ER mapping |

### 03_views_and_security
| File | Covers |
|---|---|
| `01_views_and_materialized_views.md` | Views, WITH CHECK OPTION, updatable views, matviews + refresh strategies, security masking |

### 04_stored_code
| File | Covers |
|---|---|
| `01_stored_procedures_and_functions.md` | Procedures/functions, params, control flow, cursors, exceptions, dynamic SQL, volatility |
| `02_triggers.md` | BEFORE/AFTER/INSTEAD OF triggers, OLD/NEW, audit/history, validation, recursion |

### 05_transactions
| File | Covers |
|---|---|
| `01_transactions_and_isolation_levels.md` | ACID, transactions/savepoints, isolation levels, all anomalies, snapshot isolation |
| `02_locking_and_concurrency.md` | Shared/exclusive locks, FOR UPDATE/SKIP LOCKED, deadlocks, optimistic vs pessimistic, gap locks |

## 04 — Performance & Optimization (4 files, 400 Q&A)

### 01_indexing
| File | Covers |
|---|---|
| `01_indexes_and_covering_indexes.md` | B-tree, clustered vs non-clustered, composite/leftmost-prefix, covering, functional/partial, DESC |

### 02_query_optimization
| File | Covers |
|---|---|
| `01_explain_analyze_and_execution_plans.md` | EXPLAIN in all dialects, reading plans, join strategies, plan-driven fixes, statistics |
| `02_optimization_anti_patterns.md` | Bad-vs-good rewrites for every classic anti-pattern (non-sargable, SELECT *, deep OFFSET, etc.) |

### 03_large_scale_patterns
| File | Covers |
|---|---|
| `01_partitioning_sharding_and_big_data_patterns.md` | Table partitioning, partition pruning, sharding keys, replicas, OLTP vs OLAP, bulk loading |

## 05 — Interview Scenario Playbook (14 files, 1,400 Q&A)

### 01_tier1_company_rounds
| File | Covers |
|---|---|
| `01_faang_style_round1.md` | Classic screening: nth-highest, top-N, duplicates, manager-vs-employee, overlaps |
| `02_faang_style_round2.md` | Advanced: sessionization, funnels, retention, gaps-and-islands, products affinity, medians |
| `03_product_analytics_metric_queries.md` | DAU/WAU/MAU, funnels, stickiness, churn, LTV, MRR waterfall, cohort curves |

### 02_domain_specific
| File | Covers |
|---|---|
| `01_ecommerce_retail_queries.md` | Revenue, AOV, cross-sell, inventory, restock, delivery, reviews, returns |
| `02_social_media_friendship_queries.md` | Friend graphs, mutual friends, suggestions, triangles, PageRank-style reach |
| `03_finance_banking_queries.md` | Balances, overdrafts, fraud flags, EMI schedules, drawdown, mark-to-market |
| `04_employee_hr_analytics.md` | Org trees, attrition, tenure, payroll, performance, headcount trends |
| `05_logistics_and_event_queries.md` | Delivery times, SLA, dwell times, utilization, waybill event streams, ETA |

### 03_advanced_top_company_patterns
| File | Covers |
|---|---|
| `01_recursive_cte_and_hierarchies.md` | Recursive CTEs, org/comment trees, BOM explosion, cycle safety, CONNECT BY |
| `02_gaps_and_islands.md` | Streaks, consecutive days, missing ranges, interval merging, seat/version gaps |
| `03_pivoting_and_transposition.md` | Conditional aggregation, CROSSTAB, PIVOT/UNPIVOT, dynamic pivots |
| `04_dedup_and_top_n_per_group.md` | Dedup (self-join/window), keep-newest, top-N variants, tie handling |
| `05_sessionization_and_funnels.md` | Time-based sessions, session metrics, funnel conversion, step velocity |
| `06_retention_and_cohort_analytics.md` | Cohort tables, N-day/window retention, churn, resurrection, cohort LTV |

---

## Quick stat line
- 45 files · 4,500 questions · 3-level folder depth (folder → subfolder → subsubfolder → files)
- Every answer ships runnable SQL, most with 1+ alternative approach
- Dialects: MySQL 8+, PostgreSQL, SQL Server (T-SQL), Oracle (PL/SQL), SQLite where relevant

## Practice protocol (for the interview itself)
1. **Always ask** about assumed schema before writing SQL.
2. **State the technique** before the query ("I will use ROW_NUMBER with a partition").
3. **Name the alternatives** verbally — this is what separates senior candidates.
4. **Verify ties/NULLs/duplicates** in your head before answering.
5. **Mention indexes/EXPLAIN** when performance is called out.
