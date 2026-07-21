# Sequential Logic Circuits

## 1. Introduction to Sequential Logic

Sequential logic circuits are digital circuits whose outputs depend on both current inputs and the history of inputs (stored state). Unlike combinational logic, they contain memory elements that retain information between clock cycles.

### 1.1 Characteristics of Sequential Circuits

| Property | Description |
|----------|-------------|
| Memory | Contains flip-flops or latches for state storage |
| Feedback | Output fed back to affect next state |
| Timing | State changes synchronized by clock signal |
| State | Internal state determines output behavior |
| Examples | Registers, counters, FSMs, memory |

### 1.2 Classification

```
Sequential Circuits
├── Synchronous
│   ├── Clocked Flip-Flops
│   ├── Registers
│   ├── Counters
│   └── Synchronous FSMs
└── Asynchronous
    ├── Latches
    ├── Ripple Counters
    └── Asynchronous FSMs
```

### 1.3 General Model

```
Inputs → [Combinational Logic] → Outputs
              ↑     ↓
         [Memory] ← Current State
              ↑
         Clock Signal

Next State = F(Current State, Inputs)
Outputs = G(Current State, Inputs)  [Mealy]
       = G(Current State)           [Moore]
```

## 2. Latches (Level-Sensitive)

### 2.1 SR Latch (Set-Reset)

```
Cross-Coupled NOR Implementation:
Q   ┌────────┐
    │        │
    ├─┐   ┌──┤
S ──┤ ├───┤  ├─── Q'
    │ │   │  │
    └─┤ ──┘  │
      └──────┘
      R ──┘

Truth Table:
S | R | Q(t+1) | Q'(t+1) | Comment
--|---|--------|---------|--------
0 | 0 | Q(t)   | Q'(t)   | Hold
0 | 1 | 0      | 1       | Reset
1 | 0 | 1      | 0       | Set
1 | 1 | X      | X       | Invalid/Undefined

Characteristic Equation:
Q(t+1) = S + R'·Q(t)
Constraint: S·R = 0 (S and R cannot both be 1)
```

### 2.2 Gated SR Latch

```
Add enable gate to basic SR latch:

S ──[AND]─┐
           ├─── SR Latch ─── Q
Enable ──[AND]─┘             Q'

Truth Table:
EN | S | R | Q(t+1) | Comment
---|---|---|--------|--------
 0 | X | X | Q(t)   | Hold
 1 | 0 | 0 | Q(t)   | Hold
 1 | 0 | 1 | 0      | Reset
 1 | 1 | 0 | 1      | Set
 1 | 1 | 1 | X      | Invalid
```

### 2.3 Gated D Latch (Transparent Latch)

```
Fix invalid state by inverting D to R:

D ──[AND]─┐
           ├─── SR Latch ─── Q
D'──[AND]─┘─── Enable        Q'

Or using NAND implementation:
D ──[NAND]──┐
            ├─── Cross-coupled NANDs ─── Q
EN ──[NAND]─┘─── EN'                          Q'

Truth Table:
EN | D | Q(t+1) | Comment
---|---|--------|--------
 0 | X | Q(t)   | Hold (transparent when EN=1)
 1 | 0 | 0      | Reset
 1 | 1 | 1      | Set

Characteristics:
- Transparent: When EN=1, Q follows D
- Opaque: When EN=0, Q holds state
- Level-sensitive: Responds to input while enabled
```

### 2.4 Master-Slave Configuration

```
Eliminate transparency issue with master-slave:

D → [Master Latch] → [Slave Latch] → Q
         ↑                  ↑
      EN = CLK           EN = CLK'

Operation:
- CLK = 1: Master transparent, Slave holds
- CLK = 0: Master holds, Slave transparent
- Data transferred on CLK falling edge (negative-edge triggered)

This creates edge-triggered behavior from level-sensitive latches
```

## 3. Flip-Flops (Edge-Triggered)

### 3.1 D Flip-Flop (Data/Delay)

