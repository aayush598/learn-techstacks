# File Concept, Attributes and Operations

> **TL;DR**: A file is a named, persistent sequence of bytes plus **metadata** (name, type, size, timestamps, permissions, owner); the OS exposes a fixed set of **operations** (create/open/read/write/seek/close/delete/truncate) with shared open-file semantics — the fundamental durable-storage abstraction.

## 1. Why Does This Exist?
Programs need to persist data beyond their lifetime and share it between processes/users. Raw disk bytes are useless without naming, structure, and metadata. The **file** abstraction exists to give the OS a uniform unit: a named container of bytes with attributes, managed by the filesystem, so programs can create, read, modify, and destroy data without knowing disk geometry. The abstraction's power is *uniformity* — one API (`open`/`read`/`write`…) works across disks, SSDs, network filesystems, and even pseudo-files like `/proc` — which is exactly what enables "everything is a file" in Unix.

## 2. How Does It Work?
A file = **data** (the bytes) + **metadata** (attributes). The OS:
1. Maintains an **inode** (index node) or file-control block per file: attributes + pointers to data blocks (Chapter 02).
2. Resolves a **pathname** via directory entries that map names → inode numbers (Chapter 01 Sec 02).
3. On `open()`, creates an **open-file description** (offset, mode, reference counts) and hands the process a **file descriptor** — an index into the process FD table (Part 09 Sec 03).
4. `read()/write()` move data between the page cache and user buffers at the current offset; `seek()` moves the offset; `close()` releases the descriptor.
Core attributes (Unix `stat`): name (in the directory, not the inode), type (regular/dir/char/block/FIFO/socket/symlink), size, permissions (mode), owner/group, timestamps (atime/mtime/ctime), link count, and on-disk layout info.

