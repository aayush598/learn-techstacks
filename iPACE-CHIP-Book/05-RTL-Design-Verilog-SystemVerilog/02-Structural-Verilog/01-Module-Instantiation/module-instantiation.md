# Module Instantiation in Verilog

## 5.2.1 — Overview

Structural Verilog describes hardware as a **hierarchy of interconnected
modules**. Module instantiation creates copies of modules and connects them
via named or ordered port mapping. For iPACE-CHIP, the digital top level
instantiates the pacing controller, sensing ADC interface, telemetry encoder,
power controller, and SPI peripheral bus as structural instances.

---

## 5.2.2 — Instantiation Syntax

### Named Port Mapping (Preferred)

```verilog
module_name instance_name (
    .port_name_a(signal_a),
    .port_name_b(signal_b),
    .port_name_c(signal_c)
);
```

### Ordered Port Mapping (Legacy)

```verilog
module_name instance_name (signal_a, signal_b, signal_c);
```

> **iPACE-CHIP Rule:** Named port mapping is mandatory. Ordered mapping is
> prohibited because reordering ports silently creates wrong connections.

---

## 5.2.3 — Basic Instantiation Example

```verilog
// Module declaration
module d_flip_flop (
    input  wire clk,
    input  wire rst_n,
    input  wire d,
    output reg  q
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) q <= 1'b0;
        else        q <= d;
    end
endmodule

// Instantiation in parent module
module shift_register (
    input  wire clk,
    input  wire rst_n,
    input  wire serial_in,
    output wire serial_out
);
    wire ff1_q, ff2_q, ff3_q;

    d_flip_flop u_ff0 (
        .clk   (clk),
        .rst_n (rst_n),
        .d     (serial_in),
        .q     (ff1_q)
    );

    d_flip_flop u_ff1 (
        .clk   (clk),
        .rst_n (rst_n),
        .d     (ff1_q),
        .q     (ff2_q)
    );

    d_flip_flop u_ff2 (
        .clk   (clk),
        .rst_n (rst_n),
        .d     (ff2_q),
        .q     (ff3_q)
    );

    d_flip_flop u_ff3 (
        .clk   (clk),
        .rst_n (rst_n),
        .d     (ff3_q),
        .q     (serial_out)
    );

endmodule
```

---

## 5.2.4 — Parameterized Instantiation

### Module with Parameters

```verilog
module counter #(
    parameter WIDTH = 16
)(
    input  wire             clk,
    input  wire             rst_n,
    input  wire             enable,
    output reg  [WIDTH-1:0] count,
    output wire             overflow
);
    assign overflow = (count == {WIDTH{1'b1}}) && enable;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            count <= {WIDTH{1'b0}};
        else if (enable)
            count <= count + 1'b1;
    end
endmodule
```

### Instantiating with Overridden Parameters

```verilog
module timer_subsystem (
    input  wire clk,
    input  wire rst_n,
    output wire [15:0] free_running_count,
    output wire [7:0]  prescaler_count,
    output wire        tick_1hz
);

    // 16-bit free-running counter (default width)
    counter #(
        .WIDTH(16)
    ) u_free_counter (
        .clk     (clk),
        .rst_n   (rst_n),
        .enable  (1'b1),
        .count   (free_running_count),
        .overflow()
    );

    // 8-bit prescaler
    counter #(
        .WIDTH(8)
    ) u_prescaler (
        .clk     (clk),
        .rst_n   (rst_n),
        .enable  (1'b1),
        .count   (prescaler_count),
        .overflow(tick_1hz)
    );

endmodule
```

---

## 5.2.5 — Hierarchical Name References

Signals in child modules are accessible via hierarchical paths in
simulation (not synthesis).

```verilog
// Access internal signal of instance
wire [15:0] timer_count = u_timer_subsystem.u_free_counter.count;

// In testbench
initial begin
    $monitor("Count: %0d", u_dut.u_timer.count);
end

// Force value in testbench (simulation only)
initial begin
    force u_dut.u_adc_controller.adc_data = 12'h800;
    #100;
    release u_dut.u_adc_controller.adc_data;
end
```

