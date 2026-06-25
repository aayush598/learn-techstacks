# I/O Hardware Basics

## Device Categories
- **Block devices**: store data in fixed-size blocks (disk, SSD); support random access; mounted as filesystems
- **Character devices**: stream of bytes (keyboard, mouse, serial port); no seek; accessed sequentially
- **Network devices**: sockets interface (not block/char); **bidirectional**, asynchronous

## I/O Ports & Addressing

| Method | Description | Example |
|--------|-------------|---------|
| **Port-mapped I/O** | Separate address space; special `IN`/`OUT` instructions | x86 legacy (0x60 = keyboard) |
| **Memory-mapped I/O** | Device registers mapped to memory address space; accessed via regular `LOAD`/`STORE` | Modern devices, PCIe bars |
| **Hybrid** | Some control registers port-mapped, data buffers memory-mapped | Many modern GPUs |

## Data Transfer Methods

### Polling (Programmed I/O)
- CPU repeatedly checks **status register** for `BUSY` → `DONE`
- **Wastes CPU cycles** while waiting
- Simple, no interrupt overhead
- Acceptable: for very fast operations or when CPU has nothing else to do

### Interrupt-Driven I/O
- Device sends **interrupt signal** when operation completes
- Steps:
  1. Device raises interrupt line
  2. CPU saves current state (PC, registers)
  3. CPU jumps to **interrupt vector** (handler address from IDT)
  4. Handler runs, determines cause (device identification)
  5. Handles data, sends acknowledgment
  6. Restores state, returns to interrupted process
- **Multi-level interrupts**: higher priority interrupts can preempt lower ones
- **Maskable** vs **Non-maskable** (NMI): critical events like hardware failure

### DMA (Direct Memory Access)
- Device writes/reads memory **without CPU** (covered in detail in 03-dma)
- CPU initiates transfer, DMA controller executes, interrupts when done

## Important Hardware Concepts
- **Interrupt vector table** (IVT) / **Interrupt descriptor table** (IDT): maps interrupt number → handler address
- **Programmable Interrupt Controller** (PIC) / **Advanced PIC** (APIC): manages multiple interrupts, priorities
- **MMIO vs Port I/O** on x86: `inb`/`outb` vs `mov` to memory address
- **Bus**: PCIe, SATA, USB — each with its own protocol stack

## Key Interview Questions
- Why memory-mapped I/O? → Faster (no special instructions), simpler programming model
- What is an **interrupt storm**? → Excessive interrupts from a malfunctioning device, overwhelming CPU
- What is **APIC**? → Advanced Programmable Interrupt Controller; enables multi-CPU interrupt routing
- Difference between **edge-triggered** and **level-triggered** interrupts? → Edge: one pulse; Level: continuous signal until acknowledged
- What is **MSI-X**? → Message Signaled Interrupts (PCIe); device writes to memory to signal interrupt, no dedicated IRQ lines
