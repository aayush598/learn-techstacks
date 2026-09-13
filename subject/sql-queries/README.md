# SQL — Master Interview Resource (45 files · 4,500 Q&A)

One-stop, deeply organized SQL interview prep built for senior/principal-level loops at top companies (FAANG, MAANG, Tesla, Samsung, Nvidia, Infosys, and more). Every file contains exactly **100 scenario-based questions**, answered with runnable SQL, and typically **multiple alternative queries** (different dialect, technique, or approach) per question.

**How to use this resource**
1. Start at `01_sql_fundamentals` and work bottom-up. Do not read file 2 before file 1.
2. For every question: cover the answer, write your own SQL, then compare. The `**Alt1:**` variants are the real interview signal — they are the alternative solutions senior engineers are expected to know.
3. When timing an interview, do `05_interview_scenario_playbook/...` rounds as mock sprints.
4. Dialects are mixed (MySQL 8+, PostgreSQL, SQL Server, Oracle, SQLite) and marked with `-- MySQL`, `-- PostgreSQL`, etc. Prefer standard SQL where possible; know the vendor-specific syntax for the company you are interviewing with.

---

## 01 — SQL Fundamentals (11 files, 1,100 Q&A)

### select_and_filter
| File | Covers |
|---|---|
| `basic_select.md` | SELECT columns, aliases, DISTINCT, expressions, computed fields, row-limiting |
| `where_and_operators.md` | Comparison/boolean logic, IN/BETWEEN/LIKE/NULL, operator precedence, ANY/ALL/EXISTS |
| `sorting_and_pagination.md` | ORDER BY patterns, NULL ordering, custom sorts, LIMIT/OFFSET vs keyset pagination, TOP/ROWNUM |

### joins
| File | Covers |
|---|---|
| `inner_and_self_joins.md` | INNER JOIN, explicit vs implicit, compound keys, SELF JOIN families (pairs, managers, duplicates) |
| `outer_and_cross_joins.md` | LEFT/RIGHT/FULL OUTER, CROSS JOIN, anti-joins, ON vs WHERE traps, emulations |
| `multi_table_join_scenarios.md` | 3+ table business joins, fan-out control, 2-hop graphs, many roles of one table |

### aggregation
| File | Covers |
|---|---|
| `group_by_and_having.md` | GROUP BY, WHERE vs HAVING, ROLLUP/GROUPING SETS, bucket grouping, group filters |
| `aggregate_functions.md` | COUNT/SUM/AVG/MIN/MAX semantics, NULL traps, conditional aggregation, median/mode, STRING_AGG |

### subqueries_and_ctes
| File | Covers |
|---|---|
| `subqueries.md` | Scalar/derived/IN/EXISTS/ANY/ALL subqueries, NULL pitfalls, two-step nesting |
| `correlated_subqueries.md` | Correlated SELECT/WHERE/HAVING, per-group top rows without windows, rewrites |
| `ctes.md` | CTE anatomy, chained/multiple CTEs, pipeline architecture, CTE in DML |

## 02 — Advanced SQL (8 files, 800 Q&A)

### window_functions
| File | Covers |
|---|---|
| `ranking_window_functions.md` | ROW_NUMBER/RANK/DENSE_RANK/NTILE, top-N-per-group with ties, distribution ranks |
| `lag_lead_and_value_windows.md` | LAG/LEAD, FIRST/LAST/NTH_VALUE, framing, day-over-day deltas, backfill |
| `running_totals_and_moving_averages.md` | Cumulative sums, moving/weighted averages, expanding/trailing frames, window-over-window traps |

### string_date_case_logic
| File | Covers |
|---|---|
| `string_manipulation.md` | CONCAT/SUBSTR/TRIM/REPLACE/SPLIT/regex, string parsing, GROUP_CONCAT |
| `date_time_functions.md` | Date arithmetic, extraction, truncation, timezones, date ranges, business days, date series |
| `case_conditional_logic.md` | CASE both forms, conditional aggregation, IF/IIF/DECODE, bucketing, order-by logic |

### set_operations_and_nulls
| File | Covers |
|---|---|
| `union_intersect_except.md` | UNION/UNION ALL, INTERSECT/EXCEPT/MINUS across dialects, ALL-variants, table diffing |
| `nulls_and_coalesce.md` | Three-valued logic, NULL traps in every context, COALESCE/IFNULL/NVL/NULLIF |

