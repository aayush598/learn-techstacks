# I/O Software Layers

## Layered I/O Architecture

```
User Process (application code)
    ↓ (syscall: read, write, ioctl)
User-Level I/O Libraries (printf, scanf — C stdio)
    ↓ (wraps syscalls with buffering)
Device-Independent OS Layer (buffering, caching, error handling)
    ↓ (uniform interface)
Device Drivers (device-specific code)
    ↓ (hardware access)
Interrupt Handlers (bottom half / top half)
    ↓
Hardware Device
```

## Layer Details

### 1. Interrupt Handlers
- **Bottom half** (hardirq): quick acknowledgment, minimal work, runs with interrupts disabled
- **Top half** (softirq/tasklet/workqueue): heavy lifting, runs with interrupts enabled
- Linux: `request_irq()` registers handler; handler should be fast
- Modern: **threaded interrupts** — handler runs as kernel thread

### 2. Device Drivers
- **Device-specific code** that knows hardware registers, protocols
- Provides **uniform interface** to the OS via driver operations structure
- Linux: `struct file_operations` — `open`, `release`, `read`, `write`, `ioctl`, `mmap`
- Drivers register with kernel: `register_chrdev()`, `pci_register_driver()`
- Can be **loaded/unloaded dynamically** (kernel modules, `.ko` files)

### 3. Device-Independent OS Layer
- **Buffering**: absorb speed differences between device and consumer
- **Caching**: retain frequently accessed data in faster memory
- **Error handling**: retry, log, or report errors to user process
- **I/O scheduling**: reorder requests for efficiency
- **Protection**: validate that user has permission for device access
- **Naming**: device files (`/dev/sda`, `/dev/tty`) provide file-like interface

### 4. User-Level I/O Libraries
- Example: `printf()` wraps `write()` syscall with stdio buffering
- `setvbuf()` controls buffering mode: `_IOFBF` (full), `_IOLBF` (line), `_IONBF` (none)
- System calls are expensive (context switch); buffering reduces syscall frequency

## Spooling
- **Spooling**: Simultaneous Peripheral Operation On-Line
- Queue output for **shared devices** that cannot be concurrently accessed (printers)
- Daemon process reads spool and sends to device
- Multiplexing: one physical device → many virtual devices via spooling

## Key Interview Questions
- Why are device drivers needed? → Each device has unique registers/protocols; OS cannot know every device
- What's the difference between **character device** and **block device** driver? → char: stream, block: random access with caching
- What is **ioctl**? → I/O control; device-specific operations not covered by read/write (e.g., configure baud rate on serial port)
- How does Linux handle a network packet? → NIC → DMA to ring buffer → hardirq → softirq (NAPI) → protocol stack → socket buffer
