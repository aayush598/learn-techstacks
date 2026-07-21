# Concurrent Assertions for iPACE-CHIP Pacemaker

## 1. Introduction

Concurrent assertions in SystemVerilog evaluate properties at every clock cycle, checking temporal relationships between signals. For the iPACE-CHIP pacemaker, concurrent assertions monitor ongoing DUT behavior, detecting timing violations, protocol errors, and safety hazards in real-time during simulation.

## 2. Concurrent Assertion Fundamentals

### 2.1 Basic Structure

```systemverilog
// Concurrent assertion: evaluated every clock cycle
property concurrent_pace_check;
  @(posedge clk) disable iff (!rst_n)
    pace_pulse |-> pace_amplitude > 0;
endproperty

assert property (concurrent_pace_check) else
  `uvm_error("CONCURRENT", "Zero amplitude during pace pulse");
```

### 2.2 Clocking and Disable

```systemverilog
// Edge-sensitive concurrent assertions
property rising_edge_check;
  @(posedge clk) disable iff (!rst_n)
    $rose(pace_pulse) |=> pace_amplitude == expected_amplitude;
endproperty

property falling_edge_check;
  @(posedge clk) disable iff (!rst_n)
    $fell(pace_pulse) |-> pace_amplitude == 0;
endproperty

// Multi-clock assertions (for跨时钟域)
property cdc_safe;
  @(posedge clk_fast) disable iff (!rst_n)
    $rose(slow_signal_sync)
    |=> $stable(slow_signal_sync) [*2];
endproperty
```

## 3. Pacing Concurrency Checks

### 3.1 Pulse Generation Concurrency

```systemverilog
// Property: Pace pulse width concurrent check
property pace_width_concurrent;
  @(posedge clk) disable iff (!rst_n)
    $rose(pace_pulse) |-> ##[1:MAX_PULSE_CYCLES] $fell(pace_pulse);
endproperty

assert property (pace_width_concurrent) else
  `uvm_error("PACE", "Pulse width exceeded");

// Property: Amplitude stable during pulse
property amplitude_stable_concurrent;
  @(posedge clk) disable iff (!rst_n)
    pace_pulse |-> $stable(pace_amplitude);
endproperty

assert property (amplitude_stable_concurrent) else
  `uvm_error("PACE", "Amplitude unstable during pulse");

// Property: No pulse during refractory
property no_pace_refractory_concurrent;
  @(posedge clk) disable iff (!rst_n)
    in_refractory |-> !pace_pulse;
endproperty

assert property (no_pace_refractory_concurrent) else
  `uvm_error("PACE", "Pace during refractory");
```

### 3.2 Sensing Concurrency

```systemverilog
// Property: Sense signal sampling
property sense_sampled_concurrent;
  @(posedge clk) disable iff (!rst_n)
    $fell(sense_amp_out) |-> sense_detected;
endproperty

assert property (sense_sampled_concurrent) else
  `uvm_error("SENSE", "Sense signal not sampled");

// Property: Inhibit after sense
property inhibit_after_sense_concurrent;
  @(posedge clk) disable iff (!rst_n)
    $fell(sense_amp_out) && mode_active |-> ##1 inhibit_active;
endproperty

assert property (inhibit_after_sense_concurrent) else
  `uvm_error("SENSE", "Inhibit not asserted after sense");
```

## 4. Timing Concurrency

### 4.1 Clock-Accurate Checks

```systemverilog
// Property: Inter-beat interval accuracy
property ibi_accuracy_concurrent;
  @(posedge clk) disable iff (!rst_n)
    $rose(pace_pulse) |->
      ##[MIN_IBI_CYCLES-5:MAX_IBI_CYCLES+5] $rose(pace_pulse);
endproperty

assert property (ibi_accuracy_concurrent) else
  `uvm_error("TIMING", "Inter-beat interval out of tolerance");

// Property: Timer countdown accuracy
property timer_accuracy_concurrent;
  @(posedge clk) disable iff (!rst_n)
    timer_running && timer_cnt > 0 |-> timer_cnt == $past(timer_cnt) - 1;
