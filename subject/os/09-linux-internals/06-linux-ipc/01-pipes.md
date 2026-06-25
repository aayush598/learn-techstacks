# Pipes

## Unnamed Pipes
- Created with `int pipe(int fd[2])`
- `fd[0]`: read end
- `fd[1]`: write end
- Data flows **one direction**: write end → kernel buffer → read end

## Usage Pattern
```c
int fd[2];
pipe(fd);
if (fork() == 0) {
    close(fd[1]);   // child reads
    read(fd[0], buf, size);
} else {
    close(fd[0]);   // parent writes
    write(fd[1], buf, size);
}
```
- Created **before fork** so child inherits both file descriptors
- Unused ends should be **closed** (otherwise EOF never sent)

## Key Characteristics
- **Byte stream**: no message boundaries (unlike SYSV message queues)
- **Unidirectional**: one pipe = one direction
- **Limited capacity**: kernel buffer (typically **16 x 4KB = 64KB** on Linux)
  - `PIPE_BUF`: maximum **atomic** write (POSIX requires ≥ 512 bytes, Linux = 4096)
  - Writes ≤ PIPE_BUF are atomic; larger writes may interleave
- **Blocking behavior**:
  - `read()` blocks if pipe empty (until data or EOF)
  - `write()` blocks if pipe full (until reader consumes)

## Process Relationships
- Only processes with **common ancestor** can share unnamed pipe
- Typical: parent + child via fork()
- Named pipes (FIFOs) solve this limitation

## Shell Example
```bash
ls -la | grep ".txt" | wc -l
```
- `ls` writes to pipe 1 → `grep` reads pipe 1, writes to pipe 2 → `wc` reads pipe 2
- Each `|` creates a pipe, shell forks commands between them
