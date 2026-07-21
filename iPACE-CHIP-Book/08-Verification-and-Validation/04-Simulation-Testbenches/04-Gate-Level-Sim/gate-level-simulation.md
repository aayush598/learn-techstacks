# Gate-Level Simulation for iPACE-CHIP Pacemaker

## 1. Introduction

Gate-level simulation (GLS) verifies the synthesized netlist of the iPACE-CHIP pacemaker, ensuring that synthesis, place-and-route, and timing optimization have not introduced functional errors. GLS uses the gate-level netlist with timing annotations from the .sdf file to verify correct operation at the actual implementation level.

## 2. Gate-Level Simulation Flow

### 2.1 GLS Setup

```
RTL Design
    │
    ▼
Synthesis (Design Compiler)
    │
    ▼
Gate-Level Netlist (.v)
    │
    ▼
Place & Route (ICC2)
    │
    ▼
Post-Layout Netlist (.v)
    │
    ▼
SDF Extraction (.sdf)
    │
    ▼
Gate-Level Simulation
    ├── Functional GLS (no timing)
    └── Timing GLS (with SDF back-annotation)
```

### 2.2 GLS Compilation

```bash
# Gate-level simulation compile script
xrun -sv -64bit \
  -timescale 1ns/1ps \
  -sdf_version SDF_3.0 \
  +sdf+../../pnr/pacemaker_top.sdf \
  +define+GLS \
  -f filelist_gls.f \
  +UVM_TESTNAME=smoke_test \
  +UVM_VERBOSITY=UVM_MEDIUM \
  -l gls_sim.log \
  pacemaker_gls_tb.sv
```

### 2.3 GLS File List

```
# filelist_gls.f
// Gate-level netlist
../../syn/pacemaker_top_netlist.v
../../pnr/pacemaker_top物理.v

// Timing libraries
../../lib/pacemaker_fast.lib
../../lib/pacemaker_slow.lib

// Testbench
../../tb/pacemaker_gls_tb.sv
../../tb/heart_model.sv
../../tb/battery_model.sv

// Constraints
../../syn/pacemaker_top.sdc
```

## 3. SDF Back-Annotation

### 3.1 SDF Timing Application

```systemverilog
// GLS testbench with SDF
module pacemaker_gls_tb;

  // Instantiate synthesized netlist
  pacemaker_top u_dut (
    // Port connections
  );

  // Apply SDF timing
  initial begin
    $sdf_annotate("../../pnr/pacemaker_top.sdf", u_dut);
  end

  // Monitor timing violations
  initial begin
    $timeformat(-12, 0, "ps", 6);
  end

  // Check for timing violations
  always @(negedge clk) begin
    if ($realtime > 0 && $realtime % 10000 == 0)
      check_timing_violations();
  end

endmodule
```

### 3.2 Timing Modes

```
Mode           SDF File              Purpose
────────────────────────────────────────────────────
Fast           pacemaker_fast.sdf    Max frequency check
Slow           pacemaker_slow.sdf    Min frequency check
Typical        pacemaker_typ.sdf     Normal operation
```

## 4. GLS Test Categories

### 4.1 Functional GLS (No Timing)

```systemverilog
// Functional gate-level simulation
// No SDF annotation - pure logic verification
class functional_gls_test extends pacemaker_base_test;
  `uvm_component_utils(functional_gls_test)

  virtual task run_phase(uvm_phase phase);
    phase.raise_objection(this);

    // Run all directed tests
    run_smoke_test();
    run_mode_test();
    run_timing_test();
    run_safety_test();

    // Verify against RTL golden results
    compare_with_rtl_results();

    phase.drop_objection(this);
  endtask
endclass
```

### 4.2 Timing GLS (With SDF)

```systemverilog
// Timing gate-level simulation
class timing_gls_test extends pacemaker_base_test;
  `uvm_component_utils(timing_gls_test)

  virtual task run_phase(uvm_phase phase);
    phase.raise_objection(this);

    // Apply slow-corner SDF
    $sdf_annotate("../../pnr/pacemaker_top_slow.sdf", u_dut);

    // Run timing-critical tests
    run_max_frequency_test();
    run_setup_hold_test();
    run_clock_reconstruction_test();

    // Verify no timing violations
    check_timing_report();

    phase.drop_objection(this);
  endtask
endclass
```

