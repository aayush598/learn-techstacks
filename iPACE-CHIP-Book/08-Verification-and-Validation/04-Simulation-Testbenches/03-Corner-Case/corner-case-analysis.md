# Corner Case Analysis for iPACE-CHIP Pacemaker

## 1. Introduction

Corner case analysis systematically tests extreme values, boundary conditions, and rare combinations that are most likely to expose design bugs. For the iPACE-CHIP pacemaker, corner cases involve maximum/minimum timing parameters, extreme cardiac rates, boundary battery levels, and simultaneous fault conditions.

## 2. Timing Corner Cases

### 2.1 Pulse Width Boundaries

```systemverilog
// Minimum pulse width
task test_min_pulse_width();
  apb_write(8'h10, 32'h0000_0001); // 0.1ms - minimum
  start_pacing();
  check_pulse_width(1); // Verify minimum width met
endtask

// Maximum pulse width
task test_max_pulse_width();
  apb_write(8'h10, 32'h0000_0015); // 2.0ms - maximum
  start_pacing();
  check_pulse_width(20); // Verify maximum width
endtask

// Zero pulse width (boundary)
task test_zero_pulse_width();
  apb_write(8'h10, 32'h0000_0000); // 0.0ms
  start_pacing();
  check_pace_behavior(); // Should handle gracefully
endtask
```

### 2.2 Rate Boundaries

```systemverilog
// Minimum rate (30 BPM)
task test_min_rate();
  apb_write(8'h04, 32'h0000_001E); // LRL = 30
  apb_write(8'h08, 32'h0000_0078); // URL = 120
  run_for_duration(10_000); // 10 seconds
  check_rate_accuracy(30, 2); // 30 BPM ±2
endtask

// Maximum rate (180 BPM)
task test_max_rate();
  apb_write(8'h04, 32'h0000_003C); // LRL = 60
  apb_write(8'h08, 32'h0000_00B4); // URL = 180
  inject_tachycardia(180);
  run_for_duration(5_000);
  check_rate_accuracy(180, 2);
endtask

// Boundary rate (100 BPM)
task test_boundary_rate();
  apb_write(8'h04, 32'h0000_0064); // LRL = 100
  apb_write(8'h08, 32'h0000_0078); // URL = 120
  run_for_duration(5_000);
  check_rate_accuracy(100, 2);
endtask
```

### 2.3 Refractory Period Boundaries

```systemverilog
// Minimum refractory period
task test_min_refractory();
  apb_write(8'h14, 32'h0000_000A); // 100μs minimum
  start_pacing();
  verify_no_double_pace();
endtask

// Maximum refractory period
task test_max_refractory();
  apb_write(8'h14, 32'h0000_0064); // 1.0ms maximum
  start_pacing();
  verify_refractory_enforced();
endtask
```

## 3. Amplitude Corner Cases

### 3.1 Amplitude Boundaries

```systemverilog
// Minimum amplitude
task test_min_amplitude();
  apb_write(8'h0C, 32'h0000_000A); // 1.0V minimum
  start_pacing();
  check_amplitude(10);
  verify_capture_threshold(); // Check if minimum amplitude captures
endtask

// Maximum amplitude
task test_max_amplitude();
  apb_write(8'h0C, 32'h0000_0064); // 10.0V maximum
  start_pacing();
  check_amplitude(100);
  verify_no_damage(); // Check no damage at max amplitude
endtask

// Zero amplitude (invalid)
task test_zero_amplitude();
  apb_write(8'h0C, 32'h0000_0000); // 0V
  start_pacing();
  check_error_handling(); // Should reject or handle
endtask
```

## 4. Battery Corner Cases

### 4.1 Battery Level Boundaries

