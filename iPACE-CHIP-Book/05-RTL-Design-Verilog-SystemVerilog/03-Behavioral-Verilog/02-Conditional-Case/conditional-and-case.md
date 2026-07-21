# Conditional and Case Statements

## 5.3.2 — Overview

`if-else` and `case` statements implement **decision logic** in behavioral
Verilog. They map to multiplexers, priority encoders, and state machine
transitions in hardware. Proper use prevents latches, priority bugs, and
simulation mismatches. For iPACE-CHIP, these constructs drive FSM transitions,
mux selection, and conditional data processing.

---

## 5.3.3 — If-Else Statements

### Basic Syntax

```verilog
if (condition)
    statement;
else if (condition2)
    statement2;
else
    statement3;
```

### Synthesized Hardware

`if-else` chains synthesize to **priority-encoded multiplexers**:

```verilog
// if-else priority mux
always_comb begin
    if (high_priority_req)
        grant = 3'b100;
    else if (med_priority_req)
        grant = 3'b010;
    else if (low_priority_req)
        grant = 3'b001;
    else
        grant = 3'b000;
end
// Synthesizes to priority mux: high > med > low
```

### Pacemaker: Mode-Dependent Threshold Selection

```verilog
reg [11:0] sensing_threshold;

always_comb begin
    if (mode == MODE_VVI)
        sensing_threshold = vvi_threshold;
    else if (mode == MODE_AAI)
        sensing_threshold = aai_threshold;
    else if (mode == MODE_DDD)
        sensing_threshold = ddd_threshold;
    else
        sensing_threshold = DEFAULT_THRESHOLD;
end
```

---

## 5.3.4 — Latch Prevention with If-Else

### Common Latch Sources

```verilog
// LATCH: missing else
always_comb begin
    if (enable)
        out = data;
end

// LATCH: incomplete nested if
always_comb begin
    if (sel_a) begin
        if (sel_b)
            out = a;
        // No else for sel_b → latch
    end
    // No else for sel_a → latch
end
```

### Prevention Strategies

```verilog
// STRATEGY 1: Default assignment at top
always_comb begin
    out = 1'b0;  // default
    if (enable)
        out = data;
end

// STRATEGY 2: Complete if-else chain
always_comb begin
    if (sel_a)
        out = a;
    else if (sel_b)
        out = b;
    else
        out = c;  // always has default
end

// STRATEGY 3: Use case statement instead
always_comb begin
    case ({enable, sel_a, sel_b})
        3'b110: out = a;
        3'b101: out = b;
        3'b100: out = c;
        default: out = 1'b0;
    endcase
end
```

---

## 5.3.5 — Case Statements

### Basic Case

```verilog
always_comb begin
    case (selector)
        2'b00: out = data_a;
        2'b01: out = data_b;
        2'b10: out = data_c;
        2'b11: out = data_d;
        default: out = 1'b0;
    endcase
end
```

### Case Variants

| Statement | Matching | Synthesis |
|-----------|----------|-----------|
| `case` | Exact match (0, 1, x, z all distinct) | MUX |
| `casez` | z matches any bit | Priority logic with don't-cares |
| `casex` | x and z match any bit | Avoid in RTL (ambiguous) |
| `unique case` | SV: no overlap check | Parallel MUX |
| `priority case` | SV: priority encoded | Priority logic |

---

## 5.3.6 — Casez for Don't-Care Patterns

```verilog
// Priority encoder with don't-cares
always_comb begin
    casez (irq_vector)
        8'b1???????: priority = 3'd7;
        8'b01??????: priority = 3'd6;
        8'b001?????: priority = 3'd5;
        8'b0001????: priority = 3'd4;
        8'b00001???: priority = 3'd3;
        8'b000001??: priority = 3'd2;
        8'b0000001?: priority = 3'd1;
        8'b00000001: priority = 3'd0;
        default:     priority = 3'd0;
    endcase
end
```

### Pacemaker: Interrupt Priority Decoder

```verilog
reg [3:0] interrupt_ack;

always_comb begin
    interrupt_ack = 4'b0000;
    casez ({batt_crit, batt_low, lead_fault, sensing_event})
        4'b1???: interrupt_ack = 4'b1000;  // battery critical
        4'b01??: interrupt_ack = 4'b0100;  // battery low
        4'b001?: interrupt_ack = 4'b0010;  // lead fault
        4'b0001: interrupt_ack = 4'b0001;  // sensing event
        default: interrupt_ack = 4'b0000;
    endcase
end
```

---

## 5.3.7 — Unique Case (SystemVerilog)

```verilog
// Unique case: synthesis tool assumes cases are mutually exclusive
// If overlap exists → simulation may not match synthesis
always_comb begin
    unique case (state)
        IDLE:    next = START;
        START:   next = RUN;
        RUN:     next = STOP;
        STOP:    next = IDLE;
        default: next = IDLE;  // unreachable (but needed)
    endcase
end
```

