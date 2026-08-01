# Pipes and FIFOs

> **TL;DR**: A **pipe** is a kernel-buffered, unidirectional byte stream created by `pipe(2)` — a pair of fds (`[0]=read end, [1]=write end`) backed by a pipe inode with a ring buffer. A **FIFO** (named pipe, `mkfifo`) is the same mechanism but created by name in the filesystem so *unrelated* processes can connect. Pipes are the glue behind `cmd1 | cmd2`.

## 1. Why Does This Exist?
Processes have separate address spaces — a process can't just read another's memory. For two processes to communicate, data must flow through the kernel. The *simplest* model is a byte stream: producer writes, consumer reads, in order, reliably, with the kernel buffering and blocking as needed. Pipes give exactly that with zero setup cost (a single syscall) and are the mechanism behind every `|` in a shell. They exist because the common case — "process A produces a stream, process B consumes it" — needs something cheaper and simpler than sockets or shared memory.

## 2. How Does It Work?
- `pipe(int fds[2])`: creates a pipe with `fds[0]` (read end) and `fds[1]` (write end). Unidirectional: data flows from write end to read end.
- Kernel data: a `struct pipe_inode_info` with a circular buffer of `struct pipe_buffer` entries (each references a page), plus wait queues for both ends.
- Semantics:
  - `write` when the read end is closed → `SIGPIPE` (default: terminate process); `EPIPE` if ignored.
  - `read` when the write end is closed → returns 0 (EOF).
  - `write` to a full pipe → blocks until space (unless `O_NONBLOCK` → `EAGAIN`).
  - `read` from an empty pipe → blocks until data (or `O_NONBLOCK` → `EAGAIN`).
- **FIFO** (`mkfifo` / `mkfifo(3)` / `mknod`): a filesystem object (`p` type). `open` blocks until both a reader and a writer open it (unless `O_NONBLOCK`). After that, identical to a pipe.
- Buffer size: since Linux 2.6.35, 16 KB default, adjustable via `fcntl(F_SETPIPE_SZ)` up to a max (typically 1 MB); capacity per `struct pipe_buffer`.
- **Zero-copy-ish**: Linux `vmsplice`/`splice`/`tee` let the kernel move pages between pipes and files without copying to userspace — the basis of efficient data movement in `splice`-based servers.

## 3. When Is It Used?
- **Shell pipelines**: `cat file | grep foo | wc -l` — three processes, two pipes.
- **Parent–child coordination**: parent writes config/commands, child reads them.
- **Producer–consumer** within one host: streaming logs, feeding a worker.
- **`FIFO` for unrelated processes**: e.g., two daemons exchange commands via a named pipe in `/tmp`.
- **Named pipe servers**: `logger`/`syslog` historically; gstreamer/multimedia frameworks.
- Kernel `splice`/`sendfile`-style data movement (network servers, `nginx`).

## 4. Why Wasn't Another Approach Chosen?
- **Sockets (more general, heavier)**: pipes are cheaper (no address namespace, no connection setup, no socket buffers) — perfect for local byte streams.
- **Shared memory (faster, but needs sync)**: pipes give built-in flow control (blocking) and ordering — shared memory requires the app to implement both.
- **Message queues (structured, heavier copies)**: pipes are byte-oriented and in-order — MQs add priority/copy overhead that byte streams don't need.
- **Files as the exchange medium (slow, no blocking)**: pipes have in-memory buffers and automatic blocking semantics; file exchange requires polling.
- **Signals (tiny payloads, async)**: pipes carry arbitrary byte streams with backpressure — signals are one-shot events.

## 5. Intuition
**A water hose between two taps**: one end is connected to a faucet (writer), the other to a glass (reader). The hose holds a certain volume (kernel buffer). If you pour faster than the glass is being emptied, the hose fills up and pouring blocks (full pipe). If the faucet is turned off (writer closed), the reader eventually drains the hose and sees the end (EOF). It flows in one direction only — you can't pour back up the same hose.

## 6. Real-World Analogy
**A courier tunnel**: two offices (processes) share a single-lane tunnel. One office sends documents (bytes) down the tunnel; the other receives them. The tunnel has a small holding bay (ring buffer). If the bay is full, senders queue up and wait (blocking). If the receiving office closes its door permanently (read end closed), senders get told "this tunnel is dead" (SIGPIPE) and stop. The tunnel is one-way — for two-way you'd need two tunnels (or a `socketpair`).

