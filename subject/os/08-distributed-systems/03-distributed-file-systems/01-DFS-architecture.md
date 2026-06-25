# Distributed File Systems

## What is DFS?
- Files accessible across network as if **locally stored**
- Provides **location transparency**, naming, consistency
- Challenges: network latency, partial failure, concurrent access

## NFS (Network File System)
- **Stateless** protocol (v3): server doesn't track client state
  - Crash recovery: client retries, server doesn't need to remember
- **NFSv4**: stateful (delegations, compound operations), improved security
- Uses **RPC** (ONC RPC) over UDP/TCP
- Mount protocol: client mounts remote directory
- Security: AUTH_SYS (weak), Kerberos (stronger)

## AFS (Andrew File System)
- **Stateful**: server tracks open files, caches state
- **Whole-file caching**: entire file cached locally on first open
- **Callback**: server notifies client when file modified (cache invalidation)
- Better scalability than NFS (reduces server load)
- Used in educational environments (CMU, MIT)

## NFS vs AFS
| Feature | NFS | AFS |
|---------|-----|-----|
| State | Stateless (v3) | Stateful |
| Caching | Block-level | Whole-file |
| Consistency | Check-on-access | Callback |
| Scalability | Moderate | High |
| Crash recovery | Client retries | Server tracks state |

## GFS (Google File System)
- **Single master** + chunk servers
- Fixed-size **chunks** (64 MB). Chunk handle = 64-bit ID
- **Replication**: 3 copies by default (different racks)
- Writes: appended to chunk (atomic record append)
- Designed for large streaming reads, append-heavy writes
- Master stores metadata in memory (~64 bytes per chunk)

## HDFS
- Open-source implementation of GFS concepts
- **NameNode**: manages metadata (single point of failure — now HA)
- **DataNodes**: store blocks (default 128 MB, replication 3)
- `fsck` reports block health, `hdfs dfs` CLI
- Rack-aware placement: 1st copy same node, 2nd same rack, 3rd different rack