```systemverilog
// Full battery
task test_full_battery();
  set_battery_level(8'hFF); // 100%
  run_for_duration(10_000);
  verify_no_battery_alert();
endtask

// Battery at EOL threshold
task test_battery_eol();
  set_battery_level(8'h32); // 50% - EOL threshold
  run_for_duration(5_000);
  verify_battery_alert();
  verify_telemetry_sent();
endtask

// Battery at critical level
task test_battery_critical();
  set_battery_level(8'h14); // 20% - critical
  run_for_duration(2_000);
  verify_critical_alert();
  verify_mode_change(); // Should switch to safe mode
endtask

// Battery depleted
task test_battery_depleted();
  set_battery_level(8'h00); // 0%
  run_for_duration(1_000);
  verify_depletion_response();
endtask
```

### 4.2 Battery Transition Edge Cases

```systemverilog
// Battery crossing EOL during pacing
task test_battery_crossing_eol();
  set_battery_level(8'h33); // Just above EOL
  start_pacing();
  gradually_deplete(8'h31); // Cross EOL threshold
  verify_seamless_transition();
  verify_alert_generated();
endtask

// Battery fluctuation near threshold
task test_battery_fluctuation();
  repeat (10) begin
    set_battery_level(8'h32); // At threshold
    run_for_duration(100);
    set_battery_level(8'h33); // Above threshold
    run_for_duration(100);
  end
  verify_no_spurious_alerts();
endtask
```

## 5. Impedance Corner Cases

### 5.1 Lead Impedance Boundaries

```systemverilog
// Nominal impedance
task test_nominal_impedance();
  set_lead_impedance(16'h01F4); // 500Ω nominal
  run_for_duration(10_000);
  verify_normal_operation();
endtask

// Low impedance (near short)
task test_low_impedance();
  set_lead_impedance(16'h0064); // 100Ω
  run_for_duration(5_000);
  verify_fault_detected();
endtask

// Short circuit
task test_short_circuit();
  set_lead_impedance(16'h0001); // 1Ω - short
  run_for_duration(1_000);
  verify_fault_response();
  verify_pacing_inhibited();
endtask

// High impedance (near open)
task test_high_impedance();
  set_lead_impedance(16'h05DC); // 1500Ω
  run_for_duration(5_000);
  verify_fault_detected();
endtask

// Open circuit
task test_open_circuit();
  set_lead_impedance(16'hFFFF); // 65535Ω - open
  run_for_duration(1_000);
  verify_fault_response();
  verify_safe_mode();
endtask
```

## 6. Mode Corner Cases

### 6.1 Mode Transition Edge Cases

```systemverilog
// Rapid mode switching
task test_rapid_mode_switch();
  repeat (10) begin
    apb_write(8'h00, 32'h0000_0006); // VVI
    #1000;
    apb_write(8'h00, 32'h0000_0008); // AAI
    #1000;
    apb_write(8'h00, 32'h0000_000D); // DDD
    #1000;
  end
  verify_no_mode_instability();
endtask

// Mode switch during active pacing
task test_mode_switch_during_pace();
  start_pacing();
  #500; // During active pacing cycle
  apb_write(8'h00, 32'h0000_0008); // Switch to AAI
  verify_seamless_transition();
  verify_correct_behavior();
endtask

// Invalid mode register value
task test_invalid_mode();
  apb_write(8'h00, 32'h0000_000F); // Invalid mode
  verify_error_handling();
  verify_default_mode();
endtask
```

## 7. Simultaneous Corner Cases

### 7.1 Multiple Fault Conditions

```systemverilog
// Simultaneous battery low and lead fault
task test_simultaneous_faults();
  set_battery_level(8'h14); // Critical battery
  set_lead_impedance(16'h0001); // Short circuit
  run_for_duration(2_000);
  verify_highest_priority_fault();
  verify_safe_operation();
endtask

// Fault during mode transition
task test_fault_during_mode_transition();
  start_pacing();
  set_lead_impedance(16'hFFFF); // Open circuit
  apb_write(8'h00, 32'h0000_000D); // Switch to DDD
  verify_fault_priority();
  verify_mode_stability();
endtask
```

## 8. Corner Case Test Suite

