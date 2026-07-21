# Bus Architectures

## 1. Introduction to Bus Architecture

A bus is a shared communication pathway that connects multiple components in a system. Bus architecture is fundamental to computer systems, providing a standardized interface for data transfer between processors, memory, and peripherals.

### 1.1 Bus Characteristics

```
Bus Components:
┌─────────────────────────────────────┐
│              System Bus              │
│  ┌─────────────────────────────┐   │
│  │  Data Bus (n bits)          │   │
│  ├─────────────────────────────┤   │
│  │  Address Bus (m bits)       │   │
│  ├─────────────────────────────┤   │
│  │  Control Bus (k signals)    │   │
│  └─────────────────────────────┘   │
│         ↑           ↑              │
│    ┌────┴───┐  ┌────┴───┐         │
│    │ Master │  │ Slave  │         │
│    └────────┘  └────────┘         │
└─────────────────────────────────────┘

Bus Parameters:
- Data width: 8, 16, 32, 64 bits
- Address width: 16, 20, 32 bits
- Clock frequency: 1-100 MHz
- Bandwidth: Data width × Frequency
- Latency: Time for single transfer
```

### 1.2 Bus Types

| Type | Characteristics | Example |
|------|-----------------|---------|
| Parallel | Multiple wires, synchronous | PCI, AMBA |
| Serial | Single/few wires, asynchronous | SPI, I2C, UART |
| Shared | Multiple masters, arbitrated | ISA, VME |
| Point-to-point | Dedicated link | AXI, PCIe |

## 2. Parallel Bus Architecture

### 2.1 Simple Parallel Bus

```
8-bit Parallel Bus:

Master                          Slave
┌──────┐                      ┌──────┐
│      │──── A[15:0] ────────│      │
│ CPU  │──── D[7:0]  ────────│ MEM  │
│      │←── RD# ─────────────│      │
│      │←── WR# ─────────────│      │
│      │←── CS# ─────────────│      │
│      │←── CLK ─────────────│      │
└──────┘                      └──────┘

Signal Definitions:
A[15:0]: 16-bit address bus (64 KB address space)
D[7:0]:  8-bit data bus
RD#:     Read strobe (active low)
WR#:     Write strobe (active low)
CS#:     Chip select (active low)
CLK:     System clock

Bus Timing (Read Cycle):
CLK:   _|‾|_|‾|_|‾|_
CS#:   _____|‾‾‾‾‾|___
A:    ___|‾‾‾‾‾‾‾‾‾‾‾|___
RD#:  _____|‾‾‾‾‾‾|____
D:    XXXX|‾‾DATA‾‾|XXXX
                ↑
          Valid Data
```

### 2.2 Bus Handshaking

```
Synchronous Handshaking:
- Both devices use same clock
- Simple timing
- Fast transfer
- Requires clock distribution

Asynchronous Handshaking:
Master                    Slave
  │                        │
  │───── Address ─────────→│
  │                        │
  │───── Request ─────────→│
  │                        │
  │←──── Acknowledge ──────│
  │                        │
  │←──── Data ─────────────│
  │                        │

Handshake Protocol:
1. Master places address on bus
2. Master asserts request
3. Slave decodes address
4. Slave asserts acknowledge
5. Data transferred
6. Master de-asserts request
7. Slave de-asserts acknowledge

Benefits:
- No clock distribution needed
- Self-timed operation
- Works across clock domains
```

### 2.3 Bus Arbitration

```
Arbitration for Multiple Masters:

Round-Robin Arbitration:
┌─────────────────────────────────────┐
│          Round-Robin Arbiter        │
│  ┌─────────────────────────────┐   │
│  │  Priority: 0→1→2→3→0→1→... │   │
│  └─────────────────────────────┘   │
│         ↑     ↑     ↑     ↑        │
│     ┌───┴─┐┌─┴───┐┌─┴───┐┌─┴───┐  │
│     │M0   ││M1   ││M2   ││M3   │  │
│     └─────┘└─────┘└─────┘└─────┘  │
└─────────────────────────────────────┘

Fixed Priority Arbitration:
- Master 0: Highest priority
- Master 1: Second priority
- Master 2: Third priority
- Master 3: Lowest priority

Problem: Starvation of low-priority masters

Grant/Request Protocol:
M0: ──REQ0──┐
M1: ──REQ1──┤──→ [Arbiter] ──→ GRANT0
M2: ──REQ2──┤                ──→ GRANT1
M3: ──REQ3──┘                ──→ GRANT2
                              ──→ GRANT3
```