endproperty

assert property (timer_accuracy_concurrent) else
  `uvm_error("TIMING", "Timer countdown inaccurate");

// Property: Escape interval accuracy
property escape_accuracy_concurrent;
  @(posedge clk) disable iff (!rst_n)
    $fell(pace_pulse) |->
      ##[ESCAPE_MIN-5:ESCAPE_MAX+5] ($rose(pace_pulse) || inhibit_active);
endproperty

assert property (escape_accuracy_concurrent) else
  `uvm_error("TIMING", "Escape interval inaccurate");
```

### 4.2 Latency Checks

```systemverilog
// Property: Fault detection latency
property fault_latency_concurrent;
  @(posedge clk) disable iff (!rst_n)
    $rose(fault_condition) |-> ##[0:MAX_FAULT_LATENCY] fault_flag;
endproperty

assert property (fault_latency_concurrent) else
  `uvm_error("LATENCY", "Fault detection latency exceeded");

// Property: Mode switch latency
property mode_switch_latency_concurrent;
  @(posedge clk) disable iff (!rst_n)
    $rose(mode_switch_req) |-> ##[0:MAX_MODE_SWITCH_LATENCY]
      $stable(pacing_mode);
endproperty

assert property (mode_switch_latency_concurrent) else
  `uvm_error("LATENCY", "Mode switch latency exceeded");
```

## 5. Protocol Concurrency

### 5.1 APB Protocol Check

```systemverilog
// APB write protocol concurrent check
property apb_write_protocol;
  @(posedge clk) disable iff (!rst_n)
    $rose(psel) && pen && pwrite |-> ##[1:2] pready;
endproperty

assert property (apb_write_protocol) else
  `uvm_error("APB", "APB write protocol violation");

// APB read protocol concurrent check
property apb_read_protocol;
  @(posedge clk) disable iff (!rst_n)
    $rose(psel) && pen && !pwrite |-> ##[1:2] pready;
endproperty

assert property (apb_read_protocol) else
  `uvm_error("APB", "APB read protocol violation");

// APB idle protocol
property apb_idle_protocol;
  @(posedge clk) disable iff (!rst_n)
    !psel |-> !pen && !pready;
endproperty

assert property (apb_idle_protocol) else
  `uvm_error("APB", "APB idle protocol violation");
```

### 5.2 UART Protocol Check

```systemverilog
// UART start bit concurrent check
property uart_start_bit;
  @(posedge clk) disable iff (!rst_n)
    $fell(uart_tx) |=> !uart_tx [*BAUD_CYCLES-1:BAUD_CYCLES+1];
endproperty

assert property (uart_start_bit) else
  `uvm_error("UART", "UART start bit violation");

// UART data bit timing
property uart_data_timing;
  @(posedge clk) disable iff (!rst_n)
    uart_active |-> ##BAUD_CYCLES uart_active;
endproperty

assert property (uart_data_timing) else
  `uvm_error("UART", "UART data timing violation");
```

## 6. Multi-Clock Domain Assertions

### 6.1 Clock Domain Crossing

```systemverilog
// CDC safe assertion
property cdc_stable;
  @(posedge clk_domain_a) disable iff (!rst_n)
    $rose(signal_to_domain_b) |->
      ##[0:SYNC_STAGES] signal_to_domain_b_stable;
endproperty

assert property (cdc_stable) else
  `uvm_error("CDC", "CDC signal not stable");

// Gray code CDC check
property gray_code_cdc;
  @(posedge clk) disable iff (!rst_n)
    $changed(async_counter) |->
      $onehot(async_counter ^ $past(async_counter));
endproperty

assert property (gray_code_cdc) else
  `uvm_error("CDC", "Gray code CDC violation");
```

## 7. Temporal Assertions

### 7.1 Window Assertions

