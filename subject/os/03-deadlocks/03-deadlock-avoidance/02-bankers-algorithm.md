# Banker's Algorithm

## Data Structures
| Matrix | Size | Meaning |
|--------|------|---------|
| `Available[m]` | m resources | Number of available instances of each resource |
| `Max[n][m]` | n processes × m resources | Maximum demand of each process |
| `Allocation[n][m]` | n × m | Currently allocated to each process |
| `Need[n][m]` | n × m | Remaining need = `Max - Allocation` |
| `Request[i][m]` | per invocation | Resources process i is requesting |

## Safety Algorithm (Check if state is safe)
```
Work[m] = Available[m]       // copy of available
Finish[n] = {FALSE}

Find i where Finish[i] == FALSE && Need[i] <= Work
If found: Work += Allocation[i]; Finish[i] = TRUE; repeat
If all Finish[i] == TRUE → system is SAFE
```

### Example (5 processes, 3 resources)
```
Available = (3, 3, 2)
          Allocation    Max       Need
          A  B  C     A  B  C   A  B  C
P0        0  1  0     7  5  3   7  4  3
P1        2  0  0     3  2  2   1  2  2
P2        3  0  2     9  0  2   6  0  0
P3        2  1  1     2  2  2   0  1  1
P4        0  0  2     4  3  3   4  3  1

Safe sequence: P1 → P3 → P4 → P0 → P2
```
- P1: Need(1,2,2) ≤ Work(3,3,2) → P1 finishes → Work=(5,3,2)
- P3: Need(0,1,1) ≤ Work(5,3,2) → P3 finishes → Work=(7,4,3)
- P4: Need(4,3,1) ≤ Work(7,4,3) → P4 finishes → Work=(7,4,5)
- P0: Need(7,4,3) ≤ Work(7,4,5) → P0 finishes → Work=(7,5,5)
- P2: Need(6,0,0) ≤ Work(7,5,5) → P2 finishes → All done ✅

## Resource-Request Algorithm
```
If Request[i] > Need[i] → error (exceeded max claim)
If Request[i] > Available → must wait
Else: pretend to grant:
  Available -= Request[i]
  Allocation[i] += Request[i]
  Need[i] -= Request[i]
  Run Safety Algorithm → if safe, grant; else rollback
```

## Limitations
- Processes must know **maximum** resource needs in advance (often unrealistic)
- Processes must be **independent** (no synchronization constraints)
- Number of processes must be **fixed**
- **O(m × n²)** complexity per request
- Not used in practice in pure form; inspires **resource reservation** in RTOS
