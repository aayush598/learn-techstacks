# Power Controller RTL Design

## 5.5.4 — Overview

The **power controller** manages the iPACE-CHIP's limited battery budget,
monitors voltage levels, controls power modes, and ensures safe operation
during brownout conditions. With a 10-year battery life target and a 2 μAh
daily budget, every microamp counts. This chapter covers the complete RTL
design of the power management subsystem.

---

## 5.5.5 — Power Requirements

| Parameter | Value | Unit |
|-----------|-------|------|
| Battery Chemistry | Li-Ion | — |
| Nominal Voltage | 3.0 | V |
| Cutoff Voltage | 2.4 | V |
| Full Charge Voltage | 4.2 | V |
| Total Capacity | 120 | mAh |
| Daily Budget | 2 | μAh |
| Clock Frequency | 32.768 | kHz |
| Active Power | 5 | μW |
| Sleep Power | 0.1 | μW |
| Target Lifetime | 10 | years |

---

## 5.5.6 — Power Controller Top Module

```systemverilog
module power_controller #(
    parameter ADC_WIDTH     = 12,
    parameter VOLTAGE_WIDTH = 12
)(
    input  logic                      clk,
    input  logic                      rst_n,

    // Battery monitoring ADC
    output logic                      vmon_start,
    input  logic [ADC_WIDTH-1:0]      vmon_data,
    input  logic                      vmon_eoc,

    // Power control outputs
    output logic                      ldo_enable,
    output logic                      vref_enable,
    output logic                      adc_power_enable,
    output logic                      rf_power_enable,
    output logic                      clk_gate,       // global clock gate

    // Power mode
    input  logic [1:0]                power_mode,     // 00=sleep,01=active,10=low-power,11=emergency

    // Status
    output logic                      battery_low,
    output logic                      battery_critical,
    output logic                      power_good,
    output logic [VOLTAGE_WIDTH-1:0]  battery_voltage,

    // Interrupts
    output logic                      irq_power,

    // Control
    input  logic                      clear_alarm,
    input  logic                      watchdog_reset
);

    // Voltage thresholds (12-bit ADC, 3.3V reference)
    localparam VOLTAGE_FULL     = 12'd3700;  // 4.2V (scaled)
    localparam VOLTAGE_NOMINAL  = 12'd2727;  // 3.0V
    localparam VOLTAGE_LOW      = 12'd2182;  // 2.4V
    localparam VOLTAGE_CRITICAL = 12'd2000;  // 2.2V (shutdown)
    localparam VOLTAGE_HYSTERESIS = 12'd50;  // hysteresis band

    typedef enum logic [2:0] {
        PWR_IDLE     = 3'd0,
        PWR_MEASURE  = 3'd1,
        PWR_EVALUATE = 3'd2,
        PWR_SHUTDOWN = 3'd3,
        PWR_SLEEP    = 3'd4,
        PWR_ACTIVE   = 3'd5
    } power_state_t;

    power_state_t state;
    logic [ADC_WIDTH-1:0] voltage_sample;
    logic [VOLTAGE_WIDTH-1:0] voltage_filtered;
    logic [$clog2(32768)-1:0] measure_timer;
    logic [2:0] consecutive_low;
    logic [2:0] consecutive_critical;

    // Measurement timer (1 second at 32.768 kHz)
    localparam MEASURE_INTERVAL = 32768;

    // Voltage monitor ADC
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            vmon_start <= 1'b0;
            voltage_sample <= '0;
            measure_timer  <= '0;
            state          <= PWR_IDLE;
        end else begin
            case (state)
                PWR_IDLE: begin
                    measure_timer <= measure_timer + 1;
                    if (measure_timer >= MEASURE_INTERVAL - 1) begin
                        state     <= PWR_MEASURE;
                        vmon_start <= 1'b1;
                    end
                end

                PWR_MEASURE: begin
                    vmon_start <= 1'b0;
                    if (vmon_eoc) begin
                        voltage_sample <= vmon_data;
                        state <= PWR_EVALUATE;
                    end
                end

                PWR_EVALUATE: begin
                    // Simple low-pass filter
                    voltage_filtered <= (voltage_filtered + {1'b0, voltage_sample}) >> 1;

                    // Check thresholds
                    if (voltage_filtered < VOLTAGE_CRITICAL)
                        consecutive_critical <= consecutive_critical + 1;
                    else
                        consecutive_critical <= 0;

                    if (voltage_filtered < VOLTAGE_LOW)
                        consecutive_low <= consecutive_low + 1;
                    else if (voltage_filtered > VOLTAGE_LOW + VOLTAGE_HYSTERESIS)
                        consecutive_low <= 0;

                    // State transitions
                    if (consecutive_critical >= 3)
                        state <= PWR_SHUTDOWN;
                    else if (power_mode == 2'b00)
                        state <= PWR_SLEEP;
                    else
                        state <= PWR_ACTIVE;

                    measure_timer <= '0;
                end

                PWR_SLEEP: begin
                    clk_gate <= 1'b1;
                    if (power_mode != 2'b00)
                        state <= PWR_ACTIVE;
                end

                PWR_ACTIVE: begin
                    clk_gate <= 1'b0;
                    state <= PWR_IDLE;
                end

                PWR_SHUTDOWN: begin
                    // Critical: disable everything
                    ldo_enable      <= 1'b0;
                    vref_enable     <= 1'b0;
                    adc_power_enable <= 1'b0;
                    rf_power_enable <= 1'b0;
                end
            endcase
        end
    end

    // Output assignments
    assign battery_low      = (consecutive_low >= 3);
    assign battery_critical = (consecutive_critical >= 3);
    assign power_good       = !battery_low && !battery_critical;
    assign battery_voltage  = voltage_filtered;

    // Power sequencing
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            ldo_enable       <= 1'b0;
            vref_enable      <= 1'b0;
            adc_power_enable <= 1'b0;
            rf_power_enable  <= 1'b0;
        end else if (power_good) begin
            ldo_enable       <= 1'b1;
            vref_enable      <= (power_mode != 2'b00);
            adc_power_enable <= (power_mode != 2'b00);
            rf_power_enable  <= (power_mode == 2'b10);
        end
    end

    // Interrupt
    assign irq_power = battery_low || battery_critical;

endmodule
```

