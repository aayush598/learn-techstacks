# Sequences and Sequencers for iPACE-CHIP Pacemaker

## 1. Introduction

UVM sequences and sequencers form the stimulus generation backbone of the verification environment. Sequences define ordered collections of sequence items that exercise specific DUT behaviors, while sequencers arbitrate among competing sequences and manage handshake with drivers.

For the iPACE-CHIP pacemaker, sequences model real cardiac events, fault conditions, configuration transitions, and edge cases that challenge the pacing algorithm.

## 2. Sequence Item Architecture

### 2.1 Base Sequence Item

```systemverilog
class pacemaker_base_item extends uvm_sequence_item;
  `uvm_object_utils(pacemaker_base_item)

  typedef enum {
    NORMAL_BEAT,
    PREMATURE_BEAT,
    SENSE_EVENT,
    PACE_EVENT,
    INHIBIT_EVENT,
    BATTERY_ALERT,
    LEAD_IMPEDANCE_ALERT,
    MODE_SWITCH,
    RESET_EVENT
  } item_type_e;

  rand item_type_e item_type;
  rand int unsigned delay_before;
  rand int unsigned duration;
  bit                is_response;
  time               timestamp;

  constraint c_reasonable_delay {
    delay_before inside {[0:50]};
  }

  constraint c_reasonable_duration {
    duration inside {[1:100]};
  }

  function new(string name = "pacemaker_base_item");
    super.new(name);
  endfunction

  virtual function string convert2string();
    return $sformatf("[%s] delay=%0d dur=%0d ts=%0t",
      item_type.name(), delay_before, duration, timestamp);
  endfunction
endclass
```

### 2.2 Cardiac Event Sequence Item

```systemverilog
class cardiac_event_item extends pacemaker_base_item;
  `uvm_object_utils(cardiac_event_item)

  typedef enum {
    NORMAL_SINUS,
    TACHYCARDIA,
    BRADYCARDIA,
    AFIB,
    VTACH,
    VFIB,
    ASYSTOLE,
    PVC
  } cardiac_rhythm_e;

  rand cardiac_rhythm_e rhythm;
  rand int unsigned      heart_rate_bpm;
  rand bit [7:0]         sense_threshold;
  rand bit               atrial_event;
  rand bit               ventricular_event;

  constraint c_heart_rate {
    heart_rate_bpm inside {[30:200]};
    if (rhythm == TACHYCARDIA) heart_rate_bpm inside {[100:200]};
    if (rhythm == BRADYCARDIA) heart_rate_bpm inside {[30:59]};
    if (rhythm == NORMAL_SINUS) heart_rate_bpm inside {[60, 100]};
  }

  constraint c_rhythm_validity {
    rhythm != VFIB; // VFIB not directly stimulable
  }

  function new(string name = "cardiac_event_item");
    super.new(name);
    item_type = SENSE_EVENT;
  endfunction

  virtual function string convert2string();
    return $sformatf("rhythm=%s HR=%0d atrial=%b ventricular=%b",
      rhythm.name(), heart_rate_bpm, atrial_event, ventricular_event);
  endfunction
endclass
```

## 3. Sequencer Implementation

### 3.1 Pacemaker Sequencer