### 2.4 Bus Bandwidth

```
Bus Bandwidth Calculation:

Bandwidth = Data Width × Frequency × Efficiency

Example (8-bit bus, 10 MHz):
Ideal Bandwidth = 8 bits × 10 MHz = 80 Mbps = 10 MB/s

Efficiency Factors:
- Address phase overhead: 20-30%
- Wait states: 10-50%
- Arbitration overhead: 5-10%
- Turnaround time: 5%

Typical Efficiency: 50-70%
Actual Bandwidth: 10 × 0.6 = 6 MB/s

For Implant Applications:
- 8-bit bus at 1 MHz: 100 KB/s (sufficient for sensors)
- 16-bit bus at 1 MHz: 200 KB/s
- Power proportional to frequency and width
```

## 3. Serial Bus Architecture

### 3.1 SPI (Serial Peripheral Interface)

```
SPI Bus Structure:

Master                          Slave
┌──────┐                      ┌──────┐
│      │──── SCLK ────────────│      │
│      │──── MOSI ────────────│      │
│      │←── MISO ─────────────│      │
│      │──── CS# ─────────────│      │
└──────┘                      └──────┘

Signals:
SCLK: Serial clock (master generated)
MOSI: Master Out Slave In (data)
MISO: Master In Slave Out (data)
CS#:  Chip Select (active low)

SPI Timing:
SCLK: _|‾|_|‾|_|‾|_|‾|_|‾|_|‾|_|‾|_|‾|_
MOSI: D7  D6  D5  D4  D3  D2  D1  D0
CS#:  __|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|___

SPI Characteristics:
- Full duplex (simultaneous send/receive)
- Clock polarity and phase configurable
- No addressing (direct CS# control)
- Speed: 1-50 MHz typical
- Wires: 4 (SCLK, MOSI, MISO, CS#)
```

### 3.2 I2C (Inter-Integrated Circuit)

```
I2C Bus Structure:

┌─────────────────────────────────────┐
│                SDA                  │
│    ┌──────────┬──────────┬────────┐│
│    │          │          │        ││
│  ┌─┴──┐    ┌─┴──┐    ┌─┴──┐    ││
│  │Dev1│    │Dev2│    │Dev3│    ││
│  └────┘    └────┘    └────┘    ││
│                                   │
│                SCL                 │
└─────────────────────────────────────┘

Signals:
SDA: Serial Data (bidirectional)
SCL: Serial Clock (bidirectional, open-drain)

I2C Protocol:
1. Start condition: SDA falls while SCL high
2. Address byte: 7-bit address + R/W bit
3. ACK/NACK: Receiver acknowledges
4. Data bytes: 8 bits each, followed by ACK
5. Stop condition: SDA rises while SCL high

I2C Characteristics:
- Half duplex (one direction at a time)
- Multi-master capable
- Built-in addressing (7 or 10 bit)
- Speed: 100 kHz (standard), 400 kHz (fast), 3.4 MHz (fast+)
- Wires: 2 (SDA, SCL)
- Pull-up resistors required
```

### 3.3 UART (Universal Asynchronous Receiver/Transmitter)

```
UART Communication:

Transmitter                    Receiver
┌──────┐                      ┌──────┐
│  TX  │───── TXD ──────────→│  RX  │
│      │←──── RXD ───────────│      │
│      │←──── RTS ───────────│      │
│      │───── CTS ──────────→│      │
└──────┘                      └──────┘

UART Frame Format:
Idle    Start  D0  D1  D2  D3  D4  D5  D6  D7  Parity Stop  Idle
High ──┬──────┬───┬───┬───┬───┬───┬───┬───┬───┬──────┬──── High
       │      │   │   │   │   │   │   │   │   │      │
       0      b0  b1  b2  b3  b4  b5  b6  b7  P      1

Parameters:
- Baud rate: 9600, 19200, 38400, 115200 bps
- Data bits: 7 or 8
- Parity: None, Even, Odd
- Stop bits: 1 or 2

UART Characteristics:
- Asynchronous (no shared clock)
- Point-to-point only
- Simple implementation
- Low power
- Speed: Up to 1 Mbps
```

