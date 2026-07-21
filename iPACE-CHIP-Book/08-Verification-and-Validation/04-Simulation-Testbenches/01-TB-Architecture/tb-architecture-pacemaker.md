# Testbench Architecture for iPACE-CHIP Pacemaker

## 1. Introduction

The simulation testbench architecture for the iPACE-CHIP pacemaker provides a comprehensive verification environment that models the cardiac system, power supply, communication interfaces, and external sensors. This chapter details the complete testbench structure, DUT instantiation, stimulus generation, and result checking.

## 2. Top-Level Testbench Structure

### 2.1 Testbench Hierarchy

```
tb_pacemaker_top
├── Clock Generator (100MHz)
├── Reset Generator
├── DUT (pacemaker_top)
│   ├── Pacing Controller
│   ├── Timing Engine
│   ├── Safety Monitor
│   ├── Configuration Registers
│   ├── APB Interface
│   ├── UART Transmitter
│   └── Battery Monitor
├── Heart Model
│   ├── Sense Amplifier Model
│   ├── Impedance Model
│   └── Intrinsic Rhythm Generator
├── Power Supply Model
│   ├── Battery Model (depleting)
│   └── Voltage Regulator Model
├── APB Master Agent
├── UART Monitor
├── Telemetry Receiver
├── Scoreboard
├── Coverage Collector
└── Waveform Dumper
```

### 2.2 Top-Level Testbench Module

```systemverilog
`timescale 1ns/1ps

module tb_pacemaker_top;

  // Clock and reset
  logic clk;
  logic rst_n;

  // DUT signals
  logic        sense_amp_out;
  logic        inhibit;
  logic        pace_pulse;
  logic [7:0]  pace_amplitude;
  logic [15:0] lead_impedance;
  logic [7:0]  battery_voltage;

  // APB interface
  logic        apb_psel;
  logic        apb_pen;
  logic        apb_pwrite;
  logic [7:0]  apb_paddr;
  logic [31:0] apb_pwdata;
  logic [31:0] apb_prdata;
  logic        apb_pready;

  // UART
  logic        uart_tx;
  logic        uart_rx;

  // Control signals
  logic        fault_flag;
  logic        battery_alert;
  logic [3:0]  alert_code;

  // Clock generation: 100MHz
  initial begin
    clk = 0;
    forever #5 clk = ~clk; // 10ns period = 100MHz
  end

  // Reset generation
  initial begin
    rst_n = 0;
    #100;
    rst_n = 1;
  end

  // DUT instantiation
  pacemaker_top u_dut (
    .clk                (clk),
    .rst_n              (rst_n),
    .sense_amp_out      (sense_amp_out),
    .inhibit            (inhibit),
    .pace_pulse         (pace_pulse),
    .pace_amplitude     (pace_amplitude),
    .lead_impedance     (lead_impedance),
    .battery_voltage    (battery_voltage),
    .apb_psel           (apb_psel),
    .apb_pen            (apb_pen),
    .apb_pwrite         (apb_pwrite),
    .apb_paddr          (apb_paddr),
    .apb_pwdata         (apb_pwdata),
    .apb_prdata         (apb_prdata),
    .apb_pready         (apb_pready),
    .uart_tx            (uart_tx),
    .uart_rx            (uart_rx),
    .fault_flag         (fault_flag),
    .battery_alert      (battery_alert),
    .alert_code         (alert_code)
  );

  // Heart model instantiation
  heart_model u_heart (
    .clk                (clk),
    .rst_n              (rst_n),
    .pace_pulse         (pace_pulse),
    .sense_amp_out      (sense_amp_out),
    .inhibit            (inhibit),
    .lead_impedance     (lead_impedance),
    .rhythm_type        (rhythm_type),
    .heart_rate_bpm     (heart_rate_bpm)
  );

  // Battery model
  battery_model u_battery (
    .clk                (clk),
    .rst_n              (rst_n),
    .battery_voltage    (battery_voltage),
    .depletion_rate     (depletion_rate),
    .initial_charge     (initial_charge)
  );

  // APB master
  apb_master u_apb (
    .clk                (clk),
    .rst_n              (rst_n),
    .psel               (apb_psel),
    .pen                (apb_pen),
    .pwrite             (apb_pwrite),
    .paddr              (apb_paddr),
    .pwdata             (apb_pwdata),
    .prdata             (apb_prdata),
    .pready             (apb_pready)
  );

  // Scoreboard
  pacemaker_scoreboard u_scb (
    .clk                (clk),
    .rst_n              (rst_n),
    .pace_pulse         (pace_pulse),
    .pace_amplitude     (pace_amplitude),
    .fault_flag         (fault_flag),
    .battery_alert      (battery_alert)
  );

  // Coverage collector
  pacemaker_coverage u_cov (
    .clk                (clk),
    .rst_n              (rst_n),
    .pace_pulse         (pace_pulse),
    .sense_amp_out      (sense_amp_out),
    .inhibit            (inhibit),
    .fault_flag         (fault_flag),
    .battery_alert      (battery_alert),
    .pace_amplitude     (pace_amplitude)
  );

  // Waveform dump
  initial begin
    $dumpfile("pacemaker.vcd");
    $dumpvars(0, tb_pacemaker_top);
  end

  // Timeout watchdog
  initial begin
    #10_000_000; // 10ms timeout
    `uvm_error("TIMEOUT", "Testbench timeout")
    $finish;
  end

endmodule
```