---

## 5.2.6 — Module Array Instantiation

### Generate-for — Array of Identical Instances

```verilog
// 8-channel analog comparator array
module comparator_array #(
    parameter WIDTH = 12,
    parameter CHANNELS = 8
)(
    input  wire [CHANNELS-1:0][WIDTH-1:0] inputs,
    input  wire [CHANNELS-1:0][WIDTH-1:0] thresholds,
    output wire [CHANNELS-1:0]             results
);

    genvar i;
    generate
        for (i = 0; i < CHANNELS; i = i + 1) begin : gen_comparators
            assign results[i] = (inputs[i] > thresholds[i]);
        end
    endgenerate

endmodule
```

### Pacemaker: Multi-Sensor Comparators

```verilog
// 4 sensing channels, each with independent threshold
module multi_sense_comparator #(
    parameter ADC_WIDTH    = 12,
    parameter NUM_CHANNELS = 4
)(
    input  wire                                    clk,
    input  wire                                    rst_n,
    input  wire [NUM_CHANNELS-1:0][ADC_WIDTH-1:0] adc_data,
    input  wire [NUM_CHANNELS-1:0][ADC_WIDTH-1:0] thresholds,
    input  wire [NUM_CHANNELS-1:0]                channel_enable,
    output wire [NUM_CHANNELS-1:0]                threshold_exceeded
);

    wire [NUM_CHANNELS-1:0] comparison_result;

    genvar ch;
    generate
        for (ch = 0; ch < NUM_CHANNELS; ch = ch + 1) begin : gen_threshold
            assign comparison_result[ch] = (adc_data[ch] > thresholds[ch])
                                         && channel_enable[ch];
        end
    endgenerate

    // Register outputs
    reg [NUM_CHANNELS-1:0] threshold_exceeded_r;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            threshold_exceeded_r <= {NUM_CHANNELS{1'b0}};
        else
            threshold_exceeded_r <= comparison_result;
    end

    assign threshold_exceeded = threshold_exceeded_r;

endmodule
```

---

## 5.2.7 — Generate-if — Conditional Instantiation

```verilog
module configurable_timer #(
    parameter USE_PRESCALER = 1,
    parameter TIMER_WIDTH   = 16
)(
    input  wire                     clk,
    input  wire                     rst_n,
    input  wire                     enable,
    input  wire [TIMER_WIDTH-1:0]   timer_limit,
    output reg                      timer_done
);

    wire tick;

    generate
        if (USE_PRESCALER) begin : gen_with_prescaler
            // Prescaler divides clock by 32
            reg [4:0] prescaler;
            assign tick = (prescaler == 5'd31);
            always @(posedge clk or negedge rst_n) begin
                if (!rst_n) prescaler <= 5'd0;
                else        prescaler <= prescaler + 1'b1;
            end
        end else begin : gen_no_prescaler
            assign tick = 1'b1;  // direct clock
        end
    endgenerate

    // Main timer
    reg [TIMER_WIDTH-1:0] count;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count     <= {TIMER_WIDTH{1'b0}};
            timer_done <= 1'b0;
        end else if (enable && tick) begin
            if (count == timer_limit) begin
                timer_done <= 1'b1;
                count      <= {TIMER_WIDTH{1'b0}};
            end else begin
                count <= count + 1'b1;
            end
        end
    end

endmodule
```

---

## 5.2.8 — Unconnected Ports

```verilog
// Leaving output unconnected
wire dummy;
d_flip_flop u_ff (
    .clk   (clk),
    .rst_n (rst_n),
    .d     (data),
    .q     ()          // unconnected output
);

// Or use open port (SystemVerilog)
d_flip_flop u_ff (
    .clk   (clk),
    .rst_n (rst_n),
    .d     (data),
    .q     ()          // open
);
```

---

## 5.2.9 — Instance Naming Conventions