## 5. GLS Test Scenarios

### 5.1 Smoke Test

```systemverilog
task gls_smoke_test();
  // Wait for reset
  @(posedge rst_n);
  #1000;

  // Configure via APB
  apb_write(8'h00, 32'h0000_0006); // VVI mode
  apb_write(8'h04, 32'h0000_0048); // 72 BPM
  apb_write(8'h0C, 32'h0000_0050); // 5.0V amplitude

  // Run for 5ms
  #5_000_000;

  // Verify basic functionality
  check_pace_generated();
  check_rate_accuracy(72, 5);
  check_amplitude(50, 5);

  `uvm_info("GLS", "Smoke test passed", UVM_LOW)
endtask
```

### 5.2 Timing Critical Test

```systemverilog
task gls_timing_critical_test();
  // Test at maximum frequency
  apb_write(8'h04, 32'h0000_0078); // 120 BPM max rate
  apb_write(8'h08, 32'h0000_00B4); // 180 BPM upper limit

  // Run for 10ms
  #10_000_000;

  // Verify timing at max rate
  check_rate_accuracy(120, 2);
  check_no_timing_violations();
endtask
```

### 5.3 Safety-Critical Test

```systemverilog
task gls_safety_critical_test();
  // Test fault detection at timing boundaries
  set_lead_impedance(16'hFFFF); // Open circuit
  #1000;
  check_fault_detected();
  check_fault_response_latency();

  // Test battery EOL detection
  set_battery_level(8'h32); // At EOL threshold
  #5000;
  check_battery_alert();
endtask
```

## 6. Timing Violation Detection

### 6.1 Setup/Hold Check

```systemverilog
// Monitor setup and hold violations
module timing_violation_monitor (
  input logic clk,
  input logic rst_n
);

  int setup_violations = 0;
  int hold_violations = 0;

  // Check for timing violations on every edge
  always @(posedge clk or negedge clk) begin
    if ($realtime > 0) begin
      // SDF annotation automatically checks timing
      // Violations reported via $sdf_annotate
    end
  end

  // Report timing violations
  task report_timing();
    `uvm_info("TIMING", $sformatf(
      "\n===== TIMING VIOLATION REPORT =====\nSetup violations: %0d\nHold violations:    %0d\n====================================",
      setup_violations, hold_violations), UVM_LOW)
  endtask

endmodule
```

### 6.2 Max Delay Check

```systemverilog
// Check maximum path delays
task check_max_delays();
  real max_combinational_delay;
  real max_setup_slack;
  real max_hold_slack;

  // Read from timing report
  max_combinational_delay = get_max_delay("pacemaker_top/pacing_controller/*");
  max_setup_slack = get_setup_slack();
  max_hold_slack = get_hold_slack();

  `uvm_info("TIMING", $sformatf(
    "Max combinational delay: %.2f ps\nSetup slack: %.2f ps\nHold slack: %.2f ps",
    max_combinational_delay, max_setup_slack, max_hold_slack), UVM_LOW)

  assert(max_setup_slack > 0) else
    `uvm_error("TIMING", "Setup violation detected");
  assert(max_hold_slack > 0) else
    `uvm_error("TIMING", "Hold violation detected");
endtask
```

## 7. GLS vs RTL Comparison

### 7.1 Golden Reference Comparison

```systemverilog
// Compare GLS results with RTL golden
task compare_with_rtl();
  // Read RTL golden results
  int rtl_pace_count;
  int rtl_rate_bpm;
  int rtl_amplitude;

  // Read from file or scoreboard
  rtl_pace_count = read_golden("pace_count");
  rtl_rate_bpm = read_golden("rate_bpm");
  rtl_amplitude = read_golden("amplitude");

  // Compare with GLS results
  assert(gls_pace_count == rtl_pace_count) else
    `uvm_error("GLS_CMP", $sformatf(
      "Pace count mismatch: GLS=%0d RTL=%0d",
      gls_pace_count, rtl_pace_count))

  assert(abs(gls_rate_bpm - rtl_rate_bpm) <= 2) else
    `uvm_error("GLS_CMP", $sformatf(
      "Rate mismatch: GLS=%0d RTL=%0d",
      gls_rate_bpm, rtl_rate_bpm))
endtask
```

### 7.2 Signal-Level Comparison

```systemverilog
// Signal-level comparison between RTL and GLS
task compare_signals();
  // Dump waveforms for manual comparison
  $dumpfile("rtl_wave.vcd");
  $dumpvars(0, pacemaker_rtl_tb);

  $dumpfile("gls_wave.vcd");
  $dumpvars(0, pacemaker_gls_tb);

  // Automated signal comparison
  compare_signal("pace_pulse", rtl_tb.pace_pulse, gls_tb.pace_pulse);
  compare_signal("pace_amplitude", rtl_tb.pace_amplitude, gls_tb.pace_amplitude);
  compare_signal("fault_flag", rtl_tb.fault_flag, gls_tb.fault_flag);
endtask
```

## 8. Multi-Corner GLS

### 8.1 Corner Matrix

```
Corner      Process    Voltage    Temperature    SDF
──────────────────────────────────────────────────────
SS_0p81V_-40C  slow     0.81V     -40°C         pacemaker_ss_0p81v_m40c.sdf
FF_0p99V_125C  fast     0.99V     125°C         pacemaker_ff_0p99v_125c.sdf
TT_0p90V_25C   typical  0.90V     25°C          pacemaker_tt_0.9v_25c.sdf
```

### 8.2 Multi-Corner Test Script

```bash
#!/bin/bash
# Multi-corner GLS script

CORNERS="ss_0p81v_m40c ff_0p99v_125c tt_0.9v_25c"

for corner in $CORNERS; do
  echo "Running GLS for corner: $corner"
  xrun -sv \
    +sdf+../../pnr/pacemaker_top_${corner}.sdf \
    +UVM_TESTNAME=gls_smoke_test \
    +UVM_VERBOSITY=UVM_LOW \
    -l gls_${corner}.log \
    pacemaker_gls_tb.sv

  if grep -q "TEST PASSED" gls_${corner}.log; then
    echo "Corner $corner: PASSED"
  else
    echo "Corner $corner: FAILED"
  fi
done
```

## 9. GLS Coverage

### 9.1 Gate-Level Coverage

```systemverilog
// Gate-level coverage collection
class gls_coverage extends uvm_subscriber #(pacemaker_seq_item);
  `uvm_component_utils(gls_coverage)

  covergroup gls_cg;
    option.per_instance = 1;

    // Timing corner coverage
    timing_corner_cp: coverpoint item.timing_corner {
      bins fast = {FAST};
      bins slow = {SLOW};
      bins typical = {TYPICAL};
    }

    // Speed bin coverage
    speed_bin_cp: coverpoint item.speed_bin {
      bins ss = {SS};
      bins ff = {FF};
      bins tt = {TT};
    }

    corner_x_speed: cross timing_corner_cp, speed_bin_cp;
  endgroup

  function new(string name = "gls_coverage", uvm_component parent);
    super.new(name, parent);
    gls_cg = new();
  endfunction

  virtual function void write(pacemaker_seq_item t);
    item = t;
    gls_cg.sample();
  endfunction
endclass
```

## 10. GLS Summary

Gate-level simulation for the iPACE-CHIP pacemaker provides:

| Test Type | Purpose | SDF Required |
|-----------|---------|--------------|
| Functional GLS | Logic verification | No |
| Timing GLS | Setup/hold checking | Yes |
| Multi-Corner GLS | PVT variation | Multiple SDF |
| Safety GLS | Fault response timing | Yes |
| Performance GLS | Max frequency | Yes |

Key GLS benefits:
- **Synthesis verification** - RTL matches gate-level
- **Timing verification** - Setup/hold violations detected
- **PVT coverage** - Multiple corner testing
- **Physical awareness** - Post-layout timing accuracy
- **Signoff confidence** - Final pre-silicon verification