## 3. Heart Model

### 3.1 Cardiac Rhythm Generator

```systemverilog
module heart_model (
  input  logic        clk,
  input  logic        rst_n,
  input  logic        pace_pulse,
  output logic        sense_amp_out,
  output logic        inhibit,
  output logic [15:0] lead_impedance,
  input  logic [3:0]  rhythm_type,
  input  logic [7:0]  heart_rate_bpm
);

  typedef enum logic [3:0] {
    NORMAL_SINUS,
    BRADYCARDIA,
    TACHYCARDIA,
    AFIB,
    VTACH,
    ASYSTOLE,
    PVC,
    NO_INTRINSIC
  } rhythm_e;

  rhythm_e current_rhythm;
  int      intrinsic_interval_ms;
  int      sense_counter;
  bit      sense_active;

  assign current_rhythm = rhythm_e'(rhythm_type);

  // Calculate intrinsic interval from BPM
  always_comb begin
    if (heart_rate_bpm > 0)
      intrinsic_interval_ms = 60000 / heart_rate_bpm;
    else
      intrinsic_interval_ms = 10000; // 10 seconds for asystole
  end

  // Generate intrinsic beats
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      sense_counter <= 0;
      sense_active <= 0;
    end else begin
      if (current_rhythm == ASYSTOLE || current_rhythm == NO_INTRINSIC) begin
        sense_active <= 0;
        sense_counter <= 0;
      end else begin
        sense_counter <= sense_counter + 1;
        if (sense_counter >= intrinsic_interval_ms * 100_000) begin // Convert to cycles
          sense_active <= 1;
          sense_counter <= 0;
        end else if (sense_counter >= 100_000) begin // 1ms pulse width
          sense_active <= 0;
        end
      end
    end
  end

  // Pace response: when paced, generate sense after refractory
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n)
      inhibit <= 0;
    else if (pace_pulse)
      inhibit <= 1;
    else if (sense_active)
      inhibit <= 0;
  end

  assign sense_amp_out = sense_active;

  // Lead impedance model
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n)
      lead_impedance <= 16'd500; // Nominal 500 ohms
    else
      lead_impedance <= lead_impedance; // Constant unless fault injected
  end

endmodule
```

## 4. Battery Model

### 4.1 Depleting Battery

```systemverilog
module battery_model (
  input  logic        clk,
  input  logic        rst_n,
  output logic [7:0]  battery_voltage,
  input  logic [7:0]  depletion_rate,
  input  logic [7:0]  initial_charge
);

  logic [15:0] charge_remaining;
  logic [31:0] cycle_count;

  assign battery_voltage = charge_remaining[15:8];

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      charge_remaining <= {initial_charge, 8'd0};
      cycle_count <= 0;
    end else begin
      cycle_count <= cycle_count + 1;
      if (cycle_count % 1000000 == 0 && charge_remaining > 0) begin
        charge_remaining <= charge_remaining - {8'd0, depletion_rate};
      end
    end
  end

endmodule
```