## 7. Formal Definition
A pipe is a one-way kernel buffer connecting a write endpoint to a read endpoint. `pipe(2)` returns a `{int fd[2]}` pair. The kernel maintains a pipe inode with a set of `pipe_buffer`s (an array of `page`, `offset`, `len`), a `head`/`tail` cursor, and wait queues for readers/writers. Writes are atomic for `PIPE_BUF` bytes or less (4096 on Linux) — concurrent small writers won't interleave; larger writes may. A FIFO is a pipe with a directory entry and a path; `open` for read or write blocks until the counterpart opens. Both use the VFS pipe filesystem (`fs/pipe.c`, `fs/fifo.c`), registered as a `struct file_operations` with `read_iter`/`write_iter` that copy between user buffers and the ring.

## 8. Example
Shell: `ls | grep txt`:
1. Shell creates a pipe `fd[0], fd[1]`.
2. `fork()` → child A (`ls`) inherits both fds; `fork()` → child B (`grep`).
3. A does `dup2(fd[1], STDOUT_FILENO); close(fd[1]); close(fd[0]); exec("ls")`. B does `dup2(fd[0], STDIN_FILENO); close(fd[0]); close(fd[1]); exec("grep")`.
4. `ls` writes directory listing bytes to the pipe; `grep` reads them and filters. The shell `waitpid`s both.
5. `grep` sees EOF when `ls` closes the write end (after exit).

A producer-consumer FIFO:
```bash
mkfifo /tmp/myfifo
producer:  echo "hello" > /tmp/myfifo   # blocks until a reader opens
consumer:  cat /tmp/myfifo              # blocks until a writer opens
```

## 9. Internal Working
1. `pipe(2)` → `do_pipe` → `create_pipe_files` (allocates inode on the pipefs) → returns two fds pointing at the same `struct pipe_inode_info` (read end has `O_RDONLY`, write end `O_WRONLY`).
2. `write(fd[1], buf, n)` → `pipe_write` → if n ≤ PIPE_BUF and concurrent, serialize; else copy into the ring (via `copy_page_from_iter`); if full, wait on `pipe->wait` (blocking) or `EAGAIN`.
3. `read(fd[0], buf, n)` → `pipe_read` → copy from ring; if empty, wait or `EAGAIN`; when all buffers consumed and no writer → return 0.
4. Closing the last write fd: `pipe_release` → wake readers with EOF; writing after that → `EPIPE` + `SIGPIPE`.
5. `splice`: `splice(fd, ..., pipefd, ...)` moves pages directly (no user-space copy), improving throughput for data movement (used by `nginx`, `sendfile` paths).

## 10. Time Complexity
- Pipe read/write: O(bytes) copy between user buffer and kernel ring (or O(1) with `splice` page transfer).
- Buffer: fixed-size ring — O(1) cursor math per op.
- Blocking: O(1) wait-queue operations; wakeups on the opposite end's activity.
- Atomicity: writes ≤ PIPE_BUF (4096) are atomic (no interleaving between processes); larger writes are not guaranteed atomic.
- `splice`/`vmsplice`: O(1) metadata transfer per segment — kernel moves pages without copy.

## 11. Advantages
- **Zero setup**: one syscall for a working channel (vs socket setup).
- **Automatic flow control**: blocking backpressure — a slow reader throttles the writer; no buffer-overrun or explicit sync.
- **Reliable + ordered**: bytes arrive in order, no loss (unlike UDP).
- **EOF/semantics are clear**: closing write end → EOF; closing read end → SIGPIPE.
- **Cheap**: small fixed kernel buffer, no connection handshake, no address namespace.
- **`splice`/`sendfile`**: kernel-to-kernel page movement avoids user-space copies.

