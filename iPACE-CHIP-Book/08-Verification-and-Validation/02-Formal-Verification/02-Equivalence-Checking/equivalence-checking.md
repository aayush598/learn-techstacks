# Equivalence Checking for iPACE-CHIP Pacemaker

## 1. Introduction

Equivalence checking (EQEC) formally proves that two representations of a design are functionally identical. For the iPACE-CHIP pacemaker, equivalence checking is used at multiple stages: RTL-to-gate-level, pre-optimization to post-optimization, and design variant comparison. This ensures that synthesis, optimization, and retiming transformations preserve the pacemaker's safety-critical functionality.

## 2. Equivalence Checking Flow

### 2.1 Verification Stages

```
RTL Design (golden)
    │
    ▼
Formal Equivalence Check ← RTL vs. Synthesized Netlist
    │
    ▼
Synthesized Netlist
    │
    ▼
Formal Equivalence Check ← Pre-layout vs. Post-layout
    │
    ▼
Post-Layout Netlist
    │
    ▼
Formal Equivalence Check ← Post-layout vs. GDS extracted
    │
    ▼
Final GDS
```

### 2.2 Equivalence Points

```
Design Partition
├── Pacing Controller
│   ├── Primary Inputs: sense_amp_out, inhibit, mode_reg[3:0]
│   ├── Primary Outputs: pace_pulse, pace_amplitude[7:0]
│   └── Sequential: state_reg, timer_reg, refractory_cnt
├── Timing Engine
│   ├── Primary Inputs: clk, rst_n, start_timer
│   ├── Primary Outputs: timeout, timer_value[15:0]
│   └── Sequential: timer_cnt, timer_running
├── Safety Monitor
│   ├── Primary Inputs: lead_impedance[15:0], battery_voltage[7:0]
│   ├── Primary Outputs: fault_flag, alert_code[3:0]
│   └── Sequential: fault_state, alert_reg
└── Configuration Register Block
    ├── Primary Inputs: apb_addr[7:0], apb_wdata[31:0], apb_write
    ├── Primary Outputs: apb_rdata[31:0]
    └── Sequential: reg_file[0:255]
```

## 3. RTL-to-Netlist Equivalence

### 3.1 Pacing Controller Mapping

```systemverilog
// RTL (Reference)
module pacing_controller (
  input  logic        clk,
  input  logic        rst_n,
  input  logic        sense_amp_out,
  input  logic        inhibit,
  input  logic [3:0]  mode_reg,
  input  logic [7:0]  lower_rate_limit,
  input  logic [7:0]  pulse_amplitude_cfg,
  output logic        pace_pulse,
  output logic [7:0]  pace_amplitude
);

  typedef enum logic [2:0] {
    IDLE, SENSE, PACE, REFRACTORY, INHIBIT_ST
  } state_t;

  state_t state, next_state;
  logic [15:0] timer_cnt;
  logic [7:0]  refractory_cnt;
  logic        timer_expired;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n)
      state <= IDLE;
    else
      state <= next_state;
  end

  always_comb begin
    next_state = state;
    case (state)
      IDLE: begin
        if (!sense_amp_out && !inhibit && timer_expired)
          next_state = PACE;
        else if (!sense_amp_out && !inhibit && !timer_expired)
          next_state = SENSE;
      end
      SENSE: begin
        if (timer_expired)
          next_state = PACE;
        else if (sense_amp_out)
          next_state = INHIBIT_ST;
      end
      PACE: begin
        next_state = REFRACTORY;
      end
      REFRACTORY: begin
        if (refractory_cnt == 0)
          next_state = IDLE;
      end
      INHIBIT_ST: begin
        if (!sense_amp_out)
          next_state = IDLE;
      end
    endcase
  end

  // Timer logic
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      timer_cnt <= 0;
    end else begin
      case (state)
        IDLE: timer_cnt <= timer_cnt + 1;
        SENSE: timer_cnt <= timer_cnt + 1;
        default: timer_cnt <= 0;
      endcase
    end
  end

  assign timer_expired = (timer_cnt >= {8'd0, lower_rate_limit, 4'd0});

  // Pace generation
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      pace_pulse <= 0;
      pace_amplitude <= 0;
    end else begin
      if (state == PACE) begin
        pace_pulse <= 1;
        pace_amplitude <= pulse_amplitude_cfg;
      end else begin
        pace_pulse <= 0;
        pace_amplitude <= 0;
      end
    end
  end

  // Refractory counter
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n)
      refractory_cnt <= 0;
    else if (state == PACE)
      refractory_cnt <= 8'd30;
    else if (state == REFRACTORY && refractory_cnt > 0)
      refractory_cnt <= refractory_cnt - 1;
  end

endmodule
```

### 3.2 Synthesized Netlist (Gate-Level)

