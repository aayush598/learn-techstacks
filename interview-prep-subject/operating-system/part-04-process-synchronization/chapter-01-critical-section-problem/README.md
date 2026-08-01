# Chapter 1: The Critical-Section Problem

> **TL;DR**: The critical-section problem is the core of synchronization: multiple threads competing to modify shared data must each access it atomically (mutual exclusion), with progress (someone gets in), bounded waiting (no infinite bypass), and the code must be race-free. This chapter builds the requirements and the first software/hardware solutions.

## Sections
| Section | Topic | Key Idea |
|---|---|---|
| 01 | Critical Section & Requirements | Mutual exclusion, progress, bounded waiting |
| 02 | Peterson's Algorithm & Hardware Support | Software solution; then test-and-set/compare-and-swap |

## What You'll Learn
- What a race condition is and why preemption creates it.
- The formal requirements of a correct critical-section solution.
- Why pure software solutions (Peterson's) exist but are impractical.
- How hardware atomic instructions (TAS/CAS) make locks practical.
