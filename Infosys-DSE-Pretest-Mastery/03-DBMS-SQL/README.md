# Section 3 — DBMS & SQL

> Infosys DSE Pre-Test · Section 3 · DBMS & SQL · _Estimated reading time: 8 hours of topic work + 6 hours of practice_

## What this section is

The Infosys DSE pre-test puts **10 questions in roughly 18 minutes** between the English section and the
25-question Java block. It is small — 16.7% of the paper — and it is the **most predictable 10 marks
you will ever sit**.

Candidates consistently report the same six sub-archetypes:

| # | Archetype | Typical share | Cost per mark |
|---|-----------|---------------|---------------|
| a | SQL fundamentals up to JOINs | ~2–3 Q | Medium |
| b | "Write a query for two tables" (free response / SQL writing) | ~1–2 Q | Medium-high |
| c | "Identify the output of the given SQL query" | ~2 Q | Medium |
| d | Normalization (1NF / 2NF / 3NF / BCNF) | ~1–2 Q | Low |
| e | ACID properties | ~1 Q | Low |
| f | General DBMS theory (keys, indexes, views, DDL/DML) | ~1–2 Q | Low |

**Target: 7–8 correct out of 10.** The five cheapest marks in the whole paper live here: ACID,
normalization, and DBMS theory are definition questions with no computation.

## The one rule that matters

> **108 seconds per question.** 10 questions × 108 s ≈ 18 minutes.
> Trace the join on paper. Do not trace it in your head.

Output-identification questions look like they take forever and actually take 60 seconds **if you
write the intermediate rows down**. Meera knows the answer and still loses marks; she tries to hold
five rows in her head. Paper first, answer second.

## Topic index

| # | Topic | Questions it covers | Time to read | Start here |
|---|-------|---------------------|--------------|------------|
| 1 | [SQL Basics: DDL & DML](01-SQL-Basics-DDL-DML/README.md) | ~1–2 Q | 70 min | [DDL/DML anatomy](01-SQL-Basics-DDL-DML/01-concepts/01-ddl-dml-anatomy.md) |
| 2 | [Joins](02-Joins/README.md) | ~2–3 Q | 70 min | [The six joins](02-Joins/01-concepts/01-the-six-joins.md) |
| 3 | [Two-Table Query Writing](03-Two-Table-Query-Writing/README.md) | ~1–2 Q | 70 min | [The eight-step recipe](03-Two-Table-Query-Writing/02-techniques/01-the-eight-step-recipe.md) |
| 4 | [Query Output Identification](04-Query-Output-Identification/README.md) | ~2 Q | 60 min | [Five-step execution model](04-Query-Output-Identification/01-concepts/01-five-step-execution-model.md) |
| 5 | [Normalization](05-Normalization/README.md) | ~1–2 Q | 60 min | [Normal forms defined](05-Normalization/01-concepts/01-normal-forms-defined.md) |
| 6 | [ACID & Transactions](06-ACID-Transactions/README.md) | ~1 Q | 45 min | [ACID and isolation levels](06-ACID-Transactions/01-concepts/01-acid-and-isolation-levels.md) |
| 7 | [DBMS Theory: Keys, Indexes, Views](07-DBMS-Theory-Keys-Indexes-Views/README.md) | ~1–2 Q | 60 min | [Schema, keys and indexes](07-DBMS-Theory-Keys-Indexes-Views/01-concepts/01-schema-keys-and-indexes.md) |
| 8 | [Functions, Aggregates & CASE](08-Functions-Aggregates-Case/README.md) | ~1 Q | 45 min | [Aggregate and scalar rules](08-Functions-Aggregates-Case/01-concepts/01-aggregate-and-scalar-function-rules.md) |
| 9 | [Question Bank](09-Question-Bank/README.md) | All 9 | 5–8 hours | [Archetype map](09-Question-Bank/README.md) |

## How each topic is organised

Every topic folder follows the same five-part structure, so you always know where to look:

| Folder | Answers | What lives there |
|---|---|---|
| `01-concepts` | "What is this actually asking?" | The rules, the definitions, the mental models |
| `02-techniques` | "How do I do it in 108 seconds?" | The procedures, the decision tables, the recipes |
| `03-worked-examples` | "What does a finished one look like?" | Fully solved questions with distractor breakdowns |
| `04-pitfalls` | "What will go wrong?" | The named traps and the option each one produces |
| `05-reference` | "What do I revise on the morning of the exam?" | One-page sheets, tables, quick-check cards |

Each topic also has a `README.md` that acts as its table of contents, and every subfolder has a
short `README.md` listing its files.

## The shared fixture

Every example in this section uses one schema so that a number you memorise in one topic is still
correct in the next. Learn it once.

