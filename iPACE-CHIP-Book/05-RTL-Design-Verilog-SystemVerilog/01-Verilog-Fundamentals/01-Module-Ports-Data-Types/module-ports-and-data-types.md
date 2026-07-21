# Module Ports and Data Types in Verilog

## 5.1.1 — Overview

Every digital design in Verilog begins with a **module**. A module encapsulates a
functional block—combinational logic, a sequential controller, an I/O pad—and
exposes its interface through **ports**. For the iPACE-CHIP pacemaker ASIC, every
subsystem from the pacing timer to the telemetry encoder is modeled as one or
more Verilog modules. Mastering modules, ports, and data types is the
prerequisite for every RTL discussion that follows.

This chapter covers:

- Module declaration syntax (IEEE 1364-2005 / IEEE 1800-2017)
- Port direction, width, and type semantics
- Wire, reg, logic, and other data types
- Parameterized and typed port lists
- Pacemaker-relevant coding examples

---

## 5.1.2 — Module Declaration Syntax

### Basic Template

```verilog
module module_name (
    // Port list
    input  wire        clk,
    input  wire        rst_n,
    output reg  [7:0]  data_out,
    inout  wire        sda
);
    // Internal declarations
    // Body
endmodule
```

A module is delimited by `module` … `endmodule`. The port list appears in
parentheses immediately after the module name. Ports can be declared inline
(ANSI style, preferred) or separately (non-ANSI, legacy).

### Non-ANSI Port Declaration (Legacy)

```verilog
module pacing_timer(clk, rst_n, timer_start, timer_done, count_out);

    input        clk;
    input        rst_n;
    input        timer_start;
    output       timer_done;
    output [15:0] count_out;

    // body
endmodule
```

Non-ANSI style separates the port list from the type declarations. Modern
projects should always use ANSI-style for clarity.

---

## 5.1.3 — Port Directions

Verilog defines three port directions:

| Direction | Keyword | Description |
|-----------|---------|-------------|
| Input | `input` | Driven by the outside; read inside the module |
| Output | `output` | Driven inside the module; read by the outside |
| Bidirectional | `inout` | Driven by either side; used for tri-state buses |

### Output Port Types

Output ports can be declared as `wire` (default for continuous assignments) or
`reg` (for procedural assignments in always blocks):

```verilog
// Combinational output — wire
output wire [7:0] adc_data;       // driven by assign

// Sequential output — reg
output reg  [7:0] sensor_reading; // driven in always @(posedge clk)
```

### Inout Ports

Tri-state buses in pacemaker SPI or I²C interfaces:

```verilog
module i2c_master (
    input  wire clk,
    input  wire rst_n,
    output wire sda_out,
    input  wire sda_in,
    output wire sda_oe,    // output enable
    output wire scl
);
    // sda is split into three signals for synthesizable tri-state control
endmodule
```

> **Pacemaker Design Note:** For ASIC synthesis, tri-state `inout` ports should
> only be used at the pad level. Internal logic should use separate `output`,
> `input`, and `output enable` signals for synthesis portability.

---

## 5.1.4 — Wire Data Type

A `wire` represents a physical connection between gates or modules. Wires
cannot store values; they are continuously driven.

```verilog
wire        heartbeat;       // single-bit wire
wire [7:0]  adc_bus;         // 8-bit bus
wire [31:0] telemetry_word;  // 32-bit bus
```

### Key Properties

| Property | Value |
|----------|-------|
| Default value | `x` (unknown) |
| Can be assigned with | `assign`, port connection, gate instance |
| Can appear in `always` | Only on RHS (right-hand side) |
| Multiple drivers | Creates resolution (multiple-driver wire) |

### Continuous Assignment to Wire

```verilog
wire [7:0] adc_data;
assign adc_data = adc_raw[11:4]; // upper 8 bits of 12-bit ADC
```

---

## 5.1.5 — Reg Data Type