### 3.4 Serial Bus Comparison

| Feature | SPI | I2C | UART |
|---------|-----|-----|------|
| Wires | 4 | 2 | 2-4 |
| Speed | 50 MHz | 3.4 MHz | 1 Mbps |
| Duplex | Full | Half | Full |
| Multi-slave | Yes (CS#) | Yes (address) | No |
| Multi-master | No | Yes | No |
| Complexity | Low | Medium | Low |
| Power | Medium | Low | Very Low |

## 4. AMBA Bus Architecture (ARM)

### 4.1 AMBA Hierarchy

```
AMBA (Advanced Microcontroller Bus Architecture):

┌─────────────────────────────────────┐
│         System Bus (AXI)            │
│  High-bandwidth, low-latency        │
├─────────────────────────────────────┤
│         │         │         │       │
│    ┌────┴───┐┌────┴───┐┌────┴───┐  │
│    │ CPU    ││ DMA    ││ High   │  │
│    │        ││        ││ Speed  │  │
│    └────────┘└────────┘└────────┘  │
│                                     │
│         Bridge                     │
│    ┌────────────────────────────┐  │
│    │      APB Bridge            │  │
│    └────────────────────────────┘  │
│         │         │         │       │
│    ┌────┴───┐┌────┴───┐┌────┴───┐  │
│    │ UART   ││ SPI    ││ Timer  │  │
│    │        ││        ││        │  │
│    └────────┘└────────┘└────────┘  │
└─────────────────────────────────────┘

AMBA Versions:
- AHB: Advanced High-performance Bus
- APB: Advanced Peripheral Bus
- AXI: Advanced eXtensible Interface
- ACE: AXI Coherency Extensions
```

### 4.2 AXI Bus Protocol

```
AXI Signal Groups:

1. Read Address Channel:
ARID, ARADDR, ARLEN, ARSIZE, ARBURST, ARVALID, ARREADY

2. Read Data Channel:
RID, RDATA, RRESP, RLAST, RVALID, RREADY

3. Write Address Channel:
AWID, AWADDR, AWLEN, AWSIZE, AWBURST, AWVALID, AWREADY

4. Write Data Channel:
WID, WDATA, WSTRB, WLAST, WVALID, WREADY

5. Write Response Channel:
BID, BRESP, BVALID, BREADY

AXI Handshake:
Source → Ready/Valid protocol
- VALID: Signal/data is available
- READY: Receiver can accept
- Transfer occurs when both VALID and READY are high
```

### 4.3 AXI Transaction

```
AXI Read Transaction:

Master                        Slave
  │                             │
  │──── ARVALID ───────────────→│
  │←─── ARREADY ───────────────│
  │──── ARADDR ────────────────→│
  │                             │
  │                             │ (memory access)
  │                             │
  │←─── RVALID ────────────────│
  │──── RREADY ────────────────→│
  │←─── RDATA ─────────────────│
  │←─── RLAST ─────────────────│

AXI Write Transaction:
Master                        Slave
  │                             │
  │──── AWVALID ───────────────→│
  │←─── AWREADY ───────────────│
  │──── AWADDR ────────────────→│
  │                             │
  │──── WVALID ────────────────→│
  │←─── WREADY ────────────────│
  │──── WDATA ─────────────────→│
  │──── WLAST ─────────────────→│
  │                             │
  │←─── BVALID ────────────────│
  │──── BREADY ────────────────→│
  │←─── BRESP ─────────────────│
```

### 4.4 AXI Performance

```
AXI Bandwidth Calculation:

Burst Length: 1-256 beats
Data Width: 64 bits (typical)
Frequency: 200 MHz

Max Bandwidth = 64 bits × 200 MHz × 1 (1 beat/transfer)
              = 12.8 Gbps = 1.6 GB/s

With burst (16 beats):
Effective Bandwidth = 64 × 200M × 16 / (16 + overhead)
                    ≈ 1.5 GB/s

AXI Features for Performance:
1. Burst transfers: Multiple data per address
2. Out-of-order completion: Multiple outstanding transactions
3. Interleaving: Mix transactions from different masters
4. Outstanding transactions: Pipeline address and data phases
```

## 5. Bus Design for Implants

### 5.1 Low-Power Bus Techniques

```
Low-Power Bus Design:

1. Clock Gating:
Gate bus clock when no transfers:
┌────────────────────────────────────┐
│  Transfer Detector                 │
│  ┌──────────┐                     │
│  │ Activity │──→ [AND] ──→ CLK   │
│  │ Monitor  │      ↑              │
│  └──────────┘    Enable           │
└────────────────────────────────────┘
Power savings: 50-80% when idle

2. Bus Invert Coding:
Reduce switching activity:
- Transmit inverted data if >50% bits change
- Extra bit indicates inversion
- Reduces switching by ~25%

3. Turn-Off Unused Lines:
- Gate data bus drivers when not in use
- Reduce dynamic power
- Simple implementation

4. Voltage Scaling:
- Run bus at lower voltage when speed permits
- V_DD_bus = 0.5V vs 0.8V for logic
- 60% power reduction
```

### 5.2 Implant Bus Architecture

```
Implant SoC Bus Architecture:

┌─────────────────────────────────────────┐
│            Main Bus (16-bit)            │
│  ┌────────┐  ┌────────┐  ┌────────┐   │
│  │  CPU   │  │  DMA   │  │Memory  │   │
│  │(Master)│  │(Master)│  │(Slave) │   │
│  └────────┘  └────────┘  └────────┘   │
└─────────────────┬───────────────────────┘
                  │
          ┌───────┴───────┐
          │   Bus Bridge  │
          └───────┬───────┘
                  │
┌─────────────────┴───────────────────────┐
│          Peripheral Bus (8-bit)         │
│  ┌────────┐  ┌────────┐  ┌────────┐   │
│  │  UART  │  │  SPI   │  │ Timer  │   │
│  │ (Slave)│  │ (Slave)│  │(Master)│   │
│  └────────┘  └────────┘  └────────┘   │
└─────────────────────────────────────────┘

Design Choices:
- 16-bit main bus: Balance speed and power
- 8-bit peripheral bus: Lower power for slow devices
- Bridge: Protocol conversion, clock domain crossing
- Single master (CPU) simplifies arbitration
- DMA for sensor data transfer (background)
```

### 5.3 Bus Timing Budget

```
Bus Timing for Implant Processor:

Main Bus (16-bit, 1 MHz):
- Clock period: 1 us
- Setup time: 100 ns
- Hold time: 50 ns
- Propagation delay: 200 ns
- Available for transfer: 650 ns
- Effective bandwidth: 16 bits / 1 us = 16 Mbps = 2 MB/s

Peripheral Bus (8-bit, 500 kHz):
- Clock period: 2 us
- Setup time: 200 ns
- Hold time: 100 ns
- Propagation delay: 400 ns
- Available for transfer: 1300 ns
- Effective bandwidth: 8 bits / 2 us = 4 Mbps = 500 KB/s

Power Budget:
Main bus: 16 bits × 1 MHz × 0.5V × C_wire ≈ 10 microwatt
Peripheral bus: 8 bits × 500 kHz × 0.5V × C_wire ≈ 2 microwatt
Total bus power: 12 microwatt
```

## 6. Network-on-Chip (NoC)

### 6.1 NoC Concepts

```
NoC Topology:

Mesh NoC (4x4):
┌────┬────┬────┬────┐
│ R0 │ R1 │ R2 │ R3 │
└─┬──┴─┬──┴─┬──┴─┬──┘
  │    │    │    │
┌─┴──┬─┴──┬─┴──┬─┴──┐
│ R4 │ R5 │ R6 │ R7 │
└─┬──┴─┬──┴─┬──┴─┬──┘
  │    │    │    │
┌─┴──┬─┴──┬─┴──┬─┴──┐
│ R8 │ R9 │R10 │R11 │
└─┬──┴─┬──┴─┬──┴─┬──┘
  │    │    │    │
┌─┴──┬─┴──┬─┴──┬─┴──┐
│R12 │R13 │R14 │R15 │
└────┴────┴────┴────┘

Router Structure:
┌────────────────────────┐
│       Router           │
│  ┌────┬────┬────┬────┐│
│  │ N  │ S  │ E  │ W  ││
│  └──┬─┴──┬─┴──┬─┴──┬─┘│
│     └────┼────┼────┘   │
│       ┌──┴────┴──┐     │
│       │ Switch   │     │
│       │ Allocator│     │
│       └────┬─────┘     │
│            │           │
│       ┌────┴─────┐     │
│       │   Local  │     │
│       │   Port   │     │
│       └──────────┘     │
└────────────────────────┘

Benefits over bus:
- Higher bandwidth (parallel paths)
- Scalable to many cores
- Predictable latency
- Lower power at high utilization
```

### 6.2 NoC for Implants

```
Simple NoC for Multi-Core Implant:

2x2 Mesh NoC:
┌───────┬───────┐
│ Core  │ Core  │
│  0    │  1    │
└───┬───┴───┬───┘
    │       │
┌───┴───┬───┴───┐
│ Core  │ Core  │
│  2    │  3    │
└───────┴───────┘

Router Parameters:
- 5 ports (N, S, E, W, Local)
- 16-bit data width
- 3-5 cycle latency per hop
- Wormhole routing

Power:
Per router: 50 microwatt
4 routers: 200 microwatt
Network interface: 50 microwatt per core
Total NoC power: 400 microwatt

For Implant Applications:
- Use simple bus for 1-2 cores
- NoC for 4+ cores
- Mesh topology sufficient
- Low-speed operation (1-10 MHz)
```

## 7. Bus Protocols

### 7.1 Wishbone Bus

```
Wishbone Bus Interface:

Signal     | Direction | Description
-----------|-----------|------------------
CYC        | Master→   | Bus cycle active
STB        | Master→   | Strobe (data valid)
ACK        | Slave→    | Acknowledge
ADR[AW-1:0]| Master→  | Address
DAT[DW-1:0]| Both     | Data (bidirectional)
SEL[SW-1:0]| Master→  | Byte select
WE         | Master→  | Write enable

Wishbone Read Transfer:
CLK: _|‾|_|‾|_|‾|_
CYC: ____|‾‾‾‾‾‾‾‾|____
STB: ____|‾‾‾‾‾‾‾‾|____
ADR: ____|‾ADDR‾‾‾‾|____
DAT: XXXX|‾‾DOUT‾‾‾|XXXX
ACK: ________|‾‾‾‾|_______
                ↑
          Valid Data In

Wishbone Features:
- Synchronous or asynchronous
- Configurable data width
- Big-endian or little-endian
- Pipelined or block transfers
- Open-source standard
```

### 7.2 Avalon Bus

```
Avalon Memory-Mapped Interface:

Signal     | Direction | Description
-----------|-----------|------------------
CLK        | System→   | Clock
RESET      | System→   | Reset
ADDRESS    | Master→   | Address
READDATA   | Slave→    | Read data
WRITEDATA  | Master→   | Write data
READ       | Master→   | Read request
WRITE      | Master→   | Write request
WAITREQUEST| Slave→    | Wait (not ready)

Avalon Characteristics:
- Simplified handshaking
- Built-in wait state handling
- Automatic bus width adaptation
- Burst transfer support
- QoS (Quality of Service) support
```

### 7.3 Protocol Comparison

| Feature | AXI | Wishbone | Avalon |
|---------|-----|----------|--------|
| Complexity | High | Low | Medium |
| Performance | Very High | Medium | High |
| Pipelining | Yes | Optional | Yes |
| Burst | Yes | Yes | Yes |
| Out-of-order | Yes | No | No |
| Open Source | No | Yes | No |
| Best For | High-perf | Simple SoC | FPGA |
| Implant Use | Overkill | Suitable | Suitable |

## 8. Bus Verification

### 8.1 Bus Protocol Check

```verilog
// Simple bus monitor
module bus_monitor (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        cs_n,
    input  wire        rd_n,
    input  wire        wr_n,
    input  wire [15:0] addr,
    input  wire [7:0]  data
);

    // Protocol checks
    property p_cs_before_transfer;
        @(posedge clk) (!cs_n) |-> (!$stable(cs_n) |-> ($rose(rd_n) || $rose(wr_n)));
    endproperty

    property p_setup_time;
        @(posedge clk) ($rose(cs_n)) |-> ($stable(addr) [*3]);
    endproperty

    property p_data_valid;
        @(posedge clk) (!cs_n && !rd_n) |-> ($stable(data) [*2]);
    endproperty

    assert property (p_cs_before_transfer)
        else $error("Bus protocol violation: CS timing");
    assert property (p_setup_time)
        else $error("Bus protocol violation: Setup time");
    assert property (p_data_valid)
        else $error("Bus protocol violation: Data validity");

endmodule
```

### 8.2 Bus Performance Metrics

```
Bus Performance Counters:

1. Transfer Count:
   - Total transfers per second
   - Read vs Write ratio

2. Bandwidth Utilization:
   - Actual vs theoretical bandwidth
   - Idle cycles

3. Latency:
   - Average transfer latency
   - Maximum latency

4. Wait States:
   - Number of wait states
   - Percentage of transfers with waits

Monitoring Implementation:
┌────────────────────────────────────┐
│  Performance Counter Unit          │
│  ┌──────────┐  ┌──────────┐      │
│  │ Transfer │  │ Cycle    │      │
│  │ Counter  │  │ Counter  │      │
│  └──────────┘  └──────────┘      │
│  ┌──────────┐  ┌──────────┐      │
│  │  Wait    │  │ Bandwidth│      │
│  │ Counter  │  │ Register │      │
│  └──────────┘  └──────────┘      │
└────────────────────────────────────┘

Performance = Transfer_Count / Total_Cycles
Bandwidth = (Data_Width × Transfer_Count × Clock_Freq) / Total_Cycles
```

## 9. Applications in Medical Implant Design

### 9.1 Implant Bus Requirements

```
Implant Bus Requirements:

1. Low Power:
   - Total bus power < 50 microwatt
   - Clock gating when idle
   - Minimal bus activity

2. Reliability:
   - Error detection on address/data
   - Parity or CRC protection
   - Redundancy for critical paths

3. Simple Implementation:
   - Single-master preferred (CPU only)
   - Minimal control signals
   - Small decoder logic

4. Low Latency:
   - Sensor data access < 10 us
   - Control register access < 1 us
   - Memory access < 100 ns

Recommended Architecture:
- 16-bit parallel bus for main system
- 8-bit SPI for sensor interface
- I2C for configuration/communication
- UART for external communication
```

### 9.2 Bus Power Optimization

```
Bus Power Optimization Techniques:

1. Activity-Based Power:
   P_bus = C_bus × V_DD² × f × alpha
   Where alpha = switching activity factor

   Optimization:
   - Reduce alpha: Bus encoding (Bus-Invert)
   - Reduce f: Clock gating when idle
   - Reduce C: Shorter wires, fewer bits

2. Example Power Calculation:
   16-bit bus, 0.5V, 1 MHz, C_wire = 10 fF per bit
   P_bus = 16 × 10e-15 × 0.25 × 1e6 × 0.3
        = 12 microwatt

   With clock gating (50% idle):
   P_bus = 12 × 0.5 = 6 microwatt

3. Voltage Scaling:
   At 0.3V instead of 0.5V:
   P_bus = 16 × 10e-15 × 0.09 × 1e6 × 0.3
        = 4.3 microwatt

4. Total Bus Power Budget:
   Main bus: 6 microwatt
   Peripheral bus: 2 microwatt
   Total: 8 microwatt (within 50 microwatt budget)
```

## 10. Summary

| Bus Type | Bandwidth | Power | Complexity | Best For |
|----------|-----------|-------|------------|----------|
| Parallel (8-bit) | 8 Mbps | Medium | Low | Simple systems |
| Parallel (16-bit) | 16 Mbps | Medium | Medium | Implant main bus |
| SPI | 50 Mbps | Low | Low | Sensor interface |
| I2C | 3.4 Mbps | Very Low | Medium | Configuration |
| UART | 1 Mbps | Very Low | Low | External comm |
| AXI | 10+ Gbps | High | High | High-performance |
| NoC | Scalable | Medium | High | Multi-core |

## 11. Exercises

1. Design an 8-bit parallel bus with handshaking protocol
2. Implement SPI master and slave in Verilog
3. Calculate bus bandwidth for different configurations
4. Design a bus arbiter for 4 masters with round-robin scheduling
5. Compare power consumption of parallel vs serial buses
6. Implement a simple I2C controller
7. Design a bus bridge between 16-bit and 8-bit domains
8. Create a bus monitor with protocol checking
