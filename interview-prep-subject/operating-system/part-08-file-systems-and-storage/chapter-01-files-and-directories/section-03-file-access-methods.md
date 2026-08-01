# File Access Methods

> **TL;DR**: Files are read via **sequential** access (byte/record stream, the default), **direct/random** access (seek to record N by index), or **indexed** access (an index of keys → offsets for large, key-addressable files) — the choice is dictated by workload and supported by filesystem seeking and in-memory or on-disk indexes.

## 1. Why Does This Exist?
Reading a file "from the start each time" is fine for logs but wasteful for databases, images, and archives where you need *random* records. Access methods exist to make each workload efficient: sequential (streaming), direct (fixed-record random access), and indexed (key-based lookup into huge files). They also shape the API: `read`/`write` are sequential by default with `lseek` to reposition, and indexed access is usually implemented *above* the FS (databases, search indexes) because the FS itself offers byte offsets, not records. Understanding access methods clarifies why `lseek`, `pread`, and index structures exist at all.

## 2. How Does It Work?
- **Sequential**: maintain a current file position (offset). `read` returns the next n bytes and advances the position; EOF returns 0. Best for streams, tapes, logs, pipes. Efficient when combined with readahead (Part 07 Sec 02).
- **Direct (random) access**: files are conceptualized as fixed-length records (e.g., 512-byte records); `record N` lives at byte `N × record_size`. `read`/`write` at an offset (or `lseek` + read). No ordering requirement; the "record" abstraction is app-level — the FS sees bytes.
- **Indexed access**: build an index (in-memory or on-disk) mapping keys → byte offsets (or record numbers); lookup the key, then direct-access the file at the returned offset. This is the DBMS pattern (B-trees) and search engines.

## 3. When Is It Used?
- **Sequential**: log files, streaming media, `tar`, `cat`, compilers, `readline`-style parsers, tapes.
- **Direct**: database tables with fixed-size rows (though real DBs use B-trees/indexes on top), audio/video frames (seek to chunk), embedded filesystems with record semantics.
- **Indexed**: B-tree indexes (Postgres/MySQL), inverted indexes (Elasticsearch), `BTREE`-ordered files, memory-mapped key-value stores (LMDB), and `seek`-based reading of large archives.
- **Hybrid**: a log file *with* an index (append-only + index rebuild) — common in streaming systems.

## 4. Why Wasn't Another Approach Chosen?
- **Sequential-only (rejected)**: fine for tapes but impossible for interactive/random workloads — DBs would be unusable.
- **Direct-only (rejected)**: awkward for variable-length content and streams; offsets leak record sizes into every caller.
- **OS-enforced indexed access (rejected)**: Unix chose bytes + `lseek`, leaving record semantics to apps — simpler, more flexible; Windows' historical `FILE_ATTRIBUTE_`/structured models didn't win either.
- **In-memory whole-file (rejected)**: not persistent-scalable; mmap exists for the "treat as memory" case.
- **App-level indexing (chosen)**: the FS gives offsets; databases/servers build indexes — clean separation and specialization.

## 5. Intuition
- **Sequential** = reading a book front to back; a bookmark tracks where you are; you rarely skip.
- **Direct** = a textbook with fixed-size pages: "page 42" is always `page_size × 41` bytes in — no scanning needed.
- **Indexed** = a dictionary's index: look up the word, get the page number, jump there. The index is the map; the file is the data.

## 6. Real-World Analogy
- **Sequential**: a conveyor belt of boxes — you can only take the next box.
- **Direct**: a parking garage with numbered slots — "slot 143" is a known spot, no searching.
- **Indexed**: a phone directory with a "who's calling" reverse lookup table — you look up the person in the index and know the entry number instantly.

