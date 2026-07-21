# Parameters and Generic Programming

## 5.4.2 — Overview

SystemVerilog enhances Verilog's `parameter` with `localparam`, `parameterized
classes`, and `type parameters`. Proper parameterization makes modules reusable,
configurable, and maintainable. For iPACE-CHIP, parameterized designs enable
the same RTL to support multiple pacemaker variants (single-chamber,
dual-chamber, biventricular) with different ADC widths, timer sizes, and
channel counts.

---

## 5.4.3 — Verilog-2001 Parameters

### Module Parameters

```systemverilog
module pacing_timer #(
    parameter WIDTH      = 16,
    parameter MAX_COUNT  = 16'hFFFF,
    parameter RESET_VAL  = 16'h0000
)(
    input  wire                clk,
    input  wire                rst_n,
    input  wire                enable,
    input  wire [WIDTH-1:0]    limit,
    output reg  [WIDTH-1:0]    count,
    output reg                 done
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count <= RESET_VAL;
            done  <= 1'b0;
        end else if (enable) begin
            if (count == limit) begin
                count <= RESET_VAL;
                done  <= 1'b1;
            end else begin
                count <= count + 1'b1;
                done  <= 1'b0;
            end
        end
    end
endmodule
```

### Parameter Override at Instantiation

```systemverilog
// Override parameters
pacing_timer #(
    .WIDTH(32),
    .MAX_COUNT(32'hFFFFFFFF),
    .RESET_VAL(32'h00000000)
) u_32bit_timer (
    .clk    (clk),
    .rst_n  (rst_n),
    .enable (timer_en),
    .limit  (timer_limit),
    .count  (timer_count),
    .done   (timer_done)
);
```

### defparam (Legacy — Avoid)

```systemverilog
// Legacy parameter override — DO NOT USE
defparam u_timer.WIDTH = 32;
// Difficult to trace, error-prone
```

---

## 5.4.4 — Local Parameters

```systemverilog
module state_machine (
    input  wire       clk,
    input  wire       rst_n,
    input  wire [1:0] mode,
    output reg  [2:0] action
);

    // States as localparams — not overridable from outside
    localparam S_IDLE    = 3'b000;
    localparam S_PACE    = 3'b001;
    localparam S_SENSE   = 3'b010;
    localparam S_TELEM   = 3'b011;
    localparam S_SLEEP   = 3'b100;
    localparam S_FAULT   = 3'b111;

    // Derived constants
    localparam NUM_STATES = 6;
    localparam STATE_WIDTH = $clog2(NUM_STATES);

    reg [STATE_WIDTH-1:0] state, next_state;

    // ... state machine logic
endmodule
```

---

## 5.4.5 — SystemVerilog Type Parameters

### Parameterized Types

```systemverilog
module data_fifo #(
    parameter type DATA_T = logic [7:0],
    parameter int  DEPTH  = 16,
    parameter int  ALMOST_FULL = 14
)(
    input  logic    clk,
    input  logic    rst_n,
    input  logic    wr_en,
    input  DATA_T   wr_data,
    output logic    full,
    output logic    almost_full,
    input  logic    rd_en,
    output DATA_T   rd_data,
    output logic    empty
);

    DATA_T mem [0:DEPTH-1];
    logic [$clog2(DEPTH)-1:0] wr_ptr, rd_ptr;
    logic [$clog2(DEPTH):0]   count;

    assign full       = (count == DEPTH);
    assign almost_full = (count >= ALMOST_FULL);
    assign empty      = (count == 0);

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            wr_ptr <= '0;
            rd_ptr <= '0;
            count  <= '0;
        end else begin
            if (wr_en && !full) begin
                mem[wr_ptr] <= wr_data;
                wr_ptr <= wr_ptr + 1;
            end
            if (rd_en && !empty) begin
                rd_ptr <= rd_ptr + 1;
            end
            if (wr_en && !full && !(rd_en && !empty))
                count <= count + 1;
            else if (rd_en && !empty && !(wr_en && !full))
                count <= count - 1;
        end
    end

    assign rd_data = mem[rd_ptr];

endmodule
```

### Using Type Parameters

```systemverilog
// 8-bit FIFO
data_fifo #(
    .DATA_T (logic [7:0]),
    .DEPTH  (16)
) u_byte_fifo (...);

// 12-bit FIFO for ADC data
data_fifo #(
    .DATA_T (logic [11:0]),
    .DEPTH  (64)
) u_adc_fifo (...);

// 32-bit FIFO for telemetry
data_fifo #(
    .DATA_T (logic [31:0]),
    .DEPTH  (8)
) u_telem_fifo (...);
```

---

## 5.4.6 — Localparam for Derived Constants

```systemverilog
module configurable_adc_interface #(
    parameter ADC_WIDTH    = 12,
    parameter NUM_CHANNELS = 4,
    parameter FIFO_DEPTH   = 64
)(
    input  logic                                    clk,
    input  logic                                    rst_n,
    input  logic [NUM_CHANNELS-1:0][ADC_WIDTH-1:0] adc_data,
    input  logic [NUM_CHANNELS-1:0]                adc_valid,
    output logic [ADC_WIDTH-1:0]                   selected_data,
    output logic                                    data_valid
);

    // Derived localparams
    localparam CHANNEL_ADDR_W = $clog2(NUM_CHANNELS);
    localparam FIFO_WIDTH     = ADC_WIDTH;
    localparam FIFO_ALMOST_FULL = FIFO_DEPTH - 2;

    // Internal signals using derived widths
    logic [CHANNEL_ADDR_W-1:0] channel_sel;
    logic [$clog2(FIFO_DEPTH)-1:0] fifo_count;
    logic fifo_full, fifo_empty;

    // Channel selector
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            channel_sel <= '0;
        else if (adc_valid[channel_sel])
            channel_sel <= channel_sel + 1;
    end

    assign selected_data = adc_data[channel_sel];
    assign data_valid    = adc_valid[channel_sel];

