# FIFO (Named Pipe)

## What is a FIFO?
- **Named pipe**: exists as a file in the filesystem
- Created with `mkfifo()` syscall or `mkfifo` command
- Unrelated processes can communicate (no fork needed)
- Removed with `unlink()` / `rm`

## Creation
```bash
mkfifo my_pipe            # create named pipe
mkfifo -m 644 my_pipe    # with specific permissions
```
```c
int mkfifo(const char *pathname, mode_t mode);
```

## Semantics
- Data is **byte stream** (same as unnamed pipes)
- `PIPE_BUF` defines atomic write size (4KB on Linux)
- **Blocking open**:
  - `open(O_RDONLY)` blocks until writer opens
  - `open(O_WRONLY)` blocks until reader opens
  - `open(O_RDWR)` returns immediately (but not recommended)
  - `O_NONBLOCK`: `open(O_RDONLY | O_NONBLOCK)` returns immediately
    - `open(O_WRONLY | O_NONBLOCK)` returns `ENXIO` if no reader

## Use Cases
- **Client-Server**: server reads from well-known FIFO path
- **Process pipelines**: shell commands like...
  ```bash
  mkfifo log_pipe
  logger < log_pipe &    # background reader
  process_a > log_pipe   # writer
  ```
- **Shell one-liners** with named FIFOs for bidirectional communication

## Comparison: Pipe vs FIFO
| Feature | Unnamed Pipe | FIFO |
|---------|-------------|------|
| Persistence | Process lifetime (until no references) | Filesystem (removed explicitly) |
| Processes | Related (fork) | Any |
| Open | `pipe()` returns two fds | `open()` on pathname |
| Creation | Implicit | `mkfifo()` |

## Limitations
- Cannot `lseek()` — data is sequential stream
- No message boundaries (byte stream)
- Blocking behavior can cause deadlocks if not careful
- One direction only (use two FIFOs for bidirectional)
