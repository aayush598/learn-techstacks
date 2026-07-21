# Coverage-Driven Verification for iPACE-CHIP Pacemaker

## 1. Introduction

Coverage-driven verification (CDV) is the cornerstone methodology for achieving verification closure on the iPACE-CHIP pacemaker. CDV uses functional coverage models to measure what has been verified, directs constrained-random stimulus to fill coverage gaps, and provides objective criteria for test completion.

This chapter covers functional coverage modeling, coverage collection infrastructure, closure analysis, and coverage-driven test generation specific to pacemaker verification.

## 2. Coverage Model Hierarchy

### 2.1 Coverage Architecture

```
Coverage Model
├── Functional Coverage
│   ├── Pacing Mode Coverage
│   ├── Cardiac Scenario Coverage
│   ├── Fault Condition Coverage
│   ├── Timing Boundary Coverage
│   ├── Configuration Coverage
│   └── State Transition Coverage
├── Code Coverage
│   ├── Statement Coverage
│   ├── Branch Coverage
│   ├── Toggle Coverage
│   └── FSM State Coverage
├── Assertion Coverage
│   ├── SVA Property Coverage
│   └── Temporal Coverage
└── Protocol Coverage
    ├── APB Transaction Coverage
    ├── UART Message Coverage
    └── SPI Register Coverage
```

## 3. Functional Coverage Definitions

### 3.1 Pacing Mode Coverage

