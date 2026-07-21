# Finite State Machines (FSMs)

## 1. Introduction to Finite State Machines

A Finite State Machine (FSM) is a mathematical model of computation that can be in exactly one of a finite number of states at any given time. FSMs are fundamental to digital design, control systems, and sequential circuit design.

### 1.1 Formal Definition

```
FSM = (S, S₀, Σ, Ω, δ, λ)

Where:
S    = Finite set of states
S₀   = Initial state (S₀ ∈ S)
Σ    = Input alphabet (finite set of inputs)
Ω    = Output alphabet (finite set of outputs)
δ    = State transition function: S × Σ → S
λ    = Output function: S → Ω or S × Σ → Ω
```

### 1.2 Types of FSMs

```
FSM Classification:
├── By Output Function:
│   ├── Moore Machine: Output depends only on current state
│   └── Mealy Machine: Output depends on current state AND inputs
├── By State Encoding:
│   ├── Binary Encoded
│   ├── One-Hot Encoded
│   └── Gray Code Encoded
└── By Implementation:
    ├── Direct Implementation
    └── ROM-Based Implementation
```

### 1.3 Moore vs Mealy Comparison

| Property | Moore Machine | Mealy Machine |
|----------|--------------|---------------|
| Output depends on | Current state only | Current state + inputs |
| Output function | λ(S) | λ(S, Σ) |
| Output timing | Changes after state change | Changes with input change |
| Glitch prone | Less prone | More prone (input glitches) |
| State count | Generally more states | Generally fewer states |
| Speed | One clock cycle latency | Immediate response |
| Example | Traffic light controller | Vending machine |

## 2. Moore Machine

### 2.1 Definition

```
Moore Machine M = (S, S₀, Σ, Ω, δ, λ)

Output: λ: S → Ω
Each state has exactly one output value

State Diagram Convention:
┌──────┐
│      │─── Output
│State │
│      │
└──┬───┘
   │
   ↓ (Input)
```

### 2.2 Example: Traffic Light Controller

```
States: S0 (Red), S1 (Green), S2 (Yellow)
Inputs: Timer_expired (T)
Outputs: Light[2:0] (R,G,Y)

State Diagram:
                    T=1
         ┌─────────────────────┐
         │                     │
    ┌────┴────┐          ┌─────┴────┐
    │  S0     │          │   S1     │
    │ Red=1   │ T=1      │ Green=1  │ T=1
    │ Grn=0   ├─────────→│ Grn=1    ├─────────┐
    │ Yel=0   │          │ Yel=0    │          │
    └─────────┘          └──────────┘          ↓
         ↑                                 ┌────┴────┐
         └─────────────────────────────────│   S2    │
                T=1                        │ Red=0   │
                                           │ Grn=0   │
                                           │ Yel=1   │
                                           └─────────┘

State Table:
Present State | Input T | Next State | Output (R,G,Y)
-------------|----------|------------|----------------
    S0       |    0     |     S0     |    (1,0,0)
    S0       |    1     |     S1     |    (1,0,0)
    S1       |    0     |     S1     |    (0,1,0)
    S1       |    1     |     S2     |    (0,1,0)
    S2       |    0     |     S2     |    (0,0,1)
    S2       |    1     |     S0     |    (0,0,1)

State Encoding (Binary):
S0 = 00, S1 = 01, S2 = 10

Encoded State Table:
Present State (Q1Q0) | Input T | Next State (D1D0) | Output (R,G,Y)
--------------------|----------|-------------------|----------------
        00          |    0     |        00         |    (1,0,0)
        00          |    1     |        01         |    (1,0,0)
        01          |    0     |        01         |    (0,1,0)
        01          |    1     |        10         |    (0,1,0)
        10          |    0     |        10         |    (0,0,1)
        10          |    1     |        00         |    (0,0,1)
```

### 2.3 Moore Machine Timing

```
CLK:     _|‾|_|‾|_|‾|_|‾|_|‾|_
State:   S0──S1──S2──S0──S1──S2
Output:  ───R───G───Y───R───G───Y───

Key: Output changes ONE clock cycle after state change
     Output is registered (synchronized to clock)
```

## 3. Mealy Machine