A `reg` holds a value from one procedural assignment until the next. Despite the
name, `reg` does not imply a hardware register—it can model combinational logic
when used correctly.

```verilog
reg [7:0]  mode_register;    // 8-bit register
reg        pacing_enable;    // single-bit register
reg [31:0] timer_counter;    // 32-bit counter
```

### Key Properties

| Property | Value |
|----------|-------|
| Default value | `x` (unknown) |
| Can be assigned with | Procedural assignment inside `always`, `initial` |
| Can appear in `always` | Both LHS and RHS |
| Inferred as flip-flop | Only when assigned on clock edge in sensitivity list |

### Reg in Combinational Always Block

```verilog
reg [7:0] threshold;
always @(*) begin
    if (sensing_mode == 2'b01)
        threshold = 8'd128;
    else
        threshold = 8'd64;
end
// threshold is combinational — no flip-flop inferred
```

### Reg in Sequential Always Block

```verilog
reg [15:0] pacing_count;
always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        pacing_count <= 16'd0;
    else if (timer_enable)
        pacing_count <= pacing_count + 1'b1;
end
// pacing_count is a 16-bit register (flip-flops inferred)
```

---

## 5.1.6 — Logic Data Type (SystemVerilog)

SystemVerilog introduces `logic` as a 4-state type that unifies `wire` and
`reg`. A `logic` signal can be driven by either continuous or procedural
assignment, but only by a single driver (no multiple-driver resolution).

```verilog
logic       clk;           // replaces wire
logic [7:0] data_bus;      // replaces wire [7:0] or reg [7:0]
logic       pacing_pulse;  // single driver
```

### When to Use Logic vs Wire

| Situation | Use |
|-----------|-----|
| Single-driven signal | `logic` |
| Port of module (synthesis) | `wire` for input/output, `logic` acceptable in SV |
| Multiple drivers (tri-state) | `wire` (resolution needed) |
| Interface signals | `logic` (inside SV interfaces) |

> **iPACE-CHIP Convention:** All new SystemVerilog code uses `logic`. Legacy
> Verilog files retain `wire`/`reg` for compatibility.

---

## 5.1.7 — Signed and Unsigned Types

Both `wire`, `reg`, and `logic` are unsigned by default. Verilog-2001 adds
explicit signed types:

```verilog
reg signed [7:0]    temperature;    // -128 to +127
reg        [7:0]    adc_unsigned;   // 0 to 255

wire signed [15:0]  signed_product;
wire        [15:0]  unsigned_product;
```

### Sign Extension

```verilog
reg signed [7:0]  a = -8'sd10;
reg signed [15:0] b;
assign b = { {8{a[7]}}, a };  // sign-extend 8-bit to 16-bit
// or equivalently:
assign b = $signed(a);        // SystemVerilog
```

### Pacemaker Example — Signed ADC Processing

```verilog
// Differential ADC reading: result can be negative
reg signed [11:0] adc_diff;
reg signed [11:0] baseline_offset;

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        adc_diff      <= 12'sd0;
        baseline_offset <= 12'sd0;
    end else begin
        adc_diff        <= $signed(adc_plus) - $signed(adc_minus);
        baseline_offset <= adc_diff - baseline_cal;
    end
end
```

---

## 5.1.8 — Integer, Time, and Real Types

### Integer

```verilog
integer i;  // 32-bit signed; useful for loop counters in testbenches
for (i = 0; i < 256; i = i + 1) begin
    // testbench stimulus
end
```

> **Synthesis Warning:** `integer` is rarely used in synthesizable RTL. Use
> explicit-width `reg`/`logic` for hardware.

### Time

```verilog
time current_time;  // 64-bit; testbench only
current_time = $time;
```

### Real

```verilog
real voltage_level;  // testbench only; used for analog modeling
voltage_level = 1.2 * voltage_reference;
```

---

## 5.1.9 — Arrays

### One-Dimensional Arrays

```verilog
reg [7:0] memory [0:255];  // 256 bytes of storage
reg [7:0] lookup_table [0:15];  // 16-entry lookup
```

