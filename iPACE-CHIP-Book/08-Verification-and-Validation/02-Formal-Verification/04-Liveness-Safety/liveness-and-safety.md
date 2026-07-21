# Liveness and Safety Properties for iPACE-CHIP Pacemaker

## 1. Introduction

Safety and liveness are the two fundamental categories of properties in formal verification. Safety properties assert that "something bad never happens," while liveness properties assert that "something good eventually happens." For the iPACE-CHIP pacemaker, both property types are critical: safety properties prevent dangerous pacing conditions, and liveness properties ensure the pacemaker always responds to cardiac events.

## 2. Safety Properties

### 2.1 Definition and Classification

```
Safety Property: "Nothing bad ever happens"
  - If violated, the system enters a harmful state
  - Violation is observable in a finite prefix of execution
  - Examples for pacemaker:
    • Pace amplitude never exceeds safe maximum
    • No pacing during ventricular refractory period
    • Fault always detected within latency bound
    • Battery low always generates alert
```

### 2.2 Pace Amplitude Safety

```systemverilog
// Maximum amplitude boundary
property pace_amplitude_max;
  @(posedge clk) disable iff (!rst_n)
    pace_pulse |-> pace_amplitude <= 8'd80;  // 8.0V max
endproperty

assert property (pace_amplitude_max) else
  `uvm_error("SAFETY", $sformatf(
    "Pace amplitude %0d exceeds 80 (8.0V) at time %0t",
    pace_amplitude, $time));

// Minimum amplitude for effective capture
property pace_amplitude_min;
  @(posedge clk) disable iff (!rst_n)
    pace_pulse |-> pace_amplitude >= 8'd10;  // 1.0V min
endproperty

assert property (pace_amplitude_min) else
  `uvm_error("SAFETY", $sformatf(
    "Pace amplitude %0d below 10 (1.0V) at time %0t",
    pace_amplitude, $time));

// Amplitude never zero during active pulse
property pace_nonzero_during_pulse;
  @(posedge clk) disable iff (!rst_n)
    pace_pulse |-> pace_amplitude != 0;
endproperty

assert property (pace_nonzero_during_pulse) else
  `uvm_error("SAFETY", "Zero amplitude during active pace pulse");
```

### 2.3 Timing Safety

```systemverilog
// No double-pacing within refractory period
property no_double_pace;
  @(posedge clk) disable iff (!rst_n)
    $rose(pace_pulse) |-> !pace_pulse [*1:REFRACTORY_CYCLES];
endproperty

assert property (no_double_pace) else
  `uvm_error("SAFETY", "Double-pacing detected within refractory period");

// Pace pulse width within bounds
property pulse_width_bounded;
  @(posedge clk) disable iff (!rst_n)
    $rose(pace_pulse) |-> ##[MIN_PULSE_WIDTH:MAX_PULSE_WIDTH] $fell(pace_pulse);
endproperty

assert property (pulse_width_bounded) else
  `uvm_error("SAFETY", $sformatf(
    "Pulse width out of bounds [%0d:%0d] cycles",
    MIN_PULSE_WIDTH, MAX_PULSE_WIDTH));

// Maximum heart rate never exceeded
property max_rate_safe;
  @(posedge clk) disable iff (!rst_n)
    $rose(pace_pulse) |-> !pace_pulse [*1:MIN_INTER_PACE_CYCLES-1];
endproperty

assert property (max_rate_safe) else
  `uvm_error("SAFETY", "Maximum heart rate exceeded");

// Minimum inter-pace interval enforced
property min_interval_safe;
  @(posedge clk) disable iff (!rst_n)
    $fell(pace_pulse) |-> !pace_pulse [*1:MIN_INTER_PACE_CYCLES-1];
endproperty

assert property (min_interval_safe) else
  `uvm_error("SAFETY", "Minimum inter-pace interval violated");
```

### 2.4 Fault Detection Safety

```systemverilog
// Lead impedance fault always detected
property lead_fault_detected;
  @(posedge clk) disable iff (!rst_n)
    (lead_impedance > LEAD_Z_OPEN_THRESHOLD) |->
      ##[0:DETECTION_LATENCY] fault_flag;
endproperty