```
Most common flip-flop in synchronous design:

Symbol:
D ────┐
      │ DFF ├─── Q
CLK ──┘      ├─── Q'

Truth Table (positive edge-triggered):
CLK↑ | D | Q(t+1) | Comment
-----|---|--------|--------
  ↑  | 0 |   0    | Load 0
  ↑  | 1 |   1    | Load 1

Characteristic Equation:
Q(t+1) = D

Timing Diagram:
CLK: _|‾|_|‾|_|‾|_|‾|_
D:   ___|‾‾‾‾‾‾‾|_______
Q:   _____|‾‾‾‾‾‾‾|_____
        ↑
    Trigger edge

Implementation (Master-Slave):
D → [Master] → [Slave] → Q
CLK ─→ [Master]
CLK' ─→ [Slave]
```

### 3.2 JK Flip-Flop

```
General-purpose flip-flop:

Symbol:
J ────┐
K ────┤ JKFF ├─── Q
CLK ──┘       ├─── Q'

Truth Table:
CLK↑ | J | K | Q(t+1) | Comment
-----|---|---|--------|--------
  ↑  | 0 | 0 | Q(t)   | Hold
  ↑  | 0 | 1 |   0    | Reset
  ↑  | 1 | 0 |   1    | Set
  ↑  | 1 | 1 | Q'(t)  | Toggle

Characteristic Equation:
Q(t+1) = J·Q'(t) + K'·Q(t)

Note: When J=K=1, output toggles each clock edge
This solves SR latch's invalid state problem
```

### 3.3 T Flip-Flop (Toggle)

```
Special case of JK when J=K=T:

Symbol:
T ─────┐
       │ TFF ├─── Q
CLK ───┘      ├─── Q'

Truth Table:
CLK↑ | T | Q(t+1) | Comment
-----|---|--------|--------
  ↑  | 0 | Q(t)   | Hold
  ↑  | 1 | Q'(t)  | Toggle

Characteristic Equation:
Q(t+1) = T ⊕ Q(t)

Application: Frequency divider
- Input clock frequency: f
- Output frequency: f/2
```

### 3.4 SR Flip-Flop

```
Edge-triggered version of SR latch:

Symbol:
S ─────┐
R ─────┤ SRFF ├─── Q
CLK ───┘      ├─── Q'

Truth Table:
CLK↑ | S | R | Q(t+1) | Comment
-----|---|---|--------|--------
  ↑  | 0 | 0 | Q(t)   | Hold
  ↑  | 0 | 1 |   0    | Reset
  ↑  | 1 | 0 |   1    | Set
  ↑  | 1 | 1 | X      | Invalid (avoid in design)
```

### 3.5 Flip-Flop Comparison

| Type | Inputs | Function | Characteristic Equation | Best Use |
|------|--------|----------|------------------------|----------|
| D | D | Data storage | Q(t+1) = D | Registers, data paths |
| JK | J, K | General purpose | Q(t+1) = JQ' + K'Q | Counters, FSMs |
| T | T | Toggle control | Q(t+1) = T ⊕ Q | Frequency dividers |
| SR | S, R | Set/Reset | Q(t+1) = S + R'Q | Simple state storage |

## 4. Flip-Flop Timing Parameters

### 4.1 Setup and Hold Times

```
Setup Time (t_setup):
- Minimum time data must be stable BEFORE clock edge
- Violation causes metastability

Hold Time (t_hold):
- Minimum time data must be stable AFTER clock edge
- Violation causes data corruption

Timing Diagram:
           ← t_setup → ↑ ← t_hold →
D:    ___XXXXXXXXXXXXXXXXXXXXXXXXXX___
           ← stable →  CLK edge
CLK: _____|‾‾‾|_______

D must be stable during entire setup + hold window
```

### 4.2 Clock-to-Q Delay

```
Clock-to-Q Delay (t_cq):
- Time from clock edge to valid output
- Two variants:
  - t_pcq (propagation): Maximum delay
  - t_ccq (contamination): Minimum delay

Timing:
CLK: _____|‾‾‾|_____
              ↓ t_cq
Q:   _________|‾‾‾‾‾‾‾

Critical for determining maximum clock frequency
```