### Multi-Dimensional Arrays

```verilog
reg [7:0] register_file [0:31][0:7];  // 32 x 8 matrix
```

### Array Usage in Pacemaker

```verilog
// Telemetry data buffer — stores last 64 samples
reg [11:0] telemetry_buffer [0:63];
reg [5:0]  write_ptr;

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        write_ptr <= 6'd0;
    end else if (sample_valid) begin
        telemetry_buffer[write_ptr] <= adc_reading;
        write_ptr <= write_ptr + 1'b1;
    end
end
```

### Memory Initialization

```verilog
reg [7:0] config_rom [0:15];

initial begin
    $readmemh("pace_config.hex", config_rom);
end

// Or inline initialization
initial begin
    config_rom[0] = 8'hA0;  // threshold high byte
    config_rom[1] = 8'h3C;  // threshold low byte
    config_rom[2] = 8'h0F;  // timer prescaler
end
```

---

## 5.1.10 — Parameters and Local Parameters

Parameters allow compile-time constants that make modules reusable.

```verilog
module pacing_timer #(
    parameter DATA_WIDTH = 16,
    parameter TIMER_MAX  = 16'hFFFF
)(
    input  wire                    clk,
    input  wire                    rst_n,
    input  wire                    enable,
    output reg  [DATA_WIDTH-1:0]  count,
    output reg                     timer_done
);

    localparam IDLE    = 2'b00;
    localparam RUNNING = 2'b01;
    localparam DONE    = 2'b10;

    reg [1:0] state;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count     <= {DATA_WIDTH{1'b0}};
            timer_done <= 1'b0;
            state     <= IDLE;
        end else begin
            case (state)
                IDLE: begin
                    timer_done <= 1'b0;
                    if (enable) begin
                        count <= {DATA_WIDTH{1'b0}};
                        state <= RUNNING;
                    end
                end
                RUNNING: begin
                    count <= count + 1'b1;
                    if (count == TIMER_MAX) begin
                        timer_done <= 1'b1;
                        state      <= DONE;
                    end
                end
                DONE: begin
                    state <= IDLE;
                end
                default: state <= IDLE;
            endcase
        end
    end
endmodule
```

### Overriding Parameters

```verilog
// At instantiation time
pacing_timer #(
    .DATA_WIDTH(32),
    .TIMER_MAX(32'hFFFFFFFF)
) u_pacing_timer (
    .clk(clk),
    .rst_n(rst_n),
    .enable(start_timer),
    .count(timer_count),
    .timer_done(timer_expired)
);
```

---

## 5.1.11 — Comprehensive Pacemaker Module Example

The following module demonstrates all port and data type concepts together:

