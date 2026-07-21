# RTL Coding Guidelines for iPACE-CHIP ASIC

## 1. Introduction

RTL (Register Transfer Level) coding guidelines establish the rules and conventions for
writing synthesizable Verilog that reliably maps to the target 180nm CMOS technology. For
the iPACE-CHIP, these guidelines are not merely stylistic preferences — they directly
impact:

- **Synthesis quality**: Area, timing, and power of the final gate-level netlist
- **Verification efficiency**: Consistent coding enables automated checks and formal tools
- **Safety compliance**: IEC 62304 requires documented coding standards
- **Maintainability**: Readable code reduces errors across a 10+ year design cycle
- **DFT compatibility**: Scan insertion, MBIST, and test modes require structured RTL

## 2. Coding Style Rules

### 2.1 Naming Conventions

```
┌──────────────────────────────────────────────────────────────────┐
│                    NAMING CONVENTION TABLE                        │
├────────────────────┬──────────────────┬──────────────────────────┤
│ Object             │ Convention       │ Example                  │
├────────────────────┼──────────────────┼──────────────────────────┤
│ Module names       │ lowercase_       │ pacing_engine            │
│                    │ underscore       │ sar_adc_12bit            │
├────────────────────┼──────────────────┼──────────────────────────┤
│ Signal names       │ lowercase_       │ sense_valid_atrial       │
│                    │ underscore       │ pace_cmd_vent            │
├────────────────────┼──────────────────┼──────────────────────────┤
│ Active-low signals │ _b suffix        │ reset_b                  │
│                    │                  │ enable_b                 │
├────────────────────┼──────────────────┼──────────────────────────┤
│ Active-high signals│ _n NOT used      │ enable                   │
│                    │                  │ clear                    │
├────────────────────┼──────────────────┼──────────────────────────┤
│ Clock signals      │ clk_ prefix      │ clk_core                 │
│                    │                  │ clk_tele                 │
├────────────────────┼──────────────────┼──────────────────────────┤
│ Reset signals      │ rst_ prefix      │ rst_b (active-low)       │
│                    │                  │ rst_sync_b               │
├────────────────────┼──────────────────┼──────────────────────────┤
│ Bus signals       │ [_MSB:0] suffix  │ data_cnt[15:0]           │
│                    │                  │ addr_bus[7:0]            │
├────────────────────┼──────────────────┼──────────────────────────┤
│ Parameters        │ UPPERCASE        │ PACE_RATE_MAX            │
│                    │                  │ ADC_RESOLUTION           │
├────────────────────┼──────────────────┼──────────────────────────┤
│ Local signals      │ lowercase        │ next_state               │
│                    │                  │ mux_out                  │
├────────────────────┼──────────────────┼──────────────────────────┤
│ Test signals       │ tst_ prefix      │ tst_scan_en              │
│                    │                  │ tst_mode_b               │
├────────────────────┼──────────────────┼──────────────────────────┤
│ Safety signals     │ sfy_ prefix      │ sfy_fault_vent           │
│                    │                  │ sfy_wdog_timeout         │
└────────────────────┴──────────────────┴──────────────────────────┘
```

### 2.2 Module Structure Template