```sql
CREATE TABLE customers (
  cust_id   INT PRIMARY KEY,
  cust_name VARCHAR(50),
  city      VARCHAR(30)
);

CREATE TABLE orders (
  order_id   INT PRIMARY KEY,
  cust_id    INT,
  order_date DATE,
  amount     DECIMAL(10,2)
);

CREATE TABLE departments (
  dept_id   INT PRIMARY KEY,
  dept_name VARCHAR(30),
  location  VARCHAR(30)
);

CREATE TABLE employees (
  emp_id      INT PRIMARY KEY,
  emp_name    VARCHAR(50),
  dept_id     INT,
  salary      INT,
  manager_id  INT
);
```

**customers**

| cust_id | cust_name | city |
|---|---|---|
| 101 | Ananya | Pune |
| 102 | Rahul | Chennai |
| 103 | Meera | Pune |
| 104 | Karthik | Delhi |
| 105 | Vikram | Bengaluru |

**orders**

| order_id | cust_id | order_date | amount |
|---|---|---|---|
| 1001 | 101 | 2026-01-05 | 500.00 |
| 1002 | 101 | 2026-01-09 | 750.00 |
| 1003 | 102 | 2026-02-11 | 1200.00 |
| 1004 | 103 | 2026-02-14 | 300.00 |
| 1005 | 104 | 2026-03-02 | 950.00 |
| 1006 | 104 | 2026-03-03 | 1100.00 |

**departments**

| dept_id | dept_name | location |
|---|---|---|
| 10 | Sales | Pune |
| 20 | Engineering | Bengaluru |
| 30 | Support | Chennai |

**employees**

| emp_id | emp_name | dept_id | salary | manager_id |
|---|---|---|---|---|
| 1 | Ananya | 10 | 60000 | 4 |
| 2 | Rahul | 10 | 45000 | 4 |
| 3 | Meera | 20 | 90000 | 5 |
| 4 | Karthik | 10 | 120000 | NULL |
| 5 | Vikram | 20 | 110000 | NULL |
| 6 | Anjali | 30 | 50000 | 5 |

Facts you can rely on: customer 105 has **no orders**; customer 101 has **2 orders**; customer 104 has
**2 orders**; 6 orders total, 5 customers; department 30 has one employee; employees 4 and 5 are
managers; total salary of department 10 = 225000.

## Learning path

| Stage | Duration | Work | You are ready when |
|---|---|---|---|
| 1. Concepts | 2 days | `01-concepts` of topics 1, 2, 4, 5 | You can state the 1NF/2NF/3NF rule from memory |
| 2. Joins | 1 day | `02-Joins` complete, then `03-Two-Table-Query-Writing` | You can pick the join type in 5 seconds |
| 3. Traps | 1 hour | `04-pitfalls` of every topic | You can name the wrong option each trap produces |
| 4. Practice | 3 days | Question bank parts A → B → C, untimed | You score 70% per archetype, not just in total |
| 5. Timing | 2 days | One archetype drill a day, then a full mock | You finish 10 questions in 18 minutes |

## The 108-second rule, in practice

| Archetype | Box | If you are out of time |
|---|---|---|
| ACID, DBMS theory | 55 s | Best guess, move |
| Normalization | 70 s | Best guess, move |
| Join type selection | 70 s | Best guess, move |
| SQL writing | 108 s | Skip, mark, come back |
| Output identification | 108 s | Skip, mark, come back |

Leave **1 minute of the 18** for review. If you are still on question 6 at minute 13, skip to
question 9 and come back — three marked guesses beat one finished answer.

## The recurring cast

| Name | Who | What they represent |
|---|---|---|
| **Ananya** | 3rd-year BTech, average aptitude | Reads every question twice and runs out of time |
| **Rahul** | Strong in Java, weak in English | Writes the query but forgets the `ON` clause |
| **Meera** | Strong in DBMS, panics under time | Knows the answer and loses it by not writing the trace |
| **Karthik** | UI stream, reflecting on the last attempt | Now fixes the error log instead of repeating the mistake |

## Honest rules for this resource

- Every question has real options, a definite correct answer, and a breakdown of why each wrong
  option is wrong.
- Every output-identification question uses a real `CREATE TABLE` + `INSERT` fixture, so the answer is
  reproducible on any SQL engine.
- SQL is standard SQL. MySQL-only notes (window functions need MySQL 8+) are marked inline.
- The style is deliberately terse. If a file reads like a textbook, it has failed: the point of this
  resource is that you can use it in the last two hours before the exam.

## Related

- [Master README](../README.md) — the full pre-test study plan across all sections
- [Exam blueprint: DBMS/SQL section analysis](../00-Exam-Blueprint/02-Sectional-Analysis/01-concepts/03-dbms-sql-section-analysis.md)
- [Question Bank](09-Question-Bank/README.md) — 78 questions with a full answer key
- [Joins](02-Joins/README.md) — the single highest-yield topic in this section