### 3.1 Definition

```
Mealy Machine M = (S, S₀, Σ, Ω, δ, λ)

Output: λ: S × Σ → Ω
Output depends on both state AND current inputs

State Diagram Convention:
┌──────┐
│      │
│State │
│      │
└──┬───┘
   │
   ├─── Input / Output ───→ Next State
```

### 3.2 Example: Vending Machine

```
States: S0 (Ready), S1 (5c inserted), S2 (10c inserted), S3 (15c inserted)
Inputs: Nickel (N), Dime (D), Quarter (Q)
Outputs: Dispense, Return_Nickel, Return_Dime

State Diagram:
                    N / (0,0,0)
         ┌────────────────────────────┐
         │                            │
    ┌────┴────┐                  ┌─────┴────┐
    │   S0    │                  │   S1     │
    │ Ready   │ D / (0,0,0)     │  5c      │ D / (0,0,0)
    └─────────┼────────────────→ │          ├─────────────┐
              │                  └────┬─────┘             │
              │ Q / (1,0,1)           │ N / (0,0,0)      │ D / (1,0,0)
              ↓                      ↓                   ↓
         ┌─────────┐            ┌─────────┐         ┌─────────┐
         │   S4    │            │   S2    │         │   S3    │
         │ Dispense│            │  10c    │         │  15c    │
         └─────────┘            └────┬────┘         └────┬────┘
                                     │ N / (0,0,0)        │ N / (1,0,0)
                                     ↓                    ↓
                                ┌─────────┐         ┌─────────┐
                                │   S3    │         │   S4    │
                                │  15c    │         │ Dispense│
                                └────┬────┘         └─────────┘
                                     │ N / (1,0,0)
                                     ↓
                                ┌─────────┐
                                │   S4    │
                                │ Dispense│
                                └─────────┘

Output format: (Dispense, Return_Nickel, Return_Dime)

State Table:
Present State | Input | Next State | Output (D,RN,RD)
-------------|-------|------------|------------------
    S0       |   N   |     S1     |      (0,0,0)
    S0       |   D   |     S2     |      (0,0,0)
    S0       |   Q   |     S4     |      (1,0,1)
    S1       |   N   |     S2     |      (0,0,0)
    S1       |   D   |     S3     |      (0,0,0)
    S1       |   Q   |     S4     |      (1,0,0)
    S2       |   N   |     S3     |      (0,0,0)
    S2       |   D   |     S4     |      (1,0,0)
    S2       |   Q   |     S4     |      (1,0,1)
    S3       |   N   |     S4     |      (1,0,0)
    S3       |   D   |     S4     |      (1,0,0)
    S3       |   Q   |     S4     |      (1,0,1)
```

### 3.3 Mealy Machine Timing

```
CLK:     _|‾|_|‾|_|‾|_|‾|_|‾|_
Input:   ____|‾‾‾‾‾‾‾|_________
State:   S0──S0──S1──S1──S2
Output:  ____|‾‾‾‾‾|____________

Key: Output can change DURING clock cycle when input changes
     Output is combinational (may have glitches)
```

## 4. FSM Design Methodology

### 4.1 Design Flow

```
Step 1: Problem Specification
    ↓
Step 2: State Diagram Drawing
    ↓
Step 3: State Table Creation
    ↓
Step 4: State Minimization
    ↓
Step 5: State Encoding
    ↓
Step 6: Next State/Output Logic Derivation
    ↓
Step 7: Logic Minimization
    ↓
Step 8: Circuit Implementation
    ↓
Step 9: Verification
```

### 4.2 State Diagram to State Table