```verilog
module adc_sensing_controller #(
    parameter ADC_WIDTH    = 12,
    parameter SAMPLE_DEPTH = 64,
    parameter THRESHOLD_W  = 12
)(
    // System
    input  wire                     clk,           // 32 kHz system clock
    input  wire                     rst_n,         // active-low reset

    // ADC interface
    input  wire                     adc_valid,
    input  wire [ADC_WIDTH-1:0]     adc_data,

    // Configuration
    input  wire [THRESHOLD_W-1:0]   high_threshold,
    input  wire [THRESHOLD_W-1:0]   low_threshold,
    input  wire [1:0]               sense_mode,   // 00=off,01=on-demand,10=continuous

    // Outputs
    output reg                      event_detected,
    output reg  [ADC_WIDTH-1:0]     peak_value,
    output reg  [5:0]               sample_count,
    output wire [ADC_WIDTH-1:0]     latest_sample,
    output wire                     sensing_active
);

    // Internal signals
    reg  [ADC_WIDTH-1:0] sample_buffer [0:SAMPLE_DEPTH-1];
    reg  [5:0]           read_ptr;
    wire  signed [ADC_WIDTH-1:0] adc_signed;

    // State encoding
    localparam S_IDLE      = 2'b00;
    localparam S_SENSING   = 2'b01;
    localparam S_EVENT     = 2'b10;
    localparam S_WAIT      = 2'b11;

    reg [1:0] state, next_state;

    // Continuous assignments
    assign adc_signed      = $signed(adc_data);
    assign latest_sample   = sample_buffer[read_ptr];
    assign sensing_active  = (state == S_SENSING) || (state == S_EVENT);

    // Sequential buffer write
    integer i;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            sample_count <= 6'd0;
            read_ptr     <= 6'd0;
            for (i = 0; i < SAMPLE_DEPTH; i = i + 1)
                sample_buffer[i] <= {ADC_WIDTH{1'b0}};
        end else if (adc_valid && state == S_SENSING) begin
            sample_buffer[write_ptr] <= adc_data;
            sample_count <= sample_count + 1'b1;
            read_ptr     <= write_ptr;
        end
    end

    // Peak detection
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            peak_value      <= {ADC_WIDTH{1'b0}};
            event_detected <= 1'b0;
        end else if (adc_valid && state == S_SENSING) begin
            if (adc_data > peak_value)
                peak_value <= adc_data;

            if (adc_data > high_threshold) begin
                event_detected <= 1'b1;
            end else if (adc_data < low_threshold) begin
                event_detected <= 1'b0;
            end
        end
    end

    // State machine
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            state <= S_IDLE;
        else
            state <= next_state;
    end

    always @(*) begin
        next_state = state;
        case (state)
            S_IDLE:
                if (sense_mode != 2'b00)
                    next_state = S_SENSING;
            S_SENSING:
                if (event_detected)
                    next_state = S_EVENT;
                else if (sense_mode == 2'b00)
                    next_state = S_IDLE;
            S_EVENT:
                next_state = S_WAIT;
            S_WAIT:
                if (!event_detected)
                    next_state = S_SENSING;
                else if (sense_mode == 2'b00)
                    next_state = S_IDLE;
            default:
                next_state = S_IDLE;
        endcase
    end

    reg [5:0] write_ptr;

endmodule
```

---

## 5.1.12 — Data Type Summary Table

| Type | Width | Default | Driver | Storage | Synthesis |
|------|-------|---------|--------|---------|-----------|
| `wire` | 1 | `x` | `assign` / gate | No | Physical net |
| `reg` | 1 | `x` | Procedural | Yes | FF or Latch |
| `logic` (SV) | 1 | `x` | Either (1 driver) | Yes | FF or Latch |
| `integer` | 32 | `x` | Procedural | Yes | Avoid in RTL |
| `time` | 64 | `0` | `$time` | Yes | TB only |
| `real` | — | `0.0` | Assignment | Yes | TB only |

---

## 5.1.13 — Best Practices for iPACE-CHIP

1. **Always use ANSI-style port declarations** — makes interfaces self-documenting
2. **Use explicit widths** — never rely on defaults; always specify `[N-1:0]`
3. **Use `logic` in SystemVerilog** — cleaner semantics, single-driver enforcement
4. **Use `localparam` for FSM states** — readable, grep-friendly
5. **Parameterize all configurable values** — timer widths, thresholds, depths
6. **Initialize all `reg` in reset blocks** — avoid simulation mismatches
7. **Separate `inout` into `output`, `input`, `oe`** — synthesis portability
8. **Use `$signed()` for arithmetic comparisons** — prevents unsigned comparison bugs
9. **One module per functional unit** — maintainability and reuse
10. **Prefix ports with descriptive names** — `adc_data`, `timer_count`, `pacing_pulse`

---

## 5.1.14 — References

- IEEE Std 1364-2005, *Verilog Hardware Description Language*
- IEEE Std 1800-2017, *SystemVerilog*
- Samir Palnitkar, *Verilog HDL: A Guide to Digital Design and Synthesis*, 2nd Ed.
- iPACE-CHIP Architecture Specification, Section 4: Digital Subsystem Interfaces
