# Shared Memory in Linux

## Overview
- Multiple processes share a region of **virtual memory**
- **Fastest IPC**: no kernel copy after setup (read/write directly to memory)
- Must synchronize access (semaphore, mutex, or atomics)

## POSIX Shared Memory
```c
int fd = shm_open("/my_shm", O_CREAT | O_RDWR, 0666);
ftruncate(fd, size);                    // set size
void *addr = mmap(NULL, size, PROT_READ|PROT_WRITE,
                  MAP_SHARED, fd, 0);   // map into address space
close(fd);
shm_unlink("/my_shm");                  // remove when done
```
- `shm_open()` returns file descriptor
- Objects live under `/dev/shm/` (tmpfs, in-memory)
- Name must start with `/`

## System V Shared Memory
```c
int shmid = shmget(IPC_PRIVATE, size, IPC_CREAT | 0666);
void *addr = shmat(shmid, NULL, 0);    // attach
// ... use shared memory ...
shmdt(addr);                            // detach
shmctl(shmid, IPC_RMID, NULL);         // remove
```
- `shmget()`: create/get shared memory segment
- `shmat()`: attach to process address space
- `shmdt()`: detach
- `shmctl(IPC_RMID)`: mark for removal (actual removal when all detach)

## Synchronization
```c
// Using POSIX semaphore in shared memory:
sem_t *sem = (sem_t *)addr + SHM_SIZE;
sem_init(sem, 1, 1);  // pshared=1 (shared between processes)
sem_wait(sem);
// ... critical section ...
sem_post(sem);
```
- Can also use **futex** (fast userspace mutex)
- **Atomic operations** for simple flags/counters

## POSIX vs System V Comparison
| Aspect | POSIX | System V |
|--------|-------|----------|
| Name | `/name` (filesystem-like) | Key (int, `ftok()`) |
| API | `shm_open` + `mmap` | `shmget` + `shmat` |
| Lifecycle | Removed on last unlink | Persists until `IPC_RMID` |
| Portability | Newer, preferred | Older, widely available |

## Limits
- `shmall`: max total shared memory pages (sysctl `kernel.shmall`)
- `shmmax`: max segment size (`kernel.shmmax`)
- Default: 32 MB—several GB depending on distro
- View with `ipcs -m` (SysV) or `ls -l /dev/shm/` (POSIX)
