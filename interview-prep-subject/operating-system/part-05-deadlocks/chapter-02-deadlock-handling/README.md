# Chapter 2: Deadlock Handling

> **TL;DR**: Three strategies handle deadlocks: prevention (make a deadlock structurally impossible — break one of the four conditions), avoidance (run-time safe-state checks like Banker's algorithm), and detection + recovery (find cycles, abort a victim). Prevention is cheapest and most common; Banker's is theoretically elegant but rarely used in practice; detection is what databases actually do.

## Sections
| Section | Topic | Key Idea |
|---|---|---|
| 01 | Deadlock Prevention | Break one of the four conditions |
| 02 | Banker's Algorithm (Avoidance) | Safe-state check before grant |
| 03 | Detection & Recovery | Find cycles; abort/rollback |

## What You'll Learn
- The four prevention techniques and their costs.
- How Banker's decides whether a grant is safe.
- How production systems detect deadlocks and recover.
