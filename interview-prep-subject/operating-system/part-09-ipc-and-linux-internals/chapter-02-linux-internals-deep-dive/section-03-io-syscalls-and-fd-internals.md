# I/O Syscalls and File Descriptor Internals

> **TL;DR**: `open` allocates an **fd** (an index into the process's fd table) pointing to a `struct file` (open file description: offset, flags, `f_op`) whose `f_op` are the VFS operations that route to a specific filesystem/device. `read`/`write` go through the page cache (`address_space`) or direct to the device; `mmap` maps file pages into the address space. fd tables are **copied** on fork, **shared** with `CLONE_FILES`/threads, and `dup` shares the same `struct file`.

## 1. Why Does This Exist?
The POSIX file API (`open`/`read`/`write`/`close`/`mmap`) must work uniformly for regular files, directories, devices, sockets, pipes, and pseudo-filesystems. The fd abstraction is how: a small integer per process indexes a table of pointers to kernel objects, and every read/write dispatches through function pointers to the right implementation. It also cleanly separates three "levels" of sharing: the **fd table** (per process), the **open file description** (`struct file`, shared across `dup`/`fork`-inherited fds — they share the offset), and the **inode** (shared by all opens of the same file). Understanding the path `open`→fd→`struct file`→`f_op`→`address_space`→block/device layer answers most Linux I/O interview questions.

## 2. How Does It Work?
**Levels of the API**:
- **fd (file descriptor)**: an `int` — index into `current->files->fdtab` (an array of pointers, grown on demand). Points to `struct file *`.
- **`struct file`** (`include/linux/fs.h`): the *open file description* — `f_path` (dentry+mount), `f_pos` (file offset), `f_mode` (O_RDWR...), `f_flags` (O_APPEND, O_NONBLOCK), `f_op` (the VFS operation table), `f_mapping` (`address_space`), `f_count` (refcount). Shared by `dup`/`dup2` and inherited fds after fork → shared offset.
- **`struct inode`**: the file object itself (metadata) — shared by every open of the same file (even across processes).
- **`f_op` (file_operations)**: `read_iter`, `write_iter`, `llseek`, `mmap`, `fsync`, `open`, `release`, `flush`, `poll`, `unlocked_ioctl`... — filled in by the VFS from the filesystem/driver when the file is opened.

**`open` path**:
1. `sys_openat` → `do_sys_open` → `getname` (copy path) → `path_openat` (namei resolution: dcache → `i_op->lookup` per component) → `do_dentry_open`: sets `f_op` from the inode's `i_fop` (or special-case for sockets/pipefs), calls `f_op->open` if any.
2. Allocate an fd: `fd_install(fd, file)` — an empty slot in the fd table (lowest free, honoring `O_CLOEXEC`/`FD_CLOEXEC`).
3. Return the fd.

**`read`/`write` path**:
1. `sys_read(fd, buf, n)` → `fdget_pos(fd)` (get `struct file`, take `f_pos` lock) → `vfs_read` → `f_op->read_iter` (most FSs: `generic_file_read_iter` — page-cache backed) → `filemap_read` → `find_get_page`/`readahead` → if miss, `mapping->a_ops->readpage`/`readahead` → `submit_bio` → block layer → device driver → DMA.
2. `write`: `vfs_write` → `f_op->write_iter` → `generic_perform_write` → `a_ops->write_begin`/`write_end` (fill page cache, mark dirty) → at flush (`writepages`), `f_op->fsync`/writeback → `submit_bio`.

**`mmap` path**: `sys_mmap` → `do_mmap` (validate, find VMA range) → `f_op->mmap` (file-backed) → `filemap_mmap` → builds `vm_area_struct`; page faults on access go through `filemap_fault` → `a_ops->readpage`. For `MAP_SHARED`, writes flush back (shared file). For `MAP_PRIVATE`, COW.

**fd sharing**:
- `fork` (no `CLONE_FILES`): fd table **copied** — each copy points at the same `struct file`s (`f_count++`); offset is shared (they're the same open description).
- Threads (`CLONE_FILES`): fd table **shared** — all threads see the same fds.
- `dup`/`dup2`/`dup3`: new fd → same `struct file` → shared offset (this is how shell redirection works: `dup2(pipe_fd, 1)`).
- `open` twice: two different `struct file`s (separate offsets) → the same inode.
- `close`: `filp_close` → `f_op->release` (or `flush`) when `f_count` hits 0 → last close frees.

## 3. When Is It Used?
- Every file I/O in every program (`open`/`read`/`write`/`close`), including stdio (glibc wraps them in `fopen`/`fread`).
- Devices (character/block drivers via `open` + `ioctl`/`read`/`write`), sockets (fd-based), pipes, epoll (fds for everything), eventfd/signalfd/timerfd (fd-ized interfaces).
- Shell redirection (`dup2`), `fork` inheritance (child gets the parent's fds), `exec` with `CLOEXEC` (close-on-exec so fds don't leak into new programs).
- `mmap` for zero-copy reads, shared memory, loading executables and shared libraries.
- Polling/multiplexing: `select`/`poll`/`epoll` on fds; `io_uring` for high-performance async I/O.

## 4. Why Wasn't Another Approach Chosen?
- **Path-based I/O every time (rejected)**: resolving paths per op is slow and racy; the fd is an O(1) handle after one resolution.
- **Pointers into the kernel (rejected)**: user space must never hold kernel pointers — an fd is a safe, capability-like index.
- **One global open-file table without per-process indirection (rejected)**: per-process fd tables give isolation (each process has its own numbering) + inheritance semantics (fork) + close-on-exec control.
- **No page cache / direct I/O everywhere (rejected)**: the page cache gives readahead, sharing, and write coalescing — that's why `read`/`write` go through `address_space`; `O_DIRECT` bypasses it only when the app explicitly asks.
- **`mmap` for all I/O (rejected)**: mapping everything has page-fault costs and cache effects; `read`/`write` remain simpler for sequential streams — the API offers both.

## 5. Intuition
**A coat-check counter**: `open` hands you a numbered ticket (the fd); your coat (the `struct file`) hangs in the back with your name on it (offset, flags) and instructions for how to handle it (`f_op` — "this coat is on a hook", "this one's on a conveyor", "this one's a magic coat that generates itself"). Two people given *the same ticket number* (dup/fork-shared fds) share the same coat and the same place in line (offset). Two separate tickets for the same coat (open twice) are two separate "handlers" but the same coat (inode). `read`/`write` = asking the attendant to fetch/put items according to the coat's handler.

## 6. Real-World Analogy
**A hotel room key system**: a guest's keycard (fd) opens a specific room (`struct file`) in a specific hotel (VFS mount). The hotel knows which housekeeping team handles which room type (`f_op`). Two keycards copied at the front desk (dup) open the same room and share the thermostat setting (offset). A guest with a card for room 404 and another with a card for room 404 from the same booking (two opens) are two separate room accesses to the same room (same inode). When the last keycard for a room is returned (close), the room is cleaned and returned to inventory.

## 7. Formal Definition
An fd is an integer indexing the process's `struct fdtable` (`files_struct->fdtab`), a growing array of `struct file *`. A `struct file` is the open file description: `f_path` (struct path: vfsmount + dentry), `f_pos` (offset), `f_flags`/`f_mode`, `f_op` (file_operations table), `f_mapping` (address_space), `f_count` (atomic refcount), `f_lock`. The VFS dispatch: `sys_read` → `ksys_read` → `vfs_read` → `f_op->read_iter` (or `new_sync_read` wrapper). Buffered I/O uses the page cache through `file->f_mapping->a_ops` (`readpage`, `writepage`, `write_begin`, `write_end`, `readahead`); block-backed filesystems call `submit_bio` to the block layer. `mmap` creates a `vm_area_struct` (with `vm_ops = {fault, page_mkwrite}`) and faults route to `a_ops`. Sharing rules: `fork` copies the fd table (same `struct file`s, refcounted); `CLONE_FILES`/threads share it; `dup` aliases one `struct file`; each `open` creates a distinct `struct file` for the same inode.

## 8. Example
Shell redirection `echo hi > file`:
1. `open("file", O_WRONLY | O_CREAT | O_TRUNC, 0644)` → returns fd 3 (0/1/2 already taken).
2. `dup2(3, 1)` — copy fd table entry: now fd 1 and fd 3 point at the **same `struct file`** (shared offset). The old fd 1 (terminal) is closed.
3. `close(3)` — the alias is gone; fd 1 still refers to the file.
4. `write(1, "hi\n", 3)` → goes to the file (offset shared with the description).
5. `close(1)` → last reference → `release` → file closed.

`fork` fd inheritance:
- Parent opens `f`, then `fork()`s. Child's fd table is a copy pointing at the same `struct file` (offset shared). Parent and child both writing to fd `f` interleave at the shared offset — unless `O_APPEND` (atomic append) or each reopens.

`mmap` zero-copy read:
```c
int fd = open("big.bin", O_RDONLY);
char *p = mmap(NULL, 4096*1000, PROT_READ, MAP_PRIVATE, fd, 0);
// p[..] fault the file's pages into the page cache; no read() copy
```

## 9. Internal Working
1. `open`: `do_sys_openat2` → `path_openat` (path resolution via `nameidata`, dcache `d_lookup` → `i_op->lookup`) → `do_dentry_open` (pick `f_op` from inode's `i_fop` or `DEFINE_FILE_OPERATIONS`, apply `O_*` flags, call `f_op->open`) → `alloc_fd` (`get_unused_fd_flags`) → `fd_install`.
2. `read`: `fdget_pos` → `vfs_read` (check `f_mode` allows read, `rw_verify_area`) → `f_op->read_iter` → `generic_file_read_iter` → `filemap_read`: look up page in `mapping`'s xarray/radix → miss → `filemap_get_pages` (readahead) → `a_ops->readpage` → `submit_bio`. Copy to user via `copy_to_iter`; advance `f_pos`.
3. `write`: `vfs_write` → `f_op->write_iter` → `generic_perform_write` → `a_ops->write_begin` (grab/zero page) → copy from user → `write_end` (mark dirty, set page dirty in mapping). Dirty pages later flushed by `writeback` (`flush_dirty_buffers`/`wb_workfn`) → `f_op->writepages` → `submit_bio`. `fsync`/`fdatasync` forces.
4. `close`: `close_fd` → `filp_close` → `flush` (if `f_op->flush`) → `fput` → when `f_count==0`: `__fput` → `f_op->release` → free.
5. `mmap`: `do_mmap` → `mmap_region` → `f_op->mmap` (file-backed) → `vm_ops` installed; faults (`handle_mm_fault`) → `filemap_fault` (reads page) or `do_wp_page` (COW).
6. Multiplexing: `epoll_ctl` registers interest on fds; `epoll_wait` returns ready fds via the wait-queue mechanism.

## 10. Time Complexity
- `open`: O(path components) resolution (dcache hits O(1) each; misses hit disk) + O(1) fd alloc.
- `read`/`write` (buffered, page-cache hit): O(1) per page + copy O(bytes); syscall overhead ~µs.
- `read`/`write` (page miss): + disk I/O (ms).
- `close`: O(1) (decrement `f_count`; free when 0).
- `dup`/`dup2`: O(1) (copy one pointer, refcount++).
- `fork` fd table copy: O(fd_count).
- `mmap`: O(1) VMA insertion (rbtree O(log n)); faults O(1) per page.
- `epoll_wait`: O(ready events), registration O(1).

## 11. Advantages
- **Uniform API**: files, devices, sockets, pipes — all fds; one set of syscalls.
- **Safe handles**: no kernel pointers leak; O_CLOEXEC/close semantics control lifetime.
- **Efficient**: one-time resolution, then O(1) ops; page cache for buffered I/O; `mmap` zero-copy.
- **Flexible sharing**: fd-table copy (fork), shared (threads), alias (dup) — each intentional.
- **Extensible**: fds for eventfd/signalfd/timerfd/epoll — "everything is a file" done right.
- **Observable**: `lsof`, `/proc/<pid>/fd`, `fdinfo`.

## 12. Disadvantages
- **fd exhaustion**: `RLIMIT_NOFILE` (ulimit -n) — leaks/high fan-out hit the cap.
- **Sharing complexity**: fork-shared offsets can surprise (interleaving writes); needs O_APPEND or per-open offsets.
- **Buffer/cache effects**: page cache delays writeback; `O_DIRECT`/`fsync` semantics are subtle.
- **Security surface**: fd passing across processes (`SCM_RIGHTS`) needs care; TOCTOU on paths (mitigate with `openat`/`O_NOFOLLOW`).
- **Positional state**: shared `f_pos` across dup/fork makes thread-safe sequential I/O tricky (use pread/pwrite).

## 13. Interview Questions
1. **Q: What is a file descriptor?** A: An integer index into the process's fd table pointing to a `struct file` (the open file description) — a safe handle giving the kernel object for I/O.
2. **Q: fd table vs `struct file` vs inode?** A: fd table = per-process indices; `struct file` = one *open* instance (offset, flags, `f_op`) shared by dup/fork-inherited fds; inode = the file object itself, shared by all opens of the same path.
3. **Q: What happens in `open`?** A: `do_sys_open` → path resolution (namei/dcache) → `do_dentry_open` picks `f_op` from the inode, applies flags, calls `f_op->open` → allocate an fd slot → return the fd.
4. **Q: What is `f_op`?** A: The `file_operations` table — `read_iter`, `write_iter`, `llseek`, `mmap`, `fsync`, `release`, etc. — the VFS's per-file method vector (Part 08 Sec 04) that dispatches read/write to the right filesystem/device.
5. **Q: What is shared when you fork?** A: The fd table is *copied* (each process has its own), but the `struct file`s are shared (refcounted) — so the offset and flags are shared; threads share the whole fd table (`CLONE_FILES`).
6. **Q: What is the difference between `dup` and `open` twice?** A: `dup` creates a second fd aliasing the **same `struct file`** (shared offset); `open` twice creates two `struct file`s (independent offsets) for the same inode.
7. **Q: What does `read` actually do?** A: `sys_read` → `vfs_read` → `f_op->read_iter` → page cache (`address_space`): lookup pages, fault/readahead on miss, `submit_bio` to the block layer, copy to user, advance `f_pos`.
8. **Q: What is the page cache's role?** A: It's the `address_space`-backed cache of file pages shared across processes — buffered reads/writes go through it (readahead, write coalescing, sharing); `O_DIRECT` bypasses it.
9. **Q: How does `mmap` differ from `read`?** A: `mmap` maps file pages into the address space (`vm_area_struct` + `vm_ops`), and faults bring pages in via the page cache — reads become memory accesses (zero copy); writes go back through the cache (or COW with MAP_PRIVATE).
10. **Q: What is `O_CLOEXEC`?** A: A flag marking the fd close-on-exec — the kernel closes it during `exec` so the new program doesn't inherit it (prevents fd leaks across exec; the recommended default).
11. **Q: Why do we need `fsync`?** A: Buffered writes sit dirty in the page cache until writeback; `fsync`/`fdatasync` forces data (+ metadata) to the device — durability. Without it, a crash can lose acknowledged-but-unflushed data.
12. **Q: How does `lsof`/`/proc/<pid>/fd` work?** A: They enumerate the process's fd table (symlinks to the file paths) — reading `current->files` from `/proc` — the observable side of the fd layer.

## 14. Follow-Up Questions
1. **Q: What is the difference between `read` and `pread`?** A: `pread` takes an explicit offset and doesn't update `f_pos` — safe for concurrent I/O on a shared `struct file` (no offset race).
2. **Q: What is `io_uring`?** A: The high-performance async I/O interface: submission/completion rings in shared memory, batch syscalls, reduced overhead — the modern replacement for aio/epoll in hot paths.
3. **Q: What is `SCM_RIGHTS`?** A: Passing an fd over a Unix-domain socket (`sendmsg` ancillary data) — moving the `struct file` reference to another process.
4. **Q: What happens on `exec` with fds?** A: Fds without `FD_CLOEXEC` survive (inherited); with it, they're closed — the child starts with a cleaned fd table (stdin/stdout/stderr + deliberately-kept fds).

## 15. Coding Example
```c
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/mman.h>

int main(void) {
    // 1. open -> fd
    int fd = open("/tmp/demo.txt", O_CREAT | O_RDWR, 0644);
    write(fd, "hello fd", 8);
    printf("fd = %d\n", fd);

    // 2. dup shares the same struct file (same offset)
    int fd2 = dup(fd);
    write(fd2, " again", 6);            // appends at the shared offset

    // 3. fork copies the fd table, shares struct file
    pid_t pid = fork();
    if (pid == 0) { write(fd, " child", 6); _exit(0); }
    // parent: reads the whole file at its own offset... use pread for safety
    char buf[32] = {0};
    ssize_t n = pread(fd, buf, sizeof buf, 0);   // explicit offset, no race
    printf("file: %.*s\n", (int)n, buf);

    // 4. mmap for zero-copy read
    char *p = mmap(NULL, 64, PROT_READ, MAP_PRIVATE, fd, 0);
    printf("mmap[0]: '%c'\n", p[0]);

    close(fd); close(fd2);
    unlink("/tmp/demo.txt");
    return 0;
}
```

## 16. Industry Usage
- **Kernel**: `fs/open.c`, `fs/read_write.c`, `fs/namei.c`, `fs/file.c` (fd table), `include/linux/fs.h` (`struct file`, `file_operations`), `mm/filemap.c`, `mm/mmap.c`, `block/blk-core.c`.
- **glibc**: `fopen`/`fread` wrap fd-based syscalls; stdio buffering on top.
- **Servers**: nginx/Node/epoll and io_uring; `sendfile`/`splice` for zero-copy; databases use `O_DIRECT`/`fsync` control.
- **Shells**: redirection via `dup2`; `ulimit -n` caps.
- **Ops/debug**: `strace -e trace=open,read,write`, `lsof`, `ls /proc/<pid>/fd`.

## 17. References
- Love, *Linux Kernel Development*, Ch. "The Virtual Filesystem" (fd/file/inode), Ch. "Block I/O".
- Silberschatz, *Operating System Concepts*, Ch. 12 (file-system implementation, VFS), Ch. 11.
- Tanenbaum, *Modern Operating Systems*, Ch. 4 (files), Linux sections.
- `man 2 open`, `man 2 read`, `man 2 write`, `man 2 mmap`, `man 2 dup`, `man 2 pread`, `man 2 fsync`.
- Linux `Documentation/filesystems/vfs.rst` (file_operations).

## 18. Cheat Sheet
- fd = index into `files->fdtab`; points to `struct file`.
- `struct file` = open description (offset, flags, f_op) — shared by dup/fork-inherited.
- inode = file object (metadata) — shared by all opens.
- `open`: namei resolve → do_dentry_open (f_op) → fd_install.
- `read`: vfs_read → f_op->read_iter → page cache → submit_bio → device.
- `write`: f_op->write_iter → write_begin/end (dirty) → writeback → fsync for durability.
- `mmap`: vm_area_struct + vm_ops; faults via filemap_fault (zero-copy reads).
- fork: fd table copied (struct file shared); threads: shared; dup: alias.
- O_CLOEXEC: close fd on exec. pread/pwrite: no f_pos race.

## 19. Quiz
1. fd points to? a) inode b) struct file c) dentry d) block → **b**
2. dup shares? a) fd table b) struct file (offset) c) inode only d) nothing → **b**
3. fork's fd table? a) shared b) copied c) empty d) closed → **b**
4. Buffered read path? a) direct device b) page cache c) network d) vmalloc → **b**
5. mmap gives? a) copies b) zero-copy c) blocking d) fd → **b**
6. Which flag survives exec? a) O_CLOEXEC b) FD_CLOEXEC off c) none d) both → **b**

