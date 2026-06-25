# RAID Levels

## RAID Overview
- **RAID**: Redundant Array of Independent (Inexpensive) Disks
- Goals: **performance** (parallelism) + **reliability** (redundancy)
- **Striping**: split data across N disks (speedup for sequential/parallel I/O)
- **Mirroring**: duplicate data on 2+ disks (complete redundancy)
- **Parity**: compute XOR of N stripes, tolerates 1 disk failure

## RAID Levels

| Level | Name | Description | Min Disks | Redundancy | Capacity Efficiency | Read Speed | Write Speed |
|-------|------|-------------|-----------|------------|-------------------|------------|-------------|
| **RAID 0** | Striping | Data striped across disks | 2 | ❌ None | 100% | Excellent | Excellent |
| **RAID 1** | Mirroring | Full duplicate | 2 | ✅ 1 disk | 50% | Good (read from either) | Moderate |
| **RAID 5** | Striping + Parity | Single distributed parity | 3 | ✅ 1 disk | (N-1)/N | Good (stripe reads) | Slow (parity calc) |
| **RAID 6** | Dual Parity | Two parity blocks | 4 | ✅ 2 disks | (N-2)/N | Good | Slowest (dual parity) |
| **RAID 10** | RAID 1+0 | Mirror + stripe | 4 | ✅ 1 per mirror | 50% | Excellent | Good |

## Detailed Breakdown

### RAID 0 (Striping)
- Data split into **stripes**, written round-robin across disks
- If one disk fails → **all data lost**
- Use: temp storage, caching, non-critical data

### RAID 1 (Mirroring)
- Every write goes to both disks; read can come from either (load balancing)
- **Write penalty**: 2× writes
- Use: OS disks, critical databases (with RAID 10)

### RAID 5 (Striping + Parity)
- **Parity block** distributed across all disks (not dedicated parity disk)
- Write: read old data + old parity → compute new parity → write data + parity (**4 I/Os per write**)
- Can survive **1 disk failure**; rebuild by XOR-ing remaining data + parity
- **Write penalty**: 4 I/Os (read old data, read parity, write data, write parity)

### RAID 6 (Dual Parity)
- Two parity blocks using **Reed-Solomon** or **P+Q** encoding
- Survives **2 simultaneous disk failures**
- Write penalty: 6 I/Os

### RAID 10 (Stripe of Mirrors)
- First mirror pairs, then stripe across pairs
- Best performance + redundancy for OLTP databases
- Can lose up to N/2 disks (as long as no pair loses both)

## Key Concepts
- **Write penalty**: additional I/Os needed for parity; RAID 10 has lowest (2×), RAID 6 has highest (6×)
- **Rebuild time**: time to reconstruct data on replacement disk; larger disks = longer rebuild = higher risk
- **Hot spare**: standby disk ready to replace failed disk automatically
- **JBOD**: Just a Bunch Of Disks — no RAID, just concatenation

## Key Interview Questions
- RAID 5 vs RAID 10 for a database? → RAID 10: lower write penalty, faster rebuild, better for random writes
- Why not RAID 5 on large (10TB+) disks? → **URE rate** (Unrecoverable Read Error) makes rebuild failure likely
- What is **RAID 50/60**? → Nested RAID: RAID 0 over RAID 5 groups (striped parity sets)
- Software RAID vs hardware RAID? → Software: CPU overhead, flexible; Hardware: dedicated controller, cache, battery backup