### 4.3 Clock Skew and Jitter

```
Clock Skew (t_skew):
- Difference in clock arrival times at different flip-flops
- t_skew = t_clk2 - t_clk1

Clock Jitter (t_jitter):
- Variation in clock period from cycle to cycle
- Random fluctuation in clock edge timing

Impact on timing:
T_clk ≥ t_pcq + t_pd_logic + t_setup + t_skew

If skew is positive (late clock at capture FF):
- Helps hold time, hurts setup time
If skew is negative (early clock at capture FF):
- Helps setup time, hurts hold time
```

### 4.4 Timing Budget Example

```
Given:
- t_pcq = 0.5 ns
- t_setup = 0.3 ns
- t_hold = 0.2 ns
- t_ccq = 0.2 ns
- t_skew = 0.1 ns

Minimum clock period:
T_clk ≥ t_pcq + t_logic + t_setup + t_skew
T_clk ≥ 0.5 + t_logic + 0.3 + 0.1
T_clk ≥ 0.9 + t_logic

For T_clk = 2 ns:
t_logic ≤ 2 - 0.9 = 1.1 ns

Maximum logic depth (assuming 0.1 ns/gate):
≤ 11 gates in critical path

Hold time check:
t_ccq + t_logic_min ≥ t_hold
0.2 + t_logic_min ≥ 0.2
t_logic_min ≥ 0  (always satisfied)
```

## 5. Registers

### 5.1 Basic Register (Parallel-In Parallel-Out)

```
8-bit Register using D Flip-Flops:

D0 ──→[DFF]──→ Q0 (bit 0)
D1 ──→[DFF]──→ Q1 (bit 1)
D2 ──→[DFF]──→ Q2 (bit 2)
D3 ──→[DFF]──→ Q3 (bit 3)
D4 ──→[DFF]──→ Q4 (bit 4)
D5 ──→[DFF]──→ Q5 (bit 5)
D6 ──→[DFF]──→ Q6 (bit 6)
D7 ──→[DFF]──→ Q7 (bit 7)
      ↑
    CLK (all FFs share same clock)

All DFFs triggered simultaneously → parallel load
```

### 5.2 Register with Enable

```
Add enable signal to control loading:

D ──[AND]──→[DFF]──→ Q
EN ──[AND]─┘

Behavior:
- EN = 1: Load new data (Q = D on clock edge)
- EN = 0: Hold current value (Q unchanged)

Verilog Implementation:
always @(posedge clk) begin
    if (enable)
        Q <= D;
end
```

### 5.3 Register with Clear

```
Asynchronous Clear (overrides everything):

D ──────→[DFF]──→ Q
CLR ──→[CLR]─┘

CLR = 1: Q → 0 immediately (regardless of clock)
CLR = 0: Normal operation

Synchronous Clear (synchronized to clock):

D ──[MUX]──→[DFF]──→ Q
CLR ──→[MUX]─┘

On clock edge:
- CLR = 1: Q → 0
- CLR = 0: Q → D
```

### 5.4 Shift Register

```
Serial-In Serial-Out (SISO) 4-bit:

Data In →[DFF0]→[DFF1]→[DFF2]→[DFF3]→ Data Out
           CLK     CLK     CLK     CLK

Operation (shift right):
Cycle 0: D3 D2 D1 D0 = 0000
Cycle 1: 1  0  0  0  (data in = 1)
Cycle 2: 0  1  0  0  (data in = 0)
Cycle 3: 1  0  1  0  (data in = 1)
Cycle 4: 0  1  0  1  (data in = 0)

Serial-In Parallel-Out (SIPO):
Data In →[DFF0]→[DFF1]→[DFF2]→[DFF3]
           ↓       ↓       ↓       ↓
          Q0      Q1      Q2      Q3 (parallel output)

Parallel-In Serial-Out (PISO):
P0 →[MUX]→[DFF0]→[MUX]→[DFF1]→[MUX]→[DFF2]→[MUX]→[DFF3]→ Serial Out
P1 ─┘                  └P2                   └P3
      SEL                SEL                  SEL
      (shift/load control)

Parallel-In Parallel-Out (PIPO):
P0 →[DFF0]→ Q0
P1 →[DFF1]→ Q1
P2 →[DFF2]→ Q2
P3 →[DFF3]→ Q3
```