```systemverilog
class pacemaker_sequencer extends uvm_sequencer #(pacemaker_base_item);
  `uvm_component_utils(pacemaker_sequencer)

  // Virtual sequence arbitration port
  uvm_analysis_export #(pacemaker_base_item) seq_analysis_export;

  // Tracking active sequences
  int active_seq_count = 0;

  function new(string name = "pacemaker_sequencer", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    seq_analysis_export = new("seq_analysis_export", this);
  endfunction

  virtual function void item_done();
    super.item_done();
    active_seq_count--;
  endfunction

  virtual task run_phase(uvm_phase phase);
    // Monitor for sequence errors during runtime
    forever begin
      @(negedge uvm_top.rst_n);
      `uvm_info("SQR", "Reset detected - clearing sequence queue", UVM_MEDIUM)
      stop_sequences();
      active_seq_count = 0;
    end
  endtask
endclass
```

### 3.2 APB Configuration Sequencer

```systemverilog
class apb_sequencer extends uvm_sequencer #(apb_seq_item);
  `uvm_component_utils(apb_sequencer)

  function new(string name = "apb_sequencer", uvm_component parent);
    super.new(name, parent);
  endfunction
endclass
```

## 4. Sequence Libraries

### 4.1 Basic Sequences

```systemverilog
// Simple single-beat sequence
class single_pacing_pulse_seq extends uvm_sequence #(pacemaker_base_item);
  `uvm_object_utils(single_pacing_pulse_seq)

  int unsigned rate_bpm = 72;

  function new(string name = "single_pacing_pulse_seq");
    super.new(name);
  endfunction

  virtual task body();
    cardiac_event_item item;
    item = cardiac_event_item::type_id::create("item");
    start_item(item);
    assert(item.randomize() with {
      rhythm == NORMAL_SINUS;
      heart_rate_bpm == local::rate_bpm;
      ventricular_event == 1;
    });
    finish_item(item);
  endtask
endclass

// Continuous pacing at fixed rate
class continuous_pacing_seq extends uvm_sequence #(pacemaker_base_item);
  `uvm_object_utils(continuous_pacing_seq)

  int unsigned rate_bpm = 72;
  int unsigned num_beats = 10;

  function new(string name = "continuous_pacing_seq");
    super.new(name);
  endfunction

  virtual task body();
    cardiac_event_item item;
    int beat_interval_ms;

    beat_interval_ms = 60000 / rate_bpm;
    repeat (num_beats) begin
      item = cardiac_event_item::type_id::create("item");
      start_item(item);
      assert(item.randomize() with {
        rhythm == BRADYCARDIA;
        heart_rate_bpm < 40;
        ventricular_event == 0;
        delay_before == beat_interval_ms;
      });
      finish_item(item);
    end
  endtask
endclass
```

### 4.2 Fault Injection Sequences

```systemverilog
class lead_fault_injection_seq extends uvm_sequence #(pacemaker_base_item);
  `uvm_object_utils(lead_fault_injection_seq)

  int unsigned fault_delay_ms = 500;
  int unsigned fault_duration_ms = 100;

  function new(string name = "lead_fault_injection_seq");
    super.new(name);
  endfunction

  virtual task body();
    pacemaker_base_item item;

    // Normal operation for a while
    repeat (5) begin
      item = pacemaker_base_item::type_id::create("item");
      start_item(item);
      assert(item.randomize() with {
        item_type == SENSE_EVENT;
        delay_before == 100;
      });
      finish_item(item);
    end

    // Inject lead fault
    item = pacemaker_base_item::type_id::create("item");
    start_item(item);
    assert(item.randomize() with {
      item_type == LEAD_IMPEDANCE_ALERT;
      delay_before == fault_delay_ms;
      duration == fault_duration_ms;
    });
    finish_item(item);

    // Resume normal operation after fault clears
    repeat (5) begin
      item = pacemaker_base_item::type_id::create("item");
      start_item(item);
      assert(item.randomize() with {
        item_type == SENSE_EVENT;
        delay_before == 100;
      });
      finish_item(item);
    end
  endtask
endclass

class battery_depletion_seq extends uvm_sequence #(pacemaker_base_item);
  `uvm_object_utils(battery_depletion_seq)

  function new(string name = "battery_depletion_seq");
    super.new(name);
  endfunction

  virtual task body();
    pacemaker_base_item item;
    int unsigned levels[5] = '{200, 150, 100, 50, 20};

    foreach (levels[i]) begin
      item = pacemaker_base_item::type_id::create("item");
      start_item(item);
      assert(item.randomize() with {
        item_type == BATTERY_ALERT;
        delay_before == 200;
        duration == levels[i];
      });
      finish_item(item);
    end
  endtask
endclass
```

### 4.3 Mode Transition Sequences

```systemverilog
class mode_switch_seq extends uvm_sequence #(pacemaker_base_item);
  `uvm_object_utils(mode_switch_seq)

  typedef enum {
    MODE_AAI_TO_VVI,
    MODE_VVI_TO_DDD,
    MODE_DDD_TO_AOO,
    MODE_VOO_TO_VVI
  } switch_type_e;

  rand switch_type_e switch_type;

  function new(string name = "mode_switch_seq");
    super.new(name);
  endfunction

  virtual task body();
    pacemaker_base_item item;

    // Pre-switch normal operation
    repeat (3) begin
      item = pacemaker_base_item::type_id::create("item");
      start_item(item);
      assert(item.randomize() with { item_type == NORMAL_BEAT; });
      finish_item(item);
    end

    // Issue mode switch command
    item = pacemaker_base_item::type_id::create("item");
    start_item(item);
    assert(item.randomize() with {
      item_type == MODE_SWITCH;
      delay_before == 10;
      duration == switch_type;
    });
    finish_item(item);

    // Post-switch verification beats
    repeat (5) begin
      item = pacemaker_base_item::type_id::create("item");
      start_item(item);
      assert(item.randomize() with { item_type == SENSE_EVENT; });
      finish_item(item);
    end
  endtask
endclass
```

## 5. Virtual Sequences

### 5.1 Multi-Agent Virtual Sequence

```systemverilog
class pacemaker_virtual_seq extends uvm_sequence;
  `uvm_object_utils(pacemaker_virtual_seq)

  pacemaker_sequencer  pm_sqr;
  apb_sequencer        apb_sqr;
  timer_sequencer      tmr_sqr;

  function new(string name = "pacemaker_virtual_seq");
    super.new(name);
  endfunction

  virtual task body();
    fork
      // Main cardiac pacing stimulus
      begin
        cardiac_pacing_sub_seq cardiac_seq;
        cardiac_seq = cardiac_pacing_sub_seq::type_id::create("cardiac_seq");
        cardiac_seq.start(pm_sqr);
      end

      // Configuration writes via APB
      begin
        apb_config_sub_seq config_seq;
        config_seq = apb_config_sub_seq::type_id::create("config_seq");
        config_seq.start(apb_sqr);
      end

      // Timer tick generation
      begin
        timer_tick_sub_seq timer_seq;
        timer_seq = timer_tick_sub_seq::type_id::create("timer_seq");
        timer_seq.start(tmr_sqr);
      end
    join
  endtask
endclass
```

### 5.2 Scenario Virtual Sequence

```systemverilog
class full_scenario_virtual_seq extends uvm_sequence;
  `uvm_object_utils(full_scenario_virtual_seq)

  pacemaker_sequencer pm_sqr;
  apb_sequencer       apb_sqr;

  function new(string name = "full_scenario_virtual_seq");
    super.new(name);
  endfunction

  virtual task body();
    config_pacemaker_seq config_seq;
    normal_pacing_seq    normal_seq;
    fault_inject_seq     fault_seq;
    recovery_check_seq   recovery_seq;

    // Phase 1: Configure pacemaker
    config_seq = config_pacemaker_seq::type_id::create("config_seq");
    config_seq.start(apb_sqr);

    // Phase 2: Normal operation
    normal_seq = normal_pacing_seq::type_id::create("normal_seq");
    normal_seq.num_beats = 50;
    normal_seq.start(pm_sqr);

    // Phase 3: Fault injection
    fault_seq = fault_inject_seq::type_id::create("fault_seq");
    fault_seq.start(pm_sqr);

    // Phase 4: Recovery verification
    recovery_seq = recovery_check_seq::type_id::create("recovery_seq");
    recovery_seq.start(pm_sqr);
  endtask
endclass
```

## 6. Sequence Execution Methods

### 6.1 Fork-Join Patterns

```systemverilog
class concurrent_fault_seq extends uvm_sequence #(pacemaker_base_item);
  `uvm_object_utils(concurrent_fault_seq)

  function new(string name = "concurrent_fault_seq");
    super.new(name);
  endfunction

  virtual task body();
    pacemaker_base_item item;

    fork
      // Thread 1: Continuous pacing
      begin
        repeat (20) begin
          item = pacemaker_base_item::type_id::create("item");
          start_item(item);
          assert(item.randomize() with { item_type == SENSE_EVENT; });
          finish_item(item);
        end
      end

      // Thread 2: Battery depletion
      begin
        #500; // Start after 500 time units
        item = pacemaker_base_item::type_id::create("item");
        start_item(item);
        assert(item.randomize() with { item_type == BATTERY_ALERT; });
        finish_item(item);
      end

      // Thread 3: Lead impedance variation
      begin
        #200;
        repeat (3) begin
          item = pacemaker_base_item::type_id::create("item");
          start_item(item);
          assert(item.randomize() with { item_type == LEAD_IMPEDANCE_ALERT; });
          finish_item(item);
        end
      end
    join
  endtask
endclass
```

### 6.2 Sequence with Callbacks

```systemverilog
class monitored_pacing_seq extends uvm_sequence #(pacemaker_base_item);
  `uvm_object_utils(monitored_pacing_seq)

  int beats_sent = 0;
  int beats_inhibited = 0;

  function new(string name = "monitored_pacing_seq");
    super.new(name);
  endfunction

  virtual task body();
    cardiac_event_item item;
    repeat (100) begin
      item = cardiac_event_item::type_id::create("item");
      start_item(item);
      assert(item.randomize());
      finish_item(item);
      beats_sent++;
      if (item.item_type == INHIBIT_EVENT)
        beats_inhibited++;
    end
    `uvm_info("SEQ", $sformatf(
      "Complete: %0d beats sent, %0d inhibited",
      beats_sent, beats_inhibited), UVM_LOW)
  endtask
endclass
```

## 7. Sequence Libraries and Reuse

### 7.1 Sequence Library Declaration

```systemverilog
class pacemaker_seq_lib extends uvm_sequence_library #(pacemaker_base_item);
  `uvm_object_utils(pacemaker_seq_lib)

  function new(string name = "pacemaker_seq_lib");
    super.new(name);
  endfunction

  virtual function void init_sequence();
    add_sequence(normal_beat_seq::get_type());
    add_sequence(premature_beat_seq::get_type());
    add_sequence(bradycardia_seq::get_type());
    add_sequence(tachycardia_seq::get_type());
    add_sequence(lead_fault_seq::get_type());
    add_sequence(battery_low_seq::get_type());
    add_sequence(mode_switch_seq::get_type());
    add_sequence(asystole_seq::get_type());
  endfunction
endclass
```

### 7.2 Generic Sequence Execution

```systemverilog
class random_pacing_test extends pacemaker_base_test;
  `uvm_component_utils(random_pacing_test)

  function new(string name = "random_pacing_test", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual task run_phase(uvm_phase phase);
    pacemaker_seq_lib seq_lib;
    phase.raise_objection(this);
    seq_lib = pacemaker_seq_lib::type_id::create("seq_lib");
    seq_lib.init_sequence();
    seq_lib.start(env.agent.sqr, null, -1, 0); // Random selection
    #200_000;
    phase.drop_objection(this);
  endtask
endclass
```

## 8. Sequencer Arbitration

### 8.1 Priority-Based Arbitration

```systemverilog
class priority_pacing_test extends pacemaker_base_test;
  `uvm_component_utils(priority_pacing_test)

  function new(string name = "priority_pacing_test", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual task run_phase(uvm_phase phase);
    normal_pacing_seq   normal_seq;
    emergency_seq       emerg_seq;
    phase.raise_objection(this);

    fork
      begin
        normal_seq = normal_pacing_seq::type_id::create("normal_seq");
        normal_seq.start(env.agent.sqr, null, -1, 100); // Low priority
      end
      begin
        #500;
        emerg_seq = emergency_seq::type_id::create("emerg_seq");
        emerg_seq.start(env.agent.sqr, null, -1, 0); // High priority
      end
    join

    #100_000;
    phase.drop_objection(this);
  endtask
endclass
```

## 9. Sequence Timing and Delay Management

### 9.1 Accurate Cardiac Timing

```systemverilog
class timed_heartbeats_seq extends uvm_sequence #(pacemaker_base_item);
  `uvm_object_utils(timed_heartbeats_seq)

  int unsigned target_bpm = 72;
  real         bpm_tolerance = 5.0;

  function new(string name = "timed_heartbeats_seq");
    super.new(name);
  endfunction

  virtual task body();
    cardiac_event_item item;
    real interval_ms;
    int  interval_cycles;
    int  clk_period_ps = 10000; // 100MHz clock

    interval_ms = 60000.0 / target_bpm;
    interval_cycles = int'(interval_ms * 1_000_000 / clk_period_ps);

    `uvm_info("SEQ", $sformatf(
      "Target BPM=%0d, interval=%.2fms, cycles=%0d",
      target_bpm, interval_ms, interval_cycles), UVM_LOW)

    repeat (20) begin
      item = cardiac_event_item::type_id::create("item");
      start_item(item);
      assert(item.randomize() with {
        item_type == SENSE_EVENT;
        delay_before == interval_cycles;
        rhythm == BRADYCARDIA;
        heart_rate_bpm < 40;
      });
      finish_item(item);
    end
  endtask
endclass
```

## 10. Response Handler Sequences

### 10.1 Response Collection

```systemverilog
class pacing_response_seq extends uvm_sequence #(pacemaker_base_item);
  `uvm_object_utils(pacing_response_seq)

  pacemaker_base_item rsp_item;

  function new(string name = "pacing_response_seq");
    super.new(name);
  endfunction

  virtual task body();
    pacemaker_base_item item;

    item = pacemaker_base_item::type_id::create("item");
    start_item(item);
    assert(item.randomize() with { item_type == SENSE_EVENT; });
    finish_item(item);

    // Get response from driver
    get_response(rsp_item);
    if (rsp_item != null)
      `uvm_info("SEQ", $sformatf("Got response: %s", rsp_item.convert2string()),
        UVM_LOW)
    else
      `uvm_warning("SEQ", "No response received from driver")
  endtask
endclass
```

## 11. Best Practices for Pacemaker Sequences

| Practice | Description |
|----------|-------------|
| Constraint layering | Use `with` blocks for test-specific constraints |
| Response handling | Always check driver responses in safety sequences |
| Timing accuracy | Model real cardiac intervals (600-1000ms) |
| Fault sequencing | Inject faults during active pacing for realism |
| Objection control | Use `#delay` drain time after last sequence item |
| Sequence macros | Use `uvm_do_with` for concise inline creation |
| Library reuse | Package common sequences in `uvm_sequence_library` |

## 12. Summary

Sequences and sequencers for the iPACE-CHIP pacemaker provide:

- **Layered sequence items** modeling cardiac events, faults, and configuration
- **Sequencer arbitration** with priority-based grant mechanisms
- **Virtual sequences** coordinating multi-agent stimulus
- **Fault injection sequences** for reliability testing
- **Timing-accurate sequences** matching real cardiac cycle intervals
- **Sequence libraries** enabling random test selection

The sequence infrastructure directly maps to the pacemaker's operational scenarios, enabling both directed and constrained-random verification strategies.