```verilog
//==========================================================================
// Module: pacing_engine
// Description: Dual-chamber demand pacing state machine
//              Implements AAMI EC11 compliant pacing logic
// Author: iPACE Design Team
// Version: 1.0
// Date: 2024-01-15
// Safety: Safety-critical module (SF-001)
// Review: REQUIRED before tapeout
//==========================================================================

module pacing_engine #(
    // Parameters
    parameter P_WIDTH    = 16,  // Pulse width counter width
    parameter R_WIDTH    = 16,  // Refractory period counter width
    parameter RATE_WIDTH = 16   // Rate interval counter width
)(
    // Clock and Reset
    input  wire              clk_core,       // 32.768 kHz core clock
    input  wire              rst_b,          // Active-low async reset

    // Pacing Parameters (from parameter store)
    input  wire [3:0]        pace_amplitude, // 0.5V to 7.5V
    input  wire [3:0]        pace_width,     // 0.05ms to 1.50ms
    input  wire [7:0]        rate_interval,  // 30-180 bpm
    input  wire [R_WIDTH-1:0] refractory_per,// Refractory period
    input  wire [7:0]        av_delay,       // AV delay (ms)

    // Sensing Inputs
    input  wire              sense_atrial,   // Atrial sense detected
    input  wire              sense_vent,     // Ventricular sense detected

    // Pace Outputs
    output reg               pace_atrial,    // Atrial pace trigger
    output reg               pace_vent,      // Ventricular pace trigger
    output reg  [3:0]        pace_amp_out,   // Amplitude setting

    // Status Outputs
    output wire              active_pacing,  // Currently pacing
    output wire              in_refractory,  // In refractory period
    output reg  [P_WIDTH-1:0] pulse_cnt,     // Pulse width counter

    // Safety
    input  wire              sfy_watchdog_ok, // Watchdog healthy
    output reg               sfy_pace_valid,  // Pace output valid
    input  wire              enable           // Module enable
);

    // Internal signals
    reg  [2:0]  state, next_state;
    reg  [R_WIDTH-1:0] refractory_cnt;
    reg  [R_WIDTH-1:0] rate_cnt;
    reg  [7:0]  av_delay_cnt;

    // State encoding (one-hot for safety)
    localparam S_IDLE        = 3'b001;
    localparam S_PACING_A    = 3'b010;
    localparam S_AV_WAIT     = 3'b011;
    localparam S_PACING_V    = 3'b100;
    localparam S_REFRACTORY  = 3'b101;
    localparam S_SAFE_MODE   = 3'b110;

    // Sequential logic
    always @(posedge clk_core or negedge rst_b) begin
        if (!rst_b) begin
            state <= S_IDLE;
            pulse_cnt <= {P_WIDTH{1'b0}};
            refractory_cnt <= {R_WIDTH{1'b0}};
            rate_cnt <= {R_WIDTH{1'b0}};
            av_delay_cnt <= 8'd0;
            pace_atrial <= 1'b0;
            pace_vent <= 1'b0;
            pace_amp_out <= 4'd0;
            sfy_pace_valid <= 1'b0;
        end else if (!enable) begin
            state <= S_IDLE;
        end else begin
            state <= next_state;
            // Counter and output updates...
        end
    end

    // Combinational next-state logic (simplified)
    always @(*) begin
        next_state = state; // Default: hold state
        case (state)
            S_IDLE: begin
                if (!sfy_watchdog_ok)
                    next_state = S_SAFE_MODE;
                else if (rate_cnt >= {1'b0, rate_interval})
                    next_state = S_PACING_A;
            end
            S_PACING_A: begin
                if (pulse_cnt >= pace_width)
                    next_state = S_AV_WAIT;
            end
            // ... other states
            default: next_state = S_SAFE_MODE;
        endcase
    end

endmodule
```

### 2.3 Coding Rules Summary

```
MANDATORY CODING RULES:
═══════════════════════════════════════════════════════════════

Rule 1: ALL flip-flops MUST have an asynchronous active-low reset
        Bad:  always @(posedge clk) q <= d;
        Good: always @(posedge clk or negedge rst_b)
                if (!rst_b) q <= 1'b0;
                else q <= d;

Rule 2: NO latches allowed (unless explicitly documented)
        Bad:  always @(*) if (en) q = d;  // latch!
        Good: always @(*) begin
                q = q;  // hold default
                if (en) q = d;
              end

Rule 3: ALL state machines MUST have a safe default state
        Bad:  default: state = S_UNKNOWN;
        Good: default: state = S_SAFE_MODE;

Rule 4: ALL combinational loops MUST be broken
        Check: Synthesizer will flag as warning/error

Rule 5: ALL inputs MUST be registered at module boundary
        (for timing closure and metastability)
        always @(posedge clk or negedge rst_b)
          if (!rst_b) input_reg <= 0;
          else input_reg <= ext_input;

Rule 6: NO inferred tri-states in core logic
        Bad:  assign data = oe ? drive_data : 1'bz;
        Good: Use explicit MUX for output control

Rule 7: ALL parameters MUST have defined values
        No: parameter WIDTH;  // missing value
        OK: parameter WIDTH = 16;

Rule 8: ALL multi-bit comparisons MUST use full width
        Bad:  if (cnt == 0)  // 16-bit compared to 32-bit 0
        Good: if (cnt == 16'd0)

Rule 9: ALL operators MUST have explicit bit widths
        Bad:  result = a + b;  // width ambiguous
        Good: result = a + b;  // where a, b have clear widths

Rule 10: NO #delay or event timing in synthesizable code
         Bad:  #10 q <= d;
         Good: (omit - use timing constraints instead)
```

## 3. RTL Coding Patterns for iPACE-CHIP

### 3.1 Clock Domain Crossing (CDC) Pattern