### 8.1 Systematic Corner Case Generator

```systemverilog
class corner_case_generator;
  // Generate all boundary combinations
  function void generate_timing_corners();
    int min_pulse_widths[] = '{0, 1, 2};
    int max_pulse_widths[] = '{14, 15, 16};
    int min_rates[] = '{29, 30, 31};
    int max_rates[] = '{179, 180, 181};

    foreach (min_pulse_widths[i])
      foreach (max_pulse_widths[j])
        test_pulse_width_corner(min_pulse_widths[i], max_pulse_widths[j]);

    foreach (min_rates[i])
      foreach (max_rates[j])
        test_rate_corner(min_rates[i], max_rates[j]);
  endfunction

  function void generate_battery_corners();
    int battery_levels[] = '{0, 1, 49, 50, 51, 254, 255};
    foreach (battery_levels[i])
      test_battery_corner(battery_levels[i]);
  endfunction

  function void generate_impedance_corners();
    int impedances[] = '{0, 1, 99, 100, 101, 299, 300,
                         1000, 1499, 1500, 1501, 65534, 65535};
    foreach (impedances[i])
      test_impedance_corner(impedances[i]);
  endfunction
endclass
```

## 9. Corner Case Coverage

### 9.1 Boundary Coverage Model

```systemverilog
class boundary_coverage extends uvm_subscriber #(pacemaker_seq_item);
  `uvm_component_utils(boundary_coverage)

  covergroup boundary_cg;
    option.per_instance = 1;

    // Pulse width boundaries
    pulse_width_boundary: coverpoint item.pulse_width {
      bins at_min    = {0, 1, 2};
      bins low_mid   = {[3:7]};
      bins high_mid  = {[8:12]};
      bins at_max    = {13, 14, 15};
    }

    // Rate boundaries
    rate_boundary: coverpoint item.heart_rate_bpm {
      bins at_min    = {29, 30, 31};
      bins low_mid   = {[31:59]};
      bins normal    = {[60:100]};
      bins high_mid  = {[101:179]};
      bins at_max    = {179, 180, 181};
    }

    // Battery boundaries
    battery_boundary: coverpoint item.battery_level {
      bins depleted  = {0, 1};
      bins critical  = {[2:49]};
      bins eol       = {50, 51};
      bins warning   = {[52:149]};
      bins good      = {[150:254]};
      bins full      = {255};
    }

    // Impedance boundaries
    impedance_boundary: coverpoint item.lead_impedance {
      bins short     = {0, 1};
      bins low       = {[2:99]};
      bins low_nom   = {100, 101};
      bins nominal   = {[102:299]};
      bins nom_high  = {300, 1000};
      bins high_nom  = {1499, 1500};
      bins high      = {1501, 65534};
      bins open      = {65535};
    }

    // Cross coverage at boundaries
    rate_x_battery: cross rate_boundary, battery_boundary;
    rate_x_impedance: cross rate_boundary, impedance_boundary;
  endgroup

  function new(string name = "boundary_coverage", uvm_component parent);
    super.new(name, parent);
    boundary_cg = new();
  endfunction

  virtual function void write(pacemaker_seq_item t);
    item = t;
    boundary_cg.sample();
  endfunction
endclass
```

## 10. Summary

Corner case analysis for the iPACE-CHIP pacemaker covers:

| Category | Corner Cases | Test Count |
|----------|-------------|------------|
| Timing | Pulse width, rate, refractory | 15 |
| Amplitude | Min, max, zero | 5 |
| Battery | Full, EOL, critical, depleted | 8 |
| Impedance | Short, nominal, open | 7 |
| Mode | Transitions, invalid, rapid | 6 |
| Simultaneous | Multiple faults | 4 |
| **Total** | | **45** |

Key corner case benefits:
- **Boundary testing** at specification limits
- **Simultaneous condition** testing for priority logic
- **Automatic generation** of boundary combinations
- **Coverage tracking** for boundary completeness
- **Reproducible** corner case sequences