### 5.5 Barrel Shifter

```
4-bit Barrel Shifter:
Can rotate/shift by any amount in one cycle

Inputs: D[3:0], S[1:0] (shift amount)
Output: Y[3:0]

Truth Table (rotate left):
S1 | S0 | Y3 | Y2 | Y1 | Y0
---|----|----|----|----|----
 0 |  0 | D3 | D2 | D1 | D0  (no shift)
 0 |  1 | D2 | D1 | D0 | D3  (rotate 1)
 1 |  0 | D1 | D0 | D3 | D2  (rotate 2)
 1 |  1 | D0 | D3 | D2 | D1  (rotate 3)

Implementation using MUX tree:
Y0 = S1'·S0'·D0 + S1'·S0·D1 + S1·S0'·D2 + S1·S0·D3
Y1 = S1'·S0'·D1 + S1'·S0·D2 + S1·S0'·D3 + S1·S0·D0
Y2 = S1'·S0'·D2 + S1'·S0·D3 + S1·S0'·D0 + S1·S0·D1
Y3 = S1'·S0'·D3 + S1'·S0·D0 + S1·S0'·D1 + S1·S0·D2
```

## 6. Counters

### 6.1 Ripple (Asynchronous) Counter

```
4-bit Binary Ripple Counter:

CLK ──→[TFF0]──→ Q0 (LSB)
           ↓
CLK ──→[TFF1]──→ Q1
           ↓
CLK ──→[TFF2]──→ Q2
           ↓
CLK ──→[TFF3]──→ Q3 (MSB)

Each TFF toggles on negative edge of previous output
Total count sequence: 0→1→2→3→...→15→0

Timing Diagram (3-bit):
CLK: _|‾|_|‾|_|‾|_|‾|_|‾|_|‾|_|‾|_|‾|_
Q0:  __|‾‾‾|___|‾‾‾|___|‾‾‾|___|‾‾‾|___
Q1:  ______|‾‾‾‾‾‾‾‾|_________|‾‾‾‾‾‾‾‾
Q2:  ________________|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Count: 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7

Delay accumulation:
- Q0 toggles after CLK delay
- Q1 toggles after Q0 delay
- Q2 toggles after Q1 delay
- Total delay for N-bit: N × T_FF
```

### 6.2 Synchronous Binary Counter

```
4-bit Synchronous Counter using JK Flip-Flops:

All FFs share same clock
J0 = K0 = 1
J1 = K1 = Q0
J2 = K2 = Q0·Q1
J3 = K3 = Q0·Q1·Q2

CLK ───┬───┬───┬───┬
       ↓   ↓   ↓   ↓
      [FF0][FF1][FF2][FF3]
       ↓   ↓   ↓   ↓
       Q0  Q1  Q2  Q3

Carry chain: G_i = Q0·Q1·...·Q(i-1)

Advantages:
- All bits change simultaneously
- No ripple delay
- Higher maximum frequency

Timing:
CLK: _|‾|_|‾|_|‾|_|‾|_
Q0:  __|‾‾‾|___|‾‾‾|___
Q1:  __________|‾‾‾|___  (both change at same time!)
Q2:  __________________|‾‾‾|___
```

### 6.3 Up/Down Counter

