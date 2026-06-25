# Distributed Mutual Exclusion

## Requirements
- Mutual exclusion: only one process in critical section
- Deadlock-free, starvation-free, fairness
- Must tolerate message loss/delay

## Centralized Algorithm
- Single **coordinator** process grants access
- Request → coordinator queues → reply (grant) → release
- Pros: simple, fair (FIFO)
- Cons: **single point of failure**, bottleneck

## Distributed (Ricart-Agrawala) Algorithm
- **Multicast** request to all other processes
- Reply = no interest or lower priority (logical clock timestamp)
- Enter CS when all replies received
- **Messages**: 2(N–1) per CS entry
- Deferred reply sent when requester has higher priority
- No single point of failure

## Token-Ring Algorithm
- Processes arranged in **logical ring**
- Single **token** circulates; only token holder enters CS
- Messages: 1 (pass token) to ∞ (if nobody needs CS, token keeps circulating)
- Pros: fairness, no starvation
- Cons: lost token = deadlock, ring management

## Comparison
| Algorithm | Messages/CS | Delay | Failure Handling |
|-----------|-------------|-------|------------------|
| Centralized | 3 | 2 msgs | Coordinator fails → deadlock |
| Ricart-Agrawala | 2(N–1) | 2 msgs | Process fails → timeout |
| Token-Ring | 1 to ∞ | 0 to N | Lost token → re-election |

## Election Algorithms
- **Bully algorithm**: highest ID becomes coordinator
  - Sends ELECTION to higher IDs; if no response, wins
  - O(n²) messages in worst case
- **Ring algorithm**: logical ring, highest ID wins
  - Each node forwards election message with max ID seen