### Priority Case (SystemVerilog)

```verilog
// Priority case: explicitly tells tool to check in order
always_comb begin
    priority case (1'b1)
        fault_critical: action = SHUTDOWN;
        fault_warning:  action = REDUCE_POWER;
        normal_op:      action = FULL_SPEED;
        default:        action = STANDBY;
    endcase
end
```

---

## 5.3.8 — Nested Case for Complex MUX

```verilog
// Two-level mux for pacemaker configuration
reg [7:0] config_output;

always_comb begin
    case (config_addr[7:6])
        2'b00: begin
            case (config_addr[1:0])
                2'b00: config_output = pacing_mode_reg;
                2'b01: config_output = sensitivity_reg;
                2'b10: config_output = pulse_width_reg;
                2'b11: config_output = pulse_amp_reg;
            endcase
        end
        2'b01: begin
            case (config_addr[1:0])
                2'b00: config_output = refractory_reg;
                2'b01: config_output = timer_reg[7:0];
                2'b10: config_output = timer_reg[15:8];
                2'b11: config_output = status_reg;
            endcase
        end
        default: config_output = 8'h00;
    endcase
end
```

---

## 5.3.9 — Full Pacemaker FSM with Case

```verilog
module pacing_fsm (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        timer_expired,
    input  wire        atrial_sense,
    input  wire        vent_sense,
    input  wire [1:0]  pacing_mode,
    output reg         pace_a_out,
    output reg         pace_v_out,
    output reg         timer_start,
    output reg         timer_clear,
    output reg  [1:0]  state
);

    localparam IDLE        = 2'b00;
    localparam PACE_A      = 2'b01;
    localparam WAIT_V      = 2'b10;
    localparam PACE_V      = 2'b11;

    reg [1:0] next_state;

    // State register
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            state <= IDLE;
        else
            state <= next_state;
    end

    // Next state logic
    always_comb begin
        next_state = state;
        case (state)
            IDLE: begin
                if (timer_expired && pacing_mode != 2'b00)
                    next_state = PACE_A;
                else if (atrial_sense && pacing_mode[0])
                    next_state = WAIT_V;
            end
            PACE_A: begin
                next_state = WAIT_V;
            end
            WAIT_V: begin
                if (timer_expired)
                    next_state = PACE_V;
                else if (vent_sense)
                    next_state = IDLE;
            end
            PACE_V: begin
                next_state = IDLE;
            end
            default: next_state = IDLE;
        endcase
    end

    // Output logic (Moore-style, registered)
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            pace_a_out  <= 1'b0;
            pace_v_out  <= 1'b0;
            timer_start <= 1'b0;
            timer_clear <= 1'b0;
        end else begin
            pace_a_out  <= 1'b0;
            pace_v_out  <= 1'b0;
            timer_start <= 1'b0;
            timer_clear <= 1'b0;

            case (next_state)
                IDLE: begin
                    timer_clear <= 1'b1;
                    timer_start <= 1'b1;
                end
                PACE_A: begin
                    pace_a_out <= 1'b1;
                end
                WAIT_V: begin
                    timer_start <= 1'b1;
                end
                PACE_V: begin
                    pace_v_out <= 1'b1;
                end
            endcase
        end
    end

endmodule
```

---

## 5.3.10 — If-Else vs Case Synthesis

| Structure | Infers | Delay |
|-----------|--------|-------|
| `if-else` chain | Priority logic | Depends on depth |
| `case` (full) | Parallel MUX | Single level |
| `casez` with don't-cares | Optimized MUX | Depends on matches |
| `unique case` | Parallel MUX (SV) | Single level |
| `priority case` | Priority logic (SV) | Linear |

---

## 5.3.11 — Best Practices

1. **Always include `default`** — prevents latches and handles unexpected states
2. **Use `case` for parallel decisions** — `if-else` implies priority
3. **Use `casez` for don't-care patterns** — cleaner than nested `if`
4. **Use `unique case`** in SystemVerilog — tells tool cases are exclusive
5. **Avoid `casex`** — ambiguous x/z matching causes bugs
6. **Default all outputs** at the top of always blocks
7. **Complete all branches** — no missing cases
8. **Keep nesting < 4 levels** — readability and synthesis quality
9. **Register outputs** of complex combinational logic — timing closure
10. **Check for priority inference** — do you actually need priority?

---

## 5.3.12 — References

- IEEE Std 1364-2005, Section 4.7 — Procedural Conditional Statements
- IEEE Std 1800-2017, Section 12.4 — Conditional and Case Statements
- iPACE-CHIP RTL Coding Guidelines, Section 3.4
