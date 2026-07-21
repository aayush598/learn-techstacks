# Assertion Disable and Control for iPACE-CHIP Pacemaker

## 1. Introduction

Assertion disable mechanisms allow selective control over when assertions are active, providing flexibility during verification. For the iPACE-CHIP pacemaker, disable mechanisms are essential for handling reset sequences, mode transitions, testbench-driven stimulus, and formal verification assumptions.

## 2. Disable Mechanisms

### 2.1 disable iff

```systemverilog
// disable iff: Disable assertion when condition is true
property pace_pulse_width;
  @(posedge clk) disable iff (!rst_n)
    $rose(pace_pulse) |=> ##[1:MAX_WIDTH] $fell(pace_pulse);
endproperty

assert property (pace_pulse_width) else
  `uvm_error("SVA", "Pulse width violation");

// disable iff during reset
property amplitude_safe;
  @(posedge clk) disable iff (!rst_n || mode_switch_in_progress)
    pace_pulse |-> pace_amplitude inside {[MIN_AMP:MAX_AMP]};
endproperty

assert property (amplitude_safe) else
  `uvm_error("SAFETY", "Amplitude unsafe during operation");
```

### 2.2 disable at start

```systemverilog
// Disable at assertion start
property refractory_check;
  @(posedge clk) disable iff (!rst_n)
    ($rose(pace_pulse) && !in_refractory)
    |-> ##REFRACTORY_CYCLES !pace_pulse;
endproperty

assert property (refractory_check) else
  `uvm_error("REFRACT", "Refractory violation");
```

## 3. Assertion Control Macros

### 3.1 Conditional Assertion Enable

```systemverilog
// Macro-based assertion control
`define ENABLE_SAFETY_ASSERTIONS 1
`define ENABLE_TIMING_ASSERTIONS 1
`define ENABLE_PERFORMANCE_ASSERTIONS 0

`ifdef ENABLE_SAFETY_ASSERTIONS
  property amplitude_safe;
    @(posedge clk) disable iff (!rst_n)
      pace_pulse |-> pace_amplitude <= MAX_AMPLITUDE;
  endproperty
  assert property (amplitude_safe) else
    `uvm_error("SAFETY", "Amplitude exceeded");
`endif

`ifdef ENABLE_TIMING_ASSERTIONS
  property rate_check;
    @(posedge clk) disable iff (!rst_n)
      $rose(pace_pulse) |-> ##[MIN_RATE:MAX_RATE] $rose(pace_pulse);
  endproperty
  assert property (rate_check) else
    `uvm_error("TIMING", "Rate out of bounds");
`endif
```

### 3.2 Runtime Assertion Toggle

```systemverilog
// Runtime assertion enable/disable via variables
bit enable_safety_assertions = 1;
bit enable_timing_assertions = 1;
bit enable_debug_assertions  = 0;

property pace_amplitude_safe;
  @(posedge clk) disable iff (!rst_n || !enable_safety_assertions)
    pace_pulse |-> pace_amplitude inside {[MIN_AMP:MAX_AMP]};
endproperty

property rate_limit_check;
  @(posedge clk) disable iff (!rst_n || !enable_timing_assertions)
    $rose(pace_pulse) |-> !pace_pulse [*1:MIN_INTER_CYCLES-1];
endproperty

// Toggle assertions from test
task disable_safety_assertions();
  enable_safety_assertions = 0;
endtask

task enable_safety_assertions();
  enable_safety_assertions = 1;
endtask
```

## 4. Formal Verification Disables

### 4.1 Assume vs Assert

