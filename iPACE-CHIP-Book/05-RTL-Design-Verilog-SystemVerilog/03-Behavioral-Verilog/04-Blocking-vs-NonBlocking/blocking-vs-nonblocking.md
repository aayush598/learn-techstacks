# Blocking vs Non-Blocking Assignments

## 5.3.4 — Overview

The distinction between **blocking** (`=`) and **non-blocking** (`<=`)
assignments is one of the most critical concepts in Verilog. Incorrect usage
causes simulation-synthesis mismatches, race conditions, and functional
failures. For iPACE-CHIP pacemaker RTL, understanding this distinction is
essential for correct sequential logic design.

---

## 5.3.5 — Blocking Assignment (`=`)

### Behavior

- Executes **immediately** — the RHS is evaluated and assigned to the LHS
  before the next statement executes
- Like C/Java assignment semantics
- Used in **combinational** always blocks

```verilog
// Blocking: step-by-step execution
always @(*) begin
    a = b;      // a gets b's value NOW
    c = a + d;  // c gets (b + d) because a is already updated
end
```

### Synthesized Hardware

```verilog
// Blocking creates a chain
always @(*) begin
    temp = a & b;
    out  = temp | c;
end
// Equivalent to: assign out = (a & b) | c;
```

---

## 5.3.6 — Non-Blocking Assignment (`<=`)

### Behavior

- RHS is evaluated at the **beginning** of the time step
- Assignment occurs at the **end** of the time step
- All non-blocking assignments in the same always block execute simultaneously
- Used in **sequential** (clocked) always blocks

```verilog
// Non-blocking: parallel assignment
always @(posedge clk) begin
    a <= b;     // a gets b's OLD value (sampled at posedge)
    c <= a + d; // c gets (OLD_a + d) because a hasn't changed yet
end
```

### Simulation Timeline

```
Time 100: posedge clk
  ├─ Evaluate all RHS: a_RHS = b (current), c_RHS = a(current) + d
  ├─ End of time step: a = b(old), c = a(old) + d
  └─ All assignments happen simultaneously
```

---

## 5.3.7 — Side-by-Side Comparison

### Blocking in Combinational

```verilog
// CORRECT: blocking in combinational
always @(*) begin
    out = 1'b0;        // default
    case (sel)
        2'b00: out = a;
        2'b01: out = b;
        2'b10: out = c;
        2'b11: out = d;
    endcase
end
```

### Non-Blocking in Sequential

```verilog
// CORRECT: non-blocking in sequential
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        q1 <= 1'b0;
        q2 <= 1'b0;
    end else begin
        q1 <= d;
        q2 <= q1;  // q2 gets OLD q1 (pipeline!)
    end
end
```

---

## 5.3.8 — The Golden Rules

| Rule | Description |
|------|-------------|
| **Rule 1** | Use **blocking** (`=`) for combinational logic |
| **Rule 2** | Use **non-blocking** (`<=`) for sequential logic |
| **Rule 3** | Never mix blocking and non-blocking in the same always block |
| **Rule 4** | Never use `#delay` in synthesizable always blocks |
| **Rule 5** | Assign all outputs in all branches (prevent latches) |

---

## 5.3.9 — Common Mistakes and Consequences

### Mistake 1: Blocking in Sequential Logic

```verilog
// BUG: blocking in clocked block
always @(posedge clk) begin
    a = b;  // a gets b immediately
    c = a;  // c gets NEW a (b), not old a!
end
// Synthesizes to: c = b (bypasses a register!)
// Expected pipeline: a→b, c→a(old)
```

### Mistake 2: Non-Blocking in Combinational Logic

```verilog
// BUG: non-blocking in combinational
always @(*) begin
    out <= a & b;  // won't propagate immediately
    result <= out | c;  // uses OLD out value
end
// Simulation-synthesis mismatch — synthesis ignores <= in combinational
```

### Mistake 3: Mixing Blocking and Non-Blocking

```verilog
// BUG: mixed assignments
always @(posedge clk) begin
    a = b;      // blocking
    c <= a + d; // non-blocking — when is 'a' sampled?
end
// Race condition — unpredictable behavior
```

### Mistake 4: Non-Deterministic Order

```verilog
// BUG: blocking order dependency
always @(posedge clk) begin
    q1 = d;
    q2 = q1;  // q2 gets d, not old q1
end

// If these were in separate always blocks:
always @(posedge clk) q1 = d;
always @(posedge clk) q2 = q1;
// ORDER IS NON-DETERMINISTIC — simulator decides!
```

---

## 5.3.10 — Pacemaker: Correct Pipeline Implementation