```
Example: 3-bit Up/Down Counter with Enable

States: S0(000), S1(001), S2(010), S3(011), S4(100), S5(101), S6(110), S7(111)
Inputs: Enable (E), Up/Down (UD)
Outputs: Count[2:0]

Complete State Table:
PS   | E | UD | NS   | Output
-----|---|----|----|----------
S0   | 0 |  X | S0   | 000
S0   | 1 |  1 | S1   | 000
S0   | 1 |  0 | S7   | 000
S1   | 0 |  X | S1   | 001
S1   | 1 |  1 | S2   | 001
S1   | 1 |  0 | S0   | 001
S2   | 0 |  X | S2   | 010
S2   | 1 |  1 | S3   | 010
S2   | 1 |  0 | S1   | 010
S3   | 0 |  X | S3   | 011
S3   | 1 |  1 | S4   | 011
S3   | 1 |  0 | S2   | 011
S4   | 0 |  X | S4   | 100
S4   | 1 |  1 | S5   | 100
S4   | 1 |  0 | S3   | 100
S5   | 0 |  X | S5   | 101
S5   | 1 |  1 | S6   | 101
S5   | 1 |  0 | S4   | 101
S6   | 0 |  X | S6   | 110
S6   | 1 |  1 | S7   | 110
S6   | 1 |  0 | S5   | 110
S7   | 0 |  X | S7   | 111
S7   | 1 |  1 | S0   | 111
S7   | 1 |  0 | S6   | 111
```

## 5. State Minimization

### 5.1 Equivalent States

```
Two states are equivalent if:
1. They produce the same output for all inputs
2. They have the same next states for all inputs (or equivalent next states)

Formal Definition:
State p ≡ State q if:
For all inputs i:
  λ(p, i) = λ(q, i)  AND
  δ(p, i) ≡ δ(q, i)
```

### 5.2 Implication Table Method

```
Example State Table:
Present State | Input 0 | Input 1 | Output
--------------|---------|---------|-------
    A         |    B    |    C    |   0
    B         |    B    |    D    |   0
    C         |    B    |    E    |   0
    D         |    B    |    E    |   1
    E         |    B    |    E    |   1

Step 1: Check outputs (states with different outputs cannot be equivalent)
D and E have output 1, others have 0

Step 2: Build implication table
Compare each pair of states:
A-B: Check δ(A,0)=B vs δ(B,0)=B (match), δ(A,1)=C vs δ(B,1)=D → need C≡D
A-C: Check δ(A,0)=B vs δ(C,0)=B (match), δ(A,1)=C vs δ(C,1)=E → need C≡E
A-D: Outputs differ → NOT equivalent
A-E: Outputs differ → NOT equivalent
B-C: Check δ(B,0)=B vs δ(C,0)=B (match), δ(B,1)=D vs δ(C,1)=E → need D≡E
B-D: Outputs differ → NOT equivalent
B-E: Outputs differ → NOT equivalent
C-D: Outputs differ → NOT equivalent
C-E: Outputs differ → NOT equivalent
D-E: Check δ(D,0)=B vs δ(E,0)=B (match), δ(D,1)=E vs δ(E,1)=E (match) → EQUIVALENT

Step 3: Check implications
D≡E is confirmed (outputs match, next states match)
C≡E requires D≡E (now true) → C≡E
C≡D requires D≡E (now true) → C≡D
A≡C requires C≡E (now true) → A≡C

Step 4: Final equivalence classes
{A, C} are equivalent
{D, E} are equivalent

Minimized State Table:
Present State | Input 0 | Input 1 | Output
--------------|---------|---------|-------
    A'        |    B    |    A'   |   0
    B         |    B    |    D'   |   0
    D'        |    B    |    D'   |   1

Reduced from 5 states to 3 states!
```

### 5.3 Partition Method

```
Initial Partition (by output):
P0 = {A,B,C}, {D,E}

Iteration 1:
For group {A,B,C}:
  A: δ(A,0)=B∈{A,B,C}, δ(A,1)=C∈{A,B,C}
  B: δ(B,0)=B∈{A,B,C}, δ(B,1)=D∈{D,E}
  C: δ(C,0)=B∈{A,B,C}, δ(C,1)=E∈{D,E}

  A and B have different next-state groups for input 1
  Split: {A}, {B,C}

For group {D,E}:
  D: δ(D,0)=B∈{A,B,C}, δ(D,1)=E∈{D,E}
  E: δ(E,0)=B∈{A,B,C}, δ(E,1)=E∈{D,E}
  Same behavior → {D,E} stays together

P1 = {A}, {B,C}, {D,E}

Iteration 2:
For group {B,C}:
  B: δ(B,1)=D∈{D,E}
  C: δ(C,1)=E∈{D,E}
  Same group → no split needed

No more partitions possible
Final: {A}, {B,C}, {D,E}
```