| Prefix | Meaning | Example |
|--------|---------|---------|
| `u_` | Module instance | `u_pacing_timer` |
| `gen_` | Generate block | `gen_comparators` |
| `clk_` | Clock domain | `clk_domain_a` |
| `i_` | Input port | `i_adc_data` |
| `o_` | Output port | `o_pace_out` |
| `io_` | Bidirectional | `io_sda` |
| `n_` | Active-low | `n_cs` (chip select, active low) |

---

## 5.2.10 — Pacemaker Digital Top: Structural Instantiation

```verilog
module ipace_digital_top #(
    parameter ADC_WIDTH      = 12,
    parameter TIMER_WIDTH    = 16,
    parameter SPI_CLK_DIV    = 4
)(
    // System
    input  wire                    clk_32khz,
    input  wire                    rst_n,
    input  wire                    power_on_reset,

    // ADC interface
    input  wire [ADC_WIDTH-1:0]    adc_atrial,
    input  wire [ADC_WIDTH-1:0]    adc_ventricular,
    input  wire                    adc_valid,

    // Pacing output
    output wire                    atrial_pulse,
    output wire                    ventricular_pulse,
    output wire [7:0]              pulse_amplitude,
    output wire [15:0]             pulse_width,

    // SPI slave (to telemetry ASIC)
    output wire                    spi_miso,
    input  wire                    spi_mosi,
    input  wire                    spi_sclk,
    input  wire                    spi_cs_n,

    // Interrupts
    output wire                    irq_pacing,
    output wire                    irq_sensing,
    output wire                    irq_telemetry
);

    // Internal wires
    wire        timer_expired;
    wire        atrial_sense;
    wire        vent_sense;
    wire [7:0]  config_byte;
    wire        telemetry_active;
    wire        low_battery;

    // Pacing controller
    pacing_controller u_pacing (
        .clk              (clk_32khz),
        .rst_n            (rst_n),
        .timer_expired    (timer_expired),
        .atrial_sense     (atrial_sense),
        .vent_sense       (vent_sense),
        .config           (config_byte),
        .atrial_pulse     (atrial_pulse),
        .ventricular_pulse(ventricular_pulse),
        .pulse_amplitude  (pulse_amplitude),
        .pulse_width      (pulse_width)
    );

    // Sensing ADC interface
    sensing_adc_interface #(
        .ADC_WIDTH(ADC_WIDTH)
    ) u_sensing (
        .clk             (clk_32khz),
        .rst_n           (rst_n),
        .adc_atrial      (adc_atrial),
        .adc_ventricular (adc_ventricular),
        .adc_valid       (adc_valid),
        .atrial_sense    (atrial_sense),
        .vent_sense      (vent_sense),
        .irq_sensing     (irq_sensing)
    );

    // Telemetry controller
    telemetry_controller u_telemetry (
        .clk             (clk_32khz),
        .rst_n           (rst_n),
        .spi_miso        (spi_miso),
        .spi_mosi        (spi_mosi),
        .spi_sclk        (spi_sclk),
        .spi_cs_n        (spi_cs_n),
        .telemetry_active(telemetry_active),
        .irq_telemetry   (irq_telemetry)
    );

    // Power controller
    power_controller u_power (
        .clk           (clk_32khz),
        .rst_n         (rst_n),
        .low_battery   (low_battery),
        .irq_pacing    (irq_pacing)
    );

endmodule
```

---

## 5.2.11 — Best Practices

1. **Always use named port mapping** — never ordered
2. **Use parameters** for configurable values — width, depth, modes
3. **Prefix instances** with `u_` for clarity
4. **Use `generate` blocks** for arrays of instances
5. **Leave no outputs unconnected** intentionally — document with comments
6. **Use hierarchical references** only in testbenches, never in RTL
7. **Name generate blocks** — `gen_xxx` for better error messages
8. **One instance per logical function** — maintainability

---

## 5.2.12 — References

- IEEE Std 1364-2005, Section 12.1 — Module Instantiations
- IEEE Std 1800-2017, Section 23.2 — Generate Constructs
- iPACE-CHIP Architecture Specification, Section 5: Digital Hierarchy
