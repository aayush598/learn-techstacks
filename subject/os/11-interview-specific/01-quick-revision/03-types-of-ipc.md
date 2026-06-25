# Types of IPC (Inter-Process Communication)

## Comparison

| Method | Speed | Scope | Complexity | Data Format |
|--------|-------|-------|------------|-------------|
| **Shared Memory** | Fastest (no kernel after setup) | Any processes on same machine | Medium (synchronization needed) | Raw bytes |
| **Message Queues** | Fast | Same machine | Low | Structured messages |
| **Pipes (unnamed)** | Fast | Parent-Child only | Very low | Byte stream |
| **Named Pipes (FIFO)** | Fast | Any related/unrelated | Low | Byte stream |
| **Signals** | Async | Any process | Low | Limited (signal number) |
| **Sockets (AF_UNIX)** | Fast | Same machine | Medium | Byte stream / datagrams |
| **Sockets (AF_INET)** | Slower | Network | Higher | Byte stream / datagrams |
| **RPC** | Varies | Network | High | Serialized (protobuf, thrift) |

## Details

### 1. Shared Memory (shmget / mmap)
- **Fastest IPC:** no kernel involvement after setup
- `mmap(MAP_SHARED)`: file-backed or anonymous
- `shmget` / `shmat` (SysV shared memory)
- **Requires synchronization** (semaphore, mutex) — race conditions otherwise

### 2. Message Queues
- POSIX (`mq_open`, `mq_send`, `mq_receive`) or SysV (`msgget`, `msgsnd`)
- Messages have **type + priority**
- Kernel-managed buffer (no shared memory complexity)

### 3. Pipes
- `pipe(int fd[2])`: fd[0] = read end, fd[1] = write end
- Unidirectional, byte stream
- Named: `mkfifo` — works between **unrelated** processes

### 4. Signals
- Async notification: `SIGINT`, `SIGTERM`, `SIGKILL`, `SIGUSR1/2`
- Limited data (signal number + `sigqueue` for small payload)
- **Signal handler** is global to process

### 5. Sockets
- **AF_UNIX:** same-machine, path-based (`/tmp/mysocket`)
  - SOCK_STREAM (TCP-like) or SOCK_DGRAM (UDP-like)
- **AF_INET:** TCP/UDP over network

### 6. RPC (Remote Procedure Call)
- Abstraction: call function on another machine
- gRPC (HTTP/2 + protobuf), Apache Thrift, CORBA
- **Transparent** to programmer (almost)

## Interview Tips
- *"Shared memory is fastest but needs synchronization (semaphores/mutexes)"*
- *"Pipes are for parent-child; FIFO/named pipes for unrelated"*
- *"Sockets work for both local and remote IPC — most flexible"*
- *"RPC is architectural — not just OS-level IPC"*
