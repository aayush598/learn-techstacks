# Memory Hierarchy Design

## 1. Introduction to Memory Hierarchy

Memory hierarchy exploits the principle of locality to provide fast access to frequently used data while maintaining large storage capacity at lower cost.

### 1.1 Principle of Locality

```
Temporal Locality:
If a memory location is accessed, it is likely to be accessed again soon.
Example: Loop variables, stack data

Spatial Locality:
If a memory location is accessed, nearby locations are likely to be accessed.
Example: Array elements, sequential code

Combined Effect:
Small, fast memory (cache) can capture most accesses
Hit rate typically > 95% with proper hierarchy design
```

### 1.2 Memory Hierarchy Structure

```
┌─────────────────────────────────────┐
│      Registers (32-64 bytes)        │ ← 1 cycle, ~0.1 mW
│      Speed: 0.2 ns                  │
├─────────────────────────────────────┤
│      L1 Cache (8-64 KB)            │ ← 1-2 cycles, ~1 mW
│      Speed: 0.5-1 ns               │
├─────────────────────────────────────┤
│      L2 Cache (64-512 KB)          │ ← 5-10 cycles, ~10 mW
│      Speed: 2-5 ns                 │
├─────────────────────────────────────┤
│      Main Memory (1-16 MB)         │ ← 50-100 cycles, ~100 mW
│      Speed: 20-50 ns               │
├─────────────────────────────────────┤
│      Storage (16-256 MB)           │ ← 1000+ cycles, ~1 mW
│      Speed: 50-100 us              │
└─────────────────────────────────────┘

For Implant Applications:
- Eliminate L2 cache (save power/area)
- Small L1 cache (8-16 KB)
- Low-power SRAM technology
- Near-threshold operation
```

## 2. SRAM Design

### 2.1 SRAM Cell

```
6T SRAM Cell:

      V_DD          V_DD
       │              │
    ┌──┴──┐        ┌──┴──┐
    │ M1  │        │ M2  │  ← Pull-up PMOS
    │(PMOS)│       │(PMOS)│
    └──┬──┘        └──┬──┘
       │              │
       ├──── Q ───────┤──── Q'
       │              │
    ┌──┴──┐        ┌──┴──┐
    │ M3  │        │ M4  │  ← Pull-down NMOS
    │(NMOS)│       │(NMOS)│
    └──┬──┘        └──┬──┘
       │              │
       └──────┬───────┘
              │
    ┌─────────┴─────────┐
    │         │         │
┌───┴───┐ ┌───┴───┐ ┌───┴───┐
│  M5   │ │  BL   │ │  M6   │  ← Access NMOS
│(NMOS) │ │       │ │(NMOS) │
└───┬───┘ │       │ └───┬───┘
    │     │       │     │
   WL    BL'     BL    WL'

Word Line (WL): Controls access transistors
Bit Lines (BL, BL'): Differential data lines

Stability Condition:
β = (W_pull-down / W_access) > 1.2
Read margin requires β > 1.2
Write margin requires (W_pull-up / W_access) < 1.8
```

### 2.2 SRAM Cell Sizing

```
SRAM Sizing for Stability:

Transistor Ratios (for 65nm):
Transistor | Width  | Length | Purpose
-----------|--------|--------|--------
M1, M2     | 120 nm | 60 nm  | Pull-up
M3, M4     | 180 nm | 60 nm  | Pull-down
M5, M6     | 120 nm | 60 nm  | Access

Cell Size: 6 × (120+180) × 60 = 10,800 nm2
With overhead: ~0.1 μm2 per bit

Read Stability:
β = (W_pull-down / W-access) = 180/120 = 1.5 > 1.2 ✓

Write Ability:
γ = (W_pull-up / W-access) = 120/120 = 1.0 < 1.8 ✓

Trade-off:
Larger pull-down → Better read stability, larger cell
Larger access → Better write ability, worse read stability
```

### 2.3 SRAM Array Architecture

