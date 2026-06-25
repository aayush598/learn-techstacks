# Shared Memory IPC

## IPC — Why Processes Need to Communicate

| Reason | Example |
|--------|---------|
| **Data sharing** | Web server processes sharing cache |
| **Computation speedup** | Parallel processing (divide work) |
| **Modularity** | OS broken into daemons/services |
| **Convenience** | Editor communicating with spell-checker |

## Shared Memory — Overview

- **Fastest IPC** — no kernel involvement after initial setup
- One process creates a **shared memory segment**; others attach it to their address space
- Processes **read/write directly** to the shared region
- **Synchronization required** (mutex, semaphore) — otherwise race conditions

```
Process A                        Process B
┌──────────────┐                ┌──────────────┐
│  Address     │                │  Address     │
│  Space       │                │  Space       │
│              │                │              │
│  ┌──────┐    │                │  ┌──────┐    │
│  │Stack │    │                │  │Stack │    │
│  ├──────┤    │                │  ├──────┤    │
│  │      │    │   shared       │  │      │    │
│  │ shm  │◄───┼───────────────►│  │ shm  │    │
│  │      │    │   memory       │  │      │    │
│  ├──────┤    │                │  ├──────┤    │
│  │Heap  │    │                │  │Heap  │    │
│  │Data  │    │                │  │Data  │    │
│  │Text  │    │                │  │Text  │    │
│  └──────┘    │                │  └──────┘    │
└──────────────┘                └──────────────┘
```

## Producer-Consumer (Shared Memory)

```c
// Producer
#define BUFFER_SIZE 10
typedef struct {
    int buf[BUFFER_SIZE];
    int in;    // producer writes at buf[in]
    int out;   // consumer reads from buf[out]
} shared_data;

int main() {
    int fd = shm_open("/myshm", O_CREAT | O_RDWR, 0666);
    ftruncate(fd, sizeof(shared_data));
    shared_data *sp = mmap(NULL, sizeof(shared_data),
                           PROT_READ | PROT_WRITE,
                           MAP_SHARED, fd, 0);
    // Produce items...
    sp->buf[sp->in] = item;
    sp->in = (sp->in + 1) % BUFFER_SIZE;
}
```

```c
// Consumer — attaches same shared memory segment
int main() {
    int fd = shm_open("/myshm", O_RDWR, 0666);
    shared_data *sp = mmap(NULL, sizeof(shared_data),
                           PROT_READ | PROT_WRITE,
                           MAP_SHARED, fd, 0);
    // Consume items...
    item = sp->buf[sp->out];
    sp->out = (sp->out + 1) % BUFFER_SIZE;
}
```

## POSIX Shared Memory APIs

| Function | Purpose |
|----------|---------|
| `shm_open(name, flags, mode)` | Creates/opens shared memory object |
| `ftruncate(fd, size)` | Sets size of shared memory |
| `mmap(addr, len, prot, flags, fd, offset)` | Maps shared memory into process address space |
| `munmap(addr, len)` | Unmaps shared memory |
| `shm_unlink(name)` | Removes shared memory object |

### Key Points
- **`shm_open`** creates file descriptor to `/dev/shm/` on Linux
- **`mmap` with `MAP_SHARED`** → changes visible to all processes
- **`MAP_PRIVATE`** → copy-on-write (changes not shared)
- Shared memory persists until `shm_unlink` or reboot
- Must use **synchronization** (semaphore, mutex) to avoid race conditions

### Shared Memory vs Message Passing
| Aspect | Shared Memory | Message Passing |
|--------|--------------|-----------------|
| Speed | Fastest (direct memory access) | Slower (kernel copies) |
| Kernel involvement | During setup only | Every send/receive |
| Synchronization | Manual (mutex/semaphore) | Automatic (blocking) |
| Complexity | Higher (must avoid races) | Lower (OS manages transfer) |
| Use case | Large data, performance critical | Small messages, simplicity |
