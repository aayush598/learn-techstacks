# Recovery from Deadlock

## Option 1: Process Termination

### Abort All Deadlocked Processes
- ✅ Simple, guaranteed to break deadlock
- ❌ Expensive — may have computed partial results, lost work
- ❌ May need to restart from scratch

### Abort One Process at a Time
- After each abort, re-run detection algorithm
- Continue until deadlock is eliminated
- ❌ Significant overhead per iteration

### Cost Minimization Factors
- **Priority**: lower priority first
- **CPU time used**: abort processes with least CPU consumed
- **Remaining time**: abort those closest to completion (paradoxical but common)
- **Resources held**: abort process holding the most resources (frees more)
- **Process type**: batch (easier to restart) vs interactive (user-visible)

## Option 2: Resource Preemption

### Key Decisions
| Decision | Question |
|----------|---------|
| **Select victim** | Which process to preempt? (cost-based) |
| **Rollback** | How far back? (checkpoint states) |
| **Starvation** | Ensure same process isn't repeatedly victimized |

### Checkpoint & Rollback
- Save process state at **checkpoints** (safe states)
- Rollback to a checkpoint before acquiring the deadlock-causing resource
- **Transaction-like** guarantee:
  - Database transactions: explicit `BEGIN` / `ROLLBACK`
  - OS: transparent checkpointing (expensive)

### Selecting a Victim
- Minimize **cost factors**:
  - Amount of CPU time consumed
  - Number of lines of output printed
  - Type of resource held (preemptible vs non-preemptible)
  - Time until completion

### Starvation Problem
- Same process may be repeatedly selected as victim
- **Solution**: include **rollback count** in cost factor (increase priority after each preemption)
- Ensures fairness in victim selection

## Practical Notes
- **Most OSes ignore deadlocks** (ostrich algorithm)
- **Databases** handle recovery with transaction rollback
- **Real-time systems** use prevention via resource ordering