```
SRAM Array (16 KB):

Address (14 bits):
┌─────┬─────┬─────┐
│ Row │Col H│Col L│
│ 8b  │ 3b  │ 3b  │
└─────┴─────┴─────┘

Array Structure:
                    Bit Lines (64 pairs)
                    ↓
            ┌───────┴───────┐
    WL0  ───┤ SRAM SRAM ... SRAM ├── BL0/BL0'
    WL1  ───┤ SRAM SRAM ... SRAM ├── BL1/BL1'
     ...     │      ...           │   ...
    WL255 ───┤ SRAM SRAM ... SRAM ├── BL255/BL255'
            └───────┬───────┘
                    ↑
               Word Line Decoder

Organization:
- 256 rows × 64 columns = 16,384 bits = 2 KB per bank
- 8 banks = 16 KB total
- Column mux: 8:1 (select 8 bits from 64)

Access Sequence:
1. Row decoder activates one WL (8 bits per column group)
2. 64 bit-line pairs driven by SRAM cells
3. Column mux selects 8 bits (for 8-bit data width)
4. Sense amplifiers detect small voltage swing
5. Output drivers send data to bus
```

### 2.4 Sense Amplifier

```
Cross-Coupled Sense Amplifier:

     BL         BL'
      │          │
      ├──────────┤
      │          │
   ┌──┴──┐    ┌──┴──┐
   │ M1  │    │ M2  │
   │(PMOS)│   │(PMOS)│
   └──┬──┘    └──┬──┘
      │          │
      ├──────────┤
      │          │
   ┌──┴──┐    ┌──┴──┐
   │ M3  │    │ M4  │
   │(NMOS)│   │(NMOS)│
   └──┬──┘    └──┬──┘
      │          │
      └────┬─────┘
           │
         SA_EN (Enable)

Operation:
1. BL and BL' precharged to V_DD
2. SRAM cell creates small voltage difference
3. SA_EN goes high, activates sense amplifier
4. Positive feedback amplifies small difference
5. BL goes to V_DD, BL' goes to GND (or vice versa)

Sensitivity: 50-100 mV differential
Amplification time: 0.1-0.5 ns
Power: 1-10 microwatt per sense amp
```

## 3. Cache Design

### 3.1 Cache Organization

```
Direct-Mapped Cache (8 KB):

Address (32 bits):
┌──────┬──────┬──────┐
│ Tag  │Index │Offset│
│ 20b  │ 7b   │ 5b   │
└──────┴──────┴──────┘

Cache Structure:
┌──────────────────────────────────┐
│  Tag Array     │  Data Array     │
│                │                 │
│ Tag[0] [Valid] │ Data[0] (32B)  │
│ Tag[1] [Valid] │ Data[1] (32B)  │
│ ...            │ ...             │
│ Tag[127] [Val] │ Data[127] (32B)│
└──────────────────────────────────┘

- 128 sets (7-bit index)
- 32 bytes per block (5-bit offset)
- 128 × 32 = 4,096 bytes = 4 KB
- 20-bit tag for address identification

Hit Detection:
1. Extract index from address
2. Read tag from tag array
3. Compare tag with address tag
4. If match and valid, cache hit
5. Use offset to select byte within block
```

### 3.2 Set-Associative Cache

```
2-Way Set-Associative Cache (16 KB):

Address (32 bits):
┌──────┬──────┬──────┐
│ Tag  │Index │Offset│
│ 19b  │ 7b   │ 5b   │
└──────┴──────┴──────┘

Cache Structure:
┌─────────────────────────────────────┐
│           Set 0                     │
│  ┌───────────┐  ┌───────────┐     │
│  │ Way 0     │  │ Way 1     │     │
│  │ Tag+Data  │  │ Tag+Data  │     │
│  └───────────┘  └───────────┘     │
├─────────────────────────────────────┤
│           Set 1                     │
│  ┌───────────┐  ┌───────────┐     │
│  │ Way 0     │  │ Way 1     │     │
│  │ Tag+Data  │  │ Tag+Data  │     │
│  └───────────┘  └───────────┘     │
├─────────────────────────────────────┤
│           ...                       │
├─────────────────────────────────────┤
│           Set 127                   │
│  ┌───────────┐  ┌───────────┐     │
│  │ Way 0     │  │ Way 1     │     │
│  │ Tag+Data  │  │ Tag+Data  │     │
│  └───────────┘  └───────────┘     │
└─────────────────────────────────────┘

- 128 sets, 2 ways per set
- Block size: 32 bytes
- Total: 128 × 2 × 32 = 8,192 bytes = 8 KB

Benefits over direct-mapped:
- Higher hit rate (fewer conflicts)
- More flexible replacement
- Moderate complexity increase
```

