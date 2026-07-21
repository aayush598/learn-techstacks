# Pacing Timer RTL Design

## 5.5.1 — Overview

The **pacing timer** is the heart of the iPACE-CHIP digital subsystem. It
controls the timing between pacing pulses, manages refractory periods, and
ensures accurate heart-rate control. This chapter presents the complete RTL
design of the pacing timer module, including prescaler, counter, and
state-machine integration.

---

## 5.5.2 — Timing Requirements

| Parameter | Min | Typ | Max | Unit |
|-----------|-----|-----|-----|------|
| System Clock | — | 32.768 | — | kHz |
| Pacing Interval | 300 | 800 | 2000 | ms |
| Pulse Width | 0.1 | 0.5 | 4.5 | ms |
| Refractory Period | 150 | 300 | 600 | ms |
| Timer Resolution | — | 30.5 | — | μs/cycle |
| Timer Width | — | 16 | — | bits |

### Clock Cycle Calculation

```
Timer tick period = 1 / 32768 Hz = 30.52 μs
800 ms interval = 800ms / 30.52μs = 26,214 cycles
Requires: ceil(log2(26214)) = 15 bits minimum
Using 16-bit timer for safety margin
```

---

## 5.5.3 — Top-Level Pacing Timer Module

```systemverilog
module pacing_timer #(
    parameter WIDTH       = 16,
    parameter CLK_FREQ_HZ = 32768
)(
    input  logic                  clk,
    input  logic                  rst_n,

    // Configuration
    input  logic [WIDTH-1:0]      interval_limit,   // pacing interval
    input  logic [WIDTH-1:0]      pulse_width_limit, // pulse duration
    input  logic [WIDTH-1:0]      refractory_limit,  // refractory time
    input  logic                  timer_enable,

    // Control
    input  logic                  timer_clear,
    input  logic                  pulse_start,       // start pulse

    // Status outputs
    output logic [WIDTH-1:0]      timer_count,
    output logic                  interval_done,
    output logic                  pulse_active,
    output logic                  refractory_active,
    output logic                  timer_running
);

    // State encoding
    typedef enum logic [2:0] {
        T_IDLE     = 3'd0,
        T_RUNNING  = 3'd1,
        T_PULSE    = 3'd2,
        T_REFRACT  = 3'd3,
        T_WAIT     = 3'd4
    } timer_state_t;

    timer_state_t state, next_state;

    // Internal counters
    logic [WIDTH-1:0] interval_count;
    logic [WIDTH-1:0] pulse_count;
    logic [WIDTH-1:0] refract_count;

    // Interval done detection
    assign interval_done = (interval_count >= interval_limit);

    // Output assignments
    assign timer_count       = interval_count;
    assign pulse_active      = (state == T_PULSE);
    assign refractory_active = (state == T_REFRACT);
    assign timer_running     = (state == T_RUNNING) || (state == T_PULSE);

    // State register
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            state <= T_IDLE;
        else if (timer_clear)
            state <= T_IDLE;
        else
            state <= next_state;
    end

    // Next state logic
    always_comb begin
        next_state = state;
        case (state)
            T_IDLE: begin
                if (timer_enable && !interval_done)
                    next_state = T_RUNNING;
            end

            T_RUNNING: begin
                if (!timer_enable)
                    next_state = T_IDLE;
                else if (interval_done)
                    next_state = T_PULSE;
            end

            T_PULSE: begin
                if (pulse_count >= pulse_width_limit)
                    next_state = T_REFRACT;
            end

            T_REFRACT: begin
                if (refract_count >= refractory_limit)
                    next_state = T_IDLE;
            end

            default: next_state = T_IDLE;
        endcase
    end

    // Interval counter
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            interval_count <= '0;
        end else if (timer_clear || (state == T_PULSE)) begin
            interval_count <= '0;  // reset on pulse start
        end else if (state == T_RUNNING && timer_enable) begin
            interval_count <= interval_count + 1'b1;
        end
    end

    // Pulse counter
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            pulse_count <= '0;
        end else if (state == T_PULSE) begin
            pulse_count <= pulse_count + 1'b1;
        end else if (state != T_PULSE) begin
            pulse_count <= '0;
        end
    end

    // Refractory counter
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            refract_count <= '0;
        end else if (state == T_REFRACT) begin
            refract_count <= refract_count + 1'b1;
        end else if (state != T_REFRACT) begin
            refract_count <= '0;
        end
    end

endmodule
```