```systemverilog
// Synthesized gate-level (Implementation - representative)
module pacing_controller_synth (
  input  logic        clk,
  input  logic        rst_n,
  input  logic        sense_amp_out,
  input  logic        inhibit,
  input  logic [3:0]  mode_reg,
  input  logic [7:0]  lower_rate_limit,
  input  logic [7:0]  pulse_amplitude_cfg,
  output logic        pace_pulse,
  output logic [7:0]  pace_amplitude
);

  // State encoding may differ after synthesis
  wire [2:0] state_synth;
  wire [15:0] timer_synth;
  wire [7:0] refrac_synth;
  wire timer_exp_synth;

  // Logic gates implementing the same functionality
  // with potentially different structural representation

  // The equivalence checker proves:
  // For all input combinations and initial states,
  // primary outputs match between RTL and synth
  // (after accounting for register mapping)

endmodule
```

## 4. Equivalence Check Points

### 4.1 Compare Points Definition

```systemverilog
// Equivalence check specification
module pacing_equiv_check;

  // Reference (RTL) instance
  pacing_controller u_ref (
    .clk                (clk),
    .rst_n              (rst_n),
    .sense_amp_out      (sense_amp_out),
    .inhibit            (inhibit),
    .mode_reg           (mode_reg),
    .lower_rate_limit   (lower_rate_limit),
    .pulse_amplitude_cfg(pulse_amplitude_cfg),
    .pace_pulse         (pace_pulse_ref),
    .pace_amplitude     (pace_amplitude_ref)
  );

  // Implementation (synthesized) instance
  pacing_controller_synth u_impl (
    .clk                (clk),
    .rst_n              (rst_n),
    .sense_amp_out      (sense_amp_out),
    .inhibit            (inhibit),
    .mode_reg           (mode_reg),
    .lower_rate_limit   (lower_rate_limit),
    .pulse_amplitude_cfg(pulse_amplitude_cfg),
    .pace_pulse         (pace_pulse_impl),
    .pace_amplitude     (pace_amplitude_impl)
  );

  // Sequential compare points
  // These are mapped by the equivalence checking tool
  // based on register names or manual correspondence

  // Output compare points
  wire outputs_equal =
    (pace_pulse_ref == pace_pulse_impl) &&
    (pace_amplitude_ref == pace_amplitude_impl);

endmodule
```

### 4.2 Blackbox vs Whitebox

```
Blackbox Equivalence:
  - Treat sequential elements as blackboxes
  - Only compare combinational logic equivalence
  - Faster but less complete

Whitebox Equivalence:
  - Map all registers between reference and implementation
  - Prove full sequential equivalence
  - Slower but comprehensive

Pacemaker Strategy:
  - Whitebox for safety-critical modules (pacing controller, safety monitor)
  - Blackbox for non-critical modules (telemetry, configuration registers)
```

## 5. Optimization-Aware Equivalence

### 5.1 Retiming Equivalence

```systemverilog
// Pre-retiming (reference)
module timer_pre_retiming (
  input  logic        clk,
  input  logic        rst_n,
  input  logic [7:0]  load_value,
  input  logic        load,
  output logic [7:0]  count,
  output logic        expired
);

  logic [7:0] cnt_reg;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n)
      cnt_reg <= 0;
    else if (load)
      cnt_reg <= load_value;
    else if (cnt_reg > 0)
      cnt_reg <= cnt_reg - 1;
  end

  assign count = cnt_reg;
  assign expired = (cnt_reg == 0);

endmodule

// Post-retiming (implementation) - registers moved
module timer_post_retiming (
  input  logic        clk,
  input  logic        rst_n,
  input  logic [7:0]  load_value,
  input  logic        load,
  output logic [7:0]  count,
  output logic        expired
);

  // Logic retimed: comparator moved before register
  logic [7:0] cnt_reg;
  logic       expired_comb;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n)
      cnt_reg <= 0;
    else if (load)
      cnt_reg <= load_value;
    else if (cnt_reg > 0)
      cnt_reg <= cnt_reg - 1;
  end

  assign expired_comb = (cnt_reg == 0);
  // Output register added for retiming balance
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n)
      expired <= 1;
    else
      expired <= expired_comb;
  end

  assign count = cnt_reg;

endmodule
```

### 5.2 Logic Restructuring Equivalence

```systemverilog
// Pre-optimization: Behavioral description
assign pace_amplitude = (state == PACE) ? pulse_amplitude_cfg : 8'd0;

// Post-optimization: Structurally equivalent
assign pace_amplitude[0] = state[0] & state[1] & pulse_amplitude_cfg[0];
assign pace_amplitude[1] = state[0] & state[1] & pulse_amplitude_cfg[1];
// ... (structural implementation of mux)
```

## 6. Formal Equivalence Properties

### 6.1 Safety-Preserving Equivalence

