# Memory-Mapped Files

## Concept

- File is **mapped into process's virtual address space**
- Page-sized portions loaded **on demand** (demand paging)
- File access = normal memory load/store (no read/write syscalls)
- File serves as the **backing store** instead of swap

## How It Works

1. `mmap()` system call maps file to virtual memory region
2. OS creates **VMAs** (Virtual Memory Areas) tracking mapped regions
3. On first access: page fault → OS reads file page into memory
4. On eviction: dirty pages written back to file (clean pages just discarded)
5. `munmap()`: unmaps the file from address space

### Address Space Layout

```
Process virtual memory:
+------------------+
| Code (mmaped exe)|
+------------------+
| Data             |
+------------------+
| Mapped file      | ← mmap region
+------------------+
| Stack            |
+------------------+
```

## mmap() Flags

| Flag | Behavior |
|---|---|
| **MAP_SHARED** | Changes written back to file, visible to other processes |
| **MAP_PRIVATE** | Copy-on-Write: changes local to process, not written to file |
| **MAP_ANONYMOUS** | No file backing (zero-filled, used for heap/malloc) |

## Benefits

- **No read/write syscalls:** eliminates OS overhead for file I/O
- **Simpler programming:** pointer-based file access
- **Shared memory:** MAP_SHARED allows IPC via file mapping
- **On-demand loading:** only faulted pages consume physical memory
- **Lazy loading:** executables are loaded this way (code pages faulted on demand)

## Disk ↔ Memory Mapping

```
Memory-mapped I/O:
  read(fd, buf, 4096) → syscall overhead, copy to user buffer
  mmap + access → page fault + direct load (no copy)

Memory-mapped: file pages cached in page cache (unified buffer cache)
  - No double buffering (no separate page cache + user buffer)
  - Same pages serve as both cache and process memory
```

## Executable Loading

- Operating system loads executables via **memory-mapped files**
- ELF (Linux) / Mach-O (macOS) / PE (Windows) mapped into memory
- Code and read-only data mapped MAP_PRIVATE (COW for data)
- **On-demand paging:** program starts instantly, pages faulted as needed
- Dynamic linker (`ld.so`) also uses mmap for shared libraries

## Example (POSIX)

```c
int fd = open("file.txt", O_RDWR);
char *map = mmap(NULL, size, PROT_READ | PROT_WRITE,
                 MAP_SHARED, fd, 0);
map[0] = 'A';  // directly modifies file page (eventually)
munmap(map, size);
```

## Memory-Mapped Files vs Regular I/O

| Aspect | Regular I/O (read/write) | Memory-Mapped |
|---|---|---|
| **Syscall overhead** | Per operation | Only mmap + page faults |
| **Copy** | Kernel → user buffer | No copy (fault directly) |
| **Caching** | Page cache + user buffer | Unified (page cache) |
| **Random access** | lseek + read | Pointer arithmetic |
| **Sharing** | Separate buffers per process | Shared physical pages |
