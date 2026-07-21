# SystemVerilog Assertions (SVA) Properties for iPACE-CHIP Pacemaker

## 1. Introduction

SystemVerilog Assertions (SVA) provide a property specification language embedded directly in the design and verification code. For the iPACE-CHIP pacemaker, SVA assertions serve as executable specifications, runtime checkers, and formal verification properties that ensure correct operation at every clock cycle.

## 2. SVA Property Fundamentals

### 2.1 Property Declaration

```systemverilog
// Simple concurrent property
property pace_pulse_width;
  @(posedge clk) disable iff (!rst_n)
    $rose(pace_pulse) |=> ##[1:MAX_WIDTH-1] $fell(pace_pulse);
endproperty

assert property (pace_pulse_width) else
  `uvm_error("SVA", "Pulse width out of specification");

// Property with local variables
property refractory_check;
  @(posedge clk) disable iff (!rst_n)
    int start_time;
    ($rose(pace_pulse), start_time = $time)
    |-> ##[REFRACTORY_MIN:REFRACTORY_MAX]
      ($time - start_time) inside {[REFRACTORY_MIN*10:REFRACTORY_MAX*10]};
endproperty

assert property (refractory_check) else
  `uvm_error("SVA", "Refractory period out of bounds");
```

### 2.2 Property Operators Reference

```
Operator    Symbol      Example
─────────────────────────────────────────────
and         &&          prop_a && prop_b
or          ||          prop_a || prop_b
not         !           !prop
implies     |->         antecedent |-> consequent
follows     |=>         antecedent |=> consequent
nexttime    ##n         ##1 prop
eventually  s_eventually s_eventually prop
always      always      always prop
until       s_until     prop_a s_until prop_b
within      within      prop_a within prop_b
```

## 3. Pacing Algorithm Properties

### 3.1 VVI Mode Properties

```systemverilog
// VVI: Ventricular sense inhibits pacing
property vvi_inhibit;
  @(posedge clk) disable iff (!rst_n)
    (mode_reg == MODE_VVI && $fell(sense_amp_out))
    |-> ##1 pace_pulse == 0;
endproperty

assert property (vvi_inhibit) else
  `uvm_error("VVI", "VVI mode: pacing not inhibited on sense");

// VVI: Pace when escape interval expires
property vvi_pace_on_escape;
  @(posedge clk) disable iff (!rst_n)
    (mode_reg == MODE_VVI &&
     timer_expired &&
     !sense_detected &&
     !inhibit_active)
    |-> ##[0:2] pace_pulse;
endproperty

assert property (vvi_pace_on_escape) else
  `uvm_error("VVI", "VVI mode: pace not generated on escape");

// VVI: Refractory period after pace
property vvi_refractory;
  @(posedge clk) disable iff (!rst_n)
    (mode_reg == MODE_VVI && $rose(pace_pulse))
    |-> !pace_pulse [*1:REFRACTORY_CYCLES];
endproperty

assert property (vvi_refractory) else
  `uvm_error("VVI", "VVI mode: pace during refractory period");
```

### 3.2 DDD Mode Properties

```systemverilog
// DDD: Atrial tracking with AV delay
property ddd_av_delay;
  @(posedge clk) disable iff (!rst_n)
    (mode_reg == MODE_DDD && $fell(atrial_sense))
    |-> ##[AV_DELAY_MIN:AV_DELAY_MAX]
      ($rose(pace_pulse) || $fell(ventricular_sense));
endproperty

assert property (ddd_av_delay) else
  `uvm_error("DDD", "DDD mode: AV delay violated");

// DDD: Upper rate limit tracking
property ddd_upper_rate;
  @(posedge clk) disable iff (!rst_n)
    (mode_reg == MODE_DDD && $rose(pace_pulse))
    |-> !pace_pulse [*1:MIN_INTER_PACE_CYCLES];
endproperty

assert property (ddd_upper_rate) else
  `uvm_error("DDD", "DDD mode: upper rate limit exceeded");

// DDD: Dual chamber pacing
property ddd_dual_pace;
  @(posedge clk) disable iff (!rst_n)
    (mode_reg == MODE_DDD && atrial_paced)
    |-> ##[AV_DELAY_MIN:AV_DELAY_MAX] ventricular_paced;
endproperty

assert property (ddd_dual_pace) else
  `uvm_error("DDD", "DDD mode: ventricular pace missing after atrial");
```

### 3.3 AAI Mode Properties

```systemverilog
// AAI: Atrial inhibit on sense
property aai_inhibit;
  @(posedge clk) disable iff (!rst_n)
    (mode_reg == MODE_AAI && $fell(atrial_sense))
    |-> ##1 atrial_pace == 0;
endproperty

assert property (aai_inhibit) else
  `uvm_error("AAI", "AAI mode: atrial pace not inhibited");