```systemverilog
// In simulation: assert (DUT behavior)
// In formal: assume (environment constraint)

// Formal verification mode
`ifdef FORMAL
  // Input constraints (assumptions)
  assume property (@(posedge clk) disable iff (!rst_n)
    mode_reg inside {4'h0, 4'h4, 4'h6, 4'h8, 4'hD}
  );

  assume property (@(posedge clk) disable iff (!rst_n)
    lower_rate_limit inside {[50:120]}
  );

  // Properties to prove (assertions)
  assert property (@(posedge clk) disable iff (!rst_n)
    pace_pulse |-> pace_amplitude <= MAX_AMPLITUDE
  );
`else
  // Simulation mode: all are assertions
  assert property (@(posedge clk) disable iff (!rst_n)
    mode_reg inside {4'h0, 4'h4, 4'h6, 4'h8, 4'hD}
  ) else `uvm_error("MODE", "Invalid mode");

  assert property (@(posedge clk) disable iff (!rst_n)
    pace_pulse |-> pace_amplitude <= MAX_AMPLITUDE
  ) else `uvm_error("SAFETY", "Amplitude exceeded");
`endif
```

### 4.2 Formal Assumptions

```systemverilog
// Environment assumptions for formal verification
assume property (@(posedge clk) disable iff (!rst_n)
  sense_amp_out |-> sense_amp_out [*1:MAX_SENSE_CYCLES]
);

assume property (@(posedge clk) disable iff (!rst_n)
  inhibit |-> inhibit [*1:MAX_INHIBIT_CYCLES]
);

assume property (@(posedge clk) disable iff (!rst_n))
  $rose(fault_flag) |-> fault_flag [*1:MAX_FAULT_DURATION]
);

// Stability assumptions
assume property (@(posedge clk) disable iff (!rst_n)
  $stable(mode_reg) [*5:100]
);

assume property (@(posedge clk) disable iff (!rst_n)
  $stable(lower_rate_limit) [*10:200]
);
```

## 5. Assertion Layers

### 5.1 Layered Assertion Architecture

```systemverilog
// Layer 0: Critical safety (always active)
property safety_layer_amplitude;
  @(posedge clk) disable iff (!rst_n)
    pace_pulse |-> pace_amplitude <= MAX_AMP;
endproperty

// Layer 1: Protocol compliance (active during normal operation)
property protocol_layer_mode;
  @(posedge clk) disable iff (!rst_n || in_reset_sequence)
    mode_reg_valid |-> mode_behavior_correct;
endproperty

// Layer 2: Performance (active during testing)
property performance_layer_rate;
  @(posedge clk) disable iff (!rst_n || !testing_mode)
    rate_accuracy_check;
endproperty

// Layer 3: Debug (active only in debug mode)
property debug_layer_trace;
  @(posedge clk) disable iff (!rst_n || !debug_mode)
    detailed_behavior_check;
endproperty
```

### 5.2 Layer Control

```systemverilog
class assertion_layer_control;
  bit safety_layer_enabled    = 1;  // Always on
  bit protocol_layer_enabled  = 1;  // On during operation
  bit performance_layer_enabled = 0; // On during tests
  bit debug_layer_enabled     = 0;  // On in debug

  function void enable_all();
    protocol_layer_enabled = 1;
    performance_layer_enabled = 1;
    debug_layer_enabled = 1;
  endfunction

  function void enable_safety_only();
    protocol_layer_enabled = 0;
    performance_layer_enabled = 0;
    debug_layer_enabled = 0;
  endfunction

  function void enable_for_formal();
    safety_layer_enabled = 1;
    protocol_layer_enabled = 1;
    performance_layer_enabled = 0;
    debug_layer_enabled = 0;
  endfunction
endclass
```

## 6. Reset Sequence Handling

### 6.1 Assertion Suppression During Reset

```systemverilog
// Proper reset handling for assertions
property reset_behavior;
  @(posedge clk)
    !rst_n |=> state == IDLE;
endproperty

assert property (reset_behavior) else
  `uvm_error("RESET", "Reset not reaching idle state");

// Assertions disabled during reset
property normal_operation;
  @(posedge clk) disable iff (!rst_n)
    state正常使用_check;
endproperty

// Power-on reset sequence
sequence por_sequence;
  !rst_n ##1 rst_n [*10]; // 10 cycles after reset release
endsequence

property por_stability;
  @(posedge clk)
    por_sequence |-> !pace_pulse [*10];
endproperty

assert property (por_stability) else
  `uvm_error("POR", "Pace pulse during power-on reset");
