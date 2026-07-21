# Always and Assign Statements in Verilog

## 5.1.3 — Overview

Two constructs drive every Verilog module: **continuous assignments** (`assign`)
and **procedural blocks** (`always`). Understanding when and how to use each is
essential for correct synthesis. Misusing them leads to latches, simulation
mismatches, or functional failures in the iPACE-CHIP pacemaker RTL.

---

## 5.3.1 — Continuous Assignment (`assign`)

The `assign` statement creates combinational logic driven by expressions.

```verilog
assign signal_name = expression;
```

### Basic Examples

```verilog
// Simple gate
assign z = a & b;

// Mux
assign out = sel ? in1 : in0;

// Bus slice
assign data_out = data_in[15:8];

// Conditional with multiple conditions
assign pacing_pulse = timer_expired && pacing_enabled && !refractory_period;
```

### Continuous Assignment vs Wire Declaration

```verilog
// Method 1: assign statement
wire [7:0] result;
assign result = a + b;

// Method 2: Implicit wire assignment (equivalent)
wire [7:0] result = a + b;

// Method 3: Wire output from submodule
wire [7:0] sub_out;
submodule u_sub (.data_out(sub_out), ...);
```

### Tri-State with Assign

```verilog
// Bidirectional bus with output enable
assign sda = sda_oe ? sda_out : 1'bz;

// Active-low enable
assign led = ~led_enable;  // active-high LED
```

### Pacemaker: Combinational Signal Network

```verilog
module pacing_logic (
    input  wire        timer_expired,
    input  wire        sensing_valid,
    input  wire        refractory_active,
    input  wire [1:0]  pacing_mode,
    output wire        pace_out,
    output wire        charge_enable,
    output wire        discharge_enable
);

    // Derived signals
    wire pacing_allowed = timer_expired
                       && !refractory_active
                       && (pacing_mode != 2'b00);

    wire atrial_demand = sensing_valid && (pacing_mode == 2'b01);
    wire vent_demand   = sensing_valid && (pacing_mode == 2'b10);

    // Output assignments
    assign pace_out        = pacing_allowed && !atrial_demand;
    assign charge_enable   = pacing_allowed;
    assign discharge_enable = pace_out;

endmodule
```

---

## 5.3.2 — Always Blocks

`always` blocks contain **procedural** code. They are triggered by events in
the sensitivity list.

### Syntax Variants

```verilog
// Combinational
always @(*) begin ... end
always_comb begin ... end  // SystemVerilog preferred

// Sequential (posedge clock)
always @(posedge clk) begin ... end

// Sequential with async reset
always @(posedge clk or negedge rst_n) begin ... end

// Level-sensitive (latch — avoid)
always @(*) begin ... end  // can infer latch if not all paths assign
```

---

## 5.3.3 — Combinational Always Block

### SystemVerilog: `always_comb`

```verilog
always_comb begin
    case (op_code)
        3'b000: result = a + b;
        3'b001: result = a - b;
        3'b010: result = a & b;
        3'b011: result = a | b;
        3'b100: result = a ^ b;
        3'b101: result = a << shamt;
        3'b110: result = a >> shamt;
        3'b111: result = a;
        default: result = '0;
    endcase
end
```

### Completeness Requirement

Every signal assigned in a combinational block must be assigned in ALL
paths. Incomplete assignment → **latch inference**.

```verilog
// BAD — latch inferred
always_comb begin
    if (enable)
        out = data_in;
    // Missing: else out = out; ← latch!
end

// GOOD — no latch
always_comb begin
    if (enable)
        out = data_in;
    else
        out = 1'b0;  // explicit default
end
```

### Pacemaker: Combinational Decoder

```verilog
reg [2:0] alarm_code;
reg       critical_alarm;
reg       warning_alarm;
reg       info_alarm;

always_comb begin
    // Defaults (critical for latch prevention)
    alarm_code    = 3'b000;
    critical_alarm = 1'b0;
    warning_alarm  = 1'b0;
    info_alarm     = 1'b0;

    case (1'b1)  // one-hot priority
        battery_low_critical: begin
            alarm_code    = 3'b111;
            critical_alarm = 1'b1;
        end
        lead_impedance_fault: begin
            alarm_code    = 3'b110;
            critical_alarm = 1'b1;
        end
        battery_low_warning: begin
            alarm_code    = 3'b011;
            warning_alarm  = 1'b1;
        end
        sensing_threshold_exceeded: begin
            alarm_code    = 3'b010;
            info_alarm     = 1'b1;
        end
        default: begin
            alarm_code    = 3'b000;
            critical_alarm = 1'b0;
            warning_alarm  = 1'b0;
            info_alarm     = 1'b0;
        end
    endcase
end
```

