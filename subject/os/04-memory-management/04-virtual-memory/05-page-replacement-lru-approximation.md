# LRU Approximation Algorithms

## Why Approximate?

- Pure LRU is too expensive (counter update on every memory access)
- Hardware provides **reference bit** (set to 1 when page is accessed)
- OS can use reference bits to approximate LRU without per-access overhead

## Second-Chance (Clock) Algorithm

- Pages arranged in **circular list** (clock hand)
- Each page has a **reference bit** (set to 1 by hardware on access)
- On page fault: advance clock hand, check reference bit
  - **Bit = 1:** clear it, move on (second chance)
  - **Bit = 0:** evict this page
- FIFO + single reference bit = "second chance"

```
     +--[P1:1]--[P2:0]--[P3:1]--+
     |                            |
     +----------------------------+
           ^ clock hand
```

- If all bits are 1 → cycle through, clear all bits → behaves like FIFO
- Performance close to LRU, overhead low

## Enhanced Second-Chance

- Uses **two bits**: reference bit + modify (dirty) bit
- Four classes (ordered best to worst for eviction):

| Class | Reference | Modify | Meaning |
|---|---|---|---|
| (0,0) | 0 | 0 | Not used recently, clean → **best to evict** |
| (0,1) | 0 | 1 | Not used recently, dirty → write back needed |
| (1,0) | 1 | 0 | Used recently, clean |
| (1,1) | 1 | 1 | Used recently, dirty → **worst to evict** |

- Prefers clean pages (avoid disk write on eviction)
- Used in various UNIX systems (BSD, macOS)

## NFU (Not Frequently Used) with Aging

- Each page has a **counter** (typically 8 bits)
- At regular intervals (timer interrupt):
  - Shift counter right by 1
  - Add reference bit to **most significant bit** of counter
  - Clear reference bit
- Counter value = exponentially decaying history of references
- Smaller counter = less frequently used recently → evict

```
Reference bits over time: 1 0 0 1 1 0 1 0

Counter evolution (shift right, add ref at top):
Time 1: 10000000 (ref=1)
Time 2: 01000000 (ref=0)
Time 3: 00100000 (ref=0)
Time 4: 10010000 (ref=1, shift then add)
...
```

- This is actually an **aging** algorithm, very close to LRU
- Used in Linux (variant: **Page Active/Referenced** flags)

## LFU (Least Frequently Used)

- Count **how many times** each page is referenced
- Evict page with **lowest reference count**
- Problem: pages used heavily early stay in memory forever
- Solution: periodic decay (reset counters) or move to aging approach

## Comparison

| Algorithm | LRU Quality | Overhead | Complexity |
|---|---|---|---|
| Clock (Second-Chance) | Moderate | Low | Simple |
| Enhanced Clock | Good | Low | Moderate |
| NFU + Aging | Near-LRU | Moderate | Moderate |
| LFU | Poor (stale counts) | Low | Simple |