### 3.3 Replacement Policies

```
LRU (Least Recently Used):
- Track access history for each set
- Replace least recently accessed way
- Good hit rate, moderate complexity
- Implementation: 2-bit counter per way per set

FIFO (First-In First-Out):
- Replace oldest block
- Simple implementation
- Slightly lower hit rate than LRU
- Implementation: Circular pointer

Random:
- Replace random way
- No history tracking needed
- Surprisingly good performance
- Implementation: Random number generator

For Implant Applications:
- Use FIFO or Random (simpler, lower power)
- LRU adds complexity and power overhead
- Small cache sizes reduce advantage of LRU
```

### 3.4 Write Policies

```
Write-Through:
- Write to cache AND memory simultaneously
- Simpler implementation
- Higher memory traffic
- Lower power (no dirty bits)

Write-Back:
- Write to cache only
- Mark block as dirty
- Write to memory only when evicted
- Lower memory traffic
- Higher complexity (dirty bits)

Write Buffer:
┌──────────────────────────────────┐
│  Write Buffer (4-8 entries)      │
│  ┌────┬────┬────┬────┐         │
│  │Addr│Data│Addr│Data│ ...     │
│  └────┴────┴────┴────┘         │
└──────────────────────────────────┘

- Buffers writes to memory
- CPU continues execution
- Reduces write stall time

For Implants:
- Write-through preferred (simpler, more predictable)
- Small write buffer (2 entries)
- Avoid write-back complexity and dirty bit overhead
```

## 4. Cache Performance

### 4.1 Hit Rate Analysis

```
Average Memory Access Time (AMAT):

AMAT = Hit_Time + Miss_Rate × Miss_Penalty

Example (Direct-Mapped):
Hit_Time = 1 ns
Miss_Rate = 5%
Miss_Penalty = 50 ns (memory access)

AMAT = 1 + 0.05 × 50 = 1 + 2.5 = 3.5 ns

Example (2-Way Set-Associative):
Hit_Time = 1.2 ns (slightly higher due to MUX)
Miss_Rate = 3%
Miss_Penalty = 50 ns

AMAT = 1.2 + 0.03 × 50 = 1.2 + 1.5 = 2.7 ns

Improvement: 23% faster AMAT despite slower hit time
```

### 4.2 Cache Sizing

```
Cache Size vs Hit Rate:

Cache Size | Miss Rate | Area   | Power
-----------|-----------|--------|-------
1 KB       | 15%       | Small  | Low
2 KB       | 10%       | Medium | Medium
4 KB       | 6%        | Medium | Medium
8 KB       | 4%        | Large  | High
16 KB      | 3%        | Very Large | Very High
32 KB      | 2.5%      | Huge   | Huge

Diminishing Returns:
- Going from 1KB to 4KB: 60% miss rate reduction
- Going from 4KB to 16KB: 50% miss rate reduction
- Going from 16KB to 64KB: 20% miss rate reduction

For Implants:
- 4-8 KB L1 cache optimal
- Balance hit rate vs power/area
- Consider application-specific access patterns
```

### 4.3 Power Analysis