---

## 5.3.4 — Sequential Always Block

### Edge-Triggered Flip-Flop

```verilog
// D flip-flop with async reset
always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        q <= 1'b0;
    else
        q <= d;
end
```

### Pipelined Register

```verilog
// 3-stage pipeline
reg [7:0] stage1, stage2, stage3;

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        stage1 <= 8'b0;
        stage2 <= 8'b0;
        stage3 <= 8'b0;
    end else begin
        stage1 <= data_in;
        stage2 <= stage1;
        stage3 <= stage2;
    end
end
```

### Pacemaker: Pacing Timer Counter

```verilog
module pacing_timer_reg (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        timer_enable,
    input  wire        timer_clear,
    input  wire [15:0] timer_limit,
    output reg  [15:0] timer_count,
    output reg         timer_expired
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            timer_count   <= 16'd0;
            timer_expired <= 1'b0;
        end else if (timer_clear) begin
            timer_count   <= 16'd0;
            timer_expired <= 1'b0;
        end else if (timer_enable && !timer_expired) begin
            timer_count <= timer_count + 1'b1;
            if (timer_count == timer_limit - 1'b1)
                timer_expired <= 1'b1;
        end
    end

endmodule
```

---

## 5.3.5 — Latch Inference and Prevention

### How Latches Occur

```verilog
// Example 1: Incomplete if-else
always_comb begin
    if (sel)
        out = a;
    // else: out retains value → LATCH
end

// Example 2: Incomplete case
always_comb begin
    case (state)
        S_A: out = 1'b1;
        S_B: out = 1'b0;
        // Missing S_C, S_D → LATCH for those states
    endcase
end

// Example 3: Procedural assignment to reg without default
reg [7:0] data;
always_comb begin
    if (write_en)
        data = new_data;
    // data retains value when write_en=0 → LATCH
end
```

### Prevention Strategies

**Strategy 1: Explicit defaults**

```verilog
always_comb begin
    out = 1'b0;  // default
    if (enable)
        out = data_in;
end
```

**Strategy 2: Complete case/if-else**

```verilog
always_comb begin
    case (state)
        S_A: out = 2'b01;
        S_B: out = 2'b10;
        S_C: out = 2'b11;
        default: out = 2'b00;  // complete all cases
    endcase
end
```

**Strategy 3: SystemVerilog `unique case`**

```verilog
always_comb begin
    unique case (priority_encoder)
        3'b001: out = 4'b0001;
        3'b010: out = 4'b0010;
        3'b100: out = 4'b0100;
        default: out = 4'b0000;
    endcase
end
```

### Intentional Latches

```verilog
// When you WANT a latch (rare, but valid)
// Example: Level-sensitive interrupt capture
always_latch begin
    if (int_clear)
        int_pending <= 1'b0;
    else if (int_set)
        int_pending <= 1'b1;
    // int_pending holds when neither condition — intentional latch
end
```

---

## 5.3.6 — Non-Blocking (`<=`) vs Blocking (`=`) Assignment

This is covered in depth in 03-Behavioral-Verilog/04-Blocking-vs-NonBlocking,
but the key rule is stated here:

| Context | Assignment Type | Example |
|---------|----------------|---------|
| Sequential (clocked) | Non-blocking `<=` | `q <= d;` |
| Combinational (`always_comb`) | Blocking `=` | `out = a & b;` |
| Combinational (`always @(*)`) | Blocking `=` | `result = a + b;` |
| Combinational (derived signals) | `assign` | `assign z = a & b;` |

---

## 5.3.7 — SystemVerilog Procedural Blocks

### `always_ff` — Sequential

```verilog
always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        counter <= '0;
    else
        counter <= counter + 1'b1;
end
```

### `always_comb` — Combinational

```verilog
always_comb begin
    next_state = current_state;
    case (current_state)
        S_IDLE: if (start) next_state = S_RUN;
        S_RUN: if (done)   next_state = S_IDLE;
    endcase
end
```

### `always_latch` — Latch

```verilog
always_latch begin
    if (load_en)
        latch_data = data_in;
end
```

### `always_proc` — Generic Procedural

```verilog
// Used when you don't want synthesis tool to infer
// (testbench, assertions)
always_proc begin
    wait (release_signal);
    do_something();
end
```