## 3. When Is It Used?
- **Every persistent operation**: config files, logs, databases, images, source code — all files.
- **Pseudo-files**: `/proc`, `/sys`, `/dev` expose kernel state as files (read/write via the same API — this is VFS's doing, Chapter 04 Sec 04).
- **Memory-mapped I/O**: files are the backing store for `mmap` (Part 07 Sec 03).
- **Streams**: stdin/stdout/stderr are file descriptors (a pipe/terminal as a "file").
- **Network FS**: NFS/SMB make remote files look local — same abstraction.

## 4. Why Wasn't Another Approach Chosen?
- **Flat "records" as the primitive (COBOL-era, rejected)**: fixed-width records matched business data but were rigid for everything else; byte-streams + app-level structure won (flexibility).
- **No metadata (rejected)**: can't track ownership/permissions/timestamps.
- **Raw device access only (rejected)**: unusable — every app would reimplement naming/layout.
- **Single global namespace (rejected)**: no per-user/per-project separation → directories fix this (Chapter 01 Sec 02).
- **Structured file types enforced by OS (rejected)**: "the OS shouldn't care about content"; Windows originally knew extensions, Unix treats everything as bytes — Unix's minimalism won for portability.

## 5. Intuition
A file is a **labeled box** on a shelf: the label (name) tells you what's inside, the box's tag (metadata) records when it was made, who owns it, how big it is, and who may look inside. The shelf (directory) organizes boxes; the box itself is just bytes. You never think about which warehouse or shelf-row — you just say "pass me the box named `report.txt`" and the OS fetches it.

## 6. Real-World Analogy
A **library**: books = files; the catalog card (inode/metadata) records title, author, size, and location; the shelf labels (directory) tell you where to look. The librarian (VFS/OS) handles the mechanics: you request a book by title (path), get a call number (inode), and read pages (data blocks) without caring whether it's stored on the first floor or the basement.

## 7. Formal Definition
A **file** is a named, persistent collection of information, stored as a sequence of bytes (or logical records), identified by a name in a directory and described by a set of **attributes**: name, identifier, type, location, size, protection, and timestamps (creation, last access, last modification). The **file system** implements a set of **operations**: create, delete, open, close, read, write, seek (reposition), truncate, and attribute operations (get/set). The **open-file table** tracks open instances (current offsets, access modes, sharing flags) shared between the system-wide and per-process descriptor tables.

## 8. Example
`/home/aayush/docs/resume.pdf`:
- Directory `/home/aayush/docs` has an entry `resume.pdf → inode 5823`.
- Inode 5823 stores: type=regular, size=245,760 bytes, mode=`rw-r--r--` (0644), owner=aayush, group=aayush, atime/mtime/ctime, link count=1, data-block pointers.
- `open("/home/aayush/docs/resume.pdf", O_RDWR)`:
  1. VFS walks `/` → `home` → `aayush` → `docs` (directory reads) → inode 5823.
  2. Kernel allocates an open-file description: offset=0, mode=RDWR, refcount=1.
  3. Process FD table slot 5 → points to that description. Returns 5.
- `read(5, buf, 1024)` → reads 1024 bytes from offset 0 → offset becomes 1024.
- `close(5)` → refcount 0 → description freed.

## 9. Internal Working
1. **Name resolution**: `open(path)` → `path_walk` (or `openat`) traverses directories, reading each directory's data blocks, matching names, following symlinks, and checking permissions at each component.
2. **Inode fetch**: `iget`/`dentry` caches speed repeated lookups (dcache).
3. **Open-file description**: an object shared by all FDs of the same `open` call — holds `f_pos`, mode, flags; `dup()`/`fork()` share the *same* description (offset shared) vs `open()` twice (separate offsets).
4. **read**: syscall → `vfs_read` → `file->f_op->read_iter` → page-cache lookup → copy to user (`copy_to_user`).
5. **write**: `copy_from_user` into the page cache → mark dirty → `writeback` flushes to disk (flusher threads).
6. **Close**: flush, drop refcount, free description; inode refcount decremented.
7. **Unlink/delete**: remove the directory entry; decrement link count; when link count → 0 and no open handles → inode + data blocks freed.

## 10. Time Complexity
- `open`: O(path components) directory lookups (each O(1) hash in dcache, or O(dir size) on cold cache for a linear directory).
- `read`/`write` on cached data: O(bytes) copy (page cache); uncached: +O(I/O).
- `seek`: O(1) (offset update).
- `stat`: O(1) (inode metadata).
- `close`: O(1) amortized.
- Directory operations with hashed directories: O(1) average; linear dirs: O(n) per lookup.

## 11. Advantages
- **Uniform abstraction** across device types, network FS, pseudo-files.
- **Persistence** beyond process lifetime.
- **Metadata** (permissions, ownership, timestamps) enables access control and auditing.
- **Byte-stream model** is simple and universal — apps define structure.
- Clean separation: data (blocks) vs metadata (inode) → efficient caching and integrity.

## 12. Disadvantages
- **Metadata overhead**: inodes consume disk space (small).
- **Name resolution cost** for deep paths.
- **Open-file sharing semantics** are subtle (offset sharing, locking) — source of bugs.
- Byte-stream flexibility pushes structure to apps (no OS-level typing).
- Attributes live apart from data → consistency between them requires care (journaling, Chapter 04 Sec 03).

## 13. Interview Questions
1. **Q: What is a file?** A: A named, persistent sequence of bytes plus metadata (type, size, permissions, timestamps, owner); the unit of durable storage managed by the filesystem.
2. **Q: What's the difference between file data and file metadata?** A: Data = the bytes; metadata = attributes (inode): size, mode, ownership, times, link count, block pointers. `stat()` reads metadata; `read()` reads data.
3. **Q: What does `open()` do internally?** A: Resolves the path via directory traversal (dcache), locates/creates the inode, checks permissions, and allocates an open-file description (offset, mode, flags) referenced by a file descriptor.
4. **Q: What is the open-file table and when do offsets get shared?** A: Kernel-wide table of open-file descriptions. `dup()` and `fork()` share the *same* description (shared offset); two separate `open()` calls get separate offsets — a classic interview gotcha.
5. **Q: Why does `read()` return fewer bytes than requested?** A: EOF, signal interruption (partial read), or short reads from pipes/network — `read` may return 0 at EOF or <n for non-blocking/short sources; callers loop.
6. **Q: What are atime, mtime, and ctime?** A: Access, modification (content), and status-change (metadata) times. Note: ctime ≠ creation time — it's inode-change time. A chmod changes ctime, not mtime.
7. **Q: What is "everything is a file"? (Production)** A: The Unix model where devices, sockets, pipes, proc/sys state are exposed through the file API — unified I/O via `file_operations` in VFS.
8. **Q: How does `unlink` actually delete a file?** A: Removes the directory entry and decrements the inode's link count; the inode+blocks are freed only when link count hits 0 *and* no process has it open (so an open file can be unlinked safely).
9. **Q: What happens to an open file after it's unlinked? (Tricky)** A: It keeps working — the open description holds the inode reference; space is freed on last `close()`. Classic pattern for temp files.
10. **Q: What's the difference between file type and file extension?** A: Type is metadata the OS/FS knows (regular/dir/symlink/device); extension is a *naming convention* the app interprets — Unix doesn't enforce extensions.
11. **Q: Why does `stat` differ from `lstat`?** A: `stat` follows symlinks (returns the target's metadata); `lstat` returns the symlink's own metadata. Listing tools use lstat.
12. **Q: What are the differences in `O_APPEND` vs `O_TRUNC`?** A: `O_APPEND` forces all writes to end-of-file (atomic append — multiple writers safe); `O_TRUNC` empties the file on open. Combined they're the classic log-file pattern.
13. **Q: How do `fopen` and `open` relate? (Practical)** A: `open` is the syscall (FD); `fopen` is the stdio wrapper (FILE*, buffered, with `fdopen` to convert). The user-space buffer (stdio) vs the kernel page cache are different layers.

## 14. Follow-Up Questions
1. **Q: What's a file descriptor vs a file description vs an inode?** A: FD = process-local integer (FD table); description = shared open state (offset/mode); inode = the disk-resident object (content+metadata). Three layers — a frequent interview trap.
2. **Q: How do locks fit into file operations?** A: `fcntl`/`flock` place advisory/record locks on ranges; mandatory locking exists but is rarely used; locks are per-process, released on close.
3. **Q: What is `sendfile`/`splice`?** A: Zero-copy file→socket/pipe transfers avoiding the user buffer round-trip — the optimization behind web servers and proxies.
4. **Q: What does `mmap` do to the file model?** A: Maps file bytes into the address space (Part 07 Sec 03) — read/write becomes memory access; the page cache is the shared backing store.

## 15. Coding Example
```c
// Demonstrate open/read/write/seek, stat, and shared vs separate offsets
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <string.h>

int main(void) {
    const char *path = "/tmp/filedemo.txt";
    int fd = open(path, O_CREAT|O_TRUNC|O_RDWR, 0644);
    write(fd, "hello world", 11);

    // dup shares the same open-file description -> shared offset
    int fd2 = dup(fd);
    char buf[8] = {0};
    read(fd2, buf, 5);            // moves the SHARED offset to 5
    printf("after dup+read: offset shared, read via fd2='%s'\n", buf);

    // a second open() gets its own description -> offset starts at 0
    int fd3 = open(path, O_RDONLY);
    read(fd3, buf, 5);
    printf("separate open: read via fd3='%s'\n", buf);

    // stat metadata
    struct stat st; stat(path, &st);
    printf("size=%ld mode=%o links=%ld\n", (long)st.st_size,
           (unsigned)st.st_mode & 0777, (long)st.st_nlink);

    unlink(path);                  // open fds still valid until close
    close(fd); close(fd2); close(fd3);
    return 0;
}
```

## 16. Industry Usage
- **Linux**: VFS in `fs/` (open/read/write dispatch), `fs/namei.c` (path walk), `fs/open.c`, `fs/read_write.c`; inodes `include/linux/fs.h` (`struct inode`, `struct file`, `struct file_operations`).
- **Windows**: NTFS MFT records hold attributes + data runs; `CreateFile`/`ReadFile`/`WriteFile`.
- **macOS**: XNU VFS + HFS+/APFS; `open`/`fcntl`.
- **Databases**: Postgres/MySQL use files + POSIX locking + `O_DIRECT` choices; file-per-table vs tablespace design.
- **Big data**: Spark/HDFS treat files as objects; S3 object storage reuses the "named bytes + metadata" model at cloud scale.

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 11.1 "File Concept" (attributes, operations), 11.2 "Access Methods".
- Tanenbaum, *Modern Operating Systems*, Ch. 4.1-4.2.
- Linux source: `fs/namei.c`, `fs/open.c`, `fs/read_write.c`, `include/linux/fs.h`.
- `man 2 open`, `man 2 stat`, `man 2 read`, `man 2 lseek`, `man 7 path_resolution`.

## 18. Cheat Sheet
- File = bytes + metadata (inode): type/size/mode/owner/times/link count/blocks.
- Operations: create, open, read, write, seek, truncate, close, delete, get/setattr.
- FD (process) → description (shared offset/mode) → inode (disk object).
- dup()/fork() share the offset; separate opens don't.
- ctime = inode-change time, NOT creation time.
- unlink frees space only when links=0 AND no open handles.
- stat follows symlinks; lstat doesn't.
- "Everything is a file" = VFS file_operations.
- O_APPEND = atomic append; O_TRUNC = empty on open.

## 19. Quiz
1. Which lives in the inode?
   a) file name b) data bytes c) size+mode+times d) directory path → **c**
