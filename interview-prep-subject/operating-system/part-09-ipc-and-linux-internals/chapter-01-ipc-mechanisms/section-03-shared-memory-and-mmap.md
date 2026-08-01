# Shared Memory and mmap

> **TL;DR**: Shared memory is the fastest IPC: the kernel maps the **same physical pages** into multiple processes' address spaces, so reads/writes are plain memory loads/stores with **zero copy and no syscalls**. POSIX (`shm_open` + `mmap`) and System V (`shmget`/`shmat`) are the two APIs. The catch: shared memory provides **no synchronization** — the app must add locks/semaphores (Section 04).

## 1. Why Does This Exist?
Every other IPC (pipes, MQs, sockets) copies data: write copies user→kernel, read copies kernel→user — two copies per message. For high-bandwidth, high-frequency exchange (shared caches, in-memory databases, video frames, trading data), copying is the bottleneck. Shared memory removes the copies entirely: both processes get the same physical pages mapped into their virtual address spaces, so writing in one is immediately visible in the other. It exists to provide the maximum possible bandwidth with the minimum CPU and latency, at the cost of pushing synchronization responsibility onto the application.

## 2. How Does It Work?
- **POSIX shared memory**: `shm_open("/name", O_CREAT|O_RDWR, mode)` → fd (an `shmfs`/`tmpfs` file); `ftruncate(fd, size)` sets its size; `mmap(NULL, size, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0)` maps it into the address space. `munmap` unmaps; `shm_unlink("/name")` removes the object when all unmap. The same physical pages are shared by all mappers.
- **System V**: `shmget(key, size, IPC_CREAT|0666)` → `int shmid`; `shmat(shmid, NULL, 0)` attaches → returns a pointer; `shmdt(ptr)` detaches; `shmctl(shmid, IPC_RMID, NULL)` marks for removal (actually destroyed when last process detaches). `shm_nattch` tracks attachments.
- **`mmap` MAP_SHARED semantics**: page faults load the page once into the page cache; both processes' page tables point at the same physical frame. Dirty pages are shared — no copy-on-write (that's `MAP_PRIVATE`).
- **`/dev/shm`**: POSIX shm objects live in tmpfs mounted at `/dev/shm` (visible as files, size-limited by tmpfs `size=` mount option).
- Kernel structures: an inode in tmpfs/shmtmp; the page cache holds the pages; each process's mm (address space) has a `vm_area_struct` with `VM_SHARED`; the shm object's `shm_file` links them.

## 3. When Is It Used?
- **In-memory databases / caches** (Redis is single-process, but designs share hot data).
- **High-frequency messaging / trading** where latency matters.
- **Media pipelines** (video frames shared between producer and consumer).
- **Shared configurations / big data tables** read by many processes (read-only maps).
- **Message-passing implemented *over* shared memory** (boost::interprocess, C++ STL on shared memory, DPDK packet buffers).
- **`mmap` in general**: files, executables, libraries (the dynamic loader maps libs with `MAP_PRIVATE`), zero-copy file reads, databases mapping data files.

## 4. Why Wasn't Another Approach Chosen?
- **Pipes/MQs/sockets (copies)**: fine for small structured messages, but every byte copied twice — rejected for high-bandwidth/low-latency.
- **`mmap` of a file (chosen, but different)**: `mmap` a regular file shares through the page cache; `shm_open`/`shmget` share an *anonymous* tmpfs file with no disk sync — both are shared memory, `shm_*` is the pure in-RAM variant.
- **`mmap` MAP_PRIVATE (rejected for sharing)**: copy-on-write — each process's writes stay private; that's for exec/libraries, not IPC.
- **Distributed shared memory (DSM, rejected in practice)**: page-based sharing across machines is too slow/complex on modern hardware — network IPC (sockets) wins.
- **Shared memory + no sync (the actual chosen design)**: give up kernel coordination to gain speed — application-supplied locks (Section 04) are required.

## 5. Intuition
**A shared whiteboard between two rooms**: instead of messengers running between rooms with notes (copying), a wall has a glass pane both rooms can write on directly. Writing on the pane in room A is instantly visible in room B — no delivery, no copies. But: neither room "owns" the pane, so if both write at once you get gibberish — someone has to add a rule (a lock) about who writes when. The whiteboard's size (ftruncate) is fixed, and when everyone stops looking at it you can erase it (unlink).

## 6. Real-World Analogy
**A public notice board**: post a notice (data) once; everyone reads the same copy. The moment the board is updated, everyone sees the new version — there's no "mail" delay. But posting over someone else's notice simultaneously means a torn/overwritten notice — hence a moderator (semaphore/mutex) controls who can write. The board (segment) persists after one person leaves; it's destroyed only when the last reader leaves and the owner tears it down.