```systemverilog
class pacing_mode_coverage extends uvm_subscriber #(pacemaker_seq_item);
  `uvm_component_utils(pacing_mode_coverage)

  pacemaker_seq_item item;

  covergroup pacing_mode_cg;
    option.per_instance = 1;
    option.name = "pacing_mode_cg";

    // Pacing mode cross-coverage
    mode_cp: coverpoint item.pacing_mode {
      bins aoo = {4'h0};
      bins voo = {4'h4};
      bins aai = {4'h8};
      bins vvi = {4'h6};
      bins ddd = {4'hD};
      bins vat  = {4'h5};
      bins vdd  = {4'h7};
      bins adir = {4'hF};
      bins other = default;
    }

    // Heart rate range
    heart_rate_cp: coverpoint item.heart_rate_bpm {
      bins brady_low    = {[0:40]};
      bins brady_mild   = {[41:59]};
      bins normal_low   = {[60:72]};
      bins normal_high  = {[73:100]};
      bins tachy_mild   = {[101:150]};
      bins tachy_high   = {[151:200]};
      bins extreme      = {[201:255]};
    }

    // Pulse amplitude
    amplitude_cp: coverpoint item.pulse_amplitude {
      bins low    = {[0:25]};
      bins medium = {[26:75]};
      bins high   = {[76:200]};
      bins max    = {[201:255]};
    }

    // Pulse width
    pulse_width_cp: coverpoint item.pulse_width_cfg {
      bins narrow = {[0:3]};
      bins normal = {[4:7]};
      bins wide   = {[8:15]};
    }

    // Refractory period
    refractory_cp: coverpoint item.refractory_period {
      bins short  = {[0:20]};
      bins medium = {[21:50]};
      bins long   = {[51:100]};
    }

    // Key crosses
    mode_x_rate: cross mode_cp, heart_rate_cp;
    mode_x_amplitude: cross mode_cp, amplitude_cp;
    mode_x_width: cross mode_cp, pulse_width_cp;
  endgroup

  function new(string name = "pacing_mode_coverage", uvm_component parent);
    super.new(name, parent);
    pacing_mode_cg = new();
  endfunction

  virtual function void write(pacemaker_seq_item t);
    item = t;
    pacing_mode_cg.sample();
  endfunction
endclass
```

### 3.2 Cardiac Scenario Coverage

```systemverilog
class cardiac_scenario_coverage extends uvm_subscriber #(pacemaker_seq_item);
  `uvm_component_utils(cardiac_scenario_coverage)

  pacemaker_seq_item item;

  // Sequence tracking
  bit atrial_seen = 0;
  bit ventricular_seen = 0;
  bit mode_switch_seen = 0;
  bit fault_seen = 0;
  bit recovery_seen = 0;

  covergroup cardiac_scenario_cg;
    option.per_instance = 1;

    // Cardiac rhythm types
    rhythm_cp: coverpoint item.rhythm {
      bins normal_sinus   = {NORMAL_SINUS};
      bins bradycardia    = {BRADYCARDIA};
      bins tachycardia    = {TACHYCARDIA};
      bins afib           = {AFIB};
      bins vtach          = {VTACH};
      bins asystole       = {ASYSTOLE};
      bins pvc            = {PVC};
    }

    // Event sequence coverage
    event_sequence_cp: coverpoint item.item_type {
      bins sense_then_pace   = (SENSE_EVENT => PACE_EVENT);
      bins pace_then_sense   = (PACE_EVENT => SENSE_EVENT);
      bins inhibit_after_sense = (SENSE_EVENT => INHIBIT_EVENT);
      bins fault_then_recovery = (LEAD_IMPEDANCE_ALERT => SENSE_EVENT);
      bins battery_then_mode  = (BATTERY_ALERT => MODE_SWITCH);
    }

    // Inter-event timing
    timing_cp: coverpoint item.inter_event_time {
      bins immediate  = {[0:10]};
      bins short      = {[11:50]};
      bins medium     = {[51:200]};
      bins long       = {[201:1000]};
      bins very_long  = {[1001:$]};
    }

    // Sense threshold
    threshold_cp: coverpoint item.sense_threshold {
      bins low    = {[0:50]};
      bins medium = {[51:150]};
      bins high   = {[151:255]};
    }

    // Lead impedance range
    impedance_cp: coverpoint item.lead_impedance {
      bins short_circuit = {[0:100]};
      bins normal_low    = {[101:299]};
      bins nominal       = {[300:1000]};
      bins normal_high   = {[1001:1499]};
      bins high_z        = {[1500:16'hFFFF]};
    }

    // Critical scenario crosses
    rhythm_x_threshold: cross rhythm_cp, threshold_cp;
    rhythm_x_impedance: cross rhythm_cp, impedance_cp;
    rhythm_x_timing:    cross rhythm_cp, timing_cp;
  endgroup

  function new(string name = "cardiac_scenario_coverage", uvm_component parent);
    super.new(name, parent);
    cardiac_scenario_cg = new();
  endfunction

  virtual function void write(pacemaker_seq_item t);
    item = t;
    cardiac_scenario_cg.sample();

    // Update sequence tracking
    if (t.item_type == SENSE_EVENT) atrial_seen = 1;
    if (t.item_type == PACE_EVENT) ventricular_seen = 1;
    if (t.item_type == MODE_SWITCH) mode_switch_seen = 1;
    if (t.item_type == LEAD_IMPEDANCE_ALERT) fault_seen = 1;
    if (t.item_type == SENSE_EVENT && fault_seen) recovery_seen = 1;
  endfunction
endclass
```

### 3.3 Fault Condition Coverage

```systemverilog
class fault_coverage extends uvm_subscriber #(pacemaker_seq_item);
  `uvm_component_utils(fault_coverage)

  pacemaker_seq_item item;

  covergroup fault_cg;
    option.per_instance = 1;

    // Fault type coverage
    fault_type_cp: coverpoint item.item_type {
      bins battery_low     = {BATTERY_ALERT};
      bins lead_fault      = {LEAD_IMPEDANCE_ALERT};
      bins mode_switch     = {MODE_SWITCH};
    }

    // Battery level boundaries
    battery_level_cp: coverpoint item.battery_level {
      bins full    = {[200:255]};
      bins good    = {[150:199]};
      bins warning = {[100:149]};
      bins low     = {[50:99]};
      bins critical = {[20:49]};
      bins depleted = {[0:19]};
    }

    // Lead impedance boundaries
    impedance_cp: coverpoint item.impedance_value {
      bins short    = {[0:200]};
      bins low      = {[201:299]};
      bins nominal  = {[300:1000]};
      bins high     = {[1001:1500]};
      bins open     = {[1501:16'hFFFF]};
    }

    // Battery-EOL threshold crossing
    battery_eol_cross: coverpoint item.battery_level {
      bins crossing [] = (200 => 150 => 100 => 50 => 20);
    }

    // Fault sequences
    fault_sequence_cp: coverpoint item.fault_sequence {
      bins single_fault    = {SINGLE};
      bins repeated_fault  = {REPEATED};
      bins concurrent      = {CONCURRENT};
      bins alternating     = {ALTERNATING};
    }

    battery_x_impedance: cross battery_level_cp, impedance_cp;
    fault_x_sequence: cross fault_type_cp, fault_sequence_cp;
  endgroup

  function new(string name = "fault_coverage", uvm_component parent);
    super.new(name, parent);
    fault_cg = new();
  endfunction

  virtual function void write(pacemaker_seq_item t);
    item = t;
    fault_cg.sample();
  endfunction
endclass
```

### 3.4 Timing Boundary Coverage

```systemverilog
class timing_boundary_coverage extends uvm_subscriber #(pacemaker_seq_item);
  `uvm_component_utils(timing_boundary_coverage)

  pacemaker_seq_item item;

  covergroup timing_boundary_cg;
    option.per_instance = 1;

    // Escape interval boundaries
    escape_interval_cp: coverpoint item.escape_interval_us {
      bins at_minimum    = {990, 995, 1000};  // 1000ms boundary
      bins below_min     = {[0:989]};
      bins above_min     = {[1001:1100]};
      bins at_nominal    = {830, 833, 836};    // 833ms = 72bpm
      bins at_maximum    = {495, 500, 505};    // 500ms = 120bpm
      bins above_max     = {[506:600]};
      bins below_max     = {[400:494]};
    }

    // Refractory period boundaries
    refractory_cp: coverpoint item.refractory_period_us {
      bins at_min   = {[245:255]};   // 250μs
      bins at_max   = {[495:505]};   // 500μs
      bins nominal  = {[300:400]};
    }

    // Pulse width boundaries
    pulse_width_boundary_cp: coverpoint item.pulse_width_us {
      bins at_min    = {[45:55]};    // 0.5ms
      bins at_max    = {[195:205]};  // 2.0ms
      bins nominal   = {[100:150]};
    }

    // Inter-beat interval for rate accuracy
    ibi_cp: coverpoint item.inter_beat_interval_ms {
      bins at_60bpm  = {[990:1010]};   // 1000ms
      bins at_72bpm  = {[825:840]};    // 833ms
      bins at_100bpm = {[590:610]};    // 600ms
      bins at_120bpm = {[490:510]};    // 500ms
      bins at_150bpm = {[390:410]};    // 400ms
    }

    escape_x_refractory: cross escape_interval_cp, refractory_cp;
    ibi_x_pulse_width: cross ibi_cp, pulse_width_boundary_cp;
  endgroup

  function new(string name = "timing_boundary_coverage", uvm_component parent);
    super.new(name, parent);
    timing_boundary_cg = new();
  endfunction

  virtual function void write(pacemaker_seq_item t);
    item = t;
    timing_boundary_cg.sample();
  endfunction
endclass
```

## 4. Coverage Collector Infrastructure

### 4.1 Unified Coverage Collector

```systemverilog
class pacemaker_coverage_collector extends uvm_component;
  `uvm_component_utils(pacemaker_coverage_collector)

  uvm_analysis_export #(pacemaker_seq_item) analysis_export;

  pacing_mode_coverage       pacing_cov;
  cardiac_scenario_coverage  cardiac_cov;
  fault_coverage             fault_cov;
  timing_boundary_coverage   timing_cov;
  state_transition_coverage  state_cov;
  configuration_coverage     cfg_cov;

  // Coverage goals
  int pacing_goal = 95;
  int cardiac_goal = 90;
  int fault_goal = 85;
  int timing_goal = 95;
  int state_goal = 100;
  int cfg_goal = 80;

  function new(string name = "pacemaker_coverage_collector", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    analysis_export = new("analysis_export", this);

    pacing_cov  = pacing_mode_coverage::type_id::create("pacing_cov", this);
    cardiac_cov = cardiac_scenario_coverage::type_id::create("cardiac_cov", this);
    fault_cov   = fault_coverage::type_id::create("fault_cov", this);
    timing_cov  = timing_boundary_coverage::type_id::create("timing_cov", this);
    state_cov   = state_transition_coverage::type_id::create("state_cov", this);
    cfg_cov     = configuration_coverage::type_id::create("cfg_cov", this);
  endfunction

  virtual function void connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    analysis_export.connect(pacing_cov.analysis_export);
    analysis_export.connect(cardiac_cov.analysis_export);
    analysis_export.connect(fault_cov.analysis_export);
    analysis_export.connect(timing_cov.analysis_export);
    analysis_export.connect(state_cov.analysis_export);
    analysis_export.connect(cfg_cov.analysis_export);
  endfunction

  virtual function bit is_goal_met();
    return (get_overall_coverage() >= 90);
  endfunction

  virtual function real get_overall_coverage();
    real total = 0;
    int count = 0;

    total += pacing_cov.pacing_mode_cg.get_coverage();
    count++;
    total += cardiac_cov.cardiac_scenario_cg.get_coverage();
    count++;
    total += fault_cov.fault_cg.get_coverage();
    count++;
    total += timing_cov.timing_boundary_cg.get_coverage();
    count++;

    return (count > 0) ? (total / count) : 0;
  endfunction

  virtual function void report_phase(uvm_phase phase);
    super.report_phase(phase);
    `uvm_info("COV_REPORT", $sformatf({
      "\n===== COVERAGE REPORT =====",
      "\n Pacing Mode:   %0.1f%% (goal: %0d%%)",
      "\n Cardiac Scn:   %0.1f%% (goal: %0d%%)",
      "\n Fault Cond:    %0.1f%% (goal: %0d%%)",
      "\n Timing Bound:  %0.1f%% (goal: %0d%%)",
      "\n State Trans:   %0.1f%% (goal: %0d%%)",
      "\n Config:        %0.1f%% (goal: %0d%%)",
      "\n Overall:       %0.1f%%",
      "\n==========================="
    },
      pacing_cov.pacing_mode_cg.get_coverage(), pacing_goal,
      cardiac_cov.cardiac_scenario_cg.get_coverage(), cardiac_goal,
      fault_cov.fault_cg.get_coverage(), fault_goal,
      timing_cov.timing_boundary_cg.get_coverage(), timing_goal,
      state_cov.get_coverage(), state_goal,
      cfg_cov.get_coverage(), cfg_goal,
      get_overall_coverage()), UVM_LOW)
  endfunction
endclass
```

## 5. Coverage-Driven Test Generation

### 5.1 Coverage-Blind Random Test

```systemverilog
class coverage_driven_test extends pacemaker_base_test;
  `uvm_component_utils(coverage_driven_test)

  pacemaker_coverage_collector cov_collector;
  int max_iterations = 10000;

  function new(string name = "coverage_driven_test", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual task run_phase(uvm_phase phase);
    phase.raise_objection(this);
    repeat (max_iterations) begin
      if (cov_collector.is_goal_met()) begin
        `uvm_info("CDV", "Coverage goal met - stopping", UVM_LOW)
        break;
      end
      run_random_iteration();
    end
    phase.drop_objection(this);
  endtask

  virtual task run_random_iteration();
    cardiac_event_item item;
    item = cardiac_event_item::type_id::create("item");
    assert(item.randomize());
    env.agent.sqr.send_request(item);
    wait(item.done);
  endtask
endclass
```

### 5.2 Coverage-Hole Targeted Test

```systemverilog
class coverage_hole_test extends pacemaker_base_test;
  `uvm_component_utils(coverage_hole_test)

  function new(string name = "coverage_hole_test", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual task run_phase(uvm_phase phase);
    phase.raise_objection(this);
    target_coverage_holes();
    phase.drop_objection(this);
  endtask

  virtual task target_coverage_holes();
    // VVI mode with extreme rates
    vvi_extreme_rate_seq seq1;
    seq1 = vvi_extreme_rate_seq::type_id::create("seq1");
    assert(seq1.randomize() with {
      rate_bpm inside {30, 150};
    });
    seq1.start(env.agent.sqr);

    // DDD mode with atrial+ventricular events
    ddd_dual_event_seq seq2;
    seq2 = ddd_dual_event_seq::type_id::create("seq2");
    seq2.start(env.agent.sqr);

    // Concurrent faults
    concurrent_fault_seq seq3;
    seq3 = concurrent_fault_seq::type_id::create("seq3");
    seq3.start(env.agent.sqr);

    // Boundary timing
    boundary_timing_seq seq4;
    seq4 = boundary_timing_seq::type_id::create("seq4");
    assert(seq4.randomize());
    seq4.start(env.agent.sqr);
  endtask
endclass
```

## 6. State Transition Coverage

### 6.1 FSM Coverage Model

```systemverilog
class state_transition_coverage extends uvm_subscriber #(pacemaker_seq_item);
  `uvm_component_utils(state_transition_coverage)

  typedef enum {
    ST_IDLE,
    ST_SENSE_MONITOR,
    ST_PACE_GENERATE,
    ST_REFRACTORY,
    ST_INHIBIT,
    ST_BATTERY_CHECK,
    ST_FAULT_HANDLE,
    ST_MODE_SWITCH,
    ST_TELEMETRY_TX,
    ST_SLEEP
  } state_e;

  state_e current_state = ST_IDLE;
  state_e previous_state = ST_IDLE;

  covergroup fsm_cg;
    option.per_instance = 1;

    state_cp: coverpoint current_state {
      bins idle          = {ST_IDLE};
      bins sense_monitor = {ST_SENSE_MONITOR};
      bins pace_generate = {ST_PACE_GENERATE};
      bins refractory    = {ST_REFRACTORY};
      bins inhibit       = {ST_INHIBIT};
      bins battery_check = {ST_BATTERY_CHECK};
      bins fault_handle  = {ST_FAULT_HANDLE};
      bins mode_switch   = {ST_MODE_SWITCH};
      bins telemetry     = {ST_TELEMETRY_TX};
      bins sleep         = {ST_SLEEP};
    }

    prev_state_cp: coverpoint previous_state {
      bins idle          = {ST_IDLE};
      bins sense_monitor = {ST_SENSE_MONITOR};
      bins pace_generate = {ST_PACE_GENERATE};
      bins refractory    = {ST_REFRACTORY};
      bins inhibit       = {ST_INHIBIT};
      bins battery_check = {ST_BATTERY_CHECK};
      bins fault_handle  = {ST_FAULT_HANDLE};
      bins mode_switch   = {ST_MODE_SWITCH};
      bins telemetry     = {ST_TELEMETRY_TX};
      bins sleep         = {ST_SLEEP};
    }

    transition_cp: cross prev_state_cp, state_cp;
  endgroup

  function new(string name = "state_transition_coverage", uvm_component parent);
    super.new(name, parent);
    fsm_cg = new();
  endfunction

  virtual function void write(pacemaker_seq_item t);
    previous_state = current_state;
    current_state = state_e'(t.current_state);
    fsm_cg.sample();
  endfunction

  virtual function real get_coverage();
    return fsm_cg.get_coverage();
  endfunction
endclass
```

## 7. Configuration Coverage

### 7.1 Register Configuration Coverage

```systemverilog
class configuration_coverage extends uvm_subscriber #(pacemaker_seq_item);
  `uvm_component_utils(configuration_coverage)

  covergroup config_cg;
    option.per_instance = 1;

    // Mode register coverage
    mode_reg_cp: coverpoint item.pacing_mode {
      bins modes[] = {4'h0, 4'h4, 4'h6, 4'h8, 4'hD};
    }

    // Lower rate limit coverage
    lrl_cp: coverpoint item.lower_rate_limit {
      bins min_rate   = {8'd50};
      bins nominal    = {8'd60, 8'd72, 8'd80};
      bins max_rate   = {8'd100};
      bins extreme    = {8'd40, 8'd120};
    }

    // Upper rate limit
    url_cp: coverpoint item.upper_rate_limit {
      bins min_url = {8'd100};
      bins nominal = {8'd120, 8'd150};
      bins max_url = {8'd180};
    }

    // Pulse amplitude
    amplitude_reg_cp: coverpoint item.pulse_amplitude {
      bins min_amp  = {8'd10};
      bins nominal  = {8'd50};
      bins max_amp  = {8'd100};
    }

    mode_x_lrl: cross mode_reg_cp, lrl_cp;
    mode_x_amplitude: cross mode_reg_cp, amplitude_reg_cp;
  endgroup

  function new(string name = "configuration_coverage", uvm_component parent);
    super.new(name, parent);
    config_cg = new();
  endfunction

  virtual function void write(pacemaker_seq_item t);
    item = t;
    config_cg.sample();
  endfunction

  virtual function real get_coverage();
    return config_cg.get_coverage();
  endfunction
endclass
```

## 8. Coverage Closure Strategy

### 8.1 Progressive Closure Flow

```
Phase 1: Directed Tests (0-40% coverage)
  → Smoke tests, basic mode operation
  → Target critical paths

Phase 2: Constrained-Random (40-75% coverage)
  → Broad stimulus generation
  → Auto-exploration of scenarios

Phase 3: Coverage-Gap Targeted (75-90% coverage)
  → Identify uncovered bins
  → Design targeted sequences

Phase 4: Manual Analysis (90-95% coverage)
  → Review remaining holes
  → Determine if holes are reachable
  → Waive unreachable bins

Phase 5: Signoff (95%+ coverage)
  → Final regression
  → Coverage report generation
  → Review board signoff
```

### 8.2 Coverage Hole Analysis

```systemverilog
class coverage_hole_analyzer extends uvm_component;
  `uvm_component_utils(coverage_hole_analyzer)

  pacemaker_coverage_collector cov;

  typedef struct {
    string covergroup_name;
    string coverpoint_name;
    int    bin_index;
    int    hit_count;
    real   weight;
  } coverage_hole_t;

  coverage_hole_t holes[$];

  function new(string name = "coverage_hole_analyzer", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual function void analyze_holes();
    // This would typically query the coverage database
    // to identify bins with zero hits
    `uvm_info("COV_HOLE", $sformatf(
      "Identified %0d coverage holes", holes.size()), UVM_LOW)

    foreach (holes[i]) begin
      `uvm_info("HOLE", $sformatf(
        "  [%0d] %s.%s bin[%0d] hits=%0d weight=%0.1f",
        i, holes[i].covergroup_name, holes[i].coverpoint_name,
        holes[i].bin_index, holes[i].hit_count, holes[i].weight), UVM_LOW)
    end
  endfunction

  virtual function bit is_reachable(string hole_id);
    // Determine if a coverage hole represents
    // a reachable state/condition in the DUT
    // This requires designer consultation
    return 1; // Default: treat as reachable
  endfunction
endclass
```

## 9. Regression and Batch Coverage

### 9.1 Regression Configuration

```systemverilog
// Test suite definitions for regression
class pacemaker_regression_suite extends uvm_test;
  // Seed-able test collection
  string test_list[] = '{
    "pacemaker_smoke_test",
    "pacemaker_vvi_mode_test",
    "pacemaker_ddd_mode_test",
    "pacemaker_fault_test",
    "pacemaker_battery_test",
    "pacemaker_timing_test",
    "coverage_driven_test"
  };

  int seeds_per_test = 10;
endclass
```

### 9.2 Coverage Merging

```
# Coverage merge script concept
merge_coverage.pl:
  1. Collect .ucdb files from all regression runs
  2. Merge into unified coverage database
  3. Generate coverage report with hole analysis
  4. Compare against coverage goals
  5. Generate closure status
```

## 10. Summary

Coverage-driven verification for iPACE-CHIP pacemaker provides:

| Coverage Model | Purpose | Target |
|----------------|---------|--------|
| Pacing Mode | Mode-specific behavior | 95% |
| Cardiac Scenario | Clinical scenario exhaustiveness | 90% |
| Fault Condition | Reliability verification | 85% |
| Timing Boundary | Accuracy verification | 95% |
| State Transition | FSM completeness | 100% |
| Configuration | Register space exploration | 80% |

Key CDV principles applied:
- **Measurement-based closure** with objective coverage goals
- **Constrained-random** stimulus guided by coverage models
- **Coverage-hole targeting** to close gaps efficiently
- **Progressive coverage** from directed to random to targeted
- **Waiver management** for unreachable or inapplicable bins