```verilog
//==========================================================================
// Clock Domain Crossing (CDC) Synchronizer
// For signals crossing from clk_core (32.768 kHz) to clk_tele (1 MHz)
//==========================================================================

module cdc_2ff_sync #(
    parameter SYNC_WIDTH = 1
)(
    input  wire                  clk_dst,     // Destination clock
    input  wire                  rst_b,       // Reset (tied to dst domain)
    input  wire [SYNC_WIDTH-1:0] data_src,    // Source data (async)
    output reg  [SYNC_WIDTH-1:0] data_sync,   // Synchronized data
    output reg                   data_valid   // Data is stable
);

    reg [SYNC_WIDTH-1:0] sync_reg1;

    always @(posedge clk_dst or negedge rst_b) begin
        if (!rst_b) begin
            sync_reg1 <= {SYNC_WIDTH{1'b0}};
            data_sync <= {SYNC_WIDTH{1'b0}};
            data_valid <= 1'b0;
        end else begin
            sync_reg1 <= data_src;      // First sync stage
            data_sync <= sync_reg1;     // Second sync stage
            data_valid <= (sync_reg1 == data_sync);
        end
    end

endmodule

// Usage:
//   cdc_2ff_sync #(.SYNC_WIDTH(8)) u_cdc_params (
//       .clk_dst(clk_tele),
//       .rst_b(rst_b),
//       .data_src(tele_param_in),
//       .data_sync(param_synced),
//       .data_valid(param_valid)
//   );
```

### 3.2 Clock Gating Pattern

```verilog
//==========================================================================
// Integrated Clock Gating Cell (ICG)
// Safe clock gating for power reduction
//==========================================================================

module icg_cell (
    input  wire  clk_in,       // Free-running clock
    input  wire  enable,       // Clock enable (level)
    input  wire  test_mode,    // Scan test bypass
    output wire  clk_out       // Gated clock
);

    reg enable_latch;

    // Latch enable on low phase of clock (negative latch)
    always @(clk_in or enable) begin
        if (!clk_in)
            enable_latch <= enable;
    end

    // AND gate for clock gating
    assign clk_out = (clk_in & enable_latch) | test_mode;

endmodule

// Integration Example:
//   icg_cell u_icg_pacing (
//       .clk_in(clk_core),
//       .enable(pacing_active),
//       .test_mode(tst_scan_en),
//       .clk_out(clk_pacing)
//   );
```

### 3.3 Reset Synchronizer Pattern

```verilog
//==========================================================================
// Asynchronous Reset Synchronizer
// Ensures all FFs exit reset on the same clock edge
//==========================================================================

module rst_sync (
    input  wire  clk,          // Destination clock
    input  wire  rst_b_async,  // Asynchronous reset (active-low)
    output wire  rst_b_sync    // Synchronized reset
);

    reg rst_ff1;
    reg rst_ff2;

    always @(posedge clk or negedge rst_b_async) begin
        if (!rst_b_async) begin
            rst_ff1 <= 1'b0;
            rst_ff2 <= 1'b0;
        end else begin
            rst_ff1 <= 1'b1;
            rst_ff2 <= rst_ff1;
        end
    end

    assign rst_b_sync = rst_ff2;

endmodule
```

### 3.4 Parameter Register Readback Pattern

```verilog
//==========================================================================
// Parameter Register with Readback and Error Protection
// Used for programmable pacing parameters
//==========================================================================

module param_reg #(
    parameter WIDTH     = 8,
    parameter RESET_VAL = 8'h48  // Default value (72 bpm)
)(
    input  wire              clk,
    input  wire              rst_b,
    input  wire              wr_en,        // Write enable
    input  wire [WIDTH-1:0]  wr_data,      // Write data
    input  wire              rd_en,        // Read enable
    output reg  [WIDTH-1:0]  rd_data,      // Read data
    output reg  [WIDTH-1:0]  stored_val,   // Stored value
    output wire              ecc_error      // ECC error detected
);

    reg [WIDTH-1:0]  ecc_bits;
    reg [WIDTH+6:0]  stored_with_ecc;

    // SECDED encoding
    wire [6:0] ecc_gen;
    ecc_encode #(.DATA_WIDTH(WIDTH)) u_ecc_gen (
        .data_in(stored_val),
        .ecc_out(ecc_gen)
    );

    // Write with ECC protection
    always @(posedge clk or negedge rst_b) begin
        if (!rst_b) begin
            stored_val <= RESET_VAL;
            stored_with_ecc <= {RESET_VAL, 7'd0};
        end else if (wr_en) begin
            stored_val <= wr_data;
            stored_with_ecc <= {wr_data, ecc_gen};
        end
    end

    // Readback with ECC check
    always @(posedge clk or negedge rst_b) begin
        if (!rst_b) begin
            rd_data <= {WIDTH{1'b0}};
            ecc_error <= 1'b0;
        end else if (rd_en) begin
            rd_data <= stored_val;
            ecc_error <= 1'b0; // Simplified: actual ECC check here
        end
    end

endmodule
```

