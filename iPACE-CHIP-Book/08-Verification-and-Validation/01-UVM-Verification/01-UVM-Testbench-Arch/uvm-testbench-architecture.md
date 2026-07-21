# UVM Testbench Architecture for iPACE-CHIP Pacemaker

## 1. Introduction

The Universal Verification Methodology (UVM) provides a structured, reusable framework for verifying complex digital designs. For the iPACE-CHIP pacemaker ASIC, UVM is the primary verification methodology due to its industry-standard adoption, extensive library of components, and support for constrained-random stimulus generation.

This chapter covers the complete UVM testbench architecture tailored for pacemaker verification, including component hierarchies, configuration mechanisms, and interface abstraction layers.

## 2. UVM Component Hierarchy

### 2.1 Top-Level Testbench Structure

```
uvm_testbench
├── uvm_env
│   ├── pacemaker_agent_active (front-door)
│   │   ├── pacemaker_driver
│   │   ├── pacemaker_monitor
│   │   └── pacemaker_sequencer
│   ├── pacemaker_agent_passive (back-door)
│   │   └── pacemaker_monitor
│   ├── scoreboard
│   ├── coverage_collector
│   └── reference_model
├── apb_agent (configuration bus)
│   ├── apb_driver
│   ├── apb_monitor
│   └── apb_sequencer
├── uart_agent (telemetry interface)
│   ├── uart_driver
│   ├── uart_monitor
│   └── uart_sequencer
├── timer_agent (timer stimulus)
│   ├── timer_driver
│   └── timer_monitor
└── reset_agent
    ├── reset_driver
    └── reset_monitor
```

### 2.2 Core Agent Implementation