## 03 — Schema & Database Design (8 files, 800 Q&A)

### ddl_and_constraints
| File | Covers |
|---|---|
| `creating_tables_and_constraints.md` | CREATE/ALTER, data types, defaults, identities/sequences, CTAS, engines |
| `primary_foreign_and_unique_keys.md` | PK/UNIQUE/FK semantics, ON DELETE actions, composite keys, deferrable cycles, surrogate vs natural |

### normalization_and_design
| File | Covers |
|---|---|
| `normalization_and_denormalization.md` | 1NF-5NF/BCNF, functional dependencies, decomposition, star/snowflake, SCD-2, ER mapping |

### views_and_security
| File | Covers |
|---|---|
| `views_and_materialized_views.md` | Views, WITH CHECK OPTION, updatable views, matviews + refresh strategies, security masking |

### stored_code
| File | Covers |
|---|---|
| `stored_procedures_and_functions.md` | Procedures/functions, params, control flow, cursors, exceptions, dynamic SQL, volatility |
| `triggers.md` | BEFORE/AFTER/INSTEAD OF triggers, OLD/NEW, audit/history, validation, recursion |

### transactions
| File | Covers |
|---|---|
| `transactions_and_isolation_levels.md` | ACID, transactions/savepoints, isolation levels, all anomalies, snapshot isolation |
| `locking_and_concurrency.md` | Shared/exclusive locks, FOR UPDATE/SKIP LOCKED, deadlocks, optimistic vs pessimistic, gap locks |

## 04 — Performance & Optimization (4 files, 400 Q&A)

### indexing
| File | Covers |
|---|---|
| `indexes_and_covering_indexes.md` | B-tree, clustered vs non-clustered, composite/leftmost-prefix, covering, functional/partial, DESC |

### query_optimization
| File | Covers |
|---|---|
| `explain_analyze_and_execution_plans.md` | EXPLAIN in all dialects, reading plans, join strategies, plan-driven fixes, statistics |
| `optimization_anti_patterns.md` | Bad-vs-good rewrites for every classic anti-pattern (non-sargable, SELECT *, deep OFFSET, etc.) |

### large_scale_patterns
| File | Covers |
|---|---|
| `partitioning_sharding_and_big_data_patterns.md` | Table partitioning, partition pruning, sharding keys, replicas, OLTP vs OLAP, bulk loading |

## 05 — Interview Scenario Playbook (14 files, 1,400 Q&A)

### tier1_company_rounds
| File | Covers |
|---|---|
| `faang_style_round1.md` | Classic screening: nth-highest, top-N, duplicates, manager-vs-employee, overlaps |
| `faang_style_round2.md` | Advanced: sessionization, funnels, retention, gaps-and-islands, products affinity, medians |
| `product_analytics_metric_queries.md` | DAU/WAU/MAU, funnels, stickiness, churn, LTV, MRR waterfall, cohort curves |

### domain_specific
| File | Covers |
|---|---|
| `ecommerce_retail_queries.md` | Revenue, AOV, cross-sell, inventory, restock, delivery, reviews, returns |
| `social_media_friendship_queries.md` | Friend graphs, mutual friends, suggestions, triangles, PageRank-style reach |
| `finance_banking_queries.md` | Balances, overdrafts, fraud flags, EMI schedules, drawdown, mark-to-market |
| `employee_hr_analytics.md` | Org trees, attrition, tenure, payroll, performance, headcount trends |
| `logistics_and_event_queries.md` | Delivery times, SLA, dwell times, utilization, waybill event streams, ETA |

### advanced_top_company_patterns
| File | Covers |
|---|---|
| `recursive_cte_and_hierarchies.md` | Recursive CTEs, org/comment trees, BOM explosion, cycle safety, CONNECT BY |
| `gaps_and_islands.md` | Streaks, consecutive days, missing ranges, interval merging, seat/version gaps |
| `pivoting_and_transposition.md` | Conditional aggregation, CROSSTAB, PIVOT/UNPIVOT, dynamic pivots |
| `dedup_and_top_n_per_group.md` | Dedup (self-join/window), keep-newest, top-N variants, tie handling |
| `sessionization_and_funnels.md` | Time-based sessions, session metrics, funnel conversion, step velocity |
| `retention_and_cohort_analytics.md` | Cohort tables, N-day/window retention, churn, resurrection, cohort LTV |

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