```systemverilog
// Property: Amplitude valid within timing window
property amplitude_window;
  @(posedge clk) disable iff (!rst_n)
    $rose(pace_pulse) |-> ##[1:5]
      pace_amplitude inside {[MIN_AMP:MAX_AMP]};
endproperty

assert property (amplitude_window) else
  `uvm_error("WINDOW", "Amplitude outside timing window");

// Property: Response within deadline
property response_deadline;
  @(posedge clk) disable iff (!rst_n)
    $rose(request) |-> ##[1:DEADLINE_CYCLES] $rose(response);
endproperty

assert property (response_deadline) else
  `uvm_error("WINDOW", "Response deadline exceeded");
```

### 7.2 Repetition Assertions

```systemverilog
// Property: No more than N pace pulses in M cycles
property rate_limit_concurrent;
  @(posedge clk) disable iff (!rst_n)
    $countones(pace_pulse [*1:RATE_WINDOW_CYCLES]) <= MAX_PACES_IN_WINDOW;
endproperty

assert property (rate_limit_concurrent) else
  `uvm_error("RATE", "Rate limit exceeded");

// Property: Consecutive identical outputs
property output_stability;
  @(posedge clk) disable iff (!rst_n)
    $stable(state) [*5] |-> $stable(pace_amplitude);
endproperty

assert property (output_stability) else
  `uvm_error("STABILITY", "Output unstable in stable state");
```

## 8. Assertion Debugging

### 8.1 Concurrent Assertion Debug

```systemverilog
// Detailed assertion with context
property pace_concurrent_debug;
  @(posedge clk) disable iff (!rst_n)
    $rose(pace_pulse) |-> ##[1:MAX_WIDTH] $fell(pace_pulse);
endproperty

assert property (pace_concurrent_debug) else begin
  `uvm_error("DEBUG", $sformatf({
    "\n=== CONCURRENT ASSERTION FAILURE ===",
    "\nTime:           %0t",
    "\nState:          %s",
    "\nMode:           0x%h",
    "\nPulse started:  %0t",
    "\nCurrent time:   %0t",
    "\nAmplitude:      %0d",
    "\nTimer count:    %0d",
    "\n===================================="
  }, $time, state.name(), mode_reg,
     $time, $time, pace_amplitude, timer_cnt))
end
```

### 8.2 Assertion Waveform Dump

```systemverilog
// Enable assertion waveform for debug
`ifdef ASSERT_DEBUG
  // Dump assertion waveforms
  $assertoff; // Disable all assertions
  // Run specific test
  // $asserton; // Re-enable
`endif
```

## 9. Assertion Performance

### 9.1 Concurrent Assertion Overhead

```
Assertion Type          Simulation Overhead
──────────────────────────────────────────────
Simple concurrent       < 1%
Complex temporal        2-5%
Multi-clock domain      5-10%
Count-based             3-7%
Window assertions       5-8%
```

### 9.2 Assertion Optimization

```systemverilog
// Optimized concurrent assertions
// Use local variables to reduce recomputation
property optimized_rate_check;
  @(posedge clk) disable iff (!rst_n)
    int last_pace_time;
    ($rose(pace_pulse), last_pace_time = $time)
    |-> ##[MIN_RATE:MAX_RATE]
      ($time - last_pace_time) inside {[MIN_RATE*10:MAX_RATE*10]};
endproperty
```

## 10. Summary

Concurrent assertions for the iPACE-CHIP pacemaker provide:

| Check Type | Count | Application |
|------------|-------|-------------|
| Pulse Generation | 6 | Pacing correctness |
| Sensing | 4 | Input monitoring |
| Timing | 6 | Clock accuracy |
| Protocol | 5 | Interface compliance |
| CDC | 3 | Cross-domain safety |
| Temporal | 4 | Deadline checking |

Key concurrent assertion benefits:
- **Real-time monitoring** during simulation
- **Clock-accurate checking** at every cycle
- **Multi-clock domain** support
- **Protocol compliance** verification
- **Debug-friendly** with detailed failure context
- **Performance-efficient** for large designs