---

## 5.5.7 — Voltage Monitor with Debouncing

```systemverilog
module voltage_monitor #(
    parameter ADC_WIDTH     = 12,
    parameter DEBOUNCE_BITS = 16
)(
    input  logic                      clk,
    input  logic                      rst_n,
    input  logic [ADC_WIDTH-1:0]      voltage_in,
    input  logic                      voltage_valid,
    input  logic [ADC_WIDTH-1:0]      low_threshold,
    input  logic [ADC_WIDTH-1:0]      critical_threshold,
    output logic                      low_detected,
    output logic                      critical_detected,
    output logic [ADC_WIDTH-1:0]      filtered_voltage
);

    // IIR low-pass filter (alpha = 0.25)
    logic [ADC_WIDTH+1:0] filtered_acc;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            filtered_acc <= '0;
        end else if (voltage_valid) begin
            // y[n] = 0.75*y[n-1] + 0.25*x[n]
            filtered_acc <= (filtered_acc * 3 + {2'b0, voltage_in}) >> 2;
        end
    end

    assign filtered_voltage = filtered_acc[ADC_WIDTH-1:0];

    // Debounce counters
    logic [DEBOUNCE_BITS-1:0] low_count;
    logic [DEBOUNCE_BITS-1:0] critical_count;
    localparam DEBOUNCE_LIMIT = (1 << DEBOUNCE_BITS) - 1;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            low_count      <= '0;
            critical_count <= '0;
            low_detected      <= 1'b0;
            critical_detected <= 1'b0;
        end else if (voltage_valid) begin
            // Low threshold debounce
            if (filtered_voltage < low_threshold) begin
                if (low_count < DEBOUNCE_LIMIT)
                    low_count <= low_count + 1;
                else
                    low_detected <= 1'b1;
            end else begin
                low_count      <= '0;
                low_detected   <= 1'b0;
            end

            // Critical threshold debounce
            if (filtered_voltage < critical_threshold) begin
                if (critical_count < DEBOUNCE_LIMIT)
                    critical_count <= critical_count + 1;
                else
                    critical_detected <= 1'b1;
            end else begin
                critical_count    <= '0;
                critical_detected <= 1'b0;
            end
        end
    end

endmodule
```

---

## 5.5.8 — Clock Gating Cell

```systemverilog
module clock_gater (
    input  logic clk_in,
    input  logic test_enable,
    input  logic gate_enable,
    output logic clk_out
);
    // Integrated clock gating cell (ICG)
    // Prevents glitches on clock output
    logic latch_enable;

    always_latch begin
        if (!clk_in)
            latch_enable <= gate_enable || test_enable;
    end

    assign clk_out = clk_in & latch_enable;

endmodule
```

