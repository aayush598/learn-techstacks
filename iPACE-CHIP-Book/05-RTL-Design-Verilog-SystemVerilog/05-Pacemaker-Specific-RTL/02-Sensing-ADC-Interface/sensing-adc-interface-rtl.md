# Sensing ADC Interface RTL Design

## 5.5.2 — Overview

The **sensing ADC interface** captures cardiac signals from the heart,
processes them through filtering and threshold detection, and generates sense
events for the pacing controller. This module interfaces with the analog
front-end (AFE) ADC and implements digital signal processing for reliable
R-wave and P-wave detection.

---

## 5.5.3 — Sensing Requirements

| Parameter | Min | Typ | Max | Unit |
|-----------|-----|-----|-----|------|
| ADC Resolution | — | 12 | — | bits |
| Sample Rate | — | 512 | — | samples/sec |
| Input Range | 0 | — | 1.2 | V |
| Dynamic Range | — | 72 | — | dB |
| Sense Threshold | 0.1 | 0.5 | 1.0 | mV |
| Refractory Period | 150 | 200 | 400 | ms |
| Detection Latency | — | 2 | — | ms |
| Power (sensing block) | — | 2 | 5 | μW |

---

## 5.5.4 — ADC Interface Module

```systemverilog
module adc_interface #(
    parameter ADC_WIDTH  = 12,
    parameter CLK_FREQ   = 32768,
    parameter SAMPLE_RATE = 512
)(
    input  logic                    clk,
    input  logic                    rst_n,

    // ADC physical interface
    output logic                    adc_start,
    input  logic [ADC_WIDTH-1:0]    adc_data,
    input  logic                    adc_eoc,      // end of conversion

    // Configuration
    input  logic                    adc_enable,

    // Output
    output logic [ADC_WIDTH-1:0]    sample_out,
    output logic                    sample_valid,
    output logic                    adc_busy
);

    // Sample rate prescaler
    localparam SAMPLE_DIV = CLK_FREQ / SAMPLE_RATE;

    typedef enum logic [2:0] {
        ADC_IDLE     = 3'd0,
        ADC_START    = 3'd1,
        ADC_WAIT     = 3'd2,
        ADC_CAPTURE  = 3'd3,
        ADC_VALID    = 3'd4
    } adc_state_t;

    adc_state_t state;
    logic [$clog2(SAMPLE_DIV)-1:0] prescaler;
    logic sample_tick;

    // Prescaler for sample rate
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            prescaler  <= '0;
            sample_tick <= 1'b0;
        end else if (adc_enable) begin
            if (prescaler == SAMPLE_DIV - 1) begin
                prescaler   <= '0;
                sample_tick <= 1'b1;
            end else begin
                prescaler   <= prescaler + 1'b1;
                sample_tick <= 1'b0;
            end
        end else begin
            prescaler   <= '0;
            sample_tick <= 1'b0;
        end
    end

    // ADC state machine
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state        <= ADC_IDLE;
            adc_start    <= 1'b0;
            sample_out   <= '0;
            sample_valid <= 1'b0;
            adc_busy     <= 1'b0;
        end else begin
            sample_valid <= 1'b0;  // default: pulse

            case (state)
                ADC_IDLE: begin
                    adc_busy <= 1'b0;
                    if (sample_tick && adc_enable) begin
                        state     <= ADC_START;
                        adc_start <= 1'b1;
                        adc_busy  <= 1'b1;
                    end
                end

                ADC_START: begin
                    adc_start <= 1'b0;
                    state     <= ADC_WAIT;
                end

                ADC_WAIT: begin
                    if (adc_eoc) begin
                        state <= ADC_CAPTURE;
                    end
                end

                ADC_CAPTURE: begin
                    sample_out   <= adc_data;
                    sample_valid <= 1'b1;
                    state        <= ADC_VALID;
                end

                ADC_VALID: begin
                    state <= ADC_IDLE;
                end

                default: state <= ADC_IDLE;
            endcase
        end
    end

endmodule
```