## 6. State Encoding

### 6.1 Binary Encoding

```
For N states, need ⌈log₂(N)⌉ flip-flops

Example: 5 states (A,B,C,D,E) → 3 flip-flops

State | Encoding (Q2Q1Q0)
------|------------------
  A   |      000
  B   |      001
  C   |      010
  D   |      011
  E   |      100

Unused states: 101, 110, 111 (can be "don't cares" or error states)

Advantages:
- Minimum number of flip-flops
- Simple encoding

Disadvantages:
- Complex next-state logic
- May have many bit changes between states
```

### 6.2 One-Hot Encoding

```
Each state has its own flip-flop (one-hot)
For N states, need N flip-flops

Example: 5 states (A,B,C,D,E) → 5 flip-flops

State | Encoding (Q4Q3Q2Q1Q0)
------|----------------------
  A   |      00001
  B   |      00010
  C   |      00100
  D   |      01000
  E   |      10000

Advantages:
- Simple next-state and output logic
- Speed: fewer levels of logic
- Easy to debug (state is directly visible)
- No unused states to worry about

Disadvantages:
- More flip-flops than binary encoding
- Higher power consumption (more storage elements)
```

### 6.3 Gray Code Encoding

```
Only one bit changes between adjacent states

Example: 5 states using Gray code (need 3 flip-flops)

State | Encoding (Q2Q1Q0)
------|------------------
  A   |      000
  B   |      001
  C   |      011
  D   |      010
  E   |      110

Advantages:
- Minimal switching activity (power savings)
- Reduced glitching

Disadvantages:
- Complex encoding logic
- Not suitable for all FSM structures
```

### 6.4 Encoding Comparison

| Encoding | FF Count | Logic Complexity | Power | Speed | Debug |
|----------|----------|-----------------|-------|-------|-------|
| Binary | ⌈log₂(N)⌉ | High | Low | Medium | Hard |
| One-Hot | N | Low | High | High | Easy |
| Gray | ⌈log₂(N)⌉ | Medium | Low | Medium | Medium |

### 6.5 Optimal State Assignment

```
Heuristics for good state encoding:

1. Output-based encoding:
   - States with same output should have similar encodings
   - Reduces output logic complexity

2. Transition-based encoding:
   - Frequently transitioning states should be adjacent
   - Minimizes switching activity

3. Input-based encoding:
   - States sharing next states should be close
   - Reduces next-state logic

Example Optimization:
Before: States A,B,C,D with arbitrary encoding
After: Reassign to minimize XOR gates between adjacent states
```

## 7. Next-State and Output Logic

### 7.1 K-Map for Next-State Logic

```
3-bit Counter Example:
States: S0(000), S1(001), S2(010), S3(011), S4(100), S5(101), S6(110), S7(111)
Input: Up/Down (UD)

Next State Q0*:
Q2Q1\Q0  0    1
00      Q0    Q0'
01      Q0    Q0'
10      Q0    Q0'
11      Q0    Q0'

Q0* = Q0 ⊕ UD (toggle when counting up)

Next State Q1*:
Q2Q0\Q1  0    1
00      Q1    Q1'
01      Q1'   Q1
10      Q1    Q1'
11      Q1'   Q1

Q1* = Q1 ⊕ (UD·Q0 + UD'·Q0')

Next State Q2*:
Q1Q0\Q2  0    1
00      Q2    Q2'
01      Q2    Q2'
10      Q2'   Q2
11      Q2'   Q2

Q2* = Q2 ⊕ (UD·Q1·Q0 + UD'·Q1'·Q0')
```

### 7.2 Logic Minimization

```
After K-Map minimization, implement using:

Sum of Products (SOP):
Q0* = UD'·Q0' + UD·Q0 = Q0 ⊕ UD

Product of Sums (POS):
Q0* = (UD + Q0') · (UD' + Q0)

Gate count comparison:
SOP: 2 gates (XOR can be implemented as AND-OR-NOT)
POS: 2 gates
XOR: 1 gate (if available in library)
```

## 8. FSM Implementation Styles

