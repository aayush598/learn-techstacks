# Clock Synchronization

## Physical Clocks
- **Clock drift**: crystal oscillator frequency varies
- **Skew**: difference between two clocks at same time
- Quartz drift: ~1 second per 10 days

## Cristian's Algorithm
- Client requests time from time server
- Server responds with current time `T`
- Client estimates RTT, sets time to `T + RTT/2`
- Assumes symmetric network latency

## NTP (Network Time Protocol)
| Feature | Detail |
|---------|--------|
| **Hierarchy** | Stratum 0 (atomic clock) → Stratum 1 → ... → Stratum 15 |
| **Accuracy** | ~10 ms on Internet, ~1 ms on LAN |
| **Algorithm** | Intersection algorithm picks best time from multiple servers |
| **Filter** | Marzullo's algorithm, discard outliers |
| **Mode** | Client-server or symmetric peer |
- **NTPv4**: RFC 5905, IPv6 support, improved accuracy

## Lamport's Logical Clock
- **Happens-before** relation (→): event ordering without wall clock
- Each process increments **counter** on each event
- Messages carry sender's clock; receiver sets `clock = max(clock, msg_clock) + 1`
- Total ordering: (clock, process_id) ties broken by process ID

## Vector Clock
- Each process maintains vector `[t1, t2, ..., tn]`
- Process `i` increments its own entry `ti` on each event
- Messages carry entire vector
- **Compare**: `V1 ≤ V2` if all entries ≤; concurrent if neither ≤ other
- Used in Dynamo, Riak for conflict detection

## Conflict Resolution
- **Last-Writer-Wins (LWW)**: timestamp wins; simpler, loses data
- **CRDTs** (Conflict-free Replicated Data Types): automatic merge
- Application-level merge (CouchDB, Dynamo)
