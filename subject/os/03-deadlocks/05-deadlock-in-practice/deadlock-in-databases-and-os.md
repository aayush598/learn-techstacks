# Deadlocks in Practice

## OS: Ostrich Algorithm
- Most general-purpose OSes (Linux, Windows) **ignore deadlocks**
- Rationale: deadlocks are rare; prevention/avoidance overhead is not worth it
- "Stick head in sand" — pretend deadlocks never happen
- Users kill processes manually or reboot

## Databases: Full Detection + Recovery
- **Transaction**: unit of work with ACID properties
- **Two-Phase Locking (2PL)**:
  1. **Growing phase**: acquire locks, no release
  2. **Shrinking phase**: release locks, no acquire
- 2PL ensures serializability but is **deadlock-prone**

### MySQL InnoDB Deadlock Detection
```sql
-- InnoDB automatically detects deadlocks:
-- 1. Builds wait-for graph
-- 2. Selects victim (transaction with fewest locks)
-- 3. Rolls back victim transaction
-- 4. Returns error: "Deadlock found when trying to get lock"

-- Check deadlocks:
SHOW ENGINE INNODB STATUS;
```
- **Waits-for graph** built on each lock wait
- Cycle detection runs **immediately** when a transaction waits
- Victim selection: rollback the transaction that modified **fewest rows**

### Deadlock Prevention via Timeout
```sql
-- MySQL:
SET innodb_lock_wait_timeout = 50;  -- seconds
-- SQL Server:
SET LOCK_TIMEOUT 5000;  -- milliseconds
```
- Simple: process that times out is rolled back
- Problem: hard to distinguish deadlock from slow transaction

## Distributed Deadlocks
- **Wait-for graph across nodes**: harder to detect (no global state)
- **Timeout-based**: each node waits N seconds, then aborts
- **Centralized detector**: one node collects all WFG info (single point of failure)
- **Hierarchical**: local + global detection layers

## Comparison
| System | Approach | Mechanism |
|--------|----------|-----------|
| Linux kernel | Prevention | Resource ordering (lock ordering) |
| Windows | Prevention | Lock hierarchy + timeout |
| MySQL InnoDB | Detection + Recovery | WFG + victim rollback |
| PostgreSQL | Detection + Recovery | Deadlock timeout |
| Distributed systems | Timeout | Wait timeout → abort |