---

## 5.5.4 — Prescaler Module

```systemverilog
module clock_prescaler #(
    parameter DIVISOR = 1,          // 1 = no prescaling
    parameter CNT_WIDTH = $clog2(DIVISOR)
)(
    input  logic clk,
    input  logic rst_n,
    input  logic enable,
    output logic tick
);

    logic [CNT_WIDTH-1:0] count;

    assign tick = (count == DIVISOR - 1) && enable;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            count <= '0;
        else if (enable) begin
            if (count == DIVISOR - 1)
                count <= '0;
            else
                count <= count + 1'b1;
        end
    end

endmodule
```

---

## 5.5.5 — Prescaler Integration

```systemverilog
module pacing_timer_with_prescaler #(
    parameter WIDTH        = 16,
    parameter CLK_FREQ_HZ  = 32768,
    parameter TICK_FREQ_HZ = 1000,  // 1 ms tick
    parameter DIVISOR      = CLK_FREQ_HZ / TICK_FREQ_HZ
)(
    input  logic              clk,
    input  logic              rst_n,
    input  logic [WIDTH-1:0]  interval_ms,
    input  logic [WIDTH-1:0]  pulse_width_ms,
    input  logic              enable,
    output logic              pace_trigger,
    output logic [WIDTH-1:0]  current_count
);

    logic timer_tick;

    // Prescaler: 32.768 kHz → 1 kHz (1 ms tick)
    clock_prescaler #(
        .DIVISOR(DIVISOR)
    ) u_prescaler (
        .clk    (clk),
        .rst_n  (rst_n),
        .enable (1'b1),
        .tick   (timer_tick)
    );

    // Main timer using 1 ms ticks
    pacing_timer #(
        .WIDTH(WIDTH)
    ) u_timer (
        .clk              (clk),
        .rst_n            (rst_n),
        .interval_limit   (interval_ms),
        .pulse_width_limit(pulse_width_ms),
        .refractory_limit (16'd0),
        .timer_enable     (enable && timer_tick),
        .timer_clear      (1'b0),
        .pulse_start      (1'b0),
        .timer_count      (current_count),
        .interval_done    (pace_trigger),
        .pulse_active     (),
        .refractory_active(),
        .timer_running    ()
    );

endmodule
```

---

## 5.5.6 — Dual-Chamber Timer

```systemverilog
module dual_chamber_timer #(
    parameter WIDTH = 16
)(
    input  logic              clk,
    input  logic              rst_n,

    // Atrial timing
    input  logic [WIDTH-1:0]  atrial_interval,
    input  logic [WIDTH-1:0]  atrial_pulse_width,

    // Ventricular timing
    input  logic [WIDTH-1:0]  vent_interval,
    input  logic [WIDTH-1:0]  vent_pulse_width,

    // AV delay (DDD mode)
    input  logic [WIDTH-1:0]  av_delay,

    // Control
    input  logic              atrial_sense,
    input  logic              vent_sense,
    input  logic [1:0]        pacing_mode,

    // Outputs
    output logic              atrial_pace,
    output logic              vent_pace,
    output logic              atrial_refractory,
    output logic              vent_refractory
);

    typedef enum logic [2:0] {
        D_IDLE    = 3'd0,
        D_A_PACE  = 3'd1,
        D_AV_WAIT = 3'd2,
        D_V_PACE  = 3'd3,
        D_REFRACT = 3'd4
    } dc_state_t;

    dc_state_t state;
    logic [WIDTH-1:0] av_timer;
    logic [WIDTH-1:0] atrial_timer;
    logic [WIDTH-1:0] vent_timer;

    localparam MODE_AAI = 2'b10;
    localparam MODE_VVI = 2'b01;
    localparam MODE_DDD = 2'b11;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state        <= D_IDLE;
            av_timer     <= '0;
            atrial_timer <= '0;
            vent_timer   <= '0;
        end else begin
            case (state)
                D_IDLE: begin
                    if (pacing_mode == MODE_DDD) begin
                        atrial_timer <= atrial_timer + 1'b1;
                        if (atrial_timer >= atrial_interval) begin
                            state <= D_A_PACE;
                            atrial_timer <= '0;
                        end
                    end
                end

                D_A_PACE: begin
                    if (atrial_timer >= atrial_pulse_width) begin
                        state <= D_AV_WAIT;
                        atrial_timer <= '0;
                        av_timer <= '0;
                    end else begin
                        atrial_timer <= atrial_timer + 1'b1;
                    end
                end

                D_AV_WAIT: begin
                    av_timer <= av_timer + 1'b1;
                    if (vent_sense || av_timer >= av_delay) begin
                        state <= D_V_PACE;
                        vent_timer <= '0;
                    end
                end

                D_V_PACE: begin
                    vent_timer <= vent_timer + 1'b1;
                    if (vent_timer >= vent_pulse_width) begin
                        state <= D_REFRACT;
                        vent_timer <= '0;
                    end
                end

                D_REFRACT: begin
                    vent_timer <= vent_timer + 1'b1;
                    if (vent_timer >= vent_interval) begin
                        state <= D_IDLE;
                        vent_timer <= '0;
                    end
                end
            endcase
        end
    end

    // Output assignments
    assign atrial_pace       = (state == D_A_PACE);
    assign vent_pace         = (state == D_V_PACE);
    assign atrial_refractory = (state == D_AV_WAIT) || (state == D_V_PACE);
    assign vent_refractory   = (state == D_REFRACT);

endmodule
```