assert property (lead_fault_detected) else
  `uvm_error("SAFETY", "Lead impedance fault not detected");

// Short circuit detection
property short_circuit_detected;
  @(posedge clk) disable iff (!rst_n)
    (lead_impedance < LEAD_Z_SHORT_THRESHOLD) |->
      ##[0:DETECTION_LATENCY] fault_flag;
endproperty

assert property (short_circuit_detected) else
  `uvm_error("SAFETY", "Short circuit not detected");

// Battery EOL always flagged
property battery_eol_detected;
  @(posedge clk) disable iff (!rst_n)
    (battery_voltage < BATT_EOL_THRESHOLD) |->
      ##[0:DETECTION_LATENCY] battery_alert;
endproperty

assert property (battery_eol_detected) else
  `uvm_error("SAFETY", "Battery EOL not detected");
```

## 3. Liveness Properties

### 3.1 Definition and Classification

```
Liveness Property: "Something good eventually happens"
  - System makes progress toward a desired state
  - Violation may require infinite execution to observe
  - Cannot be checked by finite BMC alone
  - Examples for pacemaker:
    • Pace pulse generated when no intrinsic beat
    • Inhibit signal eventually clears
    • Timer eventually expires
    • System returns to idle state
```

### 3.2 Pacing Liveness

```systemverilog
// Pace pulse generated when needed
property pace_eventually_generated;
  @(posedge clk) disable iff (!rst_n)
    (no_intrinsic_beat && mode_active && !inhibit && !in_refractory)
    |-> s_eventually pace_pulse;
endproperty

assert property (pace_eventually_generated) else
  `uvm_error("LIVENESS", "Pace pulse not generated when needed");

// Escape interval eventually triggers pace
property escape_interval_pace;
  @(posedge clk) disable iff (!rst_n)
    (state == SENSE_MONITOR && timer_running)
    |-> s_eventually (timer_expired && pace_pulse);
endproperty

assert property (escape_interval_pace) else
  `uvm_error("LIVENESS", "Escape interval did not trigger pace");

// Inhibit eventually clears
property inhibit_clears;
  @(posedge clk) disable iff (!rst_n)
    $rose(inhibit) |-> s_eventually !inhibit;
endproperty

assert property (inhibit_clears) else
  `uvm_error("LIVENESS", "Inhibit stuck active indefinitely");
```

### 3.3 Timer Liveness

```systemverilog
// Timer eventually expires
property timer_eventually_expires;
  @(posedge clk) disable iff (!rst_n)
    $rose(timer_running) |-> s_eventually timer_expired;
endproperty

assert property (timer_eventually_expires) else
  `uvm_error("LIVENESS", "Timer never expires");

// Timer eventually clears after expiration
property timer_clears_after_exp;
  @(posedge clk) disable iff (!rst_n)
    $rose(timer_expired) |-> s_eventually !timer_running;
endproperty

assert property (timer_clears_after_exp) else
  `uvm_error("LIVENESS", "Timer stuck in expired state");
```

### 3.4 System Liveness

```systemverilog
// System always returns to idle
property system_eventually_idle;
  @(posedge clk) disable iff (!rst_n)
    (state != IDLE) |-> s_eventually (state == IDLE);
endproperty

assert property (system_eventually_idle) else
  `uvm_error("LIVENESS", "System stuck in non-idle state");

// Telemetry eventually transmitted
property telemetry_sent;
  @(posedge clk) disable iff (!rst_n)
    $rose(telemetry_pending) |-> s_eventually telemetry_complete;
endproperty

assert property (telemetry_sent) else
  `uvm_error("LIVENESS", "Telemetry never sent");

// Fault response eventually taken
property fault_responded;
  @(posedge clk) disable iff (!rst_n)
    $rose(fault_flag) |-> s_eventually fault_response_taken;
endproperty

assert property (fault_responded) else
  `uvm_error("LIVENESS", "Fault response never taken");
```

## 4. Relationship Between Safety and Liveness

### 4.1 Property Decomposition

```
Total Correctness = Safety ∧ Liveness

For pacemaker:
  "Pace correctly" = "Never pace dangerously" ∧ "Always pace when needed"

Decomposition:
  Safety: pace_amplitude ≤ MAX_AMP
  Safety: pace_width ≤ MAX_WIDTH
  Safety: no_pace_during_refractory
  Liveness: pace_generated_when_needed
  Liveness: system_progresses_to_idle
```