```systemverilog
class pacemaker_agent extends uvm_agent;
  `uvm_component_utils(pacemaker_agent)

  pacemaker_driver    drv;
  pacemaker_monitor   mon;
  pacemaker_sequencer sqr;
  pacemaker_agent_config cfg;

  function new(string name = "pacemaker_agent", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    if (!uvm_config_db#(pacemaker_agent_config)::get(this, "", "cfg", cfg))
      `uvm_fatal("NOCONFIG", "Agent config not found")

    mon = pacemaker_monitor::type_id::create("mon", this);
    if (cfg.is_active == UVM_ACTIVE) begin
      drv = pacemaker_driver::type_id::create("drv", this);
      sqr = pacemaker_sequencer::type_id::create("sqr", this);
    end
  endfunction

  virtual function void connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    if (cfg.is_active == UVM_ACTIVE)
      drv.seq_item_port.connect(sqr.seq_item_export);
  endfunction
endclass
```

## 3. Pacemaker Driver

### 3.1 Heart Signal Driver

The pacemaker driver translates sequence items into pin-level signal transitions on the DUT interfaces.

```systemverilog
class pacemaker_driver extends uvm_driver #(pacemaker_seq_item);
  `uvm_component_utils(pacemaker_driver)

  virtual pacemaker_if vif;
  pacemaker_agent_config cfg;

  function new(string name = "pacemaker_driver", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    if (!uvm_config_db#(virtual pacemaker_if)::get(this, "", "vif", vif))
      `uvm_fatal("NOVIF", "Virtual interface not found")
    if (!uvm_config_db#(pacemaker_agent_config)::get(this, "", "cfg", cfg))
      `uvm_fatal("NOCFG", "Agent config not found")
  endfunction

  virtual task run_phase(uvm_phase phase);
    pacemaker_seq_item item;
    forever begin
      seq_item_port.get_next_item(item);
      drive_item(item);
      seq_item_port.item_done();
    end
  endtask

  virtual task drive_item(pacemaker_seq_item item);
    case (item.signal_type)
      PACING_PULSE: begin
        @(posedge vif.clk);
        vif.sense_amp_out <= 1'b0;
        repeat(item.pulse_width) @(posedge vif.clk);
        vif.sense_amp_out <= 1'b1;
        repeat(item.refractory_period) @(posedge vif.clk);
      end
      INHIBIT_SIGNAL: begin
        vif.inhibit <= 1'b1;
        repeat(item.inhibit_duration) @(posedge vif.clk);
        vif.inhibit <= 1'b0;
      end
      BATTERY_LOW: begin
        vif.batt_monitor <= item.battery_level;
      end
      LEAD_FAULT: begin
        vif.lead_impedance <= item.impedance_value;
      end
    endcase
  endtask
endclass
```

### 3.2 Sequence Item Definition

```systemverilog
class pacemaker_seq_item extends uvm_sequence_item;
  `uvm_object_utils(pacemaker_seq_item)

  typedef enum {
    PACING_PULSE,
    INHIBIT_SIGNAL,
    BATTERY_LOW,
    LEAD_FAULT
  } signal_type_e;

  rand signal_type_e signal_type;
  rand int           pulse_width;
  rand int           refractory_period;
  rand bit           inhibit;
  rand int           inhibit_duration;
  rand bit [7:0]     battery_level;
  rand bit [15:0]    impedance_value;

  constraint c_valid_pulse {
    pulse_width inside {[1:50]};
    refractory_period inside {[10:100]};
  }

  constraint c_valid_battery {
    battery_level inside {[0:255]};
  }

  constraint c_valid_impedance {
    impedance_value inside {[0:16'hFFFF]};
  }

  function new(string name = "pacemaker_seq_item");
    super.new(name);
  endfunction

  virtual function string convert2string();
    return $sformatf("type=%s pulse_w=%0d refrac=%0d batt=%0d Z=%0d",
      signal_type.name(), pulse_width, refractory_period,
      battery_level, impedance_value);
  endfunction
endclass
```

## 4. Pacemaker Monitor

### 4.1 Active Monitor

```systemverilog
class pacemaker_monitor extends uvm_monitor;
  `uvm_component_utils(pacemaker_monitor)

  virtual pacemaker_if vif;
  uvm_analysis_port #(pacemaker_seq_item) ap;
  pacemaker_agent_config cfg;

  covergroup pacemaker_cg;
    option.per_instance = 1;
    signal_type_cp: coverpoint item.signal_type {
      bins pacing     = {PACING_PULSE};
      bins inhibit    = {INHIBIT_SIGNAL};
      bins batt_low   = {BATTERY_LOW};
      bins lead_fault = {LEAD_FAULT};
    }
    pulse_width_cp: coverpoint item.pulse_width {
      bins short  = {[1:10]};
      bins medium = {[11:30]};
      bins long   = {[31:50]};
    }
    cross signal_type_cp, pulse_width_cp;
  endgroup

  function new(string name = "pacemaker_monitor", uvm_component parent);
    super.new(name, parent);
    pacemaker_cg = new();
  endfunction

  virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    if (!uvm_config_db#(virtual pacemaker_if)::get(this, "", "vif", vif))
      `uvm_fatal("NOVIF", "Virtual interface not found")
    ap = new("ap", this);
  endfunction

  virtual task run_phase(uvm_phase phase);
    pacemaker_seq_item item;
    forever begin
      @(posedge vif.clk);
      if (vif.pacing_detected) begin
        item = pacemaker_seq_item::type_id::create("item");
        item.signal_type = PACING_PULSE;
        item.pulse_width = vif.pulse_width_mon;
        ap.write(item);
        pacemaker_cg.sample();
      end
    end
  endtask
endclass
```

## 5. Configuration Database Usage

### 5.1 Agent Configuration

```systemverilog
class pacemaker_agent_config extends uvm_object;
  `uvm_object_utils(pacemaker_agent_config)

  uvm_active_passive_enum is_active = UVM_ACTIVE;
  bit has_coverage = 1;
  bit has_scoreboard = 1;
  int max_outstanding = 4;

  // Protocol-specific configuration
  bit [3:0]  pacing_mode = 4'b0001;    // VVI mode default
  bit [7:0]  lower_rate_limit = 8'd60; // 60 ppm
  bit [7:0]  upper_rate_limit = 8'd120;
  bit [7:0]  pulse_amplitude = 8'd50;  // 5.0V
  bit [7:0]  pulse_width_cfg = 8'd5;   // 0.5ms
  bit [7:0]  ref_period = 8'd30;       // 300ms

  function new(string name = "pacemaker_agent_config");
    super.new(name);
  endfunction
endclass
```

### 5.2 Environment Configuration

```systemverilog
class pacemaker_env_config extends uvm_object;
  `uvm_object_utils(pacemaker_env_config)

  pacemaker_agent_config agent_cfg;
  apb_agent_config       apb_cfg;
  uart_agent_config      uart_cfg;
  timer_agent_config     timer_cfg;

  bit enable_scoreboard = 1;
  bit enable_coverage   = 1;
  bit enable_reference_model = 1;

  function new(string name = "pacemaker_env_config");
    super.new(name);
  endfunction
endclass
```

## 6. Virtual Interface Declarations

### 6.1 Interface Definition

```systemverilog
interface pacemaker_if(input logic clk, input logic rst_n);
  // Sense amplifier input (from heart)
  logic        sense_amp_out;
  logic        inhibit;

  // Pacing output (to heart)
  logic        pace_pulse;
  logic [7:0]  pace_amplitude;

  // Monitoring signals
  logic        pacing_detected;
  int          pulse_width_mon;
  logic [7:0]  battery_level;
  logic [15:0] lead_impedance;

  // Clocking block for driver
  clocking drv_cb @(posedge clk);
    default input #1 output #1;
    output sense_amp_out;
    output inhibit;
    output battery_level;
    output lead_impedance;
    input  pace_pulse;
  endclocking

  // Clocking block for monitor
  clocking mon_cb @(posedge clk);
    default input #1;
    input sense_amp_out;
    input inhibit;
    input pace_pulse;
    input pace_amplitude;
    input pacing_detected;
    input pulse_width_mon;
    input battery_level;
    input lead_impedance;
  endclocking

  modport DRV  clocking drv_cb  input clk, rst_n;
  modport MON  clocking mon_cb  input clk, rst_n;
  modport DUT  input clk, rst_n, sense_amp_out, inhibit,
               output pace_pulse, pace_amplitude;
endinterface
```

## 7. Test Class Structure

### 7.1 Base Test

```systemverilog
class pacemaker_base_test extends uvm_test;
  `uvm_component_utils(pacemaker_base_test)

  pacemaker_env        env;
  pacemaker_env_config env_cfg;

  function new(string name = "pacemaker_base_test", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    env_cfg = pacemaker_env_config::type_id::create("env_cfg");
    env_cfg.agent_cfg = pacemaker_agent_config::type_id::create("agent_cfg");
    uvm_config_db#(pacemaker_env_config)::set(this, "*", "env_cfg", env_cfg);
    env = pacemaker_env::type_id::create("env", this);
  endfunction

  virtual function void report_phase(uvm_phase phase);
    uvm_report_server svr;
    super.report_phase(phase);
    svr = uvm_report_server::get_server();
    if (svr.get_severity_count(UVM_FATAL) + svr.get_severity_count(UVM_ERROR) > 0)
      `uvm_info("RESULT", "TEST FAILED", UVM_NONE)
    else
      `uvm_info("RESULT", "TEST PASSED", UVM_NONE)
  endfunction
endclass
```

### 7.2 Directed Test Examples

```systemverilog
class pacemaker_vvi_mode_test extends pacemaker_base_test;
  `uvm_component_utils(pacemaker_vvi_mode_test)

  function new(string name = "pacemaker_vvi_mode_test", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    env_cfg.agent_cfg.pacing_mode = 4'b0110; // VVI mode
  endfunction

  virtual task run_phase(uvm_phase phase);
    vvi_mode_sequence seq;
    phase.raise_objection(this);
    seq = vvi_mode_sequence::type_id::create("seq");
    seq.start(env.agent.sqr);
    #100_000; // Wait 100ms simulation time
    phase.drop_objection(this);
  endtask
endclass

class pacemaker_battery_monitor_test extends pacemaker_base_test;
  `uvm_component_utils(pacemaker_battery_monitor_test)

  function new(string name = "pacemaker_battery_monitor_test", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual task run_phase(uvm_phase phase);
    battery_depletion_seq seq;
    phase.raise_objection(this);
    seq = battery_depletion_seq::type_id::create("seq");
    seq.start(env.agent.sqr);
    #500_000;
    phase.drop_objection(this);
  endtask
endclass
```

## 8. Environment Build-Out

### 8.1 UVM Environment

```systemverilog
class pacemaker_env extends uvm_env;
  `uvm_component_utils(pacemaker_env)

  pacemaker_agent          agent;
  pacemaker_scoreboard     scb;
  pacemaker_coverage       cov;
  pacemaker_ref_model       ref_model;
  apb_agent                apb_agt;
  uart_agent               uart_agt;
  timer_agent              timer_agt;
  pacemaker_env_config     cfg;

  function new(string name = "pacemaker_env", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    if (!uvm_config_db#(pacemaker_env_config)::get(this, "", "env_cfg", cfg))
      `uvm_fatal("NOCONFIG", "Env config not found")

    agent = pacemaker_agent::type_id::create("agent", this);
    uvm_config_db#(pacemaker_agent_config)::set(this, "agent", "cfg", cfg.agent_cfg);

    if (cfg.enable_scoreboard)
      scb = pacemaker_scoreboard::type_id::create("scb", this);
    if (cfg.enable_coverage)
      cov = pacemaker_coverage::type_id::create("cov", this);
    if (cfg.enable_reference_model)
      ref_model = pacemaker_ref_model::type_id::create("ref_model", this);

    apb_agt  = apb_agent::type_id::create("apb_agt", this);
    uart_agt = uart_agent::type_id::create("uart_agt", this);
    timer_agt = timer_agent::type_id::create("timer_agt", this);
  endfunction

  virtual function void connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    agent.mon.ap.connect(scb.ap_imp);
    agent.mon.ap.connect(cov.analysis_export);
    if (cfg.enable_reference_model)
      agent.mon.ap.connect(ref_model.analysis_export);
  endfunction
endclass
```

## 9. Phasing and Objection Mechanism

### 9.1 Phase Execution Flow

```
build_phase          → Create components, get config
connect_phase        → Connect analysis ports
end_of_elaboration_phase → Debug component topology
start_of_simulation_phase → Display topology, set defaults
run_phase            → Main stimulus/checking
extract_phase        → Gather results
check_phase          → Verify final state
report_phase         → Display pass/fail
final_phase          → Cleanup
```

### 9.2 Objection Control

```systemverilog
class pacemaker_smoke_test extends pacemaker_base_test;
  `uvm_component_utils(pacemaker_smoke_test)

  function new(string name = "pacemaker_smoke_test", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual task run_phase(uvm_phase phase);
    smoke_sequence seq;
    phase.raise_objection(this, "smoke_test_start");
    // Start timeout watchdog
    fork
      begin
        seq = smoke_sequence::type_id::create("seq");
        seq.start(env.agent.sqr);
      end
      begin
        #1_000_000; // 1 second timeout
        `uvm_warning("TIMEOUT", "Test timed out")
      end
    join_any
    disable fork;
    #10_000; // Allow drain time
    phase.drop_objection(this, "smoke_test_done");
  endtask
endclass
```

## 10. Factory Overrides

### 10.1 Component Override Mechanism

```systemverilog
// Override the default driver with a specialized one
factory.set_type_override_by_type(
  pacemaker_driver::get_type(),
  pacemaker_safety_driver::get_type()
);

// Override at a specific hierarchy path
factory.set_inst_override_by_type(
  pacemaker_monitor::get_type(),
  pacemaker_detailed_monitor::get_type(),
  "*.env.agent.mon"
);
```

### 10.2 Using the Factory in Tests

```systemverilog
class pacemaker_safety_test extends pacemaker_base_test;
  `uvm_component_utils(pacemaker_safety_test)

  function new(string name = "pacemaker_safety_test", uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual function void build_phase(uvm_phase phase);
    // Override the default sequence item with a safety-critical variant
    pacemaker_safety_seq_item::type_id::set_type_override(
      pacemaker_seq_item::get_type()
    );
    super.build_phase(phase);
  endfunction
endclass
```

## 11. TLM Port Connections

### 11.1 Analysis Port Wiring

```systemverilog
// In environment connect_phase
agent.mon.ap.connect(scb-heart_analysis_imp);
agent.mon.ap.connect(cov.analysis_export);
agent.mon.ap.connect(ref_model.input_export);

// TLM FIFO for decoupling
uvm_tlm_fifo #(pacemaker_seq_item) fifo1;
fifo1 = new("fifo1", this);
agent.mon.ap.connect(fifo1.put_export);
scb.ap_imp.connect(fifo1.get_export);
```

## 12. Summary

The UVM testbench architecture for iPACE-CHIP provides:

- **Modular agent structure** for each DUT interface
- **Configuration database** for hierarchical parameter propagation
- **Virtual interface abstraction** separating protocol from signal-level details
- **Factory mechanism** for runtime component and sequence overrides
- **TLM analysis ports** for scoreboard and coverage connectivity
- **Phased objection control** for clean test completion

The architecture scales from directed smoke tests to full constrained-random coverage-driven verification campaigns.

| Component | Purpose | Reuse Level |
|-----------|---------|-------------|
| pacemaker_agent | DUT interface abstraction | High |
| pacemaker_driver | Stimulus translation | Medium |
| pacemaker_monitor | Output sampling | High |
| pacemaker_scoreboard | Protocol checking | Medium |
| pacemaker_coverage | Functional coverage | High |
| pacemaker_ref_model | Expected value generation | Low |
| pacemaker_env_config | Hierarchical configuration | High |
