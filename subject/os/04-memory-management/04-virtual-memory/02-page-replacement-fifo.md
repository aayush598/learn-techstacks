# Page Replacement: FIFO

## Algorithm

- **First-In, First-Out:** replace the page that has been in memory the longest
- Maintain a **queue** of pages in order of arrival
- On page fault: remove head, add new page to tail

### Example

```
Reference string: 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0
Frames = 3

7    0    1    2    0    3    0    4    2    3    0
7    0    1    2    2    3    0    4    2    3    3    ← faults marked
     7    0    1    1    2    3    0    4    2    0
          7    0    0    1    2    3    0    4    2

Faults: 7, 0, 1, 2, 3, 0, 4, 2, 3, 0 → 10 faults (with 3 frames)
```

## Belady's Anomaly

- **More frames can cause *more* page faults** (unique to FIFO)
- Counterintuitive: adding memory hurts performance
- Example: 3 frames → 9 faults, 4 frames → 10 faults (for certain reference strings)

```
Reference string: 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5
3 frames: 9 faults
4 frames: 10 faults  ← Belady's anomaly!
```

## Properties

| Property | Value |
|---|---|
| **Belady's anomaly?** | Yes |
| **Stack property?** | No |
| **Implementation** | Simple FIFO queue |
| **Performance** | Poor (causes Belady's) |
| **Overhead** | Minimal (queue pointer) |

## Stack Property

- A set of frames with size `m` is a **subset** of frames with size `m+1`
- Algorithms with stack property **cannot** suffer Belady's anomaly
- FIFO lacks stack property → Belady's possible

## When to Use

- Rarely used alone in modern OS
- Sometimes combined with reference bits (Clock = improved FIFO)
- Good for understanding Belady's anomaly conceptually
