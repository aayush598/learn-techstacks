# Deadlock — 4 Necessary Conditions

## Definition
- A set of processes is **deadlocked** if each process in the set is waiting for an event that only another process in the set can cause

## 4 Necessary Conditions (ALL must hold)
| Condition | Description | Analogy |
|-----------|-------------|---------|
| **1. Mutual Exclusion** | At least one resource must be held in non-sharable mode | Single-lane bridge — only one car at a time |
| **2. Hold & Wait** | Process holds at least one resource while waiting for additional resources | Car occupies one lane while waiting for next bridge |
| **3. No Preemption** | Resources cannot be forcibly taken away — only released voluntarily | Can't push a car off the bridge |
| **4. Circular Wait** | There exists a set {P₀, P₁, ..., Pₙ} where P₀ waits for P₁, P₁ waits for P₂, ..., Pₙ waits for P₀ | Cars blocking each other at a 4-way intersection |

### Key Insight
```
ALL 4 conditions must hold simultaneously for deadlock to occur.
If any one condition is broken → deadlock is impossible.
```

## Real-World Example: Cars at Intersection
- 4 cars arrive simultaneously at a 4-way stop
- Each car holds one quadrant and waits for the next car to move
- **Mutual exclusion**: each quadrant occupied by one car
- **Hold & wait**: each car holds its quadrant, waits for next
- **No preemption**: can't push cars out of the way
- **Circular wait**: each car waits for the car to its right

## Resource Categories
- **Reusable**: memory, CPU, files — finite instances
- **Consumable**: interrupts, signals — created and destroyed