```
4-bit Up/Down Counter:
Control signal UP/DOWN determines count direction

When UP = 1: Count up (0→1→2→...→15→0)
When DOWN = 1: Count down (15→14→13→...→0→15)

Implementation:
- For up counting: Use carry from LSB to MSB
- For down counting: Use borrow from LSB to MSB

Truth Table (2-bit example):
UP | DOWN | Q1 | Q0 | Next Q1 | Next Q0
---|------|----|----|---------|--------
 1 |   0  | 0  | 0  |    0    |    1
 1 |   0  | 0  | 1  |    1    |    0
 1 |   0  | 1  | 0  |    1    |    1
 1 |   0  | 1  | 1  |    0    |    0
 0 |   1  | 0  | 0  |    1    |    1
 0 |   1  | 0  | 1  |    0    |    0
 0 |   1  | 1  | 0  |    0    |    1
 0 |   1  | 1  | 1  |    1    |    0
```

### 6.4 Ring Counter

```
4-bit Ring Counter:
Shift register with output fed back to input

Q3 →[DFF0]→ Q0 →[DFF1]→ Q1 →[DFF2]→ Q2 →[DFF3]→ Q3
                     ↑                           |
                     └───────────────────────────┘

Initialization: Q = 1000 (one-hot)
Sequence: 1000 → 0100 → 0010 → 0001 → 1000 → ...

Applications:
- Sequence generation
- State machine encoding
- Clock division

Johnson Counter (Twisted Ring):
Feedback inverted: Q3' → D0

Initialization: Q = 0000
Sequence: 0000 → 1000 → 1100 → 1110 → 1111 → 0111 → 0011 → 0001 → 0000

4-bit Johnson counter has 8 states (2×N for N bits)
```

### 6.5 Counter Comparison

| Counter Type | Speed | Power | Complexity | Application |
|--------------|-------|-------|------------|-------------|
| Ripple | Low | Low | Simple | Low-speed counting |
| Synchronous | High | Medium | Medium | High-speed systems |
| Ring | High | Low | Simple | Sequence generation |
| Johnson | High | Low | Simple | Phase generation |
| Programmable | Medium | Medium | Complex | Flexible counting |

## 7. State Registers

### 7.1 Multi-Bit State Register

```
8-bit State Register with control:

       D[7:0]
        |
    [8-bit MUX]
    ↑    ↓    ↑
   0   [REG]  1
    ↑    ↓
  CLR  Q[7:0] (current state)
       ↓
    [Logic] → Next State

Control inputs:
- Mode[1:0]:
  00: Hold (no change)
  01: Parallel load
  10: Shift right
  11: Shift left
```

### 7.2 Pipeline Register

```
Pipeline stages with registers:

Stage 1     Stage 2     Stage 3
┌───────┐   ┌───────┐   ┌───────┐
│Logic  │   │Logic  │   │Logic  │
│Block 1│   │Block 2│   │Block 3│
└───┬───┘   └───┬───┘   └───┬───┘
    ↓           ↓           ↓
 [REG]       [REG]       [REG]
    ↓           ↓           ↓

Benefits:
- Divide long combinational path into shorter segments
- Increase clock frequency
- Trade latency for throughput
- Isolate timing domains
```

## 8. Metastability

### 8.1 Metastable State

```
When setup/hold time is violated, flip-flop enters metastable state:

Normal: Q = 0 or Q = 1
Metastable: Q oscillates or stays at intermediate voltage

Resolution time (T_res) for metastability:
P(metastable) = e^(-T_res / τ)

Where:
- τ = flip-flop time constant (technology dependent)
- T_res = time allowed for resolution

To achieve error rate < 10^-9:
T_res > τ × ln(10^9) ≈ 20.7τ
```

### 8.2 Synchronizer Design

```
2-Stage Synchronizer:

Asynchronous Input → [FF1] → [FF2] → Synchronized Output
                     CLK      CLK

Stage 1 catches metastable input
Stage 2 gives full clock period for resolution

MTBF (Mean Time Between Failures):
MTBF = (e^(T_res/τ)) / (f_clk × f_input × T_w)

Where:
- T_res = clock period - t_setup - t_cq
- τ ≈ 0.3-1 ns (technology dependent)
- f_clk = clock frequency
- f_input = input transition frequency
- T_w = pulse width of metastable event

Example (typical 65nm):
τ = 0.5 ns, T_res = 2 ns, f_clk = 100 MHz, f_input = 10 MHz
MTBF = e^(2/0.5) / (100e6 × 10e6 × 0.5e-9)
MTBF = e^4 / (50) ≈ 1.1 seconds

With 3-stage synchronizer:
MTBF ≈ e^4 × e^(2/0.5) / (100e6 × 10e6 × 0.5e-9) ≈ 54 years
```

