# Page Replacement: LRU (Least Recently Used)

## Algorithm

- **Replace the page that has not been used for the longest time**
- Based on **locality of reference**: past usage predicts future usage
- Approximation of OPT (optimal) using historical data

### Example

```
Reference string: 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0
Frames = 3

7    0    1    2    0    3    0    4    2    3    0
7    0    1    2    0    3    0    4    2    3    0
     7    0    1    2    0    3    0    4    2    3
          7    0    1    2    0    3    0    4    2

Faults: 7, 0, 1, 2, 3, 4, 0 → 7 faults (with 3 frames)
```

Better than FIFO (10) and close to OPT (8) for this string.

## Implementation Approaches

### 1. Counters (software-assisted)

- Each page table entry has a **time-of-use field**
- On every memory reference, store current **clock/cycle count** into page's field
- On page fault: scan all pages, find smallest timestamp → evict
- **Problem:** massive overhead (write to PT on every memory reference, scan on fault)

### 2. Stack (hardware stack)

- Maintain stack of page numbers
- On page reference: move page to **top** of stack
- Bottom of stack = LRU page → evict
- **Problem:** updating stack on every reference (6+ pointer updates per reference)
- Requires associative hardware to do efficiently

## Properties

| Property | Value |
|---|---|
| **Belady's anomaly?** | No (has stack property) |
| **Stack property?** | Yes |
| **Implementation** | Expensive (counters or hardware stack) |
| **Performance** | Near-optimal (best practical choice) |
| **Overhead** | High without hardware support |

## Why LRU Works

- Programs exhibit **temporal locality**: recently accessed pages likely accessed again
- **Spatial locality**: nearby addresses likely accessed soon
- Past behavior is a good predictor of future behavior

## Cost in Practice

- Pure LRU is too expensive for general-purpose OS
- Modern OS uses **LRU approximations** (Clock, NFU, aging)
- Some specialized systems (databases) implement true LRU using linked lists
- LRU is the **gold standard** that approximation algorithms try to match