```
Cache Power Components:

1. Tag Array Power:
   - Read tag for hit detection
   - Compare tags
   - Per access: 10-50 microwatt

2. Data Array Power:
   - Read/write data on hit
   - Per access: 50-200 microwatt

3. Replacement Logic Power:
   - Update LRU/fifo state
   - Per access: 5-20 microwatt

Total Cache Power:
P_cache = P_tag + P_data + P_repl + P_leak

For 8 KB cache, 65nm, 0.5V:
P_dynamic = 100 microwatt (at 1 MHz)
P_static = 10 microwatt
Total: 110 microwatt

Power Breakdown:
Component    | Dynamic | Static | Total
-------------|---------|--------|------
Tag Array    | 20 uW   | 2 uW   | 22 uW
Data Array   | 70 uW   | 7 uW   | 77 uW
Replacement  | 10 uW   | 1 uW   | 11 uW
Total        | 100 uW  | 10 uW  | 110 uW
```

## 5. Low-Power Cache Design

### 5.1 Cache Partitioning

```
Banked Cache Architecture:

┌────────────────────────────────────┐
│           Cache Controller         │
└───────────────┬────────────────────┘
                │
    ┌───────────┼───────────┐
    │           │           │
┌───┴───┐   ┌───┴───┐   ┌───┴───┐
│Bank 0 │   │Bank 1 │   │Bank 2 │
│ 2 KB  │   │ 2 KB  │   │ 2 KB  │
└───────┘   └───────┘   └───────┘

Benefits:
- Only power accessed bank
- 30-50% power reduction
- Parallel bank access possible
- Flexible capacity allocation

Bank Selection:
- Address bits select bank
- Simple decoder logic
- Low overhead
```

### 5.2 Way Prediction

```
Way Prediction Cache:

Predict which way contains data:
┌────────────────────────────────────┐
│         Way Prediction Table       │
│  ┌─────┬─────┬─────┐             │
│  │Index│ Way │Valid│             │
│  │     │     │     │             │
│  └─────┴─────┴─────┘             │
└───────────────┬────────────────────┘
                │
                ↓ Predicted Way
    ┌───────────────────────────┐
    │  Read predicted way only  │
    └───────────────────────────┘
                │
         Hit? ──┼── Yes → Done
                │
                No → Read all ways

Benefits:
- Reduce power by reading one way
- 50-70% power reduction on hits
- Small prediction table overhead
- Miss penalty: additional cycle
```

### 5.3 Leakage Reduction

```
Cache Leakage Reduction Techniques:

1. Power Gating:
┌────────────────────────────────────┐
│  Sleep Transistor    │  SRAM Bank │
│  ┌──────────┐       │            │
│  │ Header   │───────│            │
│  │ PMOS     │       │            │
│  └──────────┘       │            │
└────────────────────────────────────┘
- Cut power to unused banks
- 90% leakage reduction
- Wake-up time: 1-10 ns

2. Retention Mode:
- Lower voltage for data retention
- V_DD_ret = 0.3V (vs 0.5V normal)
- 80% leakage reduction
- No wake-up time penalty

3. Selective Pull-Down:
- Disable pull-down in unused rows
- Reduce subthreshold leakage
- 50% leakage reduction
- Simple implementation
```

## 6. Memory Technology Comparison

### 6.1 SRAM vs DRAM vs Flash

```
Memory Technology Comparison:

Feature     | SRAM       | DRAM        | Flash (NAND)
------------|------------|-------------|-------------
Cell Size   | 6T (large) | 1T1C (small)| 1T (tiny)
Density     | Low        | High        | Very High
Speed       | Very Fast  | Fast        | Slow
Power       | Medium     | Medium      | Low
Cost        | High       | Medium      | Low
Volatile    | Yes        | Yes         | No
Endurance   | Unlimited  | Unlimited   | 100K-1M
Refresh     | No         | Yes         | No

For Implant Applications:
- SRAM: Registers, cache (speed critical)
- Flash: Program storage (non-volatile)
- DRAM: Not typically used (power, complexity)
```

### 6.2 SRAM Operating Modes