### 8.3 MTBF Calculations

| Synchronizer Stages | τ (ns) | T_res (ns) | MTBF (65nm, 100MHz) |
|--------------------:|-------:|-----------:|-------------------:|
| 2 | 0.5 | 2.0 | 1.1 seconds |
| 2 | 0.5 | 3.0 | 403 seconds |
| 3 | 0.5 | 2.0 | 54 years |
| 3 | 0.5 | 3.0 | 2.1 × 10^8 years |
| 4 | 0.5 | 2.0 | 2.8 × 10^9 years |

## 9. Clock Distribution

### 9.1 Clock Tree Structures

```
H-Tree (Balanced):
         CLK
          |
    ┌─────┴─────┐
    |           |
  ┌─┴─┐     ┌─┴─┐
  |   |     |   |
 FF  FF    FF  FF

Buffer Tree:
         CLK
          |
       [BUF]
      /     \
   [BUF]   [BUF]
   / \     / \
  FF  FF  FF  FF

Clock Mesh:
CLK ─┬───────┬───────┬───────┬
     │       │       │       │
    FF      FF      FF      FF
     │       │       │       │
CLK ─┴───────┴───────┴───────┴

Best for: High-performance designs
Reduces skew but increases power
```

### 9.2 Clock Skew Budget

```
Typical clock skew budget (65nm):

Component           | Budget
-------------------|-------
Source skew         | 50 ps
Buffer mismatch     | 30 ps
Wire mismatch       | 40 ps
Load variation      | 20 ps
Temperature         | 10 ps
Total (RSS)         | ~73 ps

For 1 GHz clock (T = 1000 ps):
Skew/T = 73/1000 = 7.3% (acceptable)

For 5 GHz clock (T = 200 ps):
Skew/T = 73/200 = 36.5% (problematic)
```

## 10. Verilog Implementation

### 10.1 Flip-Flop Library

```verilog
// D Flip-Flop with async reset
module dff_async_reset (
    input  wire clk,
    input  wire rst_n,  // Active-low reset
    input  wire D,
    output reg  Q
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            Q <= 1'b0;
        else
            Q <= D;
    end

endmodule

// D Flip-Flop with sync reset and enable
module dff_sync_reset_enable (
    input  wire clk,
    input  wire rst_n,
    input  wire enable,
    input  wire D,
    output reg  Q
);

    always @(posedge clk) begin
        if (!rst_n)
            Q <= 1'b0;
        else if (enable)
            Q <= D;
    end

endmodule

// JK Flip-Flop
module jkff (
    input  wire clk,
    input  wire J,
    input  wire K,
    output reg  Q
);

    always @(posedge clk) begin
        case ({J, K})
            2'b00: Q <= Q;      // Hold
            2'b01: Q <= 1'b0;   // Reset
            2'b10: Q <= 1'b1;   // Set
            2'b11: Q <= ~Q;     // Toggle
        endcase
    end

endmodule

// T Flip-Flop
module tff (
    input  wire clk,
    input  wire rst_n,
    input  wire T,
    output reg  Q
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            Q <= 1'b0;
        else if (T)
            Q <= ~Q;
    end

endmodule
```

### 10.2 Register Implementations

```verilog
// 8-bit register with enable
module register_8bit (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        enable,
    input  wire [7:0]  D,
    output reg  [7:0]  Q
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            Q <= 8'b0;
        else if (enable)
            Q <= D;
    end

endmodule

// 8-bit shift register with parallel load
module shift_reg_8bit (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        shift_en,
    input  wire        load_en,
    input  wire        serial_in,
    input  wire [7:0]  parallel_in,
    output wire [7:0]  parallel_out,
    output wire        serial_out
);

    reg [7:0] shift_reg;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            shift_reg <= 8'b0;
        else if (load_en)
            shift_reg <= parallel_in;
        else if (shift_en)
            shift_reg <= {serial_in, shift_reg[7:1]};
    end

    assign parallel_out = shift_reg;
    assign serial_out = shift_reg[0];

endmodule
```