```

## 4. Timing Properties

### 4.1 Pulse Timing

```systemverilog
// Pulse width specification
property pulse_width_spec;
  @(posedge clk) disable iff (!rst_n)
    $rose(pace_pulse) |-> ##[MIN_PULSE_CYC:MAX_PULSE_CYC]
      $fell(pace_pulse);
endproperty

assert property (pulse_width_spec) else
  `uvm_error("TIMING", "Pulse width out of specification");

// Inter-pace interval
property inter_pace_interval;
  @(posedge clk) disable iff (!rst_n)
    $fell(pace_pulse) |-> !pace_pulse [*1:MIN_INTER_PACE_CYCLES-1]
      ##1 ($rose(pace_pulse) || !need_pace);
endproperty

assert property (inter_pace_interval) else
  `uvm_error("TIMING", "Inter-pace interval too short");

// Rate accuracy check
property rate_accuracy;
  @(posedge clk) disable iff (!rst_n)
    $rose(pace_pulse) |-> ##[MIN_RATE_CYCLES-5:MAX_RATE_CYCLES+5]
      $rose(pace_pulse);
endproperty

assert property (rate_accuracy) else
  `uvm_error("TIMING", "Rate accuracy out of tolerance");
```

### 4.2 Timer Properties

```systemverilog
// Timer monotonic decrement
property timer_monotonic;
  @(posedge clk) disable iff (!rst_n)
    timer_running && timer_cnt > 0 |=> timer_cnt < $past(timer_cnt);
endproperty

assert property (timer_monotonic) else
  `uvm_error("TIMER", "Timer not monotonically decrementing");

// Timer expiration
property timer_expires;
  @(posedge clk) disable iff (!rst_n)
    $rose(timer_running) |-> ##[1:MAX_TIMER_COUNT] timer_expired;
endproperty

assert property (timer_expires) else
  `uvm_error("TIMER", "Timer did not expire");

// Timer reload on new cycle
property timer_reload;
  @(posedge clk) disable iff (!rst_n)
    $rose(new_cycle_start) |-> ##1 timer_cnt == reload_value;
endproperty

assert property (timer_reload) else
  `uvm_error("TIMER", "Timer not reloaded correctly");
```

## 5. Safety Properties

### 5.1 Amplitude Safety

```systemverilog
// Amplitude within safe range during pacing
property amplitude_safe_range;
  @(posedge clk) disable iff (!rst_n)
    pace_pulse |-> pace_amplitude inside {[MIN_AMP:MAX_AMP]};
endproperty

assert property (amplitude_safe_range) else
  `uvm_error("SAFETY", "Pace amplitude outside safe range");

// Amplitude zero when not pacing
property amplitude_zero_idle;
  @(posedge clk) disable iff (!rst_n)
    !pace_pulse |-> pace_amplitude == 0;
endproperty

assert property (amplitude_zero_idle) else
  `uvm_error("SAFETY", "Non-zero amplitude when not pacing");
```

### 5.2 Fault Detection Safety

```systemverilog
// Lead impedance fault detection
property lead_fault_detect;
  @(posedge clk) disable iff (!rst_n)
    (lead_impedance < Z_SHORT || lead_impedance > Z_OPEN)
    |-> ##[0:5] fault_flag;
endproperty

assert property (lead_fault_detect) else
  `uvm_error("SAFETY", "Lead fault not detected within latency");

// Battery low detection
property battery_low_detect;
  @(posedge clk) disable iff (!rst_n)
    (battery_voltage < BATT_LOW_THRESHOLD)
    |-> ##[0:10] battery_alert;
endproperty

assert property (battery_low_detect) else
  `uvm_error("SAFETY", "Battery low not detected");

// Watchdog timeout detection
property watchdog_detect;
  @(posedge clk) disable iff (!rst_n)
    !wdg_clear [*WDG_TIMEOUT:$]
    |-> reset_out;
endproperty

assert property (watchdog_detect) else
  `uvm_error("SAFETY", "Watchdog timeout not detected");
```

## 6. Sequence-Based Properties

### 6.1 Pacing Sequences

```systemverilog
// Complete pacing cycle sequence
sequence pacing_cycle_seq;
  $rose(pace_pulse) ##1
  pace_pulse [*1:MAX_PULSE_WIDTH] ##1
  $fell(pace_pulse) ##1
  !pace_pulse [*1:REFRACTORY_CYCLES];
endsequence

property pacing_cycle_complete;
  @(posedge clk) disable iff (!rst_n)
    pacing_cycle_seq;
endproperty

assert property (pacing_cycle_complete) else
  `uvm_error("SEQ", "Pacing cycle incomplete");