## 4. DFT-Compatible RTL Patterns

### 4.1 Scan-Chain Ready Flip-Flop

```
DFT Requirements for iPACE-CHIP RTL:
═══════════════════════════════════════════════════════════════

All flip-flops in the design MUST be scanable:
  ✓ Use scan-enabled DFF from TSMC standard cell library
  ✓ ALL flip-flops connected to scan chain
  ✓ No combinational loops that bypass FFs
  ✓ Clock gating cells must have test_mode bypass
  ✓ Asynchronous resets must be controllable during scan

Test Infrastructure Integration:
  ┌─────────────────────────────────────────────────────────────┐
  │  clk_core ──┬──►[ICG]──► clk_gated ──► Logic              │
  │             │    enable ↑                                  │
  │             │    tst_scan_en ────────► (bypass for scan)  │
  │             │                                               │
  │             └──►[ICG]──► clk_gated2 ──► Logic2            │
  └─────────────────────────────────────────────────────────────┘

  During scan test:
    • tst_scan_en = 1 → all clock gates bypassed (always on)
    • scan_data_in → shift through FF chain
    • capture cycle: load next values
    • shift out: compare with expected values
```

### 4.2 Test Mode Architecture

```
iPACE-CHIP Test Modes:
═══════════════════════════════════════════════════════════════

  ┌─────────────────────────────────────────────────────────────┐
  │  TEST_EN pin (active-high, tied to GND in field)           │
  │                                                             │
  │  When TEST_EN = 1:                                         │
  │    ┌──────────────────────────────────────────────────┐    │
  │    │ 1. All clock gates bypassed (test_mode = 1)      │    │
  │    │ 2. Scan chain loaded via TEST_DATA (serial I/O)  │    │
  │    │ 3. Test vectors applied, responses captured       │    │
  │    │ 4. MBIST runs on all SRAM instances              │    │
  │    │ 5. Analog BIST runs on AFE, ADC                  │    │
  │    │ 6. Output drivers set to high-impedance          │    │
  │    │ 7. Telemetry TX disabled                         │    │
  │    └──────────────────────────────────────────────────┘    │
  │                                                             │
  │  When TEST_EN = 0 (normal mode):                          │
  │    ┌──────────────────────────────────────────────────┐    │
  │    │ 1. Normal operation with all safety mechanisms   │    │
  │    │ 2. TEST_DATA and TEST_CLK inputs ignored         │    │
  │    │ 3. Output drivers active as programmed           │    │
  │    │ 4. Telemetry operational                         │    │
  │    └──────────────────────────────────────────────────┘    │
  │                                                             │
  │  Permanent Disable: eFuse "TEST_DISABLE" bit              │
  │  Once blown, TEST_EN has no effect (field-safe)           │
  └─────────────────────────────────────────────────────────────┘
```

## 5. Safety-Specific RTL Patterns

### 5.1 Redundant Logic Pattern (TMR)

```verilog
//==========================================================================
// Triple Modular Redundancy (TMR) with Majority Voter
// For safety-critical state machines
//==========================================================================

module tmr_dff #(
    parameter WIDTH = 1
)(
    input  wire              clk,
    input  wire              rst_b,
    input  wire [WIDTH-1:0]  d_in,
    output wire [WIDTH-1:0]  q_out,
    output wire              error  // Disagreement detected
);

    reg [WIDTH-1:0] ff_a, ff_b, ff_c;

    always @(posedge clk or negedge rst_b) begin
        if (!rst_b) begin
            ff_a <= {WIDTH{1'b0}};
            ff_b <= {WIDTH{1'b0}};
            ff_c <= {WIDTH{1'b0}};
        end else begin
            ff_a <= d_in;
            ff_b <= d_in;
            ff_c <= d_in;
        end
    end

    // Majority voter (bit-wise)
    assign q_out = (ff_a & ff_b) | (ff_a & ff_c) | (ff_b & ff_c);

    // Error detection (any disagreement)
    assign error = (ff_a != ff_b) | (ff_a != ff_c) | (ff_b != ff_c);

endmodule

// Usage in safety-critical FSM:
//   tmr_dff #(.WIDTH(3)) u_state_reg (
//       .clk(clk_core),
//       .rst_b(rst_b),
//       .d_in(next_state),
//       .q_out(current_state),
//       .error(sfy_state_error)
//   );
```