---

## 5.3.8 — Multi-Driven Signals

### Wire with Multiple Drivers

```verilog
// Two modules driving the same wire — resolves via wire logic
wire conflict;
assign conflict = a;
assign conflict = b;
// conflict = a & b  (default wire resolution = AND for multiple drivers)
```

### Reg with Multiple Drivers (BAD)

```verilog
// NEVER do this — causes simulation/synthesis mismatch
always @(posedge clk) begin
    if (sel1) data <= value1;
end
always @(posedge clk) begin
    if (sel2) data <= value2;
end
// Last assignment wins — non-deterministic with multiple always blocks
```

### Correct: Priority Structure

```verilog
always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        data <= '0;
    else if (sel1)
        data <= value1;
    else if (sel2)
        data <= value2;
    else
        data <= data;  // explicit hold
end
```

---

## 5.3.9 — Pacemaker: Complete Module with Assign and Always

```verilog
module refractory_controller (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        pace_detected,     // pulse from pacing output
    input  wire        sense_detected,    // intrinsic event detected
    input  wire [15:0] atrial_refrac_time,
    input  wire [15:0] vent_refrac_time,
    output reg         atrial_refrac,
    output reg         vent_refrac,
    output wire        any_refrac_active
);

    // Internal counters
    reg [15:0] atrial_refrac_cnt;
    reg [15:0] vent_refrac_cnt;

    // Continuous assignments — combinational
    assign any_refrac_active = atrial_refrac | vent_refrac;

    // Atrial refractory timer
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            atrial_refrac     <= 1'b0;
            atrial_refrac_cnt <= 16'd0;
        end else if (pace_detected) begin
            atrial_refrac     <= 1'b1;
            atrial_refrac_cnt <= 16'd0;
        end else if (atrial_refrac) begin
            if (atrial_refrac_cnt == atrial_refrac_time) begin
                atrial_refrac     <= 1'b0;
                atrial_refrac_cnt <= 16'd0;
            end else begin
                atrial_refrac_cnt <= atrial_refrac_cnt + 1'b1;
            end
        end
    end

    // Ventricular refractory timer
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            vent_refrac     <= 1'b0;
            vent_refrac_cnt <= 16'd0;
        end else if (sense_detected) begin
            vent_refrac     <= 1'b1;
            vent_refrac_cnt <= 16'd0;
        end else if (vent_refrac) begin
            if (vent_refrac_cnt == vent_refrac_time) begin
                vent_refrac     <= 1'b0;
                vent_refrac_cnt <= 16'd0;
            end else begin
                vent_refrac_cnt <= vent_refrac_cnt + 1'b1;
            end
        end
    end

endmodule
```

---

## 5.3.10 — Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Missing `else` in combinational | Latch inferred | Add explicit default |
| Blocking in sequential | Race condition | Use `<=` in clocked blocks |
| Combinational loop | Oscillation / synthesis error | Break loop with register |
| Missing reset | Unknown state on power-up | Initialize all `reg` |
| Mixed `=` and `<=` in same block | Unpredictable behavior | Use one type per block |
| `assign` to `reg` | Compilation error | Use `wire` for `assign` |

### Combinational Loop Detection

```verilog
// BAD — combinational loop
wire a = b | c;
wire b = a & d;  // a depends on b, b depends on a → loop!

// FIX — break with register or restructure
wire a = b | c;
wire b_int = b_int_prev & d;  // use registered version
```

---

## 5.3.11 — Best Practices Summary

1. **Use `always_comb`** instead of `always @(*)` in SystemVerilog
2. **Use `always_ff`** instead of `always @(posedge clk)` in SystemVerilog
3. **Default assignments** in combinational blocks prevent latches
4. **Complete case/if-else** chains always
5. **Non-blocking `<=`** in sequential blocks, **blocking `=`** in combinational
6. **One driver per signal** — avoid multiple `always` blocks driving same `reg`
7. **Always reset** all sequential elements
8. **Use `assign`** for simple combinational expressions
9. **Never mix blocking and non-blocking** in the same always block
10. **Check for latch inference** with synthesis tool warnings

---

## 5.3.12 — References

- IEEE Std 1364-2005, Section 4.2 — Procedural Modeling
- Clifford Cummings, *Coding Styles for Sequential and Combinational Always Blocks*
- iPACE-CHIP RTL Coding Guidelines, Section 3.3 — Assignment Rules
