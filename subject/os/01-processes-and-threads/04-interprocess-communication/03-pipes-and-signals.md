# Pipes, Signals, Sockets & RPC

## Ordinary Pipes (Unnamed)

- **Unidirectional** (one-way data flow)
- Used between **parent-child** processes only (no filesystem name)
- Created via `pipe(int fd[2])` — `fd[0]` = read end, `fd[1]` = write end
- After `fork()`, both processes share the pipe; close unused end in each

```c
int fd[2];
pipe(fd);
if (fork() == 0) {          // child
    close(fd[0]);           // close read end
    write(fd[1], "hello", 5);
} else {                    // parent
    close(fd[1]);           // close write end
    read(fd[0], buf, 5);
}
```

| Property | Ordinary Pipe |
|----------|---------------|
| **Direction** | Unidirectional |
| **Processes** | Related (parent-child only) |
| **Persistence** | Exists only while processes have fd open |
| **Named in FS?** | No |
| **Size limit** | Typically 64 KB buffer (Linux pipe capacity) |

## Named Pipes (FIFOs)

- **Bidirectional** (multiple processes can read/write)
- Unrelated processes can communicate (named in filesystem)
- Created via `mkfifo(path, mode)` — persists until deleted

```sh
# Shell example
mkfifo myfifo
echo "hello" > myfifo &   # writer (blocks until reader)
cat myfifo                 # reader
```

| Property | FIFO |
|----------|------|
| **Direction** | Bidirectional (write from any process) |
| **Processes** | Any (no relationship required) |
| **Persistence** | Filesystem entry (removed with `unlink`) |
| **Use case** | Simple client-server on same machine |

## Signals

- **Software interrupt** — notification sent to a process
- Asynchronous — can arrive at any time
- Handled by: **default action**, **ignore**, or **user-defined handler**

### Common Signals

| Signal | Default | Description |
|--------|---------|-------------|
| **SIGINT** (2) | Terminate | Ctrl+C — user interrupt |
| **SIGTERM** (15) | Terminate | Graceful termination request |
| **SIGKILL** (9) | Terminate | **Cannot be caught/ignored** — forceful kill |
| **SIGSTOP** (19) | Stop | **Cannot be caught/ignored** — pause process |
| **SIGCONT** (18) | Continue | Resume stopped process |
| **SIGSEGV** (11) | Core dump | Segmentation fault (invalid memory access) |
| **SIGPIPE** (13) | Terminate | Write to broken pipe (reader closed) |

```c
// Signal handler example
void handle_sigint(int sig) {
    printf("Caught SIGINT (Ctrl+C)\n");
    exit(0);
}
signal(SIGINT, handle_sigint);  // register handler

// SIGKILL and SIGSTOP CANNOT be caught
signal(SIGKILL, handler);  // ❌ always fails (kernel enforcement)
```

## Sockets

- **Endpoint for communication** — can be local (Unix domain) or network (TCP/UDP)
- **Pair of sockets**: One for each process, connected via a communication link
- **Unix domain sockets**: Faster than TCP for same-machine IPC (no network stack overhead)

```c
// TCP socket server (simplified)
int sfd = socket(AF_INET, SOCK_STREAM, 0);
bind(sfd, (struct sockaddr*)&addr, sizeof(addr));
listen(sfd, 5);
int cfd = accept(sfd, NULL, NULL);    // block until client connects
read(cfd, buf, 1024);                 // read from client
```

| Socket Type | Transport | Use Case |
|------------|-----------|----------|
| **SOCK_STREAM** | TCP | Reliable, ordered, connection-oriented |
| **SOCK_DGRAM** | UDP | Unreliable, unordered, connectionless |
| **SOCK_STREAM (Unix)** | Unix domain | Same-machine IPC (faster than TCP) |

## Remote Procedure Call (RPC)

- **Function call abstraction** for network communication
- Client calls a function that **appears local** but executes on a remote server
- **Stubs** handle marshalling (packing args) and unmarshalling

```
Client                  Network                  Server
┌──────────┐                             ┌──────────┐
│  app()   │                             │  func()  │
│   │      │                             │    ▲     │
│   ▼      │                             │    │     │
│ client   │──[request marshal]──────►   │ server   │
│ stub     │                             │ stub     │
│   ▲      │◄────[reply unmarshal]────── │    │     │
│   │      │                             │    ▼     │
│  app()   │                             │  func()  │
│ continues│                             │ returns  │
└──────────┘                             └──────────┘
```

- **Sun RPC**, **gRPC** (Google, HTTP/2 + Protobuf), **JSON-RPC**, **XML-RPC**
- gRPC is modern standard: language-agnostic, strongly typed, streaming support