---

## 5.5.5 — Signal Processor: Bandpass Filter

```systemverilog
module bandpass_filter #(
    parameter DATA_WIDTH = 12,
    parameter COEFF_WIDTH = 16
)(
    input  logic                      clk,
    input  logic                      rst_n,
    input  logic                      enable,
    input  logic signed [DATA_WIDTH-1:0]  sample_in,
    input  logic                      sample_valid,
    output logic signed [DATA_WIDTH-1:0]  sample_out,
    output logic                      output_valid
);

    // 4th-order IIR bandpass filter (5-50 Hz for cardiac signals)
    // Coefficients designed for 512 Hz sample rate
    // Passband: 5-50 Hz (covers P-wave and R-wave)

    // Pipeline stages
    reg signed [DATA_WIDTH+COEFF_WIDTH-1:0] stage1, stage2;
    reg signed [DATA_WIDTH-1:0] delay_line [0:3];
    reg [2:0] valid_pipe;

    // Simplified FIR approximation (real design would use proper IIR)
    // Moving average with differentiation for bandpass effect
    reg signed [DATA_WIDTH+3:0] acc;
    reg signed [DATA_WIDTH+3:0] prev_acc;
    reg signed [DATA_WIDTH+3:0] diff;
    reg signed [DATA_WIDTH+3:0] filtered;

    integer i;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for (i = 0; i < 4; i++)
                delay_line[i] <= '0;
            acc          <= '0;
            prev_acc     <= '0;
            diff         <= '0;
            filtered     <= '0;
            sample_out   <= '0;
            output_valid <= 1'b0;
            valid_pipe   <= '0;
        end else if (enable) begin
            // Shift delay line
            delay_line[0] <= sample_in;
            for (i = 1; i < 4; i++)
                delay_line[i] <= delay_line[i-1];

            // 4-sample moving average (low-pass at ~128 Hz)
            acc <= {4'b0, sample_in} + {4'b0, delay_line[0]}
                 + {4'b0, delay_line[1]} + {4'b0, delay_line[2]};

            // Differentiation (high-pass effect)
            diff <= acc - prev_acc;
            prev_acc <= acc;

            // Second stage: another averaging
            filtered <= (diff + prev_diff) >>> 1;

            // Output with pipeline delay
            sample_out   <= filtered[DATA_WIDTH-1:0];
            output_valid <= sample_valid;
        end
    end

    reg signed [DATA_WIDTH+3:0] prev_diff;
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            prev_diff <= '0;
        else if (enable)
            prev_diff <= diff;
    end

endmodule
```

---

## 5.5.6 — Peak Detector