## 7. Formal Definition
Shared memory maps the same physical page frames into ≥2 processes' virtual address spaces. **POSIX**: `int fd = shm_open(name, O_CREAT|O_RDWR, 0666); ftruncate(fd, size); void *p = mmap(NULL, size, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);` — the object is a tmpfs file (`/dev/shm`), unlink with `shm_unlink`. **System V**: `int id = shmget(key, size, IPC_CREAT|0666); void *p = shmat(id, NULL, 0); ... shmdt(p);` — removed with `shmctl(id, IPC_RMID)` (destroyed when `shm_nattch` reaches 0). The kernel gives each mapping a `vm_area_struct` (VM_SHARED) whose page-fault handler loads pages into the page cache; both processes' PTEs point at the same frames. **No synchronization is provided** — correctness requires app-level locking.

## 8. Example
Two processes share a counter and a buffer:
```c
// both processes
int fd = shm_open("/demo", O_CREAT | O_RDWR, 0666);
ftruncate(fd, 4096);
int *counter = mmap(NULL, 4096, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
```
- Process A: `counter[0]++` → visible to B immediately (same physical page).
- Process B: reads `counter[0]` — a plain load, no syscall.
- Both must agree on locking (Section 04) or increments can be lost (read-modify-write races).

System V equivalent:
```c
int id = shmget(ftok("/tmp", 7), 4096, IPC_CREAT | 0666);
int *counter = shmat(id, NULL, 0);
// ... shmdt(counter);
```

`mmap` for files (zero-copy reads):
```c
int fd = open("data.bin", O_RDONLY);
char *p = mmap(NULL, 1 << 20, PROT_READ, MAP_PRIVATE, fd, 0);
// p[0..1M-1] are the file's pages, faulted into the page cache on demand
```

## 9. Internal Working
1. `shm_open` → `do_shm_open` → open a tmpfs file (an inode in `shm_mnt`). The fd is a normal file fd.
2. `ftruncate` sets the object size.
3. `mmap(MAP_SHARED)` → `do_mmap` → create `vm_area_struct` with `VM_SHARED` → for tmpfs/shmem, `shmem_mmap` registers `shmem_file_operations`.
4. First touch of a page → page fault → `shmem_fault` → allocate a page in the shm's page cache (tmpfs) → map into the faulting process's PTE.
5. Another process `mmap`s the same object → same page-cache page → its PTE points at the **same frame**. Writes by either update the same physical page (no CoW because `VM_SHARED`).
6. `munmap`/`shmdt` → `zap_page_range` unmaps PTEs (pages stay in cache while referenced); last unmap + `shm_unlink`/`IPC_RMID` → free.
7. Cross-process visibility: **no cache-coherency problem** on a single machine — the page cache is coherent (hardware cache-coherent architecture); on NUMA, the kernel migrates/locates pages.

## 10. Time Complexity
- Map: O(page-table setup) once per mmap — one-time cost.
- Access: O(1) memory load/store — **no syscall, no copy**. That's the whole point.
- Page fault (first touch): O(1) allocation + PTE install.
- Unmap: O(mapped pages) PTEs cleared.
- Synchronization (app-level): whatever the lock costs (e.g., a futex — ~O(1) uncontended).
- Compare: pipe/MQ ≈ 2 copies + 2 syscalls per message; shm ≈ 1 store + 1 load.

## 11. Advantages
- **Zero copy**: no kernel/user copies at all — the data lives once.
- **No syscalls after setup**: reads/writes are ordinary memory instructions.
- **Maximum bandwidth/lowest latency**: ideal for high-frequency exchange.
- **Works at scale**: shared tables, media frames, in-memory data stores.
- **`mmap` unifies files and memory**: the same mechanism reads files zero-copy (page-cache-backed).
- **Two clean APIs**: POSIX (fd-based, `/dev/shm`) and System V (key-based).

## 12. Disadvantages
- **No synchronization**: the killer caveat — races are the app's job (mutex/semaphore/futex); easy to get wrong.
- **No message boundaries**: it's a blob of bytes — framing/sync protocol is up to you.
- **Fixed size**: must agree on a size up front (ftruncate); resizing is awkward.
- **Lifetime management**: System V requires `IPC_RMID` + careful attach/detach; leaks are a classic bug.
- **Security**: any process with the right key/name can attach (need permissions/namespaces).
- **Not network-capable** (unlike sockets).
- **Cache-coherency & NUMA**: cross-process visibility is hardware-dependent; on NUMA, false sharing is possible (multiple CPUs hitting the same cache line).

