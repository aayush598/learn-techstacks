# Resource Allocation Graph (RAG)

## Graph Components
| Symbol | Meaning |
|--------|---------|
| Circle (○) | Process |
| Square (□) | Resource type |
| Dot (•) inside square | Instance of resource |
| P → R | **Request edge** — process wants resource |
| R → P | **Assignment edge** — resource assigned to process |

```
    ┌───┐
P₁ →│ R │
    └───┘
```
P₁ has a request edge to R (waiting for R)

## Cycle Detection Rules
| Scenario | Deadlock? |
|----------|-----------|
| No cycle in RAG | **No deadlock** |
| Cycle exists, **1 instance per resource** | **Deadlock** |
| Cycle exists, **multiple instances** | **Possible** deadlock (may be no deadlock) |

## Examples

### Deadlock (1 instance each)
```
P₁ → R₁ → P₂ → R₂ → P₁  (cycle)
```
- P₁ holds R₂, wants R₁
- P₂ holds R₁, wants R₂
- Single-instance → **deadlock**

### Cycle but No Deadlock (multi-instance)
```
P₁ → R₁ → P₂ → R₂ → P₁  (cycle)
```
- R₁ has 2 instances, only 1 assigned to P₂
- R₂ has 2 instances, only 1 assigned to P₁
- P₁ may get R₁ from remaining instance → cycle breaks

## Reduction
- Find process that can finish (all requested resources available)
- Release its resources (remove edges)
- Repeat: if all edges removed → no deadlock; else → deadlocked

## Wait-For Graph (WFG)
- Convert RAG: if P₁ is waiting for resource held by P₂ → edge P₁ → P₂
- Used by detection algorithms (simplifies cycle detection)
