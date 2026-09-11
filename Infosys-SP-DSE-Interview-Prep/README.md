# Infosys SP / DSE Interview Preparation

Complete interview-prep resource for the **Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)** role.

> **248 topics × 100 Q&A = 24,800 interview questions**, organized into 9 domains. Every leaf folder contains a `questions.md` with exactly 100 questions in expandable `<details>` blocks.

## Format

Every topic folder (`questions.md`) contains:

```
# <Leaf Name> — <Parent Domain>

**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**

<details open>
  <summary>Tap to expand all 100 questions</summary>

  1. **Question...**
     - Answer...

  ...

</details>
```

## Structure (248 leaves)

| Domain | Leaves | Coverage |
|--------|--------|----------|
| `01-DSA` | 63 | Arrays, Strings, Linked Lists, Stacks & Queues, Trees, Graphs, DP, Recursion & Backtracking, Sorting & Searching, Greedy, Segment Trees & Fenwick, Two Pointers |
| `02-CS-Fundamentals` | 41 | OOP, DBMS, SQL, Operating Systems, Computer Networks |
| `03-Python` | 34 | Basics, Advanced (decorators/generators/asyncio), Python for DSA, FastAPI, Flask, Libraries |
| `04-AI-ML` | 31 | ML Fundamentals, Deep Learning, NLP, LLM & GenAI, Agentic AI |
| `05-System-Design` | 15 | Fundamentals, API Design, System Design Problems, Design Patterns |
| `06-DevOps` | 15 | Docker, Git, CI/CD, Linux |
| `07-HR-Preparation` | 17 | Behavioral Questions, Infosys-Specific, Salary & Negotiation, Common HR Questions |
| `08-Coding-Patterns` | 15 | 14 Grokking-style patterns + heap pattern |
| `09-Aptitude` | 17 | Quantitative, Logical Reasoning, Verbal |

## Exam Context

| Detail | Info |
|--------|------|
| Role | Specialist Programmer (SP L3) / Digital Specialist Engineer (DSE) |
| Coding round | 3 hours, 3 problems |
| Q1 | Easy (20 marks) — Arrays, Strings, Basic DSA |
| Q2 | Medium (30 marks) — Greedy, Graphs, Trees |
| Q3 | Hard (50 marks) — DP, Advanced Graphs, Complex Algorithms |
| HR / Tech round | Explain round-1 logic, HashMap vs TreeMap, ACID (bank transfer), OOP, projects, conflict handling |

The `07-HR-Preparation` answers are personalized to **Aayush Gid** (B.Tech ECE 2022-26) — agentic AI internships, ScriptVector RAG, OpenRTL ai, Agno open-source contributions, SIH 2024 finalist, IEEE paper. Update the `c_hr.py` content module if your profile changes.

## How to Use

1. Start with `07-HR-Preparation` and `09-Aptitude` the week before — quick wins.
2. Drill `08-Coding-Patterns` to build recognition speed for the OA.
3. Go domain-by-domain through `01-DSA` → `02-CS-Fundamentals` → `03-Python` → `04-AI-ML` → `05-System-Design` → `06-DevOps`.
4. Open each `questions.md`, read the question, answer out loud, then expand to verify.

## How to Rebuild

The `questions.md` files are generated from curated Q&A content modules:

```bash
cd 00-Build-Scripts
python3 run_build.py
```

- `00-Build-Scripts/c_*.py` — 18 curated content modules (one dict per topic; keys are folder-relative paths).
- `00-Build-Scripts/engine.py` — finds all leaf folders and writes `questions.md`, padding each topic to exactly 100 Q&A.
- `00-Build-Scripts/pad.py` — generic filler templates (DSA / numeric / behavioural / CS).
- `00-Build-Scripts/run_build.py` — merges all modules (adding the top-level domain prefix per module) and runs the build.
- `00-Build-Scripts/gen_helpers.py` — Tree/data helpers for authoring modules.