### 8.1 Two-Process FSM

```verilog
// Process 1: Sequential state register
// Process 2: Combinational next-state and output logic

module fsm_twoprocess (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       start,
    input  wire       done,
    output reg        busy,
    output reg [7:0]  data_out
);

    // State encoding
    localparam [1:0] IDLE = 2'b00,
                     PROC = 2'b01,
                     DONE = 2'b10;

    reg [1:0] state, next_state;

    // Process 1: State register
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            state <= IDLE;
        else
            state <= next_state;
    end

    // Process 2: Next-state and output logic
    always @(*) begin
        // Default assignments
        next_state = state;
        busy = 1'b0;
        data_out = 8'b0;

        case (state)
            IDLE: begin
                if (start)
                    next_state = PROC;
            end

            PROC: begin
                busy = 1'b1;
                data_out = 8'hAA;
                if (done)
                    next_state = DONE;
            end

            DONE: begin
                data_out = 8'hFF;
                next_state = IDLE;
            end

            default: next_state = IDLE;
        endcase
    end

endmodule
```

### 8.2 Three-Process FSM

```verilog
// Process 1: State register
// Process 2: Next-state logic
// Process 3: Output logic (registered)

module fsm_threeprocess (
    input  wire       clk,
    input  wire       rst_n,
    input  wire [1:0] mode,
    output reg  [3:0] count,
    output reg        done
);

    // State encoding
    localparam [2:0] S_IDLE   = 3'b000,
                     S_LOAD   = 3'b001,
                     S_COUNT  = 3'b010,
                     S_WAIT   = 3'b011,
                     S_DONE   = 3'b100;

    reg [2:0] state, next_state;

    // Process 1: State register
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            state <= S_IDLE;
        else
            state <= next_state;
    end

    // Process 2: Next-state logic
    always @(*) begin
        next_state = state;

        case (state)
            S_IDLE: next_state = S_LOAD;
            S_LOAD: next_state = S_COUNT;
            S_COUNT: begin
                if (mode == 2'b00)
                    next_state = S_WAIT;
                else if (count == 4'hF)
                    next_state = S_DONE;
            end
            S_WAIT: next_state = S_COUNT;
            S_DONE: next_state = S_IDLE;
            default: next_state = S_IDLE;
        endcase
    end

    // Process 3: Output logic (registered)
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count <= 4'b0;
            done <= 1'b0;
        end else begin
            case (next_state)
                S_IDLE: begin
                    count <= 4'b0;
                    done <= 1'b0;
                end
                S_COUNT: begin
                    count <= count + 1'b1;
                end
                S_DONE: begin
                    done <= 1'b1;
                end
                default: begin
                    count <= count;
                    done <= done;
                end
            endcase
        end
    end

endmodule
```

### 8.3 One-Process FSM

```verilog
// Single process combines state register and logic
// Output can be registered or combinational

module fsm_oneprocess (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       sensor_in,
    output reg        actuator_out,
    output reg [7:0]  status
);

    localparam [1:0] OFF    = 2'b00,
                     WARMUP = 2'b01,
                     ACTIVE = 2'b10,
                     ERROR  = 2'b11;

    reg [1:0] state;
    reg [3:0] warmup_count;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= OFF;
            actuator_out <= 1'b0;
            status <= 8'h00;
            warmup_count <= 4'b0;
        end else begin
            case (state)
                OFF: begin
                    actuator_out <= 1'b0;
                    status <= 8'h00;
                    warmup_count <= 4'b0;
                    if (sensor_in)
                        state <= WARMUP;
                end

                WARMUP: begin
                    actuator_out <= 1'b0;
                    status <= 8'h01;
                    warmup_count <= warmup_count + 1'b1;
                    if (warmup_count == 4'hF)
                        state <= ACTIVE;
                    else if (!sensor_in)
                        state <= OFF;
                end

                ACTIVE: begin
                    actuator_out <= 1'b1;
                    status <= 8'hFF;
                    if (!sensor_in)
                        state <= ERROR;
                end

                ERROR: begin
                    actuator_out <= 1'b0;
                    status <= 8'hEE;
                    if (!sensor_in)
                        state <= OFF;
                end

                default: state <= OFF;
            endcase
        end
    end

endmodule
```