```
SRAM Operating Modes:

1. Active Mode (Read/Write):
   - Full V_DD = 0.5V
   - Full speed operation
   - Power: 100-200 microwatt per KB

2. Standby Mode:
   - Full V_DD maintained
   - No access, data retained
   - Power: 10-20 microwatt per KB (leakage only)

3. Retention Mode:
   - Reduced V_DD = 0.3V
   - Data retained, no access
   - Power: 1-2 microwatt per KB

4. Sleep Mode:
   - Power gated
   - Data lost
   - Power: ~0

Mode Transitions:
Active → Standby: 1 clock cycle
Standby → Active: 1 clock cycle
Standby → Retention: 10 ns
Retention → Active: 100 ns
Active → Sleep: Immediate
Sleep → Active: 1 us (data reload needed)
```

## 7. Cache Coherence (Multi-Core)

### 7.1 Coherence Problem

```
Multi-Core Cache Coherence:

Core 0        Core 1
  │             │
┌─┴─┐         ┌─┴─┐
│C0 │         │C1 │
└─┬─┘         └─┬─┘
  │             │
  └──────┬──────┘
         │
    ┌────┴────┐
    │ Shared  │
    │ Memory  │
    └─────────┘

Problem:
Core 0 writes X = 5
Core 1 reads X → Gets stale value (1)

Solutions:
- Snooping (bus-based)
- Directory-based
- Write-invalidate
- Write-update
```

### 7.2 Snooping Protocol (MESI)

```
MESI Protocol States:

State    | Description
---------|----------------
Modified | Dirty, exclusive to this cache
Exclusive| Clean, exclusive to this cache
Shared   | Clean, may be in other caches
Invalid  | Not valid

State Transitions:
- Read miss: Fetch from memory, state = Exclusive
- Write hit (Exclusive): State = Modified
- Write hit (Shared): Broadcast invalidation, state = Modified
- Snooped read (Modified): Write back, state = Shared
- Snooped write (Shared): State = Invalid

For Implants:
- Typically single-core, no coherence needed
- If multi-core: simple snooping protocol
- Directory overhead not justified for 2-3 cores
```

## 8. Design Example: Implant Cache

### 8.1 Specifications

```
Implant Cache Specifications:

Technology: 65nm SRAM
Supply Voltage: 0.5V (near-threshold)
Organization: 8 KB, 2-way set associative
Block Size: 16 bytes
Sets: 256 (8-bit index)
Tag Width: 17 bits (with valid + LRU bits)

Target Performance:
- Hit time: 1 cycle (1 ns at 1 GHz, 1 us at 1 MHz)
- Miss rate: < 5% for target workload
- Miss penalty: 10 cycles (memory access)

Power Budget:
- Active: 100 microwatt
- Standby: 10 microwatt
- Retention: 1 microwatt
```

### 8.2 Implementation

```verilog
// Simple 8KB 2-way set-associative cache
module implant_cache (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        read_en,
    input  wire        write_en,
    input  wire [31:0] addr,
    input  wire [31:0] wdata,
    output reg  [31:0] rdata,
    output reg         hit,
    output reg         miss
);

    // Cache parameters
    parameter CACHE_SIZE = 8192;  // 8 KB
    parameter BLOCK_SIZE = 16;    // 16 bytes
    parameter WAYS = 2;
    parameter SETS = CACHE_SIZE / (BLOCK_SIZE * WAYS);

    // Address breakdown
    wire [4:0]  offset = addr[4:0];   // 5-bit block offset
    wire [7:0]  index = addr[12:5];   // 8-bit set index
    wire [18:0] tag = addr[31:13];    // 19-bit tag

    // Cache storage
    reg [31:0] data_array [0:SETS-1][0:WAYS-1][0:3];
    reg [18:0] tag_array [0:SETS-1][0:WAYS-1];
    reg        valid_array [0:SETS-1][0:WAYS-1];
    reg        lru_array [0:SETS-1];  // LRU bit per set

    // Cache logic
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            hit <= 0;
            miss <= 0;
            rdata <= 0;
        end else begin
            if (read_en) begin
                // Check way 0
                if (valid_array[index][0] && tag_array[index][0] == tag) begin
                    hit <= 1;
                    miss <= 0;
                    rdata <= data_array[index][0][offset[4:2]];
                    lru_array[index] <= 1;  // Mark way 1 as LRU
                end
                // Check way 1
                else if (valid_array[index][1] && tag_array[index][1] == tag) begin
                    hit <= 1;
                    miss <= 0;
                    rdata <= data_array[index][1][offset[4:2]];
                    lru_array[index] <= 0;  // Mark way 0 as LRU
                end
                // Miss
                else begin
                    hit <= 0;
                    miss <= 1;
                    // In real implementation: fetch from memory
                end
            end

            if (write_en) begin
                // Simplified write logic
                if (valid_array[index][0] && tag_array[index][0] == tag) begin
                    data_array[index][0][offset[4:2]] <= wdata;
                end else if (valid_array[index][1] && tag_array[index][1] == tag) begin
                    data_array[index][1][offset[4:2]] <= wdata;
                end
            end
        end
    end

endmodule
```