endmodule
```

---

## 5.4.7 — Parameterized Pacemaker Variant

```systemverilog
module ipace_pacing_core #(
    parameter MODE           = "VVI",     // VVI, AAI, DDD
    parameter ADC_WIDTH      = 12,
    parameter TIMER_WIDTH    = 16,
    parameter NUM_CHANNELS   = 1,
    parameter HAS_TELEMETRY  = 1
)(
    input  logic                          clk,
    input  logic                          rst_n,
    input  logic [ADC_WIDTH-1:0]          adc_data [NUM_CHANNELS],
    input  logic                          adc_valid,
    output logic                          pace_out,
    output logic [7:0]                    amplitude,
    output logic                          telemetry_active
);

    // Mode-specific localparams
    localparam IS_DDD     = (MODE == "DDD");
    localparam IS_AAI     = (MODE == "AAI");
    localparam IS_VVI     = (MODE == "VVI");

    // Timer widths
    localparam REFRACTORY_WIDTH = TIMER_WIDTH;
    localparam PULSE_WIDTH_MAX  = (1 << 8) - 1;  // 8-bit pulse width

    // Internal wires
    logic timer_expired;
    logic sense_event;
    logic refractory_active;

    pacing_timer #(
        .WIDTH     (TIMER_WIDTH),
        .MAX_COUNT ({TIMER_WIDTH{1'b1}})
    ) u_timer (
        .clk     (clk),
        .rst_n   (rst_n),
        .enable  (1'b1),
        .limit   (timer_limit),
        .count   (),
        .done    (timer_expired)
    );

    // Mode-conditional sensing
    generate
        if (NUM_CHANNELS > 0) begin : gen_sense_ch0
            sensing_channel #(.WIDTH(ADC_WIDTH)) u_sense0 (
                .clk       (clk),
                .rst_n     (rst_n),
                .adc_data  (adc_data[0]),
                .adc_valid (adc_valid),
                .sense_out (sense_event)
            );
        end
    endgenerate

    // Telemetry (optional)
    generate
        if (HAS_TELEMETRY) begin : gen_telem
            telemetry_controller u_telem (
                .clk     (clk),
                .rst_n   (rst_n),
                .active  (telemetry_active)
            );
        end else begin : gen_no_telem
            assign telemetry_active = 1'b0;
        end
    endgenerate

endmodule
```

---

## 5.4.8 — Generate-for with Parameters

```systemverilog
module parameterized_adder_tree #(
    parameter NUM_INPUTS = 8,
    parameter DATA_WIDTH = 12
)(
    input  logic [NUM_INPUTS-1:0][DATA_WIDTH-1:0] inputs,
    output logic [DATA_WIDTH+$clog2(NUM_INPUTS)-1:0] sum
);

    // Localparams for intermediate widths
    localparam NUM_STAGES = $clog2(NUM_INPUTS);
    localparam SUM_WIDTH  = DATA_WIDTH + NUM_STAGES;

    // Generate tree of adders
    logic [SUM_WIDTH-1:0] stage [0:NUM_STAGES];

    genvar i;
    generate
        for (i = 0; i < NUM_STAGES; i = i + 1) begin : gen_level
            localparam LOCAL_NUM = (i == 0) ?
                NUM_INPUTS : (NUM_INPUTS >> i);
            // Simplified: actual implementation would be more complex
        end
    endgenerate

    assign sum = stage[NUM_STAGES-1];

endmodule
```

---

## 5.4.9 — Preprocessor vs Parameters

| Feature | `define | `parameter |
|---------|---------|-----------|
| Scope | Global (file-level) | Module-level |
| Override | `define override | `parameter override |
| Synthesis | Preprocessor | Synthesizable |
| Use case | File-level constants | Module configuration |

```systemverilog
// Preprocessor — global, not synthesizable
`define ADC_WIDTH 12
`define TIMER_MAX 16'hFFFF

module my_module (
    input wire [`ADC_WIDTH-1:0] data  // expanded by preprocessor
);

// Parameter — module-level, synthesizable
parameter WIDTH = 12;
wire [WIDTH-1:0] data;  // parameter-based width
endmodule
```

---

## 5.4.10 — Best Practices

1. **Use `parameter`** for all configurable values — never hardcode
2. **Use `localparam`** for derived constants and FSM states
3. **Use `parameter type`** for type-generic modules (SystemVerilog)
4. **Document parameters** — purpose, valid ranges, default values
5. **Use `$clog2()`** for automatic address width calculation
6. **Avoid `defparam`** — use inline parameter override only
7. **Use generate** with parameters for conditional instantiation
8. **Parameterize at top level** — propagate through hierarchy
9. **Validate parameters** — use `initial` checks or assertions
10. **One parameter per design decision** — separate concerns

---

## 5.4.11 — References

- IEEE Std 1800-2017, Section 6.2 — Parameterized Values
- SystemVerilog for Verification, Chris Spear, Chapter 5
- iPACE-CHIP Configuration Register Specification