## 13. Interview Questions
1. **Q: Why is shared memory the fastest IPC?** A: Zero copies and zero syscalls after mapping — both processes' PTEs point at the same physical pages; access is a plain load/store.
2. **Q: What is the main danger of shared memory?** A: No synchronization — concurrent writes race and lost updates are possible; the application must add locks (futex/semaphore/mutex). "Shared memory needs synchronization" is the key line.
3. **Q: POSIX vs System V shared memory?** A: POSIX: `shm_open`+`mmap` (fd-based, `/dev/shm`, unlink via `shm_unlink`). System V: `shmget`/`shmat`/`shmdt`/`shmctl` (key-based, persistent until IPC_RMID).
4. **Q: What does `MAP_SHARED` vs `MAP_PRIVATE` mean?** A: `MAP_SHARED`: writes visible to all mappers (shared memory — used for IPC). `MAP_PRIVATE`: copy-on-write — writes stay private (used for exec/libraries/fork).
5. **Q: How does `mmap` of a file work?** A: The file's pages are mapped into the address space and faulted into the page cache on first access — reads/writes happen via memory, with writeback to disk; zero-copy file I/O and the basis of the page cache.
6. **Q: What is `/dev/shm`?** A: The tmpfs where POSIX shm objects live — visible as files, mounted at `/dev/shm`, size-limited by the mount's `size=` option.
7. **Q: What happens to a System V segment when a process detaches?** A: `shmdt` unmaps it; the segment stays until `shmctl(IPC_RMID)` marks it and the last process detaches (`shm_nattch` hits 0) — only then is it destroyed.
8. **Q: Is shared memory safe across process crash?** A: The object persists (POSIX until unlink; SysV until IPC_RMID) — the *data* may be mid-write and inconsistent on crash; a leftover segment is a leak, not a crash bug per se.
9. **Q: When would you NOT use shared memory?** A: When messages are small/rare (overhead of sync + fixed-size segments outweighs copy cost), when you need structured messages or priorities (MQs), or when processes might be on different hosts (sockets).
10. **Q: What is the page-cache connection?** A: Shared-memory pages live in the page cache (tmpfs/shmem) — `mmap` reads fault the pages there; multiple mappings point at the same cached frames; writeback rules differ for shm (no disk) vs files.
11. **Q: How do you resize shared memory?** A: POSIX: `ftruncate` to a new size (mappings see more/less); System V: `shmctl(IPC_SET)` can change `shm_segsz` for the mapping. In practice, allocate the max size up front.
12. **Q: What is false sharing?** A: When two processes/CPUs update different variables that share a cache line, the cache line bounces between cores — a performance bug; solved by padding/alignment (per-thread slots).

## 14. Follow-Up Questions
1. **Q: What is the difference between mapping an anonymous file and a shm object?** A: Both are tmpfs pages; a shm object is just a named/anonymous tmpfs file used for sharing — anonymous `mmap(MAP_ANONYMOUS|MAP_SHARED)` shares only between a process and its fork children.
2. **Q: How is shared memory cleaned up in containers?** A: IPC namespaces isolate shm objects; removing the namespace destroys its segments; `/dev/shm` also gets a fresh tmpfs per mount namespace.
3. **Q: What is a futex?** A: "Fast user-space mutex" — the primitive Linux uses for app-level sync over shared memory: atomic test in user space, syscall only on contention (Section 04 / Part 04).
4. **Q: `mmap` vs `read/write` for files?** A: `mmap` zero-copy + random-access convenience + page-cache reuse, but page-fault latency and cache effects; `read/write` do explicit copies with simpler semantics — pick by access pattern.

## 15. Coding Example
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/wait.h>

