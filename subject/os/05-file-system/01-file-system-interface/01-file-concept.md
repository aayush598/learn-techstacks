# File Concept

## What is a File?
- **File**: named collection of related information stored on secondary storage
- Contiguous logical address space mapped to physical blocks by the OS

## File Attributes
| Attribute | Description |
|-----------|-------------|
| **Name** | Human-readable symbolic name |
| **Identifier** | Unique numeric tag (e.g., inode number) |
| **Type** | Regular, directory, device, pipe, socket |
| **Location** | Pointer to device + location on device |
| **Size** | Current size in bytes/blocks |
| **Protection** | Read/write/execute permissions (owner/group/other) |
| **Timestamp** | Creation, last access, last modification |

## File Operations
`Create` → `Write` → `Read` → `Reposition` (seek) → `Delete` → `Truncate` → `Open(F_i)` → `Close(F_i)`

- **Open**: copies file metadata into memory; returns a **file descriptor**
- **Close**: removes entry from per-process open-file table
- **Truncate**: keep attributes, erase data blocks

## Open File Tables (Two-Level)
```
Per-Process Table → System-Wide Open-File Table
```
- **Per-process table**: tracks file descriptors per process
- **System-wide table**: tracks all open files (reference count)
- On `open()`: entry created in per-process table pointing to system-wide entry
- On `fork()`: parent's file table copied; **shared** system-wide entry (shared offset)

## File Sharing & Locks
- **Shared lock** (read lock): multiple readers allowed
- **Exclusive lock** (write lock): only one writer
- **Mandatory locking**: OS enforces locks
- **Advisory locking**: processes cooperate (POSIX `flock`, `fcntl`)
- **Sticky bit**: `/tmp` — only owner can delete own files

## Key Interview Questions
- What happens when `open()` is called? → Path resolution → dentry lookup → inode loaded → file object created
- Difference between `open()` and `fopen()`? → `open()` is syscall, `fopen()` is stdio wrapper with buffering
- How does `dup2()` work? → Copies fd to another number, both share same system-wide file table entry
