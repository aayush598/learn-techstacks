# Always Blocks and Sensitivity Lists

## 5.3.1 — Overview

The `always` block is the primary behavioral construct in Verilog. It executes
repeatedly, triggered by changes in its **sensitivity list**. Correct sensitivity
list usage is essential for synthesis accuracy — an incorrect list causes
simulation-synthesis mismatch. For iPACE-CHIP pacemaker RTL, every sequential
and combinational module depends on properly constructed always blocks.

---

## 5.3.2 — Sensitivity List Types

### Level-Sensitive (Combinational)

```verilog
// Verilog-2001 style
always @(*) begin
    // Re-evaluates whenever any RHS signal changes
    out = a & b | c;
end

// Equivalent explicit form
always @(a or b or c) begin
    out = a & b | c;
end

// SystemVerilog preferred
always_comb begin
    out = a & b | c;
end
```

### Edge-Sensitive (Sequential)

```verilog
// Positive edge (rising)
always @(posedge clk) begin
    q <= d;
end

// Negative edge (falling)
always @(negedge clk) begin
    q <= d;
end

// Both edges
always @(posedge clk or negedge clk) begin
    toggle <= ~toggle;
end
```

### Asynchronous Reset

```verilog
// Async active-low reset (most common in iPACE-CHIP)
always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        q <= 1'b0;
    else
        q <= d;
end

// Async active-high reset
always @(posedge clk or posedge rst) begin
    if (rst)
        q <= 1'b0;
    else
        q <= d;
end
```

### Synchronous Reset

```verilog
always @(posedge clk) begin
    if (!rst_n)
        q <= 1'b0;
    else
        q <= d;
end
```

---

## 5.3.3 — Combinational Sensitivity: Common Errors

### Error 1: Incomplete Sensitivity List

```verilog
// BUG: missing 'c' from sensitivity list
always @(a or b) begin  // ← missing 'c'
    out = a & b | c;
end
// Simulation: out won't update when c changes
// Synthesis: produces correct combinational logic
// RESULT: simulation-synthesis MISMATCH
```

### Error 2: Using `always @(*)` Correctly

```verilog
// GOOD: @(*) includes all signals
always @(*) begin
    out = a & b | c;
end
// Automatically sensitive to a, b, and c

// GOOD: SystemVerilog
always_comb begin
    out = a & b | c;
end
```

### Error 3: Latch from Incomplete Assignment

```verilog
// BUG: latch inferred
always @(*) begin
    if (sel)
        out = a;
    // Missing else branch → latch
end

// FIX: explicit default
always @(*) begin
    if (sel)
        out = a;
    else
        out = 1'b0;
end
```

---

## 5.3.4 — Sequential Sensitivity: Detailed Examples

### Positive-Edge D Flip-Flop

```verilog
module dff_basic (
    input  wire clk,
    input  wire d,
    output reg  q
);
    always @(posedge clk) begin
        q <= d;
    end
endmodule
```

### D Flip-Flop with Async Reset and Enable

```verilog
module dff_rst_en (
    input  wire clk,
    input  wire rst_n,
    input  wire enable,
    input  wire d,
    output reg  q
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            q <= 1'b0;
        else if (enable)
            q <= d;
    end
endmodule
```

### D Flip-Flop with Sync Reset

```verilog
module dff_sync_rst (
    input  wire clk,
    input  wire rst_n,
    input  wire d,
    output reg  q
);
    always @(posedge clk) begin
        if (!rst_n)
            q <= 1'b0;
        else
            q <= d;
    end
endmodule
```

---

## 5.3.5 — SystemVerilog Procedural Blocks

### `always_comb`

```verilog
// Automatic sensitivity list — always complete
always_comb begin
    unique case (state)
        S_IDLE:  next = start ? S_RUN : S_IDLE;
        S_RUN:   next = done  ? S_STOP : S_RUN;
        S_STOP:  next = S_IDLE;
        default: next = S_IDLE;
    endcase
end
```

### `always_ff`

```verilog
// Explicitly marks sequential — synthesis tool enforces clock
always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        state <= S_IDLE;
    else
        state <= next;
end
```

### `always_latch`

```verilog
// Intentional latch — explicit
always_latch begin
    if (load_en)
        latch_data = data_in;
    // Holds when load_en = 0 — INTENTIONAL
end
```

---

## 5.3.6 — Multi-Clock Sensitivity

### Two Clock Domains (Avoid if Possible)

```verilog
// Synchronizer — crosses clock domain
module cdc_synchronizer (
    input  wire clk_a,
    input  wire clk_b,
    input  wire rst_n,
    input  wire async_in,
    output reg  sync_out
);
    reg sync_stage1;

    // Domain A: capture
    always @(posedge clk_a or negedge rst_n) begin
        if (!rst_n)
            sync_stage1 <= 1'b0;
        else
            sync_stage1 <= async_in;
    end

    // Domain B: synchronize
    always @(posedge clk_b or negedge rst_n) begin
        if (!rst_n)
            sync_out <= 1'b0;
        else
            sync_out <= sync_stage1;
    end
endmodule
```