int main(void) {
    const char *name = "/shmdemo";
    int fd = shm_open(name, O_CREAT | O_RDWR, 0666);
    if (fd == -1) { perror("shm_open"); return 1; }
    if (ftruncate(fd, 4096) == -1) { perror("ftruncate"); return 1; }

    int *shm = mmap(NULL, 4096, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (shm == MAP_FAILED) { perror("mmap"); return 1; }
    *shm = 0;                       // init shared counter

    pid_t pid = fork();
    if (pid == 0) {
        for (int i = 0; i < 1000000; i++) (*shm)++;   // child writes
        _exit(0);
    }
    for (int i = 0; i < 1000000; i++) (*shm)++;       // parent writes
    wait(NULL);
    printf("final counter: %d (expected 2000000)\n", *shm);
    // NOTE: without a lock this races — the result is often < 2000000.

    munmap(shm, 4096);
    shm_unlink(name);
    return 0;
}
```
Run it a few times: you'll see values below 2,000,000 — the classic demonstration that shared memory needs synchronization (Section 04).

## 16. Industry Usage
- **Linux kernel**: `mm/shmem.c` (tmpfs/shmem), `ipc/shm.c` (System V), `mm/mmap.c`, `mm/memory.c` (faults); `/dev/shm` via `fs/shmem`.
- **Middleware**: boost::interprocess, Qt QSharedMemory, Apache Arrow IPC, Cap'n Proto shared-memory transport.
- **Databases/in-memory**: Redis Cluster hash slots stay single-process, but MMO/game servers share state; SQLite shared cache mode; Varnish uses shm for object metadata.
- **DPDK**: packet buffers in shared hugepages between NIC and app.
- **Containers/K8s**: emptyDir medium=Memory, shared /dev/shm for pods; PostgreSQL shared_buffers (its own shm).
- **`mmap` everywhere**: glibc dynamic loader, JVM (Metaspace/class files), databases mapping datafiles, `perf` mmap rings.

## 17. References
- `man 2 shm_open`, `man 3 shm_open`, `man 2 ftruncate`, `man 2 mmap`, `man 2 munmap`, `man 2 shm_unlink`.
- `man 2 shmget`, `man 2 shmat`, `man 2 shmdt`, `man 2 shmctl`.
- `man 5 shm_open`, `man 7 sysvipc`, `man 7 shm_overview`, `man 5 tmpfs`.
- Silberschatz, *Operating System Concepts*, Ch. 3.5.3 (shared memory), Ch. 9 (virtual memory, mmap).
- Love, *Linux Kernel Development*, Ch. "Memory Management" (`vm_area_struct`, page fault path).

## 18. Cheat Sheet
- POSIX: `shm_open("/n", O_CREAT|O_RDWR)` → `ftruncate` → `mmap(MAP_SHARED)` → `shm_unlink`.
- System V: `shmget(key)` → `shmat` → `shmdt` → `shmctl(IPC_RMID)`.
- Zero copy, zero syscalls after mapping; same physical pages.
- NO synchronization — app must lock (futex/semaphore/mutex).
- `MAP_SHARED` = visible to all; `MAP_PRIVATE` = CoW (exec/libs).
- `/dev/shm` = tmpfs where POSIX shm lives; `size=` limits it.
- System V object persists until IPC_RMID + last detach.
- Page cache hosts the pages; faults load them.

## 19. Quiz
1. Fastest IPC? a) pipe b) shm c) MQ d) socket → **b**
2. shm provides synchronization? a) yes b) no c) sometimes d) kernel only → **b**
3. POSIX shm lives in? a) /tmp b) /dev/shm c) /proc d) /var → **b**
4. `MAP_SHARED` means writes are? a) private b) visible to all mappers c) dropped d) CoW → **b**
5. System V segment destroyed when? a) first detach b) IPC_RMID + last detach c) unlink d) exit → **b**
6. Access cost after mapping? a) syscall b) copy c) load/store d) fault → **c**

## 20. Flashcards
- **Q: Why fastest?** → **A:** Zero copy, zero syscalls after setup.
- **Q: Main catch?** → **A:** No synchronization — app must lock.
- **Q: POSIX API?** → **A:** shm_open + ftruncate + mmap + shm_unlink.
- **Q: System V API?** → **A:** shmget/shmatt/shmdt/shmctl.
- **Q: /dev/shm?** → **A:** tmpfs where POSIX shm objects live.
- **Q: MAP_SHARED vs PRIVATE?** → **A:** Shared/visible vs copy-on-write.

## 21. Revision
Shared memory maps the same physical pages into multiple processes — zero copy, zero syscalls, and the fastest IPC, made possible by `mmap(MAP_SHARED)` over tmpfs (POSIX `shm_open`/`/dev/shm`) or the key-based System V API (`shmget`/`shmat`). Its defining weakness is that it provides *only* the channel, not the protocol: no message boundaries, no ordering, and — critically — no synchronization, so the app must add mutexes/semaphores/futexes (Section 04) or data races corrupt results (the demo counter never reaches 2,000,000). Choose it when bandwidth/latency dominate and you can manage the coordination; use pipes/MQs/sockets when structure, ordering, or portability matter more.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Why is shm fastest?" | 13 Q1 / 1 Why |
| "Main danger of shm?" | 13 Q2 / 12 Disadvantages |
| "POSIX vs System V shm?" | 13 Q3 / 2 How |
| "MAP_SHARED vs MAP_PRIVATE?" | 13 Q4 / 2 How |
| "What is /dev/shm?" | 13 Q6 / 2 How |
| "Lifetime of SysV segments?" | 13 Q7 / 9 Internal |
| "When NOT to use shm?" | 13 Q9 / 3 When |
| "What is false sharing?" | 13 Q12 / 12 Disadvantages |
