# Random and Constrained-Random Testing for iPACE-CHIP Pacemaker

## 1. Introduction

Constrained-random testing (CRT) generates stimulus by randomizing sequence items with constraints that ensure legal and meaningful DUT inputs. For the iPACE-CHIP pacemaker, CRT explores scenarios that directed tests might miss, such as rare timing combinations, edge-case parameter values, and fault injection timing.

## 2. Randomization Infrastructure

### 2.1 Constrained Sequence Item

```systemverilog
class cardiac_stimulus extends uvm_sequence_item;
  `uvm_object_utils(cardiac_stimulus)

  // Stimulus parameters
  rand bit [7:0]  heart_rate_bpm;
  rand bit [3:0]  pacing_mode;
  rand bit [7:0]  pulse_amplitude;
  rand bit [7:0]  pulse_width;
  rand bit [7:0]  lower_rate_limit;
  rand bit [7:0]  upper_rate_limit;
  rand bit [7:0]  refractory_period;
  rand bit        inhibit_active;
  rand bit        fault_inject;
  rand bit [15:0] lead_impedance;
  rand bit [7:0]  battery_level;
  rand int        duration_ms;

  // Constraints
  constraint c_heart_rate {
    heart_rate_bpm inside {[30:200]};
  }

  constraint c_pacing_mode {
    pacing_mode inside {4'h0, 4'h4, 4'h6, 4'h8, 4'hD};
  }

  constraint c_amplitude {
    pulse_amplitude inside {[10:100]};
  }

  constraint c_pulse_width {
    pulse_width inside {[1:15]};
  }

  constraint c_rate_limits {
    lower_rate_limit inside {[40:100]};
    upper_rate_limit inside {[100:180]};
    upper_rate_limit > lower_rate_limit;
  }

  constraint c_refractory {
    refractory_period inside {[10:50]};
  }

  constraint c_lead_impedance {
    lead_impedance dist {
      [0:100]     := 5,    // Short circuit (5%)
      [101:299]   := 10,   // Low impedance (10%)
      [300:1000]  := 60,   // Nominal (60%)
      [1001:1500] := 15,   // High impedance (15%)
      [1501:65535]:= 10    // Open circuit (10%)
    };
  }

  constraint c_battery {
    battery_level dist {
      [200:255] := 30,   // Full (30%)
      [150:199] := 25,   // Good (25%)
      [100:149] := 20,   // Warning (20%)
      [50:99]   := 15,   // Low (15%)
      [0:49]    := 10    // Critical (10%)
    };
  }

  constraint c_duration {
    duration_ms inside {[100:5000]};
  }

  constraint c_realistic {
    // Mode-specific constraints
    if (pacing_mode == 4'hD) { // DDD
      heart_rate_bpm inside {[60:120]};
      pulse_amplitude inside {[20:80]};
    }
    if (pacing_mode == 4'h8) { // AAI
      heart_rate_bpm inside {[50:100]};
    }
  }

  function new(string name = "cardiac_stimulus");
    super.new(name);
  endfunction

  virtual function string convert2string();
    return $sformatf(
      "HR=%0d Mode=0x%h Amp=%0d Width=%0d LRL=%0d URL=%0d Ref=%0d Batt=%0d Z=%0d",
      heart_rate_bpm, pacing_mode, pulse_amplitude, pulse_width,
      lower_rate_limit, upper_rate_limit, refractory_period,
      battery_level, lead_impedance);
  endfunction
endclass
```

### 2.2 Weighted Distribution

```systemverilog
// Weighted stimulus distribution for realistic testing
class weighted_stimulus extends uvm_sequence_item;
  `uvm_object_utils(weighted_stimulus)

  typedef enum {
    NORMAL_OPERATION,    // 50% weight
    BRADYCARDIA_EVENT,   // 15% weight
    TACHYCARDIA_EVENT,   // 10% weight
    FAULT_CONDITION,     // 10% weight
    BATTERY_LOW_EVENT,   // 8% weight
    MODE_TRANSITION,     // 5% weight
    EDGE_CASE            // 2% weight
  } scenario_e;

  rand scenario_e scenario;

  constraint c_scenario_weight {
    scenario dist {
      NORMAL_OPERATION   := 50,
      BRADYCARDIA_EVENT  := 15,
      TACHYCARDIA_EVENT  := 10,
      FAULT_CONDITION    := 10,
      BATTERY_LOW_EVENT  := 8,
      MODE_TRANSITION    := 5,
      EDGE_CASE          := 2
    };
  }
endclass
```

## 3. Constrained-Random Sequences

### 3.1 Basic Random Sequence

```systemverilog
class random_pacing_seq extends uvm_sequence #(cardiac_stimulus);
  `uvm_object_utils(random_pacing_seq)

  int num_transactions = 1000;

  function new(string name = "random_pacing_seq");
    super.new(name);
  endfunction

  virtual task body();
    cardiac_stimulus item;
    repeat (num_transactions) begin
      item = cardiac_stimulus::type_id::create("item");
      start_item(item);
      assert(item.randomize()) else
        `uvm_fatal("RAND", "Randomization failed")
      finish_item(item);
    end
  endtask
endclass
```

### 3.2 Scenario-Based Random Sequence

```systemverilog
class scenario_random_seq extends uvm_sequence #(cardiac_stimulus);
  `uvm_object_utils(scenario_random_seq)

  function new(string name = "scenario_random_seq");
    super.new(name);
  endfunction

  virtual task body();
    weighted_stimulus scenario_item;
    cardiac_stimulus  stim_item;

    repeat (500) begin
      // Select scenario
      scenario_item = weighted_stimulus::type_id::create("scenario_item");
      assert(scenario_item.randomize());

      // Generate stimulus for scenario
      stim_item = cardiac_stimulus::type_id::create("stim_item");

      case (scenario_item.scenario)
        NORMAL_OPERATION: begin
          assert(stim_item.randomize() with {
            pacing_mode inside {4'h6, 4'h8}; // VVI or AAI
            heart_rate_bpm inside {[60:100]};
            pulse_amplitude inside {[30:70]};
            fault_inject == 0;
            battery_level inside {[150:255]};
          });
        end

        BRADYCARDIA_EVENT: begin
          assert(stim_item.randomize() with {
            heart_rate_bpm inside {[30:50]};
            pacing_mode inside {4'h6, 4'hD};
            inhibit_active == 0;
          });
        end

        TACHYCARDIA_EVENT: begin
          assert(stim_item.randomize() with {
            heart_rate_bpm inside {[120:200]};
            pacing_mode inside {4'h6};
          });
        end

        FAULT_CONDITION: begin
          assert(stim_item.randomize() with {
            fault_inject == 1;
            lead_impedance inside {[0:100], [1500:65535]};
          });
        end

        BATTERY_LOW_EVENT: begin
          assert(stim_item.randomize() with {
            battery_level inside {[0:50]};
          });
        end

        MODE_TRANSITION: begin
          assert(stim_item.randomize() with {
            pacing_mode inside {4'h0, 4'h4, 4'h6, 4'h8, 4'hD};
          });
        end

        EDGE_CASE: begin
          assert(stim_item.randomize() with {
            heart_rate_bpm inside {30, 200};
            pulse_amplitude inside {10, 100};
            lead_impedance inside {0, 65535};
            battery_level inside {0, 255};
          });
        end
      endcase

      start_item(stim_item);
      finish_item(stim_item);
    end
  endtask
endclass
```

### 3.3 Time-Controlled Random Sequence

```systemverilog
class timed_random_seq extends uvm_sequence #(cardiac_stimulus);
  `uvm_object_utils(timed_random_seq)

  int simulation_time_ms = 100;

  function new(string name = "timed_random_seq");
    super.new(name);
  endfunction

  virtual task body();
    cardiac_stimulus item;
    int time_elapsed_ms = 0;

    while (time_elapsed_ms < simulation_time_ms) begin
      item = cardiac_stimulus::type_id::create("item");
      start_item(item);
      assert(item.randomize());
      finish_item(item);

      time_elapsed_ms += item.duration_ms;
    end
  endtask
endclass
```

## 4. Constraint Techniques

### 4.1 Inline Constraints

```systemverilog
// Using 'with' clause for inline constraints
class inline_constraint_seq extends uvm_sequence #(cardiac_stimulus);
  `uvm_object_utils(inline_constraint_seq)

  virtual task body();
    cardiac_stimulus item;

    // Constraint for VVI mode only
    item = cardiac_stimulus::type_id::create("item");
    start_item(item);
    assert(item.randomize() with {
      pacing_mode == 4'h6; // VVI only
      heart_rate_bpm inside {[60:80]};
    });
    finish_item(item);

    // Constraint for high amplitude
    item = cardiac_stimulus::type_id::create("item");
    start_item(item);
    assert(item.randomize() with {
      pulse_amplitude inside {[80:100]};
      pulse_width inside {[5:15]};
    });
    finish_item(item);

    // Constraint for fault scenario
    item = cardiac_stimulus::type_id::create("item");
    start_item(item);
    assert(item.randomize() with {
      fault_inject == 1;
      lead_impedance inside {[0:50]}; // Short circuit
      pacing_mode == 4'h6;
    });
    finish_item(item);
  endtask
endclass
```

### 4.2 Soft Constraints

```systemverilog
class soft_constraint_seq extends uvm_sequence #(cardiac_stimulus);
  `uvm_object_utils(soft_constraint_seq)

  virtual task body();
    cardiac_stimulus item;
    item = cardiac_stimulus::type_id::create("item");

    // Soft constraints: prefer these values but allow override
    assert(item.randomize() with {
      soft heart_rate_bpm == 72;
      soft pacing_mode == 4'h6;
      soft pulse_amplitude == 50;
      // Hard constraint: must satisfy
      battery_level inside {[100:255]};
    });

    start_item(item);
    finish_item(item);
  endtask
endclass
```

### 4.3 Implication Constraints

```systemverilog
class implication_seq extends uvm_sequence #(cardiac_stimulus);
  `uvm_object_utils(implication_seq)

  virtual task body();
    cardiac_stimulus item;
    repeat (100) begin
      item = cardiac_stimulus::type_id::create("item");
      start_item(item);
      assert(item.randomize() with {
        // If DDD mode, stricter constraints
        (pacing_mode == 4'hD) -> {
          heart_rate_bpm inside {[60:100]};
          pulse_amplitude inside {[20:80]};
          pulse_width inside {[3:10]};
        };
        // If VVI mode, different constraints
        (pacing_mode == 4'h6) -> {
          heart_rate_bpm inside {[50:120]};
        };
        // Fault always has extreme impedance
        fault_inject -> {
          lead_impedance inside {[0:100], [1500:65535]};
        };
      });
      finish_item(item);
    end
  endtask
endclass
```

## 5. Random Stability

### 5.1 Seeded Randomization

```systemverilog
class seeded_random_seq extends uvm_sequence #(cardiac_stimulus);
  `uvm_object_utils(seeded_random_seq)

  int unsigned seed = 0;

  virtual task body();
    cardiac_stimulus item;
    // Use seed for reproducible randomization
    item = cardiac_stimulus::type_id::create("item");
    item.srandom(seed); // Set seed for this item
    start_item(item);
    assert(item.randomize());
    finish_item(item);
  endtask
endclass
```

### 5.2 Random Stability Verification

```systemverilog
// Verify same seed produces same sequence
task verify_random_stability();
  cardiac_stimulus item1, item2;

  item1 = cardiac_stimulus::type_id::create("item1");
  item1.srandom(12345);
  assert(item1.randomize());

  item2 = cardiac_stimulus::type_id::create("item2");
  item2.srandom(12345);
  assert(item2.randomize());

  assert(item1.heart_rate_bpm == item2.heart_rate_bpm)
    else `uvm_error("STABILITY", "Random stability violated");
  assert(item1.pacing_mode == item2.pacing_mode)
    else `uvm_error("STABILITY", "Random stability violated");
endtask
```

## 6. Constraint Solver Debugging

### 6.1 Failed Randomization Debug

```systemverilog
class debug_constraint_seq extends uvm_sequence #(cardiac_stimulus);
  `uvm_object_utils(debug_constraint_seq)

  virtual task body();
    cardiac_stimulus item;
    item = cardiac_stimulus::type_id::create("item");

    if (!item.randomize()) begin
      `uvm_error("RAND_DEBUG", "Randomization failed")
      // Print solver constraints
      item.print();
      // Try to solve incrementally
      item.randomize(heart_rate_bpm);
      item.randomize(pacing_mode);
      item.randomize(pulse_amplitude);
    end
  endtask
endclass
```

### 6.2 Constraint Coverage

```systemverilog
// Track which constraint combinations are exercised
class constraint_coverage extends uvm_subscriber #(cardiac_stimulus);
  `uvm_component_utils(constraint_coverage)

  covergroup constraint_cg;
    option.per_instance = 1;

    mode_x_rate: coverpoint item.pacing_mode X item.heart_rate_bpm {
      bins vvi_brady = (4'h6, [30:59]);
      bins vvi_normal = (4'h6, [60:100]);
      bins vvi_tachy = (4'h6, [101:200]);
      bins ddd_normal = (4'hD, [60:100]);
    }

    fault_x_mode: coverpoint item.fault_inject X item.pacing_mode {
      bins fault_vvi = (1, 4'h6);
      bins fault_ddd = (1, 4'hD);
      bins normal_vvi = (0, 4'h6);
    }

    battery_x_mode: coverpoint item.battery_level X item.pacing_mode {
      bins low_battery_vvi = ([0:50], 4'h6);
      bins normal_battery_vvi = ([150:255], 4'h6);
    }
  endgroup

  function new(string name = "constraint_coverage", uvm_component parent);
    super.new(name, parent);
    constraint_cg = new();
  endfunction

  virtual function void write(cardiac_stimulus t);
    item = t;
    constraint_cg.sample();
  endfunction
endclass
```

## 7. Constrained-Random Test Suites

### 7.1 Test Configuration

```systemverilog
class cr_test_config extends uvm_object;
  `uvm_object_utils(cr_test_config)

  int num_transactions = 10000;
  int max_iterations = 100000;
  real coverage_goal = 95.0;
  int seed = 0;
  bit enable_coverage = 1;
  bit enable_scoreboard = 1;

  function new(string name = "cr_test_config");
    super.new(name);
  endfunction
endclass
```

### 7.2 Constrained-Random Test

```systemverilog
class cr_pacemaker_test extends pacemaker_base_test;
  `uvm_component_utils(cr_pacemaker_test)

  cr_test_config cr_cfg;

  function new(string name = "cr_pacemaker_test", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    cr_cfg = cr_test_config::type_id::create("cr_cfg");
    uvm_config_db#(cr_test_config)::set(this, "*", "cr_cfg", cr_cfg);
  endfunction

  virtual task run_phase(uvm_phase phase);
    scenario_random_seq seq;
    phase.raise_objection(this);

    seq = scenario_random_seq::type_id::create("seq");
    repeat (cr_cfg.num_transactions / 500) begin
      seq.start(env.agent.sqr);
    end

    #100_000; // Drain time
    phase.drop_objection(this);
  endtask
endclass
```

## 8. Summary

Constrained-random testing for the iPACE-CHIP pacemaker provides:

| Technique | Application | Benefit |
|-----------|-------------|---------|
| Weighted distribution | Scenario selection | Realistic stimulus |
| Inline constraints | Targeted testing | Specific scenarios |
| Soft constraints | Preference with flexibility | Natural distributions |
| Implication constraints | Mode-specific rules | Legal combinations |
| Seed control | Reproducibility | Debug efficiency |
| Constraint coverage | Gap identification | Closure analysis |

Key CRT benefits:
- **Automatic exploration** of design space
- **Reproducible** with seed control
- **Constraint-driven** for legal stimulus
- **Coverage-guided** for closure
- **Scalable** to large parameter spaces