```verilog
// 3-stage pipeline for ADC data processing
module adc_pipeline (
    input  wire        clk,
    input  wire        rst_n,
    input  wire [11:0] adc_raw,
    input  wire        adc_valid,
    output reg  [11:0] adc_filtered,
    output reg         filtered_valid,
    output reg  [11:0] adc_peak,
    output reg         peak_valid
);
    // Stage 1: Sample registration
    reg [11:0] stage1_data;
    reg        stage1_valid;

    // Stage 2: Moving average
    reg [15:0] accumulator;
    reg [11:0] stage2_data;
    reg        stage2_valid;

    // Stage 3: Peak detection
    reg [11:0] running_peak;

    // ALL non-blocking — correct pipeline behavior
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            stage1_data    <= 12'd0;
            stage1_valid   <= 1'b0;
            stage2_data    <= 12'd0;
            stage2_valid   <= 1'b0;
            accumulator    <= 16'd0;
            adc_filtered   <= 12'd0;
            filtered_valid <= 1'b0;
            running_peak   <= 12'd0;
            adc_peak       <= 12'd0;
            peak_valid     <= 1'b0;
        end else begin
            // Stage 1: Register raw ADC
            stage1_data  <= adc_raw;
            stage1_valid <= adc_valid;

            // Stage 2: Moving average (accumulate then shift)
            if (stage1_valid) begin
                accumulator <= accumulator + {4'b0, stage1_data}
                             - {4'b0, stage2_data};
                stage2_data <= stage1_data;
            end
            stage2_valid <= stage1_valid;

            // Stage 3: Peak detection and output
            adc_filtered   <= accumulator[15:4];  // /16
            filtered_valid <= stage2_valid;

            if (stage2_valid && stage2_data > running_peak)
                running_peak <= stage2_data;

            adc_peak   <= running_peak;
            peak_valid <= stage2_valid;
        end
    end
endmodule
```

---

## 5.3.11 — Pacemaker: Register Transfer Examples

### Shift Register (Correct)

```verilog
module shift_reg_correct (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       serial_in,
    output wire       serial_out,
    output wire [7:0] parallel_out
);
    reg [7:0] shift_reg;

    // Non-blocking: all bits shift simultaneously
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            shift_reg <= 8'h00;
        else
            shift_reg <= {shift_reg[6:0], serial_in};
    end

    assign serial_out  = shift_reg[7];
    assign parallel_out = shift_reg;

endmodule
```

### Shift Register (WRONG — Blocking)

```verilog
// DO NOT USE — demonstrates the bug
module shift_reg_wrong (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       serial_in,
    output reg  [7:0] shift_reg
);
    // Blocking: sequential cascade — only serial_in propagates!
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            shift_reg = 8'h00;
        else begin
            shift_reg[0] = serial_in;      // immediate
            shift_reg[1] = shift_reg[0];   // gets NEW [0]
            shift_reg[2] = shift_reg[1];   // gets NEW [1]
            // ... all bits become serial_in!
        end
    end
endmodule
```

---

## 5.3.12 — Case Study: FSM Output Encoding

### Correct: Registered Output (Non-Blocking)

```verilog
// One-hot state register
reg [3:0] state, next_state;

always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        state <= 4'b0001;
    else
        state <= next_state;
end

// Output logic — registered (non-blocking)
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        pace_out    <= 1'b0;
        charge_out  <= 1'b0;
    end else begin
        pace_out    <= (next_state == S_PACE);
        charge_out  <= (next_state == S_CHARGE);
    end
end
```

### Correct: Combinational Output (Blocking)

```verilog
// Combinational output decode
always @(*) begin
    pace_out   = 1'b0;
    charge_out = 1'b0;
    case (state)
        S_IDLE: begin end
        S_PACE: pace_out = 1'b1;
        S_CHARGE: charge_out = 1'b1;
    endcase
end
```

---

## 5.3.13 — Blocking Assignment Applications

### Temp Variables in Combinational Logic

```verilog
// Blocking is fine for temporary variables
always @(*) begin
    wire [7:0] temp_a, temp_b;
    temp_a = input_a & mask;
    temp_b = input_b | mask;
    output_val = temp_a ^ temp_b;
end
```

### Flip-Flop Reset Values

```verilog
// Blocking for reset value computation (testbench)
initial begin
    rst_n = 0;
    #100;
    rst_n = 1;
end
```

---

## 5.3.14 — Summary Table

| Aspect | Blocking (`=`) | Non-Blocking (`<=`) |
|--------|----------------|---------------------|
| Evaluation | Immediate | Deferred to end of time step |
| Use in | Combinational `always @(*)` | Sequential `always @(posedge clk)` |
| Temp variables | Yes | No (use wires instead) |
| Pipeline registers | No | Yes |
| Synthesis | Combinational logic | Flip-flops |
| Race conditions | Possible (avoid in sequential) | None (parallel) |

---

## 5.3.15 — Best Practices

1. **Non-blocking for ALL sequential logic** — no exceptions
2. **Blocking for ALL combinational logic** — clean semantics
3. **Never mix** blocking and non-blocking in the same always block
4. **Use intermediate `wire`** for combinational multi-step expressions
5. **Check synthesis warnings** — tools detect blocking in sequential
6. **Use SystemVerilog `always_ff`** — prevents accidental combinational
7. **Verify with formal tools** — catch race conditions automatically
8. **Document the convention** — team consistency is critical

---

## 5.3.16 — References

- Clifford Cummings, *Nonblocking Assignments in Verilog Synthesis, Coding Styles That Kill!*
- IEEE Std 1364-2005, Section 4.4 — Procedural Assignments
- IEEE Std 1800-2017, Section 10.4 — Blocking and Nonblocking Assignments
- iPACE-CHIP RTL Coding Guidelines, Section 3.7 — Assignment Conventions
