# Buffering in I/O

## What is Buffering?
- Temporary storage in memory to **transfer data between two devices/systems** with different speeds or data sizes
- **Buffer ≠ Cache**: buffer holds data in transit; cache holds copies for reuse

## Why Buffer?

| Reason | Description | Example |
|--------|-------------|---------|
| **Speed mismatch** | Producer faster than consumer (or vice versa) | Modem → disk |
| **Data size mismatch** | Device handles different size units | Network packets reassembled |
| **DMA requirement** | DMA needs contiguous memory; user buffer may not be | `read()` → kernel buffer → user buffer |
| **Copy semantics** | Application buffer changes during I/O | Kernel copies data to preserve integrity |

## Buffering Strategies

### Single Buffer
- OS allocates one kernel buffer
- Device fills kernel buffer → OS copies to user space → user processes data
- While user processes, OS can start next I/O

### Double Buffer (Buffer Swapping)
- Two kernel buffers: OS fills A while system copies B to user, then swap
- **Eliminates wait** for single buffer copy
- Used in: audio/video streaming, high-speed I/O

### Circular Buffer (Ring Buffer)
- Multiple buffers arranged in a circle
- **Producer** (device) writes, **consumer** (process) reads
- Two pointers: `head` (write) and `tail` (read)
- Used in: **network drivers** (ring buffer for RX/TX packets), serial ports

## Buffer Management in Linux
- **Page cache**: caches file data (unified, replaces old buffer cache)
- **Buffer cache** (legacy): caches disk blocks (mostly absorbed into page cache)
- `struct buffer_head`: metadata about a block-sized buffer in memory
- `bio` (Block I/O): modern Linux block I/O structure; vectors of pages

## Buffering in C Library (stdio)

| Mode | `setvbuf` Constant | Behavior |
|------|-------------------|----------|
| **Full buffering** | `_IOFBF` | Buffer filled before write (files) |
| **Line buffering** | `_IOLBF` | Flush on newline (terminal) |
| **No buffering** | `_IONBF` | Write immediately (stderr) |

## Key Interview Questions
- Buffer vs Cache? → Buffer: data in transit (e.g., network packet reassembly); Cache: data stored for potential reuse (e.g., frequently read disk blocks)
- Why double buffering? → Consumer processes one buffer while producer fills the other; **overlaps I/O with computation**
- What is **buffer overflow**? → Writing more data to buffer than allocated size; security vulnerability (exploited via stack smashing)
- How does Linux page cache work? → `read()` → page cache lookup → if miss, disk I/O → page cache populated → copy to user
- What is **zero-copy**? → Avoid copying between kernel and user space (`sendfile()`, `splice()`, `mmap()`)