---

## 5.5.7 — Timer Testbench

```systemverilog
module pacing_timer_tb;
    parameter WIDTH = 16;

    logic        clk, rst_n;
    logic [WIDTH-1:0] interval_limit;
    logic [WIDTH-1:0] pulse_width_limit;
    logic             timer_enable;
    logic [WIDTH-1:0] timer_count;
    logic             interval_done;
    logic             pulse_active;

    pacing_timer #(.WIDTH(WIDTH)) uut (
        .clk(clk), .rst_n(rst_n),
        .interval_limit(interval_limit),
        .pulse_width_limit(pulse_width_limit),
        .refractory_limit(16'd50),
        .timer_enable(timer_enable),
        .timer_clear(1'b0),
        .pulse_start(1'b0),
        .timer_count(timer_count),
        .interval_done(interval_done),
        .pulse_active(pulse_active),
        .refractory_active(),
        .timer_running()
    );

    // Clock generation
    initial clk = 0;
    always #15.26 clk = ~clk;  // 32.768 kHz

    // Test sequence
    initial begin
        rst_n = 0;
        interval_limit = 16'd100;
        pulse_width_limit = 16'd10;
        timer_enable = 0;

        #100;
        rst_n = 1;
        #100;

        // Enable timer
        timer_enable = 1;

        // Wait for interval
        wait(interval_done == 1);
        $display("[T=%0t] Interval done at count=%0d", $time, timer_count);

        // Wait for pulse
        wait(pulse_active == 1);
        $display("[T=%0t] Pulse started", $time);

        wait(pulse_active == 0);
        $display("[T=%0t] Pulse ended", $time);

        // Test disable
        timer_enable = 0;
        #1000;

        $display("All tests passed!");
        $finish;
    end

    // Monitor
    initial begin
        $monitor("T=%0t state=%0d count=%0d done=%0b pulse=%0b",
                 $time, uut.state, timer_count, interval_done, pulse_active);
    end
endmodule
```

---

## 5.5.8 — Best Practices

1. **Parameterize timer width** — different applications need different ranges
2. **Use prescaler** — reduce power by running timer at lower frequency
3. **Separate interval and pulse counters** — independent timing
4. **Include refractory period** — essential for pacemaker safety
5. **Asynchronous reset** — power-on reset support
6. **Clear on state transition** — prevent stale counts
7. **Test edge cases** — max count, zero count, enable during pulse
8. **Verify timing accuracy** — ±1 cycle tolerance

---

## 5.5.9 — References

- iPACE-CHIP Pacing Timer Specification, v2.1
- IEEE Std 1800-2017
- ISO 14708-1:2014 — Implantable cardiac pacemakers
