# Directory Implementation

## Data Structures for Directories

### Linear List
- Simple **array/linked list** of (name, inode_number) pairs
- **Create**: append entry O(1)
- **Delete**: search O(n) + rearrange/compact
- **Lookup**: linear scan O(n) — slow for large directories
- Used in: very old FS, embedded systems with few files

### Hash Table
- Hash file name → index into hash table → linear list at that slot
- **Lookup**: O(1) average, O(n) worst-case (collisions)
- **Challenges**: fixed table size, resizing expensive, **collision handling**
- Used in: early Unix, some simple FS implementations
- **Rehashing** needed when load factor grows

### B-Tree (B+ Tree)
- Balanced tree with **O(log n)** for all operations
- **Ordered keys** enable range queries and sequential access
- Used in: **ext4** (HTree), **NTFS** (B+ tree), **HFS+**
- B+ tree: all data in leaves, internal nodes are keys only

## Big-O Comparison

| Structure | Lookup | Insert | Delete | Space | Notes |
|-----------|--------|--------|--------|-------|-------|
| **Linear list** | O(n) | O(1) | O(1)* | O(n) | *after lookup |
| **Hash table** | O(1) avg, O(n) worst | O(1) | O(1) | O(n) | Collision handling needed |
| **B-Tree** | O(log n) | O(log n) | O(log n) | O(n) | Balanced, disk-friendly |

## ext4 HTree
- **Hash tree index** for directories (> ~2-4KB directory)
- Uses **dx_root** and **dx_node** blocks containing hash ranges
- Lookup: hash filename → traverse HTree → locate leaf block
- Prevents O(n) scans in large directories (millions of files)

## Key Interview Questions
- Why not use B-tree for everything? → Overhead for small directories; linear list is faster for < ~100 entries
- How does ext4 handle large directories? → HTree index (directory is indexed when it exceeds one block)
- What's the **dentry cache**? → In-memory cache of recently used directory entries (path → inode); LRU eviction
- How does `ls` on a directory with 1M files work? → `getdents()` syscall; dentry cache warms up; ext4 uses HTree