### 5.2 Watchdog Timer Pattern

```verilog
//==========================================================================
// Windowed Watchdog Timer
// Must be serviced within a specific time window
//==========================================================================

module watchdog_timer #(
    parameter CLK_FREQ  = 32768,  // Hz
    parameter TIMEOUT   = 500,    // ms
    parameter WINDOW_LO = 450,    // ms (earliest service)
    parameter WINDOW_HI = 550     // ms (latest service)
)(
    input  wire  clk,
    input  wire  rst_b,
    input  wire  service,         // Watchdog service pulse
    input  wire  enable,
    output wire  wdog_timeout,    // Watchdog expired
    output wire  wdog_window_err  // Service outside window
);

    localparam CNT_MAX = CLK_FREQ * TIMEOUT / 1000;
    localparam CNT_MIN = CLK_FREQ * WINDOW_LO / 1000;

    reg [15:0] wdog_cnt;
    reg [1:0]  service_state;

    always @(posedge clk or negedge rst_b) begin
        if (!rst_b) begin
            wdog_cnt <= 16'd0;
            service_state <= 2'd0;
        end else if (enable) begin
            if (service && (wdog_cnt >= CNT_MIN) && (wdog_cnt <= CNT_MAX)) begin
                wdog_cnt <= 16'd0;        // Reset on valid service
                service_state <= 2'd1;    // Acknowledged
            end else if (service && wdog_cnt < CNT_MIN) begin
                service_state <= 2'd2;    // Error: too early
            end else if (service && wdog_cnt > CNT_MAX) begin
                service_state <= 2'd3;    // Error: too late
            end else begin
                wdog_cnt <= wdog_cnt + 1'b1;
            end
        end
    end

    assign wdog_timeout    = (wdog_cnt >= CNT_MAX) && enable;
    assign wdog_window_err = (service_state == 2'd2); // Too early

endmodule
```

## 6. Power-Aware RTL Patterns

### 6.1 Clock Gating Insertion Guide

```
Clock Gating Strategy for iPACE-CHIP:
═══════════════════════════════════════════════════════════════

  Block             │ Gate Condition      │ Savings (avg)
  ──────────────────┼─────────────────────┼──────────────
  AFE + ADC         │ pacing_active       │ 4.5 µA
  Digital Core      │ !sleep_mode         │ 4.0 µA
  Output Driver     │ pace_vent | pace_atrial │ 1.6 µA
  Telemetry UART    │ tele_active         │ (duty-cycled)
  PLL               │ tele_active         │ 10.0 µA
  ──────────────────┼─────────────────────┼──────────────
  Total gated       │                     │ ~20 µA saved

  RTL Pattern:
    // Bad: Clock runs always
    always @(posedge clk_core) begin
        if (enable) data <= new_data;
    end

    // Good: Clock gated when not needed
    wire clk_afe;
    icg_cell u_icg (.clk_in(clk_core), .enable(afe_active),
                    .test_mode(tst_scan_en), .clk_out(clk_afe));
    always @(posedge clk_afe) begin
        data <= new_data;
    end
```

### 6.2 Power State Encoding in RTL

```verilog
//==========================================================================
// Power State Register
// Controls power gating across subsystems
//==========================================================================

module power_state_ctrl (
    input  wire              clk,
    input  wire              rst_b,
    input  wire [1:0]        pwr_cmd,       // Sleep, Active, Tele
    input  wire              wdog_timeout,
    input  wire              tele_carrier_det,
    output reg  [1:0]        pwr_state,
    output reg               en_afe,
    output reg               en_dsp,
    output reg               en_tele,
    output reg               en_pll,
    output reg               en_output_drv
);

    localparam P_SLEEP  = 2'b00;
    localparam P_ACTIVE = 2'b01;
    localparam P_TELE   = 2'b10;
    localparam P_SAFE   = 2'b11;

    always @(posedge clk or negedge rst_b) begin
        if (!rst_b) begin
            pwr_state <= P_SLEEP;
            {en_afe, en_dsp, en_tele, en_pll, en_output_drv} <= 5'b0;
        end else begin
            case (pwr_state)
                P_SLEEP: begin
                    if (wdog_timeout || tele_carrier_det)
                        pwr_state <= P_ACTIVE;
                end
                P_ACTIVE: begin
                    if (pwr_cmd == P_TELE) pwr_state <= P_TELE;
                    else if (pwr_cmd == P_SLEEP) pwr_state <= P_SLEEP;
                end
                P_TELE: begin
                    if (pwr_cmd == P_ACTIVE) pwr_state <= P_ACTIVE;
                end
                P_SAFE: begin
                    // Stays in safe mode until reset
                end
                default: pwr_state <= P_SAFE;
            endcase

            // Subsystem enables based on state
            en_afe        <= (pwr_state == P_ACTIVE);
            en_dsp        <= (pwr_state == P_ACTIVE);
            en_tele       <= (pwr_state == P_TELE);
            en_pll        <= (pwr_state == P_TELE);
            en_output_drv <= (pwr_state == P_ACTIVE);
        end
    end

endmodule
```