---

## 5.5.9 — Power Sequencer

```systemverilog
module power_sequencer (
    input  logic       clk,
    input  logic       rst_n,
    input  logic       power_on,
    input  logic       power_off,
    output logic       ldo_enable,
    output logic       vref_enable,
    output logic       adc_enable,
    output logic       rf_enable,
    output logic       ready
);

    typedef enum logic [2:0] {
        SEQ_OFF      = 3'd0,
        SEQ_LDO_ON   = 3'd1,
        SEQ_VREF_ON  = 3'd2,
        SEQ_ADC_ON   = 3'd3,
        SEQ_RF_ON    = 3'd4,
        SEQ_READY    = 3'd5,
        SEQ_SHUTDOWN = 3'd6
    } seq_state_t;

    seq_state_t state;
    logic [15:0] settle_timer;

    // Settle time: 1 ms at 32.768 kHz = 33 cycles
    localparam SETTLE_CYCLES = 16'd33;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state        <= SEQ_OFF;
            ldo_enable   <= 1'b0;
            vref_enable  <= 1'b0;
            adc_enable   <= 1'b0;
            rf_enable    <= 1'b0;
            ready        <= 1'b0;
            settle_timer <= '0;
        end else begin
            case (state)
                SEQ_OFF: begin
                    if (power_on) begin
                        state <= SEQ_LDO_ON;
                        settle_timer <= '0;
                    end
                end

                SEQ_LDO_ON: begin
                    ldo_enable <= 1'b1;
                    settle_timer <= settle_timer + 1;
                    if (settle_timer >= SETTLE_CYCLES) begin
                        state <= SEQ_VREF_ON;
                        settle_timer <= '0;
                    end
                end

                SEQ_VREF_ON: begin
                    vref_enable <= 1'b1;
                    settle_timer <= settle_timer + 1;
                    if (settle_timer >= SETTLE_CYCLES) begin
                        state <= SEQ_ADC_ON;
                        settle_timer <= '0;
                    end
                end

                SEQ_ADC_ON: begin
                    adc_enable <= 1'b1;
                    settle_timer <= settle_timer + 1;
                    if (settle_timer >= SETTLE_CYCLES) begin
                        state <= SEQ_READY;
                    end
                end

                SEQ_READY: begin
                    ready <= 1'b1;
                    if (power_off) begin
                        state <= SEQ_SHUTDOWN;
                        ready <= 1'b0;
                    end
                end

                SEQ_SHUTDOWN: begin
                    rf_enable   <= 1'b0;
                    adc_enable  <= 1'b0;
                    vref_enable <= 1'b0;
                    ldo_enable  <= 1'b0;
                    state       <= SEQ_OFF;
                end
            endcase
        end
    end

endmodule
```

---

## 5.5.10 — Watchdog Timer

```systemverilog
module watchdog_timer #(
    parameter WIDTH = 16,
    parameter TIMEOUT = 16'hFFFF
)(
    input  logic             clk,
    input  logic             rst_n,
    input  logic             enable,
    input  logic             kick,          // feed the watchdog
    output logic             timeout,
    output logic             reset_out
);

    logic [WIDTH-1:0] count;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count      <= '0;
            timeout    <= 1'b0;
            reset_out  <= 1'b0;
        end else if (enable) begin
            if (kick) begin
                count   <= '0;
                timeout <= 1'b0;
            end else begin
                count <= count + 1'b1;
                if (count >= TIMEOUT) begin
                    timeout   <= 1'b1;
                    reset_out <= 1'b1;
                end
            end
        end else begin
            count <= '0;
        end
    end

endmodule
```

---

## 5.5.11 — Best Practices

1. **Measure battery voltage** periodically — 1 Hz minimum
2. **Debounce voltage readings** — prevent false alarms from noise
3. **Power sequencing** — enable supplies in correct order
4. **Clock gating** — disable clock to unused blocks
5. **Brownout detection** — critical threshold triggers safe shutdown
6. **Hysteresis** — prevent oscillation at threshold boundaries
7. **Watchdog timer** — recover from software hangs
8. **Test all power modes** — verify transitions and timing

---

## 5.5.12 — References

- iPACE-CHIP Power Management Specification, v1.5
- ISO 14708-1:2014 — Power and battery requirements
- Weste & Harris, *CMOS VLSI Design*, Chapter 5 — Power
