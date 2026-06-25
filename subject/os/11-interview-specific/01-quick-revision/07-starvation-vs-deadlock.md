# Starvation vs Deadlock

## Comparison Table

| Property | Starvation | Deadlock |
|----------|------------|----------|
| **Definition** | Process never gets resources it needs | Processes blocked waiting for each other |
| **Progress** | Could resolve eventually (aging) | **Permanent** without intervention |
| **Recovery** | Automatic possible (priority aging) | Requires external action (kill, preempt, reboot) |
| **Conditions** | No specific conditions needed | 4 necessary conditions (Coffman) |
| **Example** | SJF scheduling: short jobs always arrive → long job starves | Thread A locks R1 waits R2; Thread B locks R2 waits R1 |
| **System impact** | One process affected (others run fine) | **All** deadlocked processes blocked permanently |
| **Detection** | Hard (lack of progress over time) | Easier (cycle detection in resource graph) |

## Deadlock — 4 Necessary Conditions (Coffman)
1. **Mutual Exclusion:** resource can only be held by one process at a time
2. **Hold & Wait:** process holds resources while waiting for others
3. **No Preemption:** resource can't be taken away forcibly
4. **Circular Wait:** cycle of processes each waiting for the next

### Deadlock Prevention (Break one condition)
- **No Hold & Wait:** request all resources at once (low utilization)
- **Preemption:** if waiting, release held resources (complex rollback)
- **No Circular Wait:** resource ordering/hierarchy (always lock in same order)

### Deadlock Avoidance (Banker's Algorithm)
- Pre-declare max resource needs
- OS checks if granting leads to **safe state** (sequence where all finish)
- **Safe state:** there exists a sequence of completion for all processes

### Deadlock Detection + Recovery
- **Detection:** wait-for graph → cycle detection (O(n²))
- **Recovery:** preempt resource, kill process, rollback
- Linux: **not implemented** — OOM killer is closest for memory

## Starvation — Causes & Solutions
- **Priority scheduling** (high-priority jobs always skip low-priority)
- **SJF** (short jobs keep arriving)
- **Reader-writer locks** (writers starve if readers keep coming)
- **Solution: Aging** — gradually increase priority of waiting processes
- Linux CFS: weighted fair queuing prevents starvation (all processes get CPU time)

## Dining Philosophers Example
- **Deadlock:** all pick up left chopstick → wait for right
- **Starvation:** philosopher next to a fast eater may never eat
- Deadlock-free solution: pick up both or none (odd/even), resource hierarchy, max 4

## Interview Tip
- *"Deadlock = circular wait with no escape; starvation = never scheduled despite being ready"*
- *"Deadlock prevention: lock ordering is the most practical approach"*
- *"Aging solves starvation: gradually increase priority of waiting processes"*