## 7. Formal Definition
**Sequential access** processes file records in order; a file position advances monotonically with each read/write and is controlled by an explicit reposition operation (`seek`). **Direct (random) access** treats a file as a sequence of fixed-length records, indexed by position `n` at byte offset `n × record_length`, permitting reads/writes in arbitrary order. **Indexed access** augments direct access with an index structure mapping logical keys (or record numbers) to byte offsets, enabling key-based lookup without scanning; the index is typically maintained by the application layer (DBMS) or an indexed filesystem feature. `lseek`, `pread`/`pwrite`, and `mmap` are the POSIX mechanisms underpinning direct access.

## 8. Example
A 100-record file, record size 512 B:
- **Sequential**: `read(fd, buf, 512)` repeatedly → records 0, 1, 2… The position advances automatically.
- **Direct**: `pread(fd, buf, 512, 42*512)` reads record 42 *without* changing the shared position (thread-safe random read). Or `lseek(fd, 42*512, SEEK_SET); read(...)`.
- **Indexed**: a phone-book file where an in-memory map `"Smith" → byte_offset` lets `search("Smith")` compute `offset` and `pread` exactly that record — 1 index lookup + 1 I/O instead of scanning the file.
- **Worked offsets**: record 42 at byte 21,504. A misaligned seek (e.g., 21,513) yields a torn read — a reason databases pad records.

## 9. Internal Working
1. **Sequential**: the open-file description's `f_pos` advances on each read/write; the page cache + readahead prefetch future pages (Part 07).
2. **Direct**: `pread`/`pwrite` take an explicit offset and don't touch `f_pos` — thread-safe; `lseek` updates `f_pos` (O(1) in the description).
3. **Indexed**: the app keeps an index (B-tree in memory/on disk). Lookup: index search (O(log n)) → offset → `pread`/mmap at offset.
4. **FS mapping**: for direct/indexed reads, the FS translates byte offsets → block numbers (ext4 extents, Chapter 02/04) → disk I/O via the page cache.
5. **O_DIRECT**: bypasses the page cache for aligned direct I/O (DBs that manage their own cache).

## 10. Time Complexity
- Sequential: O(1) amortized per record with readahead; O(records) total.
- Direct: O(1) per record (offset math + single I/O or cache hit).
- Indexed: O(log n) index lookup + O(1) data fetch (B-tree) — the index pays for itself vs O(n) scan.
- `lseek`: O(1).
- Readahead benefit: sequential reads amortize I/O over many pages.

## 11. Advantages
- **Sequential**: simple, streaming-friendly, maximizes readahead/bandwidth.
- **Direct**: thread-safe random access (`pread`), no position contention, O(1) record fetch.
- **Indexed**: key-based lookup at scale — the basis of databases and search.
- App-level indexing keeps the FS minimal (bytes + offsets).
- `mmap` unifies direct access with memory semantics.

## 12. Disadvantages
- **Sequential** alone can't do random access (needs seek).
- **Direct** needs fixed-size records or app-level variable-length handling; torn reads on misalignment.
- **Indexed** adds index build/update/rebuild overhead, index storage, and consistency concerns.
- Record/offset semantics aren't enforced by the FS (app responsibility — errors are silent corruption risks).
- Direct I/O (O_DIRECT) requires alignment and loses the page cache.