## 20. Flashcards
- **Q: fd?** → **A:** Index into fd table → struct file.
- **Q: dup vs open twice?** → **A:** Same struct file (shared offset) vs new struct file.
- **Q: read path?** → **A:** vfs_read → f_op->read_iter → page cache → block layer.
- **Q: mmap?** → **A:** Map file pages; faults read them (zero copy).
- **Q: fsync?** → **A:** Force dirty cache to disk (durability).
- **Q: O_CLOEXEC?** → **A:** Close fd on exec.

## 21. Revision
The fd abstraction is the spine of Linux I/O. An `open` resolves a path into a `struct file` (open description with offset, flags, and the `f_op` method table) and hands back a small integer index into the process's fd table. Reads/writes dispatch through `f_op->read_iter`/`write_iter` into the page cache (`address_space`) and down to `submit_bio`; `mmap` turns file pages into address-space mappings for zero-copy access; `fsync` makes buffered writes durable. Sharing is precise: fork copies the fd table (sharing `struct file`s and offsets), threads share it, `dup` aliases one description, and re-opening creates a fresh description for the same inode. This is the user-space face of Part 08's VFS — and Section 04 shows exactly how those syscalls reach the kernel.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a file descriptor?" | 13 Q1 / 2 How |
| "fd vs struct file vs inode?" | 13 Q2 / 7 Formal |
| "What happens in open?" | 13 Q3 / 9 Internal |
| "What is f_op?" | 13 Q4 / 2 How |
| "What's shared on fork?" | 13 Q5 / 7 Formal |
| "dup vs open twice?" | 13 Q6 / 8 Example |
| "What does read do?" | 13 Q7 / 9 Internal |
| "What is the page cache?" | 13 Q8 / 2 How |
| "Why fsync?" | 13 Q11 / 12 Disadvantages |