### 4.2 Complementary Properties

```systemverilog
// Safety-Liveness pair: pacing
// Safety: When pacing, amplitude is safe
property pace_safety;
  @(posedge clk) disable iff (!rst_n)
    pace_pulse |-> pace_amplitude inside {[MIN_AMP:MAX_AMP]};
endproperty

// Liveness: When pacing is needed, it happens
property pace_liveness;
  @(posedge clk) disable iff (!rst_n)
    (need_pace && !inhibit) |-> s_eventually pace_pulse;
endproperty

// Together they guarantee correct pacing behavior

// Safety-Liveness pair: fault handling
// Safety: Faults are detected
property fault_safety;
  @(posedge clk) disable iff (!rst_n)
    (lead_impedance < LEAD_Z_MIN || lead_impedance > LEAD_Z_MAX)
    |-> ##[0:5] fault_flag;
endproperty

// Liveness: Faults are responded to
property fault_liveness;
  @(posedge clk) disable iff (!rst_n)
    $rose(fault_flag) |-> s_eventually fault_resolved;
endproperty
```

## 5. Fairness and Guarantee Properties

### 5.1 Fairness Assumptions

```systemverilog
// Weak fairness: If condition continuously enabled, it eventually happens
// Example: If timer is running, it eventually gets a clock tick
property weak_fairness_timer;
  @(posedge clk) disable iff (!rst_n)
    always (timer_running && clk_en) |-> s_eventually timer_tick;
endproperty

// Strong fairness: If condition infinitely often enabled, it eventually happens
// Example: If sense signal infinitely often available, it's eventually sampled
property strong_fairness_sense;
  @(posedge clk) disable iff (!rst_n)
    always (sense_available) |-> s_eventually sense_sampled;
endproperty
```

### 5.2 Guarantee Properties

```systemverilog
// Response guarantee: Every request gets a response
property response_guarantee;
  @(posedge clk) disable iff (!rst_n)
    $rose(pacing_request) |-> s_eventually [1:MAX_RESPONSE_TIME]
      $rose(pace_pulse) || $rose(inhibit);
endproperty

// Completion guarantee: Every operation completes
property completion_guarantee;
  @(posedge clk) disable iff (!rst_n)
    $rose(start_pacing_cycle) |-> s_eventually [1:MAX_CYCLE_TIME]
      (state == IDLE);
endproperty

// Progress guarantee: System makes forward progress
property progress_guarantee;
  @(posedge clk) disable iff (!rst_n)
    (state == SENSE_MONITOR) |-> s_eventually [1:MAX_SENSE_TIME]
      (state == PACE_GEN || state == INHIBIT || state == IDLE);
endproperty
```

## 6. Safety Property Patterns

### 6.1 State Invariants

```systemverilog
// Property: Always in a valid state
property valid_state;
  @(posedge clk) disable iff (!rst_n)
    state inside {IDLE, SENSE_MON, PACE_GEN, REFRACT, INHIBIT_ST};
endproperty

// Property: Only one active output at a time
property single_active_output;
  @(posedge clk) disable iff (!rst_n)
    !(pace_pulse && inhibit_active);
endproperty

// Property: Timer count bounded
property timer_bounded;
  @(posedge clk) disable iff (!rst_n)
    timer_cnt <= MAX_TIMER_VALUE;
endproperty
```

### 6.2 Transition Safety

```systemverilog
// Property: Legal state transitions only
property legal_transitions;
  @(posedge clk) disable iff (!rst_n)
    case (state)
      IDLE: next_state inside {SENSE_MON, PACE_GEN, INHIBIT_ST};
      SENSE_MON: next_state inside {PACE_GEN, INHIBIT_ST, IDLE};
      PACE_GEN: next_state == REFRACT;
      REFRACT: next_state inside {IDLE, REFRACT};
      INHIBIT_ST: next_state == IDLE;
      default: next_state == IDLE;
    endcase
endproperty

// Property: No unauthorized mode changes
property mode_stable_during_operation;
  @(posedge clk) disable iff (!rst_n)
    (state != IDLE) |-> $stable(pacing_mode);
endproperty
```

## 7. Liveness Property Patterns