### 8.4 FSM Style Comparison

| Style | Registers | Logic Level | Glitch Free | Best Use |
|-------|-----------|-------------|-------------|----------|
| Two-Process | State only | Mixed | Yes (state) | General purpose |
| Three-Process | State + Output | Separate | Yes (both) | Complex FSMs |
| One-Process | Everything | Single | Yes | Simple FSMs |

## 9. FSM Verification

### 9.1 Properties to Verify

```
1. Reachability: All states are reachable from reset
2. Liveness: No deadlocks or livelocks
3. Safety: No illegal state transitions
4. Output correctness: Correct outputs in each state
5. Timing: Transitions meet setup/hold requirements
```

### 9.2 Assertion-Based Verification

```verilog
// SystemVerilog assertions for FSM verification
module fsm_assertions (
    input  wire       clk,
    input  wire       rst_n,
    input  wire [1:0] state,
    input  wire       valid
);

    // Property: After reset, FSM starts in IDLE
    property p_reset_to_idle;
        @(posedge clk) !rst_n |=> (state == 2'b00);
    endproperty

    // Property: Valid can only be asserted in ACTIVE state
    property p_valid_only_active;
        @(posedge clk) valid |-> (state == 2'b10);
    endproperty

    // Property: FSM never reaches illegal state
    property p_no_illegal_state;
        @(posedge clk) disable iff (!rst_n)
        state != 2'b11;
    endproperty

    // Property: Every state has a valid exit
    property p_no_deadlock;
        @(posedge clk) disable iff (!rst_n)
        state == 2'b10 |=> state != 2'b10;
    endproperty

    // Assertions
    assert property (p_reset_to_idle)
        else $error("FSM did not reset to IDLE");

    assert property (p_valid_only_active)
        else $error("Valid asserted in non-ACTIVE state");

    assert property (p_no_illegal_state)
        else $error("FSM reached illegal state");

    assert property (p_no_deadlock)
        else $error("FSM deadlock detected");

endmodule
```

### 9.3 Testbench for FSM

```verilog
module tb_fsm;

    reg clk, rst_n, start, done;
    wire busy;
    wire [7:0] data_out;

    // Instantiate FSM
    fsm_twoprocess dut (
        .clk(clk),
        .rst_n(rst_n),
        .start(start),
        .done(done),
        .busy(busy),
        .data_out(data_out)
    );

    // Clock generation
    always #5 clk = ~clk;

    // Test sequence
    initial begin
        clk = 0;
        rst_n = 0;
        start = 0;
        done = 0;

        // Reset
        #20 rst_n = 1;
        #10;

        // Test 1: Normal operation
        start = 1;
        #10 start = 0;
        #20;
        done = 1;
        #10 done = 0;
        #20;

        // Test 2: Start during operation
        start = 1;
        #10 start = 0;
        #10 start = 1;
        #10 start = 0;
        #30;

        // Test 3: Reset during operation
        rst_n = 0;
        #10 rst_n = 1;
        #20;

        $display("All tests completed");
        $finish;
    end

    // Monitor state transitions
    always @(posedge clk) begin
        $display("Time=%0t State=%b Busy=%b Data=%h",
                 $time, dut.state, busy, data_out);
    end

endmodule
```

## 10. FSM Optimization

### 10.1 Power Optimization

```
Techniques for low-power FSMs:

1. Clock Gating:
   - Gate clock when FSM is in idle state
   - Reduces dynamic power by ~50%

2. State Encoding for Low Power:
   - Use Gray code to minimize switching
   - Assign popular transitions to adjacent codes

3. Logic Optimization:
   - Minimize XOR gates (high switching activity)
   - Use precomputed outputs

4. Multi-Voltage Design:
   - Critical path: High voltage
   - Non-critical path: Low voltage

Power Model:
P_total = P_static + P_dynamic
P_dynamic = α × C × V² × f

Where:
α = switching activity factor
C = capacitance
V = supply voltage
f = clock frequency
```

### 10.2 Area Optimization