### Pulse Synchronizer

```verilog
module pulse_cdc (
    input  wire clk_src,
    input  wire clk_dst,
    input  wire rst_n,
    input  wire pulse_in,
    output wire pulse_out
);
    reg toggle_src;
    reg [2:0] sync_dst;

    // Source domain: toggle on pulse
    always @(posedge clk_src or negedge rst_n) begin
        if (!rst_n)
            toggle_src <= 1'b0;
        else if (pulse_in)
            toggle_src <= ~toggle_src;
    end

    // Destination domain: 3-stage sync + edge detect
    always @(posedge clk_dst or negedge rst_n) begin
        if (!rst_n)
            sync_dst <= 3'b0;
        else
            sync_dst <= {sync_dst[1:0], toggle_src};
    end

    assign pulse_out = sync_dst[2] ^ sync_dst[1];

endmodule
```

---

## 5.3.7 — Pacemaker: Complete Sensitivity Examples

### Atrial Sensing Always Block

```verilog
module atrial_sense_detector (
    input  wire        clk,
    input  wire        rst_n,
    input  wire [11:0] adc_data,
    input  wire        adc_valid,
    input  wire [11:0] threshold,
    input  wire        refractory,
    output reg         sense_event,
    output reg  [11:0] peak_amplitude
);
    reg [11:0] prev_adc;
    reg [11:0] running_peak;

    // Detect R-wave or P-wave crossing threshold
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            sense_event    <= 1'b0;
            peak_amplitude <= 12'd0;
            prev_adc       <= 12'd0;
            running_peak   <= 12'd0;
        end else if (adc_valid && !refractory) begin
            prev_adc <= adc_data;

            // Positive-slope threshold crossing
            if (adc_data >= threshold && prev_adc < threshold) begin
                sense_event    <= 1'b1;
                peak_amplitude <= adc_data;
                running_peak   <= adc_data;
            end else if (adc_data > running_peak) begin
                running_peak   <= adc_data;
                peak_amplitude <= adc_data;
            end else if (sense_event && adc_data < peak_amplitude) begin
                // Allow peak tracking, then clear
                if (adc_data < (peak_amplitude >> 1))
                    sense_event <= 1'b0;
            end
        end else if (refractory) begin
            sense_event    <= 1'b0;
            running_peak   <= 12'd0;
        end
    end
endmodule
```

### Pacing Output Controller

```verilog
module pacing_output_ctrl (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        pace_trigger,
    input  wire [15:0] pulse_width_cycles,
    input  wire [7:0]  amplitude_setting,
    output reg         pace_out,
    output reg  [7:0]  dac_output
);
    reg [15:0] pulse_counter;
    reg        pulse_active;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            pulse_counter <= 16'd0;
            pulse_active  <= 1'b0;
            pace_out      <= 1'b0;
            dac_output    <= 8'd0;
        end else if (pace_trigger && !pulse_active) begin
            pulse_active  <= 1'b1;
            pulse_counter <= 16'd0;
            pace_out      <= 1'b1;
            dac_output    <= amplitude_setting;
        end else if (pulse_active) begin
            pulse_counter <= pulse_counter + 1'b1;
            if (pulse_counter >= pulse_width_cycles) begin
                pulse_active <= 1'b0;
                pace_out     <= 1'b0;
                dac_output   <= 8'd0;
            end
        end
    end
endmodule
```

---

## 5.3.8 — Sensitivity List Synthesis Implications

| Sensitivity | Infers | Example |
|------------|--------|---------|
| `posedge clk` | D flip-flop | Counter, register |
| `posedge clk or negedge rst_n` | DFF with async reset | Most iPACE registers |
| `posedge clk` + if(rst_n) | DFF with sync reset | Sync reset design |
| `@(*)` / `always_comb` | Combinational logic | MUX, decoder, ALU |
| `@(*)` (incomplete) | Latch | Avoid unless intentional |
| `posedge clk or negedge clk` | Toggle flip-flop | Clock divider |

---

## 5.3.9 — Best Practices

1. **Use `always_comb`** instead of `always @(*)` — SystemVerilog enforces completeness
2. **Use `always_ff`** for sequential blocks — prevents accidental combinational inference
3. **List ALL signals** in combinational sensitivity — avoid simulation mismatch
4. **Async reset only when architecturally required** — sync reset is more reliable
5. **One clock per always block** — multi-clock blocks cause synthesis issues
6. **Never put `#delay` in synthesizable always blocks**
7. **Use `casez`/`casex`** for don't-care patterns in combinational logic
8. **Default assignments** prevent latch inference in combinational blocks

---

## 5.3.10 — References

- IEEE Std 1364-2005, Section 4.2 — Procedural Blocks
- IEEE Std 1800-2017, Section 9.2 — Procedural Blocks
- Clifford Cummings, *Simulation/Synthesis Mismatches in Verilog*
- iPACE-CHIP RTL Coding Guidelines, Section 3.3