## 9. Applications in Medical Implant Design

### 9.1 Implant Memory Architecture

```
Complete Implant Memory System:

┌─────────────────────────────────────┐
│            CPU Core                 │
│  ┌──────────┐  ┌──────────┐        │
│  │ Registers│  │   ALU    │        │
│  │ (32x32)  │  │          │        │
│  └──────────┘  └──────────┘        │
└───────────────┬─────────────────────┘
                │
┌───────────────┴─────────────────────┐
│         L1 Cache (8 KB)            │
│  ┌──────────┐  ┌──────────┐        │
│  │ 2 KB I$  │  │ 2 KB D$  │        │
│  └──────────┘  └──────────┘        │
└───────────────┬─────────────────────┘
                │
┌───────────────┴─────────────────────┐
│      Main Memory (16 KB SRAM)      │
│  ┌──────────┐  ┌──────────┐        │
│  │ Program  │  │   Data   │        │
│  │ (8 KB)   │  │  (8 KB)  │        │
│  └──────────┘  └──────────┘        │
└───────────────┬─────────────────────┘
                │
┌───────────────┴─────────────────────┐
│      Storage (64 KB Flash)         │
│  ┌──────────┐  ┌──────────┐        │
│  │ Program  │  │ Calibration│       │
│  │ Storage  │  │   Data    │        │
│  └──────────┘  └──────────┘        │
└─────────────────────────────────────┘

Power Breakdown:
Component     | Power
--------------|------
Registers     | 10 uW
L1 Cache      | 100 uW
Main Memory   | 200 uW
Storage       | 50 uW (when accessed)
Total Memory  | 360 uW
```

### 9.2 Power Management

```
Memory Power Management:

States:
1. Full Speed: 0.5V, 1 MHz, 360 uW
2. Low Speed: 0.5V, 100 kHz, 36 uW
3. Retention: 0.3V, 36 uW (all memory)
4. Sleep: Power gated, 0 uW

Transitions:
- Full Speed → Low Speed: 1 us (clock change)
- Low Speed → Retention: 10 ns (voltage change)
- Retention → Full Speed: 100 ns (voltage + clock)
- Any → Sleep: Immediate
- Sleep → Full Speed: 10 ms (reload program)

Optimization:
- Cache: Always retention (small power, fast wake-up)
- Main Memory: Retention when idle
- Storage: Sleep when not accessed
```

## 10. Summary

| Memory Level | Size | Speed | Power | Purpose |
|--------------|------|-------|-------|---------|
| Registers | 128 B | 1 cycle | Very Low | Temporary data |
| L1 Cache | 8 KB | 1-2 cycles | Low | Frequent data |
| Main Memory | 16 KB | 10-50 cycles | Medium | Working data |
| Storage | 64 KB | 1000+ cycles | Low | Program + data |

## 11. Exercises

1. Design a 4 KB direct-mapped cache with 16-byte blocks
2. Calculate AMAT for different cache sizes and associativities
3. Implement a sense amplifier in Verilog
4. Design a low-power cache bank switching scheme
5. Compare SRAM cell sizing for stability vs area
6. Create a memory map for a complete implant processor
7. Design a cache controller with write-through policy
8. Analyze power consumption for different cache configurations