```systemverilog
module peak_detector #(
    parameter DATA_WIDTH = 12
)(
    input  logic                        clk,
    input  logic                        rst_n,
    input  logic                        enable,
    input  logic signed [DATA_WIDTH-1:0]  sample_in,
    input  logic                        sample_valid,
    input  logic                        refractory,
    output logic                        peak_detected,
    output logic [DATA_WIDTH-1:0]       peak_value,
    output logic [DATA_WIDTH-1:0]       threshold_level
);

    typedef enum logic [1:0] {
        PKT_IDLE    = 2'd0,
        PKT_RISING  = 2'd1,
        PKT_FALLING = 2'd2,
        PKT_PEAK    = 2'd3
    } peak_state_t;

    peak_state_t state;
    logic [DATA_WIDTH-1:0] current_sample;
    logic [DATA_WIDTH-1:0] prev_sample;
    logic [DATA_WIDTH-1:0] running_peak;
    logic signed [DATA_WIDTH-1:0] threshold;

    // Absolute value and threshold comparison
    assign current_sample = sample_in[DATA_WIDTH-1] ?
        -sample_in : sample_in;  // rectify
    assign threshold_level = threshold[DATA_WIDTH-1:0];

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state         <= PKT_IDLE;
            running_peak  <= '0;
            peak_value    <= '0;
            peak_detected <= 1'b0;
            prev_sample   <= '0;
        end else if (enable && sample_valid && !refractory) begin
            prev_sample <= current_sample;

            case (state)
                PKT_IDLE: begin
                    peak_detected <= 1'b0;
                    if (current_sample > threshold[DATA_WIDTH-1:0]) begin
                        state        <= PKT_RISING;
                        running_peak <= current_sample;
                    end
                end

                PKT_RISING: begin
                    if (current_sample > running_peak)
                        running_peak <= current_sample;
                    else if (current_sample < running_peak) begin
                        state <= PKT_PEAK;
                    end
                end

                PKT_PEAK: begin
                    peak_value    <= running_peak;
                    peak_detected <= 1'b1;
                    state         <= PKT_FALLING;
                end

                PKT_FALLING: begin
                    peak_detected <= 1'b0;
                    if (current_sample < (running_peak >>> 2)) begin
                        state <= PKT_IDLE;
                    end
                end
            endcase
        end else if (refractory) begin
            state         <= PKT_IDLE;
            peak_detected <= 1'b0;
            running_peak  <= '0;
        end
    end

    // Adaptive threshold
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            threshold <= {1'b0, {DATA_WIDTH-1{1'b1}}};  // 50% full scale
        else if (peak_detected) begin
            // Update threshold to 50% of detected peak
            threshold <= {1'b0, running_peak[DATA_WIDTH-1:1]};
        end
    end

endmodule
```

---

## 5.5.7 — Complete Sensing Channel

```systemverilog
module sensing_channel #(
    parameter ADC_WIDTH    = 12,
    parameter THRESH_WIDTH = 12
)(
    input  logic                        clk,
    input  logic                        rst_n,

    // ADC interface
    output logic                        adc_start,
    input  logic [ADC_WIDTH-1:0]        adc_data,
    input  logic                        adc_eoc,

    // Configuration
    input  logic                        channel_enable,
    input  logic [THRESH_WIDTH-1:0]     manual_threshold,
    input  logic                        use_auto_threshold,

    // Control
    input  logic                        refractory,
    input  logic [1:0]                  filter_mode,  // 0=off,1=low,2=high,3=bp

    // Output
    output logic                        sense_event,
    output logic [ADC_WIDTH-1:0]        sense_amplitude,
    output logic [THRESH_WIDTH-1:0]     current_threshold
);

    // Internal signals
    logic [ADC_WIDTH-1:0] raw_sample;
    logic                 raw_valid;
    logic signed [ADC_WIDTH-1:0] filtered_sample;
    logic                 filtered_valid;
    logic [ADC_WIDTH-1:0] peak_val;
    logic                 peak_valid;
    logic [ADC_WIDTH-1:0] auto_threshold;

    // ADC interface
    adc_interface #(
        .ADC_WIDTH(ADC_WIDTH)
    ) u_adc (
        .clk          (clk),
        .rst_n        (rst_n),
        .adc_start    (adc_start),
        .adc_data     (adc_data),
        .adc_eoc      (adc_eoc),
        .adc_enable   (channel_enable),
        .sample_out   (raw_sample),
        .sample_valid (raw_valid),
        .adc_busy     ()
    );

    // Bandpass filter
    bandpass_filter #(
        .DATA_WIDTH(ADC_WIDTH)
    ) u_filter (
        .clk          (clk),
        .rst_n        (rst_n),
        .enable       (channel_enable),
        .sample_in    (filtered_sample),
        .sample_valid (raw_valid),
        .sample_out   (filtered_sample),
        .output_valid (filtered_valid)
    );

    // Peak detector
    peak_detector #(
        .DATA_WIDTH(ADC_WIDTH)
    ) u_peak (
        .clk            (clk),
        .rst_n          (rst_n),
        .enable         (channel_enable),
        .sample_in      (filtered_sample),
        .sample_valid   (filtered_valid),
        .refractory     (refractory),
        .peak_detected  (peak_valid),
        .peak_value     (peak_val),
        .threshold_level(auto_threshold)
    );

    // Output assignments
    assign sense_event      = peak_valid && !refractory;
    assign sense_amplitude  = peak_val;
    assign current_threshold = use_auto_threshold ?
                               auto_threshold : manual_threshold;

endmodule
```

