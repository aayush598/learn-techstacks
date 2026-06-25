# Spooling

## Definition
- **Spool**: Simultaneous Peripheral Operation On-Line
- A technique to manage **shared devices** that cannot handle concurrent access
- Queues output from multiple processes and sends to device one at a time

## Spooling vs Buffering

| Aspect | **Spooling** | **Buffering** |
|--------|-------------|---------------|
| **Duration** | Holds output for later processing | Temporary, short-lived |
| **Storage** | Disk (spool file) | Memory (RAM) |
| **Destination** | Shared device (printer, fax) | Any I/O channel |
| **Direction** | Usually output | Input or output |
| **Persistence** | Survives process lifetime | Dies with process |

## Classic Example: Printer Spooler
1. Process opens `/dev/lp0` or writes to spool directory (`/var/spool/cups/`)
2. Spooler daemon (CUPS, LPD) queues the print job
3. Daemon sends jobs to printer one-by-one as printer becomes free
4. User gets prompt return (doesn't wait for printer)

```
Process A → [spool file A]
Process B → [spool file B]    ← daemon reads → Printer
Process C → [spool file C]          ↓
                               Job Queue (FIFO)
```

## Multiplexing via Spooling
- One physical device → **N virtual devices** via spooler queue
- Processes think they have exclusive access to the device
- Spooler serializes access

## Spooling in Modern Systems

| Use Case | Implementation |
|----------|---------------|
| **Printing** | CUPS (Linux), Windows Print Spooler |
| **Email** | Mail queue (sendmail, postfix) |
| **Batch jobs** | Print job spool for mainframe |
| **Fax** | Outgoing fax queue |
| **File transfer** | Upload queue in web servers |

## Spooling Internals (CUPS Example)
- **IPP** (Internet Printing Protocol): modern print protocol
- Spool directory: `/var/spool/cups/`
- Daemon: `cupsd` listens on port 631 (HTTP)
- Jobs: numbered sequentially (`d00001-001`)
- Filters: convert PostScript/PDF → printer-specific PDL

## Potential Problems
- **Spool space exhaustion**: large jobs fill disk; spool on separate partition
- **Daemon crash**: jobs may be lost if not journaled
- **Stuck jobs**: deadlock if printer requires manual intervention
- **Security**: spool files may contain sensitive data

## Key Interview Questions
- Spool vs Buffer: when to use which? → Spool: shared device with non-overlapping usage (printer); Buffer: speed mismatch (keyboard → program)
- Why not just let processes write directly to printer? → Jumbled output (interleaved pages from different processes)
- What is **CUPS**? → Common Unix Printing System; modern print spooler with IPP support
- How does spooling handle priority? → Queues can implement priority (CUPS supports `lp -q 100` for high priority)