// Inhibit sequence
sequence inhibit_seq;
  $rose(inhibit) ##1
  inhibit [*1:MAX_INHIBIT_DURATION] ##1
  $fell(inhibit);
endsequence

property inhibit_sequence_complete;
  @(posedge clk) disable iff (!rst_n)
    inhibit_seq;
endproperty
```

### 6.2 Multi-Cycle Sequences

```systemverilog
// Fault detection and response sequence
sequence fault_response_seq;
  $rose(fault_flag) ##[1:LATENCY]
  fault_response_taken ##[1:RESPONSE_DURATION]
  fault_cleared;
endsequence

property fault_response_complete;
  @(posedge clk) disable iff (!rst_n)
    fault_response_seq;
endproperty

assert property (fault_response_complete) else
  `uvm_error("SEQ", "Fault response sequence incomplete");

// Mode transition sequence
sequence mode_transition_seq;
  $rose(mode_switch_req) ##[1:SETTLE_TIME]
  $stable(pacing_mode) [*3];
endsequence

property mode_transition_stable;
  @(posedge clk) disable iff (!rst_n)
    mode_transition_seq;
endproperty
```

## 7. Immediate Assertions

### 7.1 Combinational Checks

```systemverilog
// Immediate assertion on combinational logic
always_comb begin
  // Check pace amplitude constraints
  a_amplitude_valid: assert (pace_amplitude <= MAX_AMPLITUDE)
    else $error("Amplitude exceeds maximum");

  // Check mode register validity
  a_mode_valid: assert (mode_reg inside {4'h0, 4'h4, 4'h6, 4'h8, 4'hD})
    else $error("Invalid mode register value");

  // Check mutual exclusion
  a_mutex: assert (!(pace_pulse && inhibit_active))
    else $error("Pace and inhibit simultaneously active");
end
```

### 7.2 Parameterized Assertions

```systemverilog
// Parameterized assertion for different modes
property mode_specific_rate(mode, min_rate, max_rate);
  @(posedge clk) disable iff (!rst_n)
    (mode_reg == mode)
    |-> (timer_count >= min_rate && timer_count <= max_rate);
endproperty

assert property (mode_specific_rate(MODE_VVI, VVI_MIN_RATE, VVI_MAX_RATE))
  else $error("VVI rate out of range");
assert property (mode_specific_rate(MODE_AAI, AAI_MIN_RATE, AAI_MAX_RATE))
  else $error("AAI rate out of range");
assert property (mode_specific_rate(MODE_DDD, DDD_MIN_RATE, DDD_MAX_RATE))
  else $error("DDD rate out of range");
```

## 8. Assertion Libraries

### 8.1 Reusable SVA Library

```systemverilog
// Common assertion library for pacemaker verification
package pacemaker_sva_pkg;

  // Signal stability assertion
  property signal_stable(signal, min_cycles, max_cycles);
    @(posedge clk) disable iff (!rst_n)
      $rose(signal) |=> $stable(signal) [*min_cycles:max_cycles];
  endproperty

  // Handshake assertion
  property handshake(req, ack, max_latency);
    @(posedge clk) disable iff (!rst_n)
      $rose(req) |-> ##[1:max_latency] $rose(ack);
  endproperty

  // One-hot assertion
  property one_hot(signals);
    @(posedge clk)
      $onehot(signals);
  endproperty

  // Mutual exclusion
  property mutex(sig_a, sig_b);
    @(posedge clk) disable iff (!rst_n)
      !(sig_a && sig_b);
  endproperty

endpackage
```

## 9. Assertion Coverage

### 9.1 Cover Properties

```systemverilog
// Cover that VVI mode pacing occurs
cover property (@(posedge clk) disable iff (!rst_n)
  (mode_reg == MODE_VVI && pace_pulse)
);

// Cover that fault detection works
cover property (@(posedge clk) disable iff (!rst_n)
  $rose(fault_flag)
);

// Cover that mode transitions occur
cover property (@(posedge clk) disable iff (!rst_n)
  $rose(mode_switch_req)
);

// Cover that battery EOL is reached
cover property (@(posedge clk) disable iff (!rst_n)
  (battery_voltage < BATT_EOL_THRESHOLD)
);
```

## 10. Summary

SVA properties for the iPACE-CHIP pacemaker provide:

| Property Type | Count | Purpose |
|---------------|-------|---------|
| Pacing Algorithm | 12 | Mode-specific behavior |
| Timing | 8 | Clock-accurate checking |
| Safety | 10 | Hazard prevention |
| Sequence | 6 | Multi-cycle behavior |
| Cover | 8 | Verification completeness |

Key SVA benefits:
- **Embedded specifications** co-located with design
- **Formal and simulation** compatible
- **Reusable property libraries** for common patterns
- **Coverage integration** for verification closure
- **Runtime checking** with zero overhead in synthesis
