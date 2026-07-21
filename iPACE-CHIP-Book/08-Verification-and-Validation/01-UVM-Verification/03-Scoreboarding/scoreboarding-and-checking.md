# Scoreboarding and Checking for iPACE-CHIP Pacemaker

## 1. Introduction

Scoreboards are the primary mechanism for automated result checking in UVM-based verification environments. For the iPACE-CHIP pacemaker, the scoreboard compares DUT outputs against a reference model to detect functional errors in pacing algorithms, timing circuits, safety monitors, and telemetry reporting.

This chapter covers scoreboarding architecture, reference model implementation, temporal checking, and multi-channel comparison strategies.

## 2. Scoreboard Architecture

### 2.1 Top-Level Scoreboard

```
pacemaker_scoreboard
├── pacing_output_checker      (pace_pulse timing/amplitude)
├── timing_checker             (rate calculation accuracy)
├── mode_transition_checker    (mode switch correctness)
├── safety_monitor_checker     (fault detection response)
├── telemetry_checker          (UART data integrity)
├── battery_monitor_checker    (EOL detection thresholds)
├── configuration_checker      (register map validation)
└── reference_model            (golden behavior model)
```

### 2.2 Base Scoreboard

```systemverilog
class pacemaker_scoreboard extends uvm_scoreboard;
  `uvm_component_utils(pacemaker_scoreboard)

  uvm_analysis_imp_decl(_dut)
  uvm_analysis_imp_decl(_ref)

  uvm_analysis_imp_dut #(pacemaker_seq_item, pacemaker_scoreboard) dut_imp;
  uvm_analysis_imp_ref  #(pacemaker_seq_item, pacemaker_scoreboard) ref_imp;

  // Expected vs Actual queues
  pacemaker_seq_item ref_queue[$];
  pacemaker_seq_item dut_queue[$];

  // Error tracking
  int total_checks = 0;
  int passed_checks = 0;
  int failed_checks = 0;
  int miscompares = 0;

  // Sub-checkers
  pacing_output_checker     pace_checker;
  timing_accuracy_checker   timing_checker;
  mode_transition_checker   mode_checker;
  safety_response_checker   safety_checker;

  function new(string name = "pacemaker_scoreboard", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    dut_imp = new("dut_imp", this);
    ref_imp = new("ref_imp", this);

    pace_checker  = pacing_output_checker::type_id::create("pace_checker", this);
    timing_checker = timing_accuracy_checker::type_id::create("timing_checker", this);
    mode_checker  = mode_transition_checker::type_id::create("mode_checker", this);
    safety_checker = safety_response_checker::type_id::create("safety_checker", this);
  endfunction

  virtual function void write_dut(pacemaker_seq_item item);
    dut_queue.push_back(item);
    compare_items();
  endfunction

  virtual function void write_ref(pacemaker_seq_item item);
    ref_queue.push_back(item);
    compare_items();
  endfunction

  virtual function void compare_items();
    pacemaker_seq_item ref_item, dut_item;

    if (ref_queue.size() > 0 && dut_queue.size() > 0) begin
      ref_item = ref_queue.pop_front();
      dut_item = dut_queue.pop_front();
      total_checks++;

      if (ref_item.compare(dut_item)) begin
        passed_checks++;
      end else begin
        failed_checks++;
        miscompares++;
        `uvm_error("SCB_MISCOMPARE",
          $sformatf("Mismatch at time %0t:\n  REF: %s\n  DUT: %s",
            $time, ref_item.convert2string(), dut_item.convert2string()))
      end
    end
  endfunction

  virtual function void check_phase(uvm_phase phase);
    super.check_phase(phase);
    if (ref_queue.size() != 0)
      `uvm_warning("SCB_QFULL", $sformatf(
        "REF queue has %0d unprocessed items", ref_queue.size()))
    if (dut_queue.size() != 0)
      `uvm_warning("SCB_QFULL", $sformatf(
        "DUT queue has %0d unprocessed items", dut_queue.size()))
  endfunction

  virtual function void report_phase(uvm_phase phase);
    super.report_phase(phase);
    `uvm_info("SCB_REPORT", $sformatf(
      "\n===== SCOREBOARD REPORT =====\nTotal Checks: %0d\nPassed: %0d\nFailed: %0d\nMiscompares: %0d\n=============================",
      total_checks, passed_checks, failed_checks, miscompares), UVM_LOW)
  endfunction
endclass
```

## 3. Reference Model

### 3.1 Pacing Algorithm Reference Model

```systemverilog
class pacemaker_ref_model extends uvm_component;
  `uvm_component_utils(pacemaker_ref_model)

  uvm_analysis_export #(pacemaker_seq_item) analysis_export;

  // Pacing state machine
  typedef enum {
    REF_IDLE,
    REF_SENSE,
    REF_PACE,
    REF_INHIBIT,
    REF_REFRACTORY,
    REF_ALERT
  } ref_state_e;

  ref_state_e current_state = REF_IDLE;

  // Configuration registers (mirror of DUT)
  bit [3:0]  pacing_mode = 4'b0110;  // VVI
  bit [7:0]  lower_rate_limit = 8'd60;
  bit [7:0]  upper_rate_limit = 8'd120;
  bit [7:0]  pulse_amplitude = 8'd50;
  bit [7:0]  pulse_width_cfg = 8'd5;
  bit [7:0]  refractory_period = 8'd30;

  // Timing state
  int        last_event_time = 0;
  int        escape_interval = 0;
  bit        ventricular_sensed = 0;
  bit        atrial_sensed = 0;

  // Output queue for checker
  uvm_analysis_port #(pacemaker_seq_item) ref_output_port;

  function new(string name = "pacemaker_ref_model", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    analysis_export = new("analysis_export", this);
    ref_output_port = new("ref_output_port", this);
  endfunction

  virtual function void write(pacemaker_seq_item item);
    pacemaker_seq_item expected;

    case (item.item_type)
      SENSE_EVENT: begin
        process_sense(item);
      end
      PACE_EVENT: begin
        process_pace(item);
      end
      INHIBIT_EVENT: begin
        process_inhibit(item);
      end
      BATTERY_ALERT: begin
        process_battery_alert(item);
      end
      LEAD_IMPEDANCE_ALERT: begin
        process_lead_fault(item);
      end
      MODE_SWITCH: begin
        process_mode_switch(item);
      end
    endcase

    // Generate expected output
    expected = generate_expected_output(item);
    ref_output_port.write(expected);
  endfunction

  virtual function void process_sense(pacemaker_seq_item item);
    int current_time;

    current_time = $time;
    case (pacing_mode)
      4'b0110: begin // VVI
        if (current_time - last_event_time > escape_interval) begin
          // No beat sensed within escape interval - should pace
          ventricular_sensed = 0;
        end else begin
          // Beat sensed - inhibit pacing, update timer
          ventricular_sensed = 1;
          last_event_time = current_time;
        end
      end
      4'b1000: begin // AAI
        if (current_time - last_event_time > escape_interval) begin
          atrial_sensed = 0;
        end else begin
          atrial_sensed = 1;
          last_event_time = current_time;
        end
      end
      default: begin
        `uvm_warning("REFMOD", $sformatf(
          "Mode 0x%h not fully modeled", pacing_mode))
      end
    endcase
  endfunction

  virtual function void process_mode_switch(pacemaker_seq_item item);
    bit [3:0] new_mode;
    new_mode = item.duration[3:0];

    `uvm_info("REFMOD", $sformatf(
      "Mode switch: 0x%h -> 0x%h", pacing_mode, new_mode), UVM_MEDIUM)

    pacing_mode = new_mode;
    last_event_time = 0;
    escape_interval = calculate_escape_interval();
    ventricular_sensed = 0;
    atrial_sensed = 0;
  endfunction

  virtual function int calculate_escape_interval();
    int interval_ms;
    interval_ms = 60000 / lower_rate_limit;
    return interval_ms * 10; // Convert to clock cycles (100MHz)
  endfunction

  virtual function void process_battery_alert(pacemaker_seq_item item);
    if (item.duration < 30) begin // Below EOL threshold
      current_state = REF_ALERT;
      `uvm_info("REFMOD", "Battery EOL alert active", UVM_MEDIUM)
    end
  endfunction

  virtual function void process_lead_fault(pacemaker_seq_item item);
    current_state = REF_ALERT;
    `uvm_info("REFMOD", $sformatf(
      "Lead fault detected: Z=%0d ohms", item.duration), UVM_MEDIUM)
  endfunction

  virtual function pacemaker_seq_item generate_expected_output(
    pacemaker_seq_item input_item
  );
    pacemaker_seq_item expected;

    expected = pacemaker_seq_item::type_id::create("expected");
    expected.signal_type = input_item.signal_type;

    case (current_state)
      REF_IDLE: begin
        if (input_item.signal_type == SENSE_EVENT && !ventricular_sensed)
          expected.pace_output = 1;
        else
          expected.pace_output = 0;
      end
      REF_SENSE: begin
        expected.pace_output = 0;
      end
      REF_PACE: begin
        expected.pace_output = 1;
        expected.amplitude = pulse_amplitude;
        expected.pulse_width_out = pulse_width_cfg;
      end
      REF_ALERT: begin
        expected.pace_output = 0;
        expected.alert_active = 1;
      end
      default: expected.pace_output = 0;
    endcase

    return expected;
  endfunction
endclass
```

## 4. Specialized Checkers

### 4.1 Pacing Output Checker

```systemverilog
class pacing_output_checker extends uvm_scoreboard;
  `uvm_component_utils(pacing_output_checker)

  typedef struct {
    time    pulse_start;
    time    pulse_end;
    bit [7:0] amplitude;
    int     pulse_width_cycles;
  } pacing_record_t;

  pacing_record_t actual_records[$];
  pacing_record_t expected_records[$];

  // Tolerance for timing checks
  int tolerance_cycles = 5;

  function new(string name = "pacing_output_checker", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual function void check_pacing_output(
    time pulse_start, time pulse_end,
    bit [7:0] amplitude, int width_cycles
  );
    pacing_record_t actual;
    pacing_record_t expected;

    actual.pulse_start = pulse_start;
    actual.pulse_end = pulse_end;
    actual.amplitude = amplitude;
    actual.pulse_width_cycles = width_cycles;
    actual_records.push_back(actual);

    if (expected_records.size() > 0) begin
      expected = expected_records.pop_front();
      verify_pacing_record(actual, expected);
    end
  endfunction

  virtual function void verify_pacing_record(
    pacing_record_t actual, pacing_record_t expected
  );
    if (actual.amplitude != expected.amplitude)
      `uvm_error("PACE_CHK", $sformatf(
        "Amplitude mismatch: actual=%0d expected=%0d",
        actual.amplitude, expected.amplitude))

    if (actual.pulse_width_cycles != expected.pulse_width_cycles) begin
      if (abs(actual.pulse_width_cycles - expected.pulse_width_cycles) > tolerance_cycles)
        `uvm_error("PACE_CHK", $sformatf(
          "Pulse width mismatch: actual=%0d expected=%0d (tol=%0d)",
          actual.pulse_width_cycles, expected.pulse_width_cycles, tolerance_cycles))
      else
        `uvm_warning("PACE_CHK", $sformatf(
          "Pulse width marginal: actual=%0d expected=%0d",
          actual.pulse_width_cycles, expected.pulse_width_cycles))
    end
  endfunction

  virtual function int abs(int val);
    return (val < 0) ? -val : val;
  endfunction
endclass
```

### 4.2 Timing Accuracy Checker

```systemverilog
class timing_accuracy_checker extends uvm_scoreboard;
  `uvm_component_utils(timing_accuracy_checker)

  typedef struct {
    time    inter_event_interval;
    int     expected_rate_bpm;
    int     measured_rate_bpm;
    bit     within_tolerance;
  } timing_record_t;

  timing_record_t records[$];

  int bpm_tolerance = 2; // ±2 BPM tolerance
  time last_event_timestamp = 0;

  function new(string name = "timing_accuracy_checker", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual function void check_timing(time current_timestamp, int expected_bpm);
    timing_record_t rec;
    real interval_ms;
    int  measured_bpm;

    if (last_event_timestamp > 0) begin
      interval_ms = real'(current_timestamp - last_event_timestamp) / 1_000_000.0;
      if (interval_ms > 0)
        measured_bpm = int'(60000.0 / interval_ms);
      else
        measured_bpm = 0;

      rec.inter_event_interval = current_timestamp - last_event_timestamp;
      rec.expected_rate_bpm = expected_bpm;
      rec.measured_rate_bpm = measured_bpm;
      rec.within_tolerance = (abs(measured_bpm - expected_bpm) <= bpm_tolerance);
      records.push_back(rec);

      if (!rec.within_tolerance)
        `uvm_error("TIMING_CHK", $sformatf(
          "Rate accuracy fail: expected=%0d BPM, measured=%0d BPM (interval=%.2fms)",
          expected_bpm, measured_bpm, interval_ms))
    end
    last_event_timestamp = current_timestamp;
  endfunction

  virtual function int abs(int val);
    return (val < 0) ? -val : val;
  endfunction

  virtual function void report_phase(uvm_phase phase);
    int total, within_tol;
    super.report_phase(phase);
    total = records.size();
    foreach (records[i])
      if (records[i].within_tolerance) within_tol++;
    `uvm_info("TIMING_REPORT", $sformatf(
      "Timing checks: %0d/%0d within tolerance", within_tol, total), UVM_LOW)
  endfunction
endclass
```

### 4.3 Mode Transition Checker

```systemverilog
class mode_transition_checker extends uvm_scoreboard;
  `uvm_component_utils(mode_transition_checker)

  typedef struct {
    bit [3:0] from_mode;
    bit [3:0] to_mode;
    time      transition_time;
    bit       valid_transition;
  } mode_transition_t;

  mode_transition_t transitions[$];

  // Valid mode transition map
  bit valid_transition_map[bit[7:0]];

  function new(string name = "mode_transition_checker", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    // Define valid transitions: {from_mode, to_mode} -> valid
    valid_transition_map[{4'h6, 4'h8}] = 1; // VVI -> AAI
    valid_transition_map[{4'h8, 4'h6}] = 1; // AAI -> VVI
    valid_transition_map[{4'h6, 4'hD}] = 1; // VVI -> DDD
    valid_transition_map[{4'hD, 4'h6}] = 1; // DDD -> VVI
    valid_transition_map[{4'h0, 4'h6}] = 1; // AOO -> VVI
    valid_transition_map[{4'h4, 4'h6}] = 1; // VOO -> VVI
  endfunction

  virtual function void check_transition(
    bit [3:0] from_mode, bit [3:0] to_mode, time trans_time
  );
    mode_transition_t rec;
    bit [7:0] key;

    rec.from_mode = from_mode;
    rec.to_mode = to_mode;
    rec.transition_time = trans_time;

    key = {from_mode, to_mode};
    rec.valid_transition = valid_transition_map.exists(key);

    transitions.push_back(rec);

    if (!rec.valid_transition)
      `uvm_error("MODE_CHK", $sformatf(
        "Invalid mode transition: 0x%h -> 0x%h at time %0t",
        from_mode, to_mode, trans_time))
    else
      `uvm_info("MODE_CHK", $sformatf(
        "Valid mode transition: 0x%h -> 0x%h", from_mode, to_mode), UVM_HIGH)
  endfunction
endclass
```

### 4.4 Safety Response Checker

```systemverilog
class safety_response_checker extends uvm_scoreboard;
  `uvm_component_utils(safety_response_checker)

  typedef struct {
    string     fault_type;
    time       fault_time;
    time       response_time;
    bit        response_received;
    bit        within_latency;
  } safety_record_t;

  safety_record_t records[$];

  int max_response_latency_us = 100; // 100μs max response

  function new(string name = "safety_response_checker", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual function void check_safety_response(
    string fault_type, time fault_time, time response_time
  );
    safety_record_t rec;
    int latency_us;

    rec.fault_type = fault_type;
    rec.fault_time = fault_time;
    rec.response_time = response_time;
    rec.response_received = (response_time > 0);
    latency_us = int'((response_time - fault_time) / 1000);
    rec.within_latency = (latency_us <= max_response_latency_us);

    records.push_back(rec);

    if (!rec.response_received)
      `uvm_error("SAFETY_CHK", $sformatf(
        "No safety response for fault '%s' at time %0t", fault_type, fault_time))
    else if (!rec.within_latency)
      `uvm_error("SAFETY_CHK", $sformatf(
        "Safety response too slow for '%s': %0dμs (max=%0dμs)",
        fault_type, latency_us, max_response_latency_us))
  endfunction
endclass
```

## 5. Multi-Channel Scoreboard

### 5.1 Channel-Based Architecture

```systemverilog
class multi_channel_scoreboard extends uvm_scoreboard;
  `uvm_component_utils(multi_channel_scoreboard)

  // Channel definitions
  typedef enum {
    CH_PACING_OUTPUT,
    CH_TIMER,
    CH_TELEMETRY,
    CH_REG_CONFIG,
    CH_SAFETY
  } channel_e;

  uvm_tlm_fifo #(pacemaker_seq_item) ref_fifos[channel_e];
  uvm_tlm_fifo #(pacemaker_seq_item) dut_fifos[channel_e];

  function new(string name = "multi_channel_scoreboard", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    foreach (ref_fifos[i]) begin
      ref_fifos[i] = new($sformatf("ref_fifo_%0d", i), this);
      dut_fifos[i] = new($sformatf("dut_fifo_%0d", i), this);
    end
  endfunction

  virtual task compare_channel(channel_e ch);
    pacemaker_seq_item ref_item, dut_item;
    forever begin
      ref_fifos[ch].get(ref_item);
      dut_fifos[ch].get(dut_item);
      if (!ref_item.compare(dut_item))
        `uvm_error("MC_SCB", $sformatf(
          "Channel %0d miscompare at time %0t", ch, $time))
    end
  endtask

  virtual task run_phase(uvm_phase phase);
    fork
      compare_channel(CH_PACING_OUTPUT);
      compare_channel(CH_TIMER);
      compare_channel(CH_TELEMETRY);
      compare_channel(CH_REG_CONFIG);
      compare_channel(CH_SAFETY);
    join
  endtask
endclass
```

## 6. FIFO-Based Scoreboarding

### 6.1 Ordered Comparison

```systemverilog
class fifo_scoreboard extends uvm_scoreboard;
  `uvm_component_utils(fifo_scoreboard)

  uvm_tlm_fifo #(pacemaker_seq_item) expected_fifo;
  uvm_tlm_fifo #(pacemaker_seq_item) actual_fifo;

  int depth = 256;

  function new(string name = "fifo_scoreboard", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    expected_fifo = new("expected_fifo", this, depth);
    actual_fifo = new("actual_fifo", this, depth);
  endfunction

  virtual task run_phase(uvm_phase phase);
    pacemaker_seq_item exp_item, act_item;
    forever begin
      expected_fifo.get(exp_item);
      actual_fifo.get(act_item);
      if (!exp_item.compare(act_item)) begin
        `uvm_error("FIFO_SCB", $sformatf(
          "Mismatch:\n  Expected: %s\n  Actual:   %s",
          exp_item.convert2string(), act_item.convert2string()))
      end
    end
  endtask
endclass
```

## 7. Alert and Self-Check Mechanisms

### 7.1 Watchdog Timer Checker

```systemverilog
class watchdog_checker extends uvm_scoreboard;
  `uvm_component_utils(watchdog_checker)

  int timeout_cycles = 100_000; // 1ms at 100MHz
  time last_pace_time = 0;
  bit  pace_active = 0;

  function new(string name = "watchdog_checker", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual function void record_pace(time t);
    last_pace_time = t;
    pace_active = 1;
  endfunction

  virtual task run_phase(uvm_phase phase);
    forever begin
      @(posedge uvm_top.rst_n);
      if (pace_active && ($time - last_pace_time) > timeout_cycles * 10) begin
        `uvm_error("WDG_CHK", $sformatf(
          "Pacing timeout: no pace pulse in %0d cycles", timeout_cycles))
      end
    end
  endtask
endclass
```

## 8. Scoreboard Configuration

### 8.1 Configurable Tolerances

```systemverilog
class scoreboard_config extends uvm_object;
  `uvm_object_utils(scoreboard_config)

  int  timing_tolerance_bpm = 2;
  int  amplitude_tolerance_mv = 50;
  int  pulse_width_tolerance_us = 10;
  int  max_safety_response_us = 100;
  int  fifo_depth = 256;
  bit  enable_verbose_logging = 0;

  function new(string name = "scoreboard_config");
    super.new(name);
  endfunction
endclass
```

## 9. Reporting and Diagnostics

### 9.1 Comprehensive Report

```systemverilog
virtual function void report_phase(uvm_phase phase);
  super.report_phase(phase);
  `uvm_info("SCB_FINAL", $sformatf({
    "\n========================================",
    "\n   PACEMAKER SCOREBOARD FINAL REPORT",
    "\n========================================",
    "\n Total Checks:     %0d",
    "\n Passed:           %0d",
    "\n Failed:           %0d",
    "\n Miscompares:      %0d",
    "\n Timing Accuracy:  %s",
    "\n Safety Checks:    %s",
    "\n Mode Transitions: %0d valid, %0d invalid",
    "\n========================================"
  }, total_checks, passed_checks, failed_checks, miscompares,
     timing_checker.get_accuracy_string(),
     safety_checker.get_status_string(),
     mode_checker.get_valid_count(),
     mode_checker.get_invalid_count()), UVM_LOW)
endfunction
```

## 10. Summary

Scoreboarding for the iPACE-CHIP pacemaker provides:

| Checker | Function | Method |
|---------|----------|--------|
| Pacing Output | Pulse amplitude/width verification | TLM FIFO |
| Timing Accuracy | Inter-beat interval validation | Timestamp comparison |
| Mode Transition | State machine correctness | Transition map |
| Safety Response | Fault detection latency | Deadline checking |
| Battery Monitor | EOL threshold tracking | Threshold comparison |
| Telemetry | UART data integrity | FIFO ordering |

Key verification goals achieved:
- Automated pass/fail determination for every test
- Configurable tolerances for timing and amplitude
- Real-time miscompare reporting with full context
- Comprehensive final statistics for coverage closure
- Self-checking mechanisms for safety-critical responses