## 5. APB Master Model

### 5.1 APB Transaction Generator

```systemverilog
module apb_master (
  input  logic        clk,
  input  logic        rst_n,
  output logic        psel,
  output logic        pen,
  output logic        pwrite,
  output logic [7:0]  paddr,
  output logic [31:0] pwdata,
  input  logic [31:0] prdata,
  input  logic        pready
);

  typedef enum logic [1:0] {
    IDLE,
    SETUP,
    ACCESS
  } apb_state_t;

  apb_state_t state;

  // Write task
  task write_reg(input logic [7:0] addr, input logic [31:0] data);
    @(posedge clk);
    state <= SETUP;
    psel <= 1;
    pwrite <= 1;
    paddr <= addr;
    pwdata <= data;
    @(posedge clk);
    state <= ACCESS;
    pen <= 1;
    @(posedge clk);
    while (!pready) @(posedge clk);
    pen <= 0;
    psel <= 0;
    state <= IDLE;
  endtask

  // Read task
  task read_reg(input logic [7:0] addr, output logic [31:0] data);
    @(posedge clk);
    state <= SETUP;
    psel <= 1;
    pwrite <= 0;
    paddr <= addr;
    @(posedge clk);
    state <= ACCESS;
    pen <= 1;
    @(posedge clk);
    while (!pready) @(posedge clk);
    data = prdata;
    pen <= 0;
    psel <= 0;
    state <= IDLE;
  endtask

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      psel <= 0;
      pen <= 0;
      pwrite <= 0;
      paddr <= 0;
      pwdata <= 0;
      state <= IDLE;
    end
  end

endmodule
```

## 6. Test Scenarios

### 6.1 Smoke Test

```systemverilog
program smoke_test;
  initial begin
    // Wait for reset
    @(posedge rst_n);
    #1000;

    // Configure pacemaker
    u_apb.write_reg(8'h00, 32'h0000_0006); // VVI mode
    u_apb.write_reg(8'h04, 32'h0000_0048); // Lower rate: 72bpm
    u_apb.write_reg(8'h08, 32'h0000_0078); // Upper rate: 120bpm
    u_apb.write_reg(8'h0C, 32'h0000_0050); // Amplitude: 5.0V
    u_apb.write_reg(8'h10, 32'h0000_0005); // Pulse width: 0.5ms

    // Wait for normal operation
    #5_000_000; // 5ms

    // Check results
    if (pace_pulse !== 0 && pace_amplitude !== 0)
      $display("PASS: Pace pulse generated correctly");
    else
      $display("FAIL: No pace pulse detected");

    $finish;
  end
endprogram
```

## 7. Simulation Control

### 7.1 Simulation Flow

```
1. Initialize signals
2. Apply reset
3. Wait for reset release
4. Configure DUT via APB
5. Start heart model
6. Run test scenario
7. Collect coverage
8. Check scoreboard
9. Generate report
10. Finish simulation
```

### 7.2 Run Script

```bash
#!/bin/bash
# Simulation run script
xrun -uvm -sv \
  +UVM_TESTNAME=smoke_test \
  +UVM_VERBOSITY=UVM_MEDIUM \
  -covoverwrite \
  -covtest pacemaker_cov \
  -l sim.log \
  pacemaker_tb.sv
```

## 8. Summary

Testbench architecture for the iPACE-CHIP pacemaker provides:

| Component | Purpose | Model Type |
|-----------|---------|------------|
| Heart Model | Cardiac rhythm generation | Behavioral |
| Battery Model | Power supply simulation | Behavioral |
| APB Master | Register configuration | Transaction |
| UART Monitor | Telemetry checking | Protocol |
| Scoreboard | Output verification | Checking |
| Coverage | Functional measurement | Collection |

Key architecture benefits:
- **Modular design** for independent component verification
- **Behavioral models** for cardiac system and power supply
- **Transaction-level** stimulus generation
- **Automated checking** with scoreboard and assertions
- **Coverage-driven** verification closure