```systemverilog
// Property: If RTL is safe, implementation must be safe
property safety_preservation;
  @(posedge clk)
    (pace_pulse_ref |-> pace_amplitude_ref <= MAX_SAFE_AMP)
    |->
    (pace_pulse_impl |-> pace_amplitude_impl <= MAX_SAFE_AMP);
endproperty

assert property (safety_preservation) else
  `uvm_error("EQEC_SAFETY", "Safety not preserved through optimization");

// Property: Timing equivalence
property timing_equivalence;
  @(posedge clk)
    (timer_expired_ref == timer_expired_impl);
endproperty

assert property (timing_equivalence) else
  `uvm_error("EQEC_TIMING", "Timing behavior changed");

// Property: Mode behavior equivalence
property mode_equivalence;
  @(posedge clk)
    (mode_reg == mode_reg_ref) &&
    (sense_amp_out == sense_amp_out_ref) &&
    (inhibit == inhibit_ref)
    |-> ##[0:3]
      (pace_pulse_ref == pace_pulse_impl);
endproperty

assert property (mode_equivalence) else
  `uvm_error("EQEC_MODE", "Mode behavior mismatch");
```

## 7. Incremental Equivalence Checking

### 7.1 Change-Based Verification

```systemverilog
// When only a subset of logic changes, check only affected paths
// Incremental equivalence flow:
//
// 1. Identify changed logic region
// 2. Create cone-of-influence for changed signals
// 3. Run targeted equivalence check on affected paths
// 4. Prove equivalence for unchanged regions by reuse

// Example: Only pulse_amplitude logic changed
// Check only: pulse_amplitude_ref == pulse_amplitude_impl
// Given: all inputs to pulse_amplitude logic are equivalent
```

### 7.2 Incremental Check Script

```
# Incremental equivalence checking flow
read_design -ref   pre_change.v
read_design -impl  post_change.v

# Identify changes
set_changed_region pacing_controller/pulse_amplitude_logic

# Set known-equivalent points
set_equivalent -point state_reg[*]
set_equivalent -point timer_cnt[*]
set_equivalent -point refractory_cnt[*]

# Run incremental check
check_equivalence -incremental

# Report
report_equivalence -summary
```

## 8. Multiple-File Equivalence

### 8.1 Module-Level Checking

```systemverilog
// Module-level equivalence pairs for iPACE-CHIP
//
// Module                    Reference         Implementation
// ─────────────────────────────────────────────────────────
// pacing_controller         RTL/pacing.v      synth/pacing_synth.v
// timing_engine             RTL/timing.v      synth/timing_synth.v
// safety_monitor            RTL/safety.v      synth/safety_synth.v
// config_registers          RTL/config.v      synth/config_synth.v
// apb_interface             RTL/apb.v         synth/apb_synth.v
// uart_transmitter          RTL/uart_tx.v     synth/uart_tx_synth.v
// battery_monitor           RTL/batt.v        synth/batt_synth.v
// clock_divider             RTL/clkdiv.v      synth/clkdiv_synth.v
```

## 9. Equivalence Checking Challenges

### 9.1 Common Non-Equivalence Issues

| Issue | Description | Resolution |
|-------|-------------|------------|
| Logic sharing | Synthesizer shares logic across outputs | Add compare points at shared nodes |
| Constant propagation | Constants folded into logic | Map constant-folded paths |
| Dead code removal | Unreachable logic eliminated | Prove dead code unreachable |
| State encoding | Different FSM encoding | Map state bits explicitly |
| Reset polarity | Synthesis may invert reset | Verify reset mapping |

### 9.2 Debugging Non-Equivalence

```systemverilog
// When equivalence fails, generate counterexample
// The tool provides:
// 1. Input sequence causing mismatch
// 2. Internal state divergent point
// 3. First cycle where outputs differ

// Debug aid: intermediate compare points
wire [7:0] timer_ref = u_ref.timer_cnt;
wire [7:0] timer_impl = u_impl.timer_cnt;
// Check: timer_ref == timer_impl (intermediate check)

wire [2:0] state_ref = u_ref.state;
wire [2:0] state_impl = u_impl.state;
// Check: state mapping correct
```

## 10. Summary

Equivalence checking for the iPACE-CHIP pacemaker ensures:

| Check Type | Scope | Tool Requirement |
|------------|-------|------------------|
| RTL-to-Gate | Full design | Formal equivalence |
| Pre-to-Post Opt | Retimed logic | Sequential equivalence |
| Blackbox | Non-critical | Combinational equivalence |
| Incremental | Changed regions | Targeted checking |
| Safety-Preserving | Safety modules | Property-based proof |

Key benefits for the pacemaker:
- **Guaranteed optimization safety** - synthesis cannot introduce bugs
- **Register mapping verification** - correct sequential element correspondence
- **Retiming validation** - latency changes preserve functionality
- **Logic restructuring proof** - structural changes maintain behavior
- **Continuous regression** - every synthesis run formally checked
