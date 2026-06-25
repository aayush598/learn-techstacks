# File Access Methods

## Sequential Access
- **Read next**, **write next**, **rewind**
- File pointer tracks current position automatically
- Most common method; simplest to implement
- Used by: text editors, compilers, log files
- **Simulates sequential tape access**

## Direct Access (Relative Access)
- **Read block N**, **write block N** (N = relative block number)
- No file pointer needed; application provides block number
- Block = logical unit (not necessarily physical sector)
- Must convert logical block → physical block via file allocation method
- Used by: **databases**, **indexing systems**, **hash tables**

## Indexed Access
- **Index block** contains pointers to data blocks
- Search index, then access data block directly
- Combines sequential + direct benefits for complex queries
- Used by: **search engines**, **large archival systems**
- Overhead: index block storage + index lookup time

## Comparison Table

| Method | Speed | Fragmentation | Space Overhead | Best For |
|--------|-------|---------------|----------------|----------|
| **Sequential** | Fast (contiguous reads) | None (logically) | Minimal | Logs, streaming |
| **Direct** | Fast random access | External possible | Low | Databases |
| **Indexed** | Moderate random access | Negligible | Index block(s) | Large data, search |

## Memory-Mapped Files
- Map file into process virtual address space via `mmap()`
- File accessed as memory: reads/writes = page faults
- Benefits: **no syscalls** after mapping, **shared memory** between processes
- OS handles **page-in/page-out** automatically
- `mmap` vs `read/write`: `mmap` better for random access, `read/write` for sequential

## Key Interview Questions
- Can a file be both sequential and direct access? → Yes; OS supports both, `lseek()` switches mode
- How is `mmap` implemented? → VMA created → page fault loads file pages into page cache
- Trade-offs of indexed access? → Fast for random, but index itself must be in memory for performance