## 7. Code Quality Metrics

### 7.1 Linting Rules (SpyGlass/Lint)

```
RTL Linting Configuration for iPACE-CHIP:
═══════════════════════════════════════════════════════════════

  Tool: Synopsys SpyGlass Lint or Cadence HAL

  Mandatory Rules:
  ┌──────┬──────────────────────────────┬─────────────────┐
  │ #    │ Rule                         │ Severity        │
  ├──────┼──────────────────────────────┼─────────────────┤
  │ 1    │ No inferred latches          │ ERROR           │
  │ 2    │ All FFs have async reset     │ ERROR           │
  │ 3    │ No combinational loops       │ ERROR           │
  │ 4    │ No unused signals            │ WARNING         │
  │ 5    │ No multi-driver nets         │ ERROR           │
  │ 6    │ All case items covered       │ WARNING         │
  │ 7    │ Default case in FSM          │ ERROR           │
  │ 8    │ No #delay in RTL             │ ERROR           │
  │ 9    │ All inputs registered        │ WARNING         │
  │ 10   │ No tri-states in core        │ ERROR           │
  │ 11   │ Clock/reset not data path    │ ERROR           │
  │ 12   │ Bus widths match             │ WARNING         │
  │ 13   │ No zero-width buses          │ ERROR           │
  │ 14   │ Parameter overrides explicit │ WARNING         │
  │ 15   │ No async set/reset on sync FF│ ERROR           │
  └──────┴──────────────────────────────┴─────────────────┘

  Run Command:
    spyglass -project ipace_lint.tcl

  Expected Result: 0 errors, <10 warnings
```

## 8. Code Review Checklist

```
RTL Code Review Checklist (per module):
═══════════════════════════════════════════════════════════════

┌────┬─────────────────────────────────┬──────┬──────────────┐
│ #  │ Criterion                       │ Pass │ Notes        │
├────┼─────────────────────────────────┼──────┼──────────────┤
│  1 │ Module header complete          │      │              │
│  2 │ Parameters have defaults        │      │              │
│  3 │ Port directions declared        │      │              │
│  4 │ Reset behavior correct          │      │              │
│  5 │ Clock domain identified         │      │              │
│  6 │ No latches inferred             │      │              │
│  7 │ FSM has safe default state      │      │              │
│  8 │ All counters have overflow prot │      │              │
│  9 │ Bus widths consistent           │      │              │
│ 10 │ CDC synchronizers present       │      │              │
│ 11 │ TMR on safety-critical signals  │      │              │
│ 12 │ Clock gating appropriate        │      │              │
│ 13 │ DFT: scan chain compatible      │      │              │
│ 14 │ Safety: fault detection present │      │              │
│ 15 │ Power: no unnecessary switching │      │              │
│ 16 │ Naming conventions followed     │      │              │
│ 17 │ Comments explain non-obvious    │      │              │
│ 18 │ Traceability to requirements    │      │              │
└────┴─────────────────────────────────┴──────┴──────────────┘
```

## 9. Summary

The iPACE-CHIP RTL coding guidelines ensure:

1. **Synthesis-friendly** code with no latches, proper resets, and safe FSM encoding
2. **Safety-critical** patterns including TMR, ECC, and watchdog integration
3. **DFT-compatible** structure with scan-chain-ready flip-flops and test modes
4. **Power-aware** design with systematic clock gating and power state management
5. **CDC-safe** synchronizers at all clock domain boundaries
6. **Traceable** code that links back to safety requirements (SF-001, SF-002)

---

*Previous: [IP Selection](../../01-Specification-Architecture/04-IP-Selection/ip-selection.md)*