2. After `dup()`, two FDs share:
   a) nothing b) the open-file description (offset) c) the inode only d) the path → **b**
3. ctime records:
   a) creation b) last access c) inode change d) last write → **c**
4. A file's space is freed when:
   a) unlink called b) links=0 and no open handles c) closed d) truncated → **b**
5. `lstat` vs `stat`:
   a) same b) lstat doesn't follow symlinks c) lstat is faster d) stat is faster → **b**
6. O_APPEND guarantees:
   a) O(1) writes b) atomic append at EOF c) truncation d) no caching → **b**

## 20. Flashcards
- **Q: What is a file?** → **A:** Named persistent bytes + metadata (inode attributes).
- **Q: FD vs description vs inode?** → **A:** FD=process handle; description=shared open state; inode=disk object.
- **Q: When do offsets get shared?** → **A:** After dup()/fork(); separate opens give separate offsets.
- **Q: What is ctime?** → **A:** Inode status-change time — not creation time.
- **Q: When is file space actually freed?** → **A:** Link count 0 and no open file descriptors.
- **Q: What does O_APPEND do?** → **A:** All writes atomically go to end-of-file.

## 21. Revision
A file is the filesystem's core object: named persistent bytes plus an inode holding metadata (type, size, mode, owner, times, link count, block pointers). Operations are create/open/read/write/seek/close/delete; the open path resolves names through directories, creates an open-file description (offset, mode), and returns a process FD. dup/fork share offsets; separate opens don't. Space is freed only when link count hits 0 and no handles remain. This API — with stat/lstat, O_APPEND, and "everything is a file" — is the uniform contract Chapter 02 lays out physically.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a file / what does it store?" | 2 How / 7 Formal |
| "What does open() do internally?" | 9 Internal / 13 Q3 |
| "When are offsets shared?" | 13 Q4 / 8 Example |
| "What is ctime?" | 13 Q6 / 18 Cheat Sheet |
| "How does unlink work?" | 13 Q8 / 9 Internal |
| "stat vs lstat?" | 13 Q11 / 2 How |
| "What is 'everything is a file'?" | 13 Q7 / 16 Industry |