```

## 7. Assertion Reports

### 7.1 Assertion Statistics

```systemverilog
// Assertion statistics collection
class assertion_stats;
  int total_assertions = 0;
  int passed_assertions = 0;
  int failed_assertions = 0;
  int disabled_assertions = 0;

  function void report();
    `uvm_info("ASSERT_STATS", $sformatf(
      "\n===== ASSERTION STATISTICS =====\nTotal:     %0d\nPassed:    %0d\nFailed:    %0d\nDisabled:  %0d\nPass Rate: %0.1f%%\n================================",
      total_assertions, passed_assertions, failed_assertions,
      disabled_assertions,
      (total_assertions > 0) ?
        100.0 * passed_assertions / total_assertions : 0.0), UVM_LOW)
  endfunction
endclass
```

### 7.2 Assertion Failure Analysis

```systemverilog
// Assertion failure with context
property amplitude_safe_detailed;
  @(posedge clk) disable iff (!rst_n)
    pace_pulse |-> pace_amplitude inside {[MIN_AMP:MAX_AMP]};
endproperty

assert property (amplitude_safe_detailed) else begin
  `uvm_error("SAFETY", $sformatf(
    "\n=== ASSERTION FAILURE ===\nTime:        %0t\nAmplitude:   %0d\nAllowed:     [%0d:%0d]\nMode:        0x%h\nFault Flag:  %b\n=========================",
    $time, pace_amplitude, MIN_AMP, MAX_AMP,
    mode_reg, fault_flag))
end
```

## 8. Assertion Masking

### 8.1 Known-Bug Masking

```systemverilog
// Mask known bugs during development
// (Must be tracked and removed before tapeout)

bit mask_known_bug_1234 = 0; // Set to 1 to mask

property pace_amplitude_safe;
  @(posedge clk) disable iff (!rst_n || mask_known_bug_1234)
    pace_pulse |-> pace_amplitude inside {[MIN_AMP:MAX_AMP]};
endproperty

// Version-controlled masking
`define BUG_1234_MASK 0  // Set to 1 to mask, 0 to enforce

property pace_amplitude_safe;
  @(posedge clk) disable iff (!rst_n || `BUG_1234_MASK)
    pace_pulse |-> pace_amplitude inside {[MIN_AMP:MAX_AMP]};
endproperty
```

### 8.2 Conditional Masking

```systemverilog
// Mask assertions based on test phase
property amplitude_check;
  @(posedge clk) disable iff (!rst_n || test_phase == RESET_PHASE)
    pace_pulse |-> pace_amplitude <= MAX_AMP;
endproperty

// Mask during mode transition
property mode_stability;
  @(posedge clk) disable iff (!rst_n || mode_transition_pending)
    $stable(pacing_mode) [*5];
endproperty

// Mask during calibration
property calibration_masked;
  @(posedge clk) disable iff (!rst_n || calibration_mode)
    1; // Effectively disabled during calibration
endproperty
```

## 9. Summary

Assertion disable and control for the iPACE-CHIP pacemaker provides:

| Mechanism | Use Case | Control |
|-----------|----------|---------|
| disable iff | Reset/mode transition | Automatic |
| Runtime toggle | Test-phase control | Software variable |
| Compile-time | Feature gating | Preprocessor macros |
| Formal assume | Environment constraints | `ifdef FORMAL |
| Layer control | Selective checking | Class-based |
| Known-bug mask | Development flexibility | Version-controlled |

Best practices:
- **Always disable during reset** to avoid false failures
- **Use layers** for progressive assertion activation
- **Track all masks** with issue tracking numbers
- **Remove masks** before final verification signoff
- **Document disable conditions** in assertion comments