```
Techniques for area-efficient FSMs:

1. State Minimization:
   - Remove equivalent states
   - Use implication tables or partition methods

2. Encoding Optimization:
   - Binary encoding (fewest flip-flops)
   - One-hot (simplest logic, but more FFs)
   - Use don't cares for unused states

3. Logic Sharing:
   - Common subexpression elimination
   - Resource sharing between states

4. ROM-Based Implementation:
   - Store state table in ROM
   - Good for complex FSMs with many states
```

### 10.3 Speed Optimization

```
Techniques for high-speed FSMs:

1. One-Hot Encoding:
   - Fewer levels of combinational logic
   - Simpler next-state logic

2. Pipeline Registers:
   - Break critical path with pipeline stages
   - Trade latency for frequency

3. Lookahead Logic:
   - Precompute next state conditions
   - Reduce combinational delay

4. Retiming:
   - Move registers to balance paths
   - Can reduce critical path by 50%
```

## 11. Applications in Medical Implant Design

### 11.1 FSM for Implant Control

```
Implant State Machine Example:

States:
- SLEEP: Ultra-low power, monitoring only
- WAKE: Checking sensors, preparing
- SENSE: Active sensing/measurement
- PROCESS: Computing/analyzing data
- TRANSMIT: Sending data externally
- ERROR: Fault detection/recovery

State Transitions:
SLEEP → WAKE (timer interrupt)
WAKE → SENSE (sensors ready)
SENSE → PROCESS (data collected)
PROCESS → TRANSMIT (analysis complete)
TRANSMIT → SLEEP (transmission done)
Any → ERROR (fault detected)
ERROR → SLEEP (after timeout/recovery)

Power Management:
- SLEEP: 100 nW (only watchdog active)
- WAKE: 10 μW (sensors warming up)
- SENSE: 100 μW (active measurement)
- PROCESS: 500 μW (digital processing)
- TRANSMIT: 1 mW (RF transmitter active)
- ERROR: 50 μW (recovery attempt)

Average Power Calculation:
With typical duty cycles:
P_avg = 0.1×100n + 0.05×10μ + 0.1×100μ + 0.05×500μ + 0.01×1m + 0.01×50μ
      = 10n + 500n + 10μ + 25μ + 10μ + 500n
      ≈ 46 μW
```

### 11.2 Fault-Tolerant FSM Design

```
For medical implants, FSM must be fault-tolerant:

1. Error Detection:
   - Parity on state encoding
   - Watchdog timer monitoring
   - CRC on data paths

2. Error Recovery:
   - State rollback to known good state
   - Triple Modular Redundancy (TMR)
   - Error Correcting Codes (ECC)

3. Safe State Definition:
   - Always define a safe default state
   - Power-on reset to safe state
   - Watchdog timeout to safe state

Example TMR FSM:
┌─────────────┐
│  FSM Copy 1  │──┐
└─────────────┘  │
┌─────────────┐  ├──→ [Voter] → Output
│  FSM Copy 2  │──┤
└─────────────┘  │
┌─────────────┐  │
│  FSM Copy 3  │──┘
└─────────────┘

Voter: Majority vote selects correct output
Area overhead: 3×
Power overhead: 3×
Reliability: Dramatically improved
```

## 12. Summary

| Concept | Key Points |
|---------|------------|
| Moore Machine | Output depends on state only |
| Mealy Machine | Output depends on state + inputs |
| State Minimization | Remove equivalent states |
| State Encoding | Binary, One-Hot, Gray |
| Implementation | Two/Three/One process styles |
| Verification | Assertions, formal methods |
| Optimization | Power, area, speed tradeoffs |
| Medical Implants | Ultra-low power, fault-tolerant |

## 13. Exercises

1. Design a Moore machine for a pedestrian crossing signal
2. Minimize the state table and implement a Mealy machine for a sequence detector (detects "101")
3. Compare binary and one-hot encoding for a 16-state FSM
4. Implement a 3-process FSM for a UART transmitter
5. Write SystemVerilog assertions to verify a given FSM
6. Design a power-optimized FSM for an implantable sensor controller
7. Create a testbench for the FSM in Exercise 4 and verify all state transitions
8. Design a fault-tolerant FSM using TMR for a critical implant function
