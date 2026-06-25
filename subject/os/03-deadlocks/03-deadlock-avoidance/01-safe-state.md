# Safe State & Deadlock Avoidance

## Definition
- A state is **safe** if there exists a **safe sequence** of process execution where:
  1. Each process can request its **maximum** needed resources
  2. Resources are available after previous processes finish
  3. All processes eventually complete

```
Safe state ⊇ Unsafe state ⊇ Deadlock state
```

## Safe vs Unsafe vs Deadlock
```
      All States
  ┌─────────────────┐
  │    Safe States   │
  │ ┌─────────────┐ │
  │ │   Unsafe    │ │
  │ │ ┌─────────┐ │ │
  │ │ │ Deadlock│ │ │
  │ │ └─────────┘ │ │
  │ └─────────────┘ │
  └─────────────────┘
```
- **Unsafe ≠ Deadlock**: an unsafe state *may* lead to deadlock depending on future requests
- Avoidance: ensure system **never enters unsafe state**

## Single Resource Example
```
Available = 10 units
P1: max=5, holding=2 → needs 3 more
P2: max=9, holding=5 → needs 4 more
P3: max=7, holding=3 → needs 4 more

Safe sequence: P1 (needs 3, avail=3 → avail becomes 2+3=5)
                 → P2 (needs 4, avail=5 → avail=5+5=10)
                 → P3 (needs 4, avail=10 → done)
```
- With avail=3 initially: P1 can finish → P2 can finish → P3 can finish ✅

## Prevention vs Avoidance
| Aspect | Prevention | Avoidance |
|--------|------------|-----------|
| Approach | **Static**: ensure one of 4 conditions never holds | **Dynamic**: evaluate each resource request |
| Knowledge needed | None | Must know **maximum** resource needs in advance |
| Utilization | Lower (overly conservative) | Higher (more flexible) |
| Example | Resource ordering | Banker's Algorithm |