### 7.1 Response Patterns

```systemverilog
// Request-response pattern
property request_response;
  @(posedge clk) disable iff (!rst_n)
    $rose(request) |-> s_eventually response;
endproperty

// Stimulus-response pattern (for cardiac events)
property cardiac_response;
  @(posedge clk) disable iff (!rst_n)
    $fell(sense_amp_out) |-> s_eventually [1:MAX_RESPONSE_TIME]
      (pace_pulse || inhibit_active);
endproperty

// Periodic pattern (for watchdog)
property periodic_check;
  @(posedge clk) disable iff (!rst_n)
    1 |-> s_eventually [*0:MAX_CHECK_INTERVAL]
      battery_check_performed;
endproperty
```

### 7.2 Progress Patterns

```systemverilog
// Loop progress: Each iteration makes progress
property loop_progress;
  @(posedge clk) disable iff (!rst_n)
    (state == SENSE_MONITOR && !timer_expired)
    |-> s_eventually (timer_expired || state != SENSE_MONITOR);
endproperty

// Down-counter progress
property counter_progress;
  @(posedge clk) disable iff (!rst_n)
    (refractory_cnt > 0 && state == REFRACT)
    |-> s_eventually refractory_cnt == 0;
endproperty

// Escalation progress (for fault handling)
property escalation_progress;
  @(posedge clk) disable iff (!rst_n)
    (fault_severity > 0)
    |-> s_eventually (fault_response_taken || fault_cleared);
endproperty
```

## 8. Verification Strategy

### 8.1 Property Priority

```
Priority  Property Type        Method
─────────────────────────────────────────────
1 (Critical) Safety            Formal proof + BMC
2 (High)     Liveness          Model checking
3 (Medium)   Timing            BMC + Simulation
4 (Standard) Protocol          Assertion-based
5 (Low)      Coverage          Simulation
```

### 8.2 Verification Coverage Matrix

| Property Category | Formal | BMC | Simulation | Total |
|-------------------|--------|-----|------------|-------|
| Safety (amplitude) | 5 | 3 | 2 | 10 |
| Safety (timing) | 4 | 4 | 3 | 11 |
| Safety (fault) | 3 | 2 | 2 | 7 |
| Liveness (pacing) | 3 | 2 | 2 | 7 |
| Liveness (timer) | 2 | 2 | 1 | 5 |
| Liveness (system) | 2 | 1 | 1 | 4 |
| **Total** | **19** | **14** | **11** | **44** |

## 9. Debugging Safety and Liveness Violations

### 9.1 Safety Violation Debug

```
Safety violations provide finite counterexamples:
  1. Identify the violating cycle
  2. Trace input sequence leading to violation
  3. Examine state at violation point
  4. Determine if violation is design bug or property error
  5. Fix design or refine property

Example:
  Violation: pace_amplitude_max at cycle 47
  Input trace: mode_reg=0x6, amp_cfg=0x80
  State: PACE_GEN, timer_expired=1
  Root cause: amplitude_cfg not clamped
  Fix: Add amplitude clamping in RTL
```

### 9.2 Liveness Violation Debug

```
Liveness violations require lasso-shaped counterexamples:
  1. Finite prefix reaching a state
  2. Cycle (lasso) returning to that state
  3. Desired condition never occurs in the lasso

Example:
  Violation: system_eventually_idle
  Lasso: IDLE → SENSE_MON → IDLE → SENSE_MON → ... (infinite)
  Missing: PACE_GEN never reached
  Root cause: Timer never expires in SENSE_MON
  Fix: Correct timer logic
```

## 10. Summary

Safety and liveness properties for the iPACE-CHIP pacemaker:

| Category | Property Count | Verification Method |
|----------|---------------|---------------------|
| Safety (Critical) | 15 | Formal + BMC |
| Safety (Standard) | 12 | BMC + Simulation |
| Liveness (Critical) | 8 | Model checking |
| Liveness (Standard) | 6 | Simulation |

Key outcomes:
- **Safety properties** prevent all dangerous pacing conditions
- **Liveness properties** guarantee the pacemaker always responds correctly
- **Complementary verification** uses formal and simulation together
- **Counterexample analysis** enables rapid bug identification
- **Property patterns** provide reusable verificationIP
