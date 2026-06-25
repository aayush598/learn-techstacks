# Important Linux System Calls

## Process Management
| Syscall | Description |
|---------|-------------|
| `fork()` | Create child process (COW) |
| `execve()` | Replace process image |
| `waitpid()` | Wait for child to change state |
| `exit()` | Terminate process |
| `getpid()` | Get process ID |
| `getppid()` | Get parent process ID |
| `clone()` | Linux-specific — creates thread/process with fine-grained control |
| `setpgid()` | Set/get process group ID |
| `sched_yield()` | Voluntarily yield CPU |

## File I/O
| Syscall | Description |
|---------|-------------|
| `open()` | Open/create file |
| `read()` | Read from file descriptor |
| `write()` | Write to file descriptor |
| `close()` | Close file descriptor |
| `lseek()` | Reposition read/write offset |
| `stat()` / `fstat()` | Get file metadata |
| `mmap()` | Memory-map file (or anonymous memory) |
| `munmap()` | Unmap memory-mapped region |
| `fsync()` / `fdatasync()` | Flush file to disk (sync file data) |

## Memory Management
| Syscall | Description |
|---------|-------------|
| `brk()` / `sbrk()` | Change program break (heap size) |
| `mmap()` (MAP_ANONYMOUS) | Allocate memory (malloc uses this or brk) |
| `munmap()` | Free memory |
| `mprotect()` | Set memory protection (RWX) |
| `mlock()` / `mlockall()` | Lock pages in RAM (prevent swapping) |

## IPC
| Syscall | Description |
|---------|-------------|
| `pipe()` | Create unnamed pipe (fd[0]=read, fd[1]=write) |
| `shmget()` | Allocate shared memory segment (SysV) |
| `shmat()` | Attach shared memory to process |
| `semget()` / `semop()` | Semaphore operations (SysV) |
| `msgget()` / `msgsnd()` / `msgrcv()` | Message queues (SysV) |

## Network / Socket
| Syscall | Description |
|---------|-------------|
| `socket()` | Create endpoint for communication |
| `bind()` | Bind socket to address |
| `listen()` | Listen for connections |
| `accept()` | Accept incoming connection |
| `connect()` | Connect to remote socket |
| `send()` / `recv()` | Send/receive data (socket-specific) |

## Threading
- `clone()`: Linux-specific — shares address space, file descriptors, etc.
- `futex()`: Fast userspace mutex (used by pthreads)
- glibc's `pthread_create` → internally uses `clone()` with flags