### 10.3 Counter Implementations

```verilog
// 4-bit synchronous binary counter
module counter_4bit (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       enable,
    output reg [3:0]  count
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            count <= 4'b0;
        else if (enable)
            count <= count + 1'b1;
    end

endmodule

// 4-bit up/down counter
module counter_updown_4bit (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       up_down,  // 1=up, 0=down
    output reg [3:0]  count
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            count <= 4'b0;
        else if (up_down)
            count <= count + 1'b1;
        else
            count <= count - 1'b1;
    end

endmodule

// 4-bit Johnson counter
module johnson_counter_4bit (
    input  wire       clk,
    input  wire       rst_n,
    output reg [3:0]  Q
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            Q <= 4'b0;
        else
            Q <= {~Q[0], Q[3:1]};
    end

endmodule
```

## 11. Applications in Medical Implant Design

### 11.1 Low-Power State Retention

```
Power Gating with State Retention:
- Turn off clock to unused blocks
- Keep minimal state in retention flip-flops
- Use header/footer sleep transistors

Retention Flip-Flop Design:
┌─────────────────────────────┐
│  Main Flip-Flop (power-gated) │
│  ┌─────┐                    │
│D─┤     ├──→ Q_normal        │
│  │ DFF │                    │
│  └─────┘                    │
│      ↓ (power-gate control) │
│  ┌─────┐                    │
│  │ Ret │──→ Q_retention     │
│  │ FF  │ (always powered)   │
│  └─────┘                    │
└─────────────────────────────┘

Power savings:
- Active: 100% (full operation)
- Sleep: 5-10% (retention only)
- Off: 0% (no state kept)
```

### 11.2 Duty-Cycled Operation

```
Implant Operation Modes:
1. Active Mode: Full clock, all registers active
2. Monitor Mode: Reduced clock, only sensor interface
3. Sleep Mode: Clock gated, state retained
4. Emergency Mode: Minimum logic, watchdog active

Duty Cycle Example:
Active:  10 ms every 100 ms = 10% duty cycle
Average Power = 0.1 × P_active + 0.9 × P_sleep
             = 0.1 × 100 μW + 0.9 × 1 μW
             = 10.9 μW (vs 100 μW continuous)
```

## 12. Summary

| Element | Function | Key Parameter | Typical Use |
|---------|----------|---------------|-------------|
| D Latch | Level-sensitive storage | Enable time | Transparent data capture |
| D Flip-Flop | Edge-triggered storage | Setup/Hold time | Registers, FSMs |
| JK Flip-Flop | Toggle/Hold storage | J,K inputs | Counters |
| T Flip-Flop | Toggle storage | Toggle input | Frequency dividers |
| Register | Multi-bit storage | Width, enable | Data path |
| Shift Register | Serial/Parallel conversion | Shift direction | Communication |
| Counter | Sequence generation | Modulus, direction | Timing, control |
| Synchronizer | Clock domain crossing | MTBF | Asynchronous interfaces |

## 13. Exercises

1. Design a 4-bit synchronous up counter using JK flip-flops
2. Implement a 8-bit shift register with serial/parallel I/O
3. Calculate MTBF for a 2-stage synchronizer at 500 MHz with τ = 0.4 ns
4. Design a 4-bit ring counter and a 4-bit Johnson counter; compare state sequences
5. Create a timing budget for a 3-stage pipeline at 2 GHz
6. Implement a BCD counter (counts 0-9 then resets)
7. Design a clock divider that generates 1 Hz from 50 MHz input
8. Analyze metastability probability for a 3-stage synchronizer with T_res = 1.5 ns