## 13. Interview Questions
1. **Q: What are the three file access methods?** A: Sequential (ordered byte/record stream, auto-advancing position), direct/random (fixed-position access by record/offset), indexed (key→offset lookup into the file).
2. **Q: How is a direct-access file addressed?** A: `record n` at byte `n × record_size`; POSIX gives `lseek`/`pread`/`pwrite`; the "record" is app-defined — the FS only sees bytes.
3. **Q: Why does the OS not implement records? (Tricky)** A: Unix chose the byte-stream + offset model for flexibility; record/index semantics vary by workload, so the OS stays minimal and apps (DBs, search) build indexes — you can't know every caller's record size.
4. **Q: What is the difference between `read`+`lseek` and `pread`?** A: `pread` specifies the offset per call and does NOT modify the shared `f_pos` — thread-safe for concurrent readers of the same FD; `lseek`+`read` mutates the shared position (racy).
5. **Q: When is sequential access better than direct?** A: When the whole file is consumed in order (logs, media, archives, compilation) — readahead and sequential I/O give the highest bandwidth.
6. **Q: How does an indexed file improve lookup vs scanning?** A: Scan is O(n); an index (B-tree) lookup is O(log n) followed by O(1) data read — the basis of every database and search index.
7. **Q: What is `mmap` relative to these methods?** A: It maps the file into the address space (Part 07 Sec 03) — random access becomes pointer dereference (a form of direct access), with the page cache as the backing store.
8. **Q: What is O_DIRECT and when is it used? (Production)** A: Bypasses the page cache for user-managed buffers (requires alignment); databases that manage their own cache (Postgres) use it to avoid double-buffering.
9. **Q: How does readahead make sequential access fast?** A: The kernel prefetches upcoming pages (Part 07 Sec 02) so sequential reads hit the page cache — near disk bandwidth.
10. **Q: What's a "torn" read?** A: Reading a record that straddles a block boundary incorrectly (or a partially-written record) — fixed by record alignment/padding and atomic write APIs.
11. **Q: How do databases combine sequential and indexed access?** A: Append-only write-ahead logs are sequential; tables use indexed (B-tree) access; checkpoints combine both — a file system design pattern, not just a file access pattern.
12. **Q: What happens if you `seek` beyond EOF and write?** A: The file grows with a **hole** (sparse file) — unread data reads as zeros, no blocks allocated for the hole — common for direct-access files (and a favorite question).
13. **Q: Which method does `tar`/`zip` use?** A: Mostly sequential for content, but archives also use the *end-of-archive* index (central directory) to jump directly to a member — a hybrid.

## 14. Follow-Up Questions
1. **Q: How do variable-length records get direct access?** A: Via an index (offset pointers) — that's the indexed method; or fixed-size slots + overflow chains (classic hashed files).
2. **Q: What's the difference between `fseek`/`ftell` (stdio) and `lseek`?** A: stdio buffers in user space and tracks a logical position; `lseek` is the syscall on the FD. Mixing them requires `fflush`/`fsync` care.
3. **Q: What is a B-tree's role in indexed files?** A: Keeps the index sorted, balanced, and disk-fanout-optimal — O(log n) lookups and updates with few I/Os — the standard DBMS index.
4. **Q: What is "sparse file" support in the FS?** A: Holes (unwritten offsets) consume no data blocks and read as zeros — `SEEK_HOLE`/`SEEK_DATA` (lseek) let tools skip them efficiently.

## 15. Coding Example
```c
// Demonstrate sequential, direct (pread), and indexed (in-memory index) access
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>

#define REC_SIZE 8
typedef struct { char key[4]; int  val; } Rec;

int main(void) {
    const char *path = "/tmp/accessdemo.bin";
    int fd = open(path, O_CREAT|O_TRUNC|O_RDWR, 0644);

    // write 4 fixed-size records
    Rec data[4] = { {"a",1},{"b",2},{"c",3},{"d",4} };
    for (int i = 0; i < 4; i++)
        write(fd, &data[i], REC_SIZE);

    // sequential: read all from position 0
    lseek(fd, 0, SEEK_SET);
    Rec r; while (read(fd, &r, REC_SIZE) == REC_SIZE)
        printf("sequential: %s=%d\n", r.key, r.val);

    // direct: read record 2 without touching shared position
    Rec r2;
    pread(fd, &r2, REC_SIZE, 2 * REC_SIZE);
    printf("direct read record 2: %s=%d\n", r2.key, r2.val);

    // indexed: "find the record with key c" via an in-memory index
    Rec rs[4]; lseek(fd, 0, SEEK_SET); read(fd, rs, sizeof rs);
    for (int i = 0; i < 4; i++)
        if (strncmp(rs[i].key, "c", 4) == 0) {
            pread(fd, &r, REC_SIZE, (off_t)i * REC_SIZE);
            printf("indexed: found %s=%d at record %d\n", r.key, r.val, i);
        }
    close(fd); unlink(path);
    return 0;
}
```

