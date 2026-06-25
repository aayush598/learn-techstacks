# Election Algorithms & Consensus

## Leader Election
- Needed when current leader fails (crash, network partition)
- All nodes must eventually agree on new leader
- Properties: safety (at most one leader), liveness (leader eventually elected)

## Bully Algorithm
1. Process `P` detects leader is down → sends **ELECTION** to all higher-ID processes
2. If no response → `P` declares itself leader (**COORDINATOR** message)
3. If higher-ID responds → `P` steps down, that process takes over
4. Worst case: O(n²) messages (lowest ID starts election)
- Greedy: highest-ID process "bullies" others

## Ring Algorithm
1. Processes arranged in logical ring (each knows successor)
2. Detect leader failure → send ELECTION message (with own ID) to successor
3. Each adds its ID and forwards
4. When message returns to sender → pick highest ID → send COORDINATOR
- Messages: **2n** (one election round, one coordinator round)

## Consensus Algorithms

### Paxos
- **Roles**: Proposer, Acceptor, Learner
- **Phases**:
  1. Prepare: proposer sends proposal number `n` to acceptors
  2. Promise: acceptor promises not to accept < `n` (returns accepted value if any)
  3. Accept: proposer sends `(n, value)` — acceptor accepts if no higher n seen
- Requires **majority** (quorum) to make progress
- Guarantees safety under async, partial failures (FLP result)

### Raft
- Understandable Paxos alternative (by Ongaro & Ousterhout)
- **Leader election**: randomized timeouts → candidate → leader
- **Log replication**: leader receives writes, replicates to followers
- **Commitment**: entry committed when majority replicates it
- **Strong leader**: all writes go through leader

### ZooKeeper (ZAB)
- **Zab protocol**: crash-recovery, atomic broadcast
- Leader ensures total order across replicas
- Used for coordination, service discovery, locks

### etcd
- **Raft**-based key-value store
- Used by Kubernetes (store cluster state)
- `etcdctl` CLI, watch API for change notifications