---

## 5.5.8 — Dual-Channel Sensing Controller

```systemverilog
module sensing_adc_controller #(
    parameter ADC_WIDTH = 12
)(
    input  logic                    clk,
    input  logic                    rst_n,

    // Dual ADC inputs
    output logic                    adc_start,
    input  logic [ADC_WIDTH-1:0]    adc_atrial,
    input  logic [ADC_WIDTH-1:0]    adc_ventricular,
    input  logic                    adc_eoc,

    // Configuration
    input  logic                    atrial_enable,
    input  logic                    ventricular_enable,
    input  logic [ADC_WIDTH-1:0]    atrial_threshold,
    input  logic [ADC_WIDTH-1:0]    vent_threshold,
    input  logic                    auto_threshold,

    // Control
    input  logic                    atrial_refractory,
    input  logic                    vent_refractory,

    // Outputs
    output logic                    atrial_sense,
    output logic                    ventricular_sense,
    output logic [ADC_WIDTH-1:0]    atrial_amplitude,
    output logic [ADC_WIDTH-1:0]    vent_amplitude,
    output logic [ADC_WIDTH-1:0]    atrial_threshold_out,
    output logic [ADC_WIDTH-1:0]    vent_threshold_out
);

    sensing_channel #(.ADC_WIDTH(ADC_WIDTH)) u_atrial (
        .clk              (clk),
        .rst_n            (rst_n),
        .adc_start        (adc_start),
        .adc_data         (adc_atrial),
        .adc_eoc          (adc_eoc),
        .channel_enable   (atrial_enable),
        .manual_threshold (atrial_threshold),
        .use_auto_threshold(auto_threshold),
        .refractory       (atrial_refractory),
        .filter_mode      (2'b11),
        .sense_event      (atrial_sense),
        .sense_amplitude  (atrial_amplitude),
        .current_threshold(atrial_threshold_out)
    );

    sensing_channel #(.ADC_WIDTH(ADC_WIDTH)) u_ventricular (
        .clk              (clk),
        .rst_n            (rst_n),
        .adc_start        (adc_start),
        .adc_data         (adc_ventricular),
        .adc_eoc          (adc_eoc),
        .channel_enable   (ventricular_enable),
        .manual_threshold (vent_threshold),
        .use_auto_threshold(auto_threshold),
        .refractory       (vent_refractory),
        .filter_mode      (2'b11),
        .sense_event      (ventricular_sense),
        .sense_amplitude  (vent_amplitude),
        .current_threshold(vent_threshold_out)
    );

endmodule
```

---

## 5.5.9 — Best Practices

1. **Fixed sample rate** — 512 Hz for cardiac signals (5-50 Hz content)
2. **Bandpass filter** — remove DC offset and high-frequency noise
3. **Adaptive threshold** — track signal amplitude variations
4. **Refractory period** — prevent double-counting of same event
5. **Pipeline ADC interface** — separate start, wait, capture, valid
6. **Test with real ECG data** — validate with clinical waveforms
7. **Power gating** — disable unused channel to save power
8. **Signed arithmetic** — handle bipolar ADC signals correctly

---

## 5.5.10 — References

- iPACE-CHIP Sensing ADC Specification, v1.3
- ISO 14708-1:2014 — Implantable cardiac pacemakers
- Webster, *Design of Cardiac Pacemakers*, Chapter 4