## 16. Industry Usage
- **Databases**: B-tree/InnoDB pages (indexed), WAL (sequential), fixed-size pages via direct/pread; Postgres uses `lseek`+`pread`-style access; MySQL similar.
- **Search**: Lucene/Elasticsearch inverted indexes (indexed access into a posting file).
- **Streaming**: Kafka/Redis AOF use sequential append + index/checkpoint files (hybrid).
- **Media**: ffmpeg/video containers seek to frames via index tables.
- **OS tools**: `tar`/`zip` central directory; `dd`/`ddrescue` direct offsets; `grep -n` sequential + line offsets.

## 17. References
- Silberschatz, *Operating System Concepts (10th ed.)*, Ch. 11.2 "Access Methods".
- Tanenbaum, *Modern Operating Systems*, Ch. 4.1.3 "File Types and Access".
- `man 2 lseek`, `man 2 pread`, `man 2 read`, `man 2 mmap`, `man 2 open` (O_DIRECT).
- Linux source: `fs/read_write.c`, `mm/filemap.c`.

## 18. Cheat Sheet
- Sequential: ordered stream, auto-advance, best with readahead.
- Direct: fixed record at `n × size`; pread/pwrite/lseek.
- Indexed: key → offset index (B-tree), O(log n) lookup + O(1) read.
- pread doesn't move f_pos → thread-safe.
- mmap = file as memory (direct access via pointers).
- O_DIRECT = bypass page cache (DB-managed caching).
- Sparse files: holes read as zeros, no blocks.
- Torn reads: misaligned record reads — align/pad.
- Indexes live in apps (DB), not the OS — Unix byte model.

## 19. Quiz
1. Which method auto-advances position?
   a) direct b) sequential c) indexed d) none → **b**
2. Record n in a fixed-size file lives at byte:
   a) n b) n × record_size c) n + record_size d) hash(n) → **b**
3. `pread` differs from `lseek`+`read` because it:
   a) is faster b) doesn't touch f_pos (thread-safe) c) reads more d) is async → **b**
4. An index makes lookup:
   a) O(n) b) O(log n) + O(1) c) O(1) always d) O(n²) → **b**
5. O_DIRECT is used when:
   a) files are small b) the app manages its own cache c) readahead fails d) always → **b**
6. A hole in a sparse file:
   a) uses blocks b) reads as zeros c) crashes d) errors → **b**

## 20. Flashcards
- **Q: Three access methods?** → **A:** Sequential (stream), direct (fixed-position), indexed (key→offset).
- **Q: How is a record addressed directly?** → **A:** `n × record_size` bytes, via pread/pwrite/lseek.
- **Q: Why pread?** → **A:** Explicit offset, doesn't mutate shared position — thread-safe.
- **Q: What makes indexed access fast?** → **A:** B-tree lookup O(log n) then O(1) data read, vs O(n) scan.
- **Q: What is a sparse file?** → **A:** Holes read as zeros without allocated blocks.
- **Q: When use O_DIRECT?** → **A:** App-managed buffering (DBs), avoids double caching.

## 21. Revision
Files are read three ways: sequentially (streams, readahead-optimized), directly (fixed records at `n×size`, via pread/lseek — thread-safe, no position mutation), and via indexes (key→offset, B-tree O(log n) — the database pattern). Unix keeps the OS at bytes+offsets, pushing record/index semantics to apps; mmap turns files into memory, O_DIRECT bypasses the page cache, and sparse files read holes as zeros. Pick the method by workload: streaming for logs, direct for frames/records, indexed for key lookups.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What are the access methods?" | 2 How / 13 Q1 |
| "How is direct access addressed?" | 13 Q2 / 8 Example |
| "Why doesn't the OS implement records?" | 13 Q3 / 4 Alternative |
| "pread vs lseek+read?" | 13 Q4 / 9 Internal |
| "How do indexes speed lookups?" | 13 Q6 / 8 Example |
| "What is O_DIRECT for?" | 13 Q8 / 3 When |
| "What are sparse files?" | 13 Q12 / 14 Q4 |