## 12. Disadvantages
- **Unidirectional**: need two pipes (or a socketpair) for bidirectional.
- **Byte-oriented**: no messages/typing/priority — everything is a stream (higher-level framing is the app's job).
- **Fixed-size buffer**: can deadlock if a full pipe blocks a writer while the reader waits on something else (though usually fine).
- **Same-host only**: no network IPC (that's sockets).
- **Copy cost**: user-space ↔ kernel ring copies per transfer (mitigated by `splice` but not for normal `read`/`write`).
- **Named-pipe `open` blocking** can surprise: FIFO `open` blocks until both ends are present.

## 13. Interview Questions
1. **Q: What is a pipe?** A: A unidirectional kernel-buffered byte stream between two processes, created by `pipe(2)` which returns a read fd and a write fd; the classic `cmd1 | cmd2` glue.
2. **Q: Pipe vs FIFO?** A: A pipe is anonymous (only usable by the process tree that created it via fork); a FIFO has a filesystem name (`mkfifo`) so unrelated processes can connect. Same kernel mechanism.
3. **Q: Is a pipe bidirectional?** A: No — unidirectional. Data flows write-end → read-end. `socketpair(AF_UNIX, SOCK_STREAM)` gives bidirectional local channels.
4. **Q: What happens on write when the read end is closed?** A: The process receives `SIGPIPE` (default: terminated); if SIGPIPE is ignored, `write` returns `EPIPE`.
5. **Q: What happens on read when the write end is closed?** A: `read` returns 0 (EOF). The reader must detect that.
6. **Q: What happens on write to a full pipe?** A: Blocks until space frees up (flow control); with `O_NONBLOCK` it returns `EAGAIN`. Read from an empty pipe blocks until data (or `EAGAIN` nonblocking).
7. **Q: What is the pipe buffer size?** A: Historically 4 KB (one page) to 64 KB; Linux ≥ 2.6.35 default 16 KB, adjustable with `fcntl(F_SETPIPE_SZ)`. It's a ring of `struct pipe_buffer`s.
8. **Q: What is the atomicity guarantee?** A: Writes ≤ `PIPE_BUF` (4096 bytes on Linux) are atomic: two processes' small writes won't interleave. Larger writes can interleave.
9. **Q: How does the shell implement `a | b`?** A: `pipe()`, then two `fork()`s; child A `dup2(write_end, stdout)`, child B `dup2(read_end, stdin)`, close the unused ends, `exec`. The parent waits for both.
10. **Q: What is `splice`/`vmsplice`?** A: Kernel API that moves pages between a pipe and a file/socket (or user memory) without copying through user space — used for efficient zero-copy-ish data movement (e.g., `nginx`).
11. **Q: When would you prefer a FIFO over a pipe?** A: When the processes are unrelated (not parent–child) — a named pipe in the filesystem lets any reader/writer connect; also persists across restarts of one side.
12. **Q: Why not use a file instead of a pipe?** A: Pipes give built-in blocking/backpressure, ordering, and in-memory speed; files need polling, locking, and cleanup — pipes are the right abstraction for streams.

## 14. Follow-Up Questions
1. **Q: How does a pipe avoid busy-waiting?** A: Wait queues — a blocked reader/writer sleeps on `pipe->wait`; the opposite end's read/write wakes it. Blocking I/O is scheduler-managed, not a busy loop.
2. **Q: What is the difference between `PIPE_BUF` atomicity and pipe capacity?** A: `PIPE_BUF` (4096) is the per-write atomicity limit; capacity is the total buffer size (16 KB+). Small writes are atomic even if the pipe is big.
3. **Q: What happens if a process is killed mid-write?** A: The pipe buffer keeps what was written; readers get a partial write (no torn guarantees for large writes) — this is why the atomicity limit matters for multi-writer designs.
4. **Q: How do you make a pipe nonblocking?** A: `fcntl(fd, F_SETFL, O_NONBLOCK)` (or `pipe2(..., O_NONBLOCK)`); then full/empty ops return `EAGAIN` instead of blocking.

## 15. Coding Example
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>

int main(void) {
    int fd[2];
    if (pipe(fd) == -1) { perror("pipe"); return 1; }

    pid_t pid = fork();
    if (pid == 0) {                       // child: reader
        close(fd[1]);                     // close write end
        char buf[128]; ssize_t n;
        while ((n = read(fd[0], buf, sizeof buf - 1)) > 0) {
            buf[n] = '\0';
            printf("child read: %s", buf);
        }
        close(fd[0]);
        return 0;
    }
    // parent: writer
    close(fd[0]);                         // close read end
    write(fd[1], "hello through the pipe\n", 23);
    close(fd[1]);                         // EOF for the child
    wait(NULL);
    return 0;
}
```
Build/run: `gcc pipe.c -o pipe && ./pipe` → `child read: hello through the pipe`.

## 16. Industry Usage
- **Linux kernel**: `fs/pipe.c`, `fs/fifo.c`, `include/linux/pipe_fs_i.h`; `splice`, `tee`, `vmsplice` in `fs/splice.c`.
- **Shells** (bash, zsh, POSIX sh) implement `|` via `pipe` + `dup2`.
- **Build systems / CI**: `make`/`ninja` pipe tool outputs; `xargs`, `tee`.
- **Servers**: `nginx`/Apache use `splice`-based sendfile paths; log pipelines (systemd-journald ↔ journalctl).
- **Named pipes**: Docker/OCI container `--entrypoint` coordination, gstreamer, `fifo` based message transport in embedded systems.

## 17. References
- `man 2 pipe`, `man 2 pipe2`, `man 2 read`, `man 2 write`, `man 2 splice`, `man 2 fcntl`.
- `man 3 mkfifo`, `man 1 mkfifo`.
- Silberschatz, *Operating System Concepts*, Ch. 3.5 (IPC), Ch. 3.6 (examples).
- Tanenbaum, *Modern Operating Systems*, Ch. 3.2 (IPC — pipes).
- Love, *Linux Kernel Development*, Ch. "Pipes" / `fs/pipe.c` in the kernel source.

## 18. Cheat Sheet
- `pipe(2)` → `fd[0]` read, `fd[1]` write; unidirectional.
- FIFO = named pipe (`mkfifo`); `open` blocks until both ends.
- Write to closed read end → `SIGPIPE`/`EPIPE`. Read from closed write end → EOF (0).
- Full pipe blocks writer; empty pipe blocks reader (`O_NONBLOCK` → `EAGAIN`).
- `PIPE_BUF` (4096): atomic-write limit. Capacity: 16 KB default, `F_SETPIPE_SZ`.
- `splice`/`vmsplice`/`tee` = kernel-to-kernel, no user copy.
- Shell `a | b`: `pipe` + `fork` ×2 + `dup2` + `exec`.

## 19. Quiz
1. `pipe()` returns? a) one fd b) two fds (read+write) c) three d) a path → **b**
2. A pipe's direction? a) bidirectional b) unidirectional c) network d) mailbox → **b**
3. Write to closed read end → a) 0 b) EAGAIN c) SIGPIPE/EPIPE d) block → **c**
4. FIFO = a) socket b) named pipe c) shm d) queue → **b**
5. Atomic write limit? a) 1 byte b) PIPE_BUF (4096) c) 64K d) capacity → **b**
6. Slow reader with full pipe → a) data loss b) writer blocks c) OOM d) SIGPIPE → **b**

## 20. Flashcards
- **Q: pipe(2)?** → **A:** Two fds, one-directional kernel-buffered stream.
- **Q: pipe vs FIFO?** → **A:** Anonymous vs named (filesystem) — same mechanism.
- **Q: SIGPIPE?** → **A:** Writing to a pipe whose read end is closed.
- **Q: EOF on a pipe?** → **A:** Read returns 0 when write end closed.
- **Q: PIPE_BUF?** → **A:** 4096 bytes — atomicity guarantee for writes.
- **Q: splice?** → **A:** Move pages between pipe and file/socket, no user copy.

## 21. Revision
Pipes are the simplest and most used IPC: a kernel ring buffer between a write fd and a read fd, giving ordering, backpressure (blocking), and clean EOF/SIGPIPE semantics. FIFOs are named pipes for unrelated processes. The atomicity limit (`PIPE_BUF`) matters for multi-writer designs, and `splice` avoids user-space copies for high-throughput data movement. This is the foundation for the rest of IPC: message queues (Section 02) add structure/priority; shared memory (Section 03) removes the copy; semaphores (Section 04) add coordination; sockets (Section 05) add generality and networking.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a pipe?" | 13 Q1 / 2 How |
| "Pipe vs FIFO?" | 13 Q2 / 2 How |
| "Is a pipe bidirectional?" | 13 Q3 / 8 Example |
| "What happens on SIGPIPE / EOF?" | 13 Q4–5 / 2 How |
| "Full/empty pipe behavior?" | 13 Q6 / 2 How |
| "How does `a | b` work?" | 13 Q9 / 8 Example |
| "What is splice?" | 13 Q10 / 9 Internal |
