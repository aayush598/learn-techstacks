# FPGA Prototyping Methodology for iPACE-CHIP Pacemaker

## 1. Introduction

FPGA prototyping creates a functional prototype of the iPACE-CHIP pacemaker on an FPGA platform, enabling real-world testing with actual cardiac models, medical equipment interfaces, and clinical scenario simulation. This chapter covers FPGA prototyping methodology, design partitioning, and validation strategies.

## 2. Prototyping Flow

### 2.1 End-to-End Flow

```
RTL Design
    │
    ▼
Synthesis for FPGA
    │
    ▼
Place and Route
    │
    ▼
Timing Closure
    │
    ▼
Bitstream Generation
    │
    ▼
FPGA Programming
    │
    ▼
Hardware Validation
    │
    ▼
Clinical Scenario Testing
```

### 2.2 Prototype Board Selection

```
Board              FPGA           Resources     Interface
────────────────────────────────────────────────────────────
Xilinx KCU105      Kintex Ultra   500K LUTs     PCIe, Ethernet
Terasic DE10-NIC   Stratix 10     933K ALMs     PCIe, USB
Digilent Genesys2  Kintex-7       200K LUTs     Ethernet, UART
Custom Medical     Zynq Ultra     600K LUTs     Medical-grade I/O
```

## 3. Design for FPGA Prototyping

### 3.1 Clock Domain Management

```systemverilog
// Clock domain crossing for prototype
module cdc_synchronizer #(
  parameter SYNC_STAGES = 2
) (
  input  logic clk_dst,
  input  logic rst_n,
  input  logic signal_src,
  output logic signal_dst
);

  logic [SYNC_STAGES-1:0] sync_reg;

  always_ff @(posedge clk_dst or negedge rst_n) begin
    if (!rst_n)
      sync_reg <= {SYNC_STAGES{1'b1}};
    else
      sync_reg <= {sync_reg[SYNC_STAGES-2:0], signal_src};
  end

  assign signal_dst = sync_reg[SYNC_STAGES-1];

endmodule

// Clock management for prototype
module prototype_clocks (
  input  logic sys_clk_100m,
  input  logic sys_rst_n,
  output logic clk_100m,
  output logic clk_50m,
  output logic clk_25m,
  output logic pll_locked
);

  logic clk_fb;

  MMCME2_ADV #(
    .CLKIN1_PERIOD(10.0),      // 100MHz input
    .CLKFBOUT_MULT_F(10.0),    // VCO = 1000MHz
    .CLKOUT0_DIVIDE_F(10.0),   // 100MHz output
    .CLKOUT1_DIVIDE_F(20.0),   // 50MHz output
    .CLKOUT2_DIVIDE_F(40.0),   // 25MHz output
    .BANDWIDTH("OPTIMIZED")
  ) pll_inst (
    .CLKIN1(sys_clk_100m),
    .CLKFBIN(clk_fb),
    .CLKFBOUT(clk_fb),
    .CLKOUT0(clk_100m),
    .CLKOUT1(clk_50m),
    .CLKOUT2(clk_25m),
    .LOCKED(pll_locked),
    .RST(!sys_rst_n),
    .PWRDWN(1'b0)
  );

endmodule
```

### 3.2 I/O Interface Design

```systemverilog
// Prototype I/O interface
module prototype_io (
  input  logic        clk,
  input  logic        rst_n,

  // Medical equipment interface
  input  logic        ecg_lead_i,
  output logic        pace_pulse_o,
  output logic [7:0]  pace_amplitude_o,

  // Status LEDs
  output logic [7:0]  status_leds,
  output logic        fault_led,
  output logic        battery_led,

  // UART for telemetry
  output logic        uart_tx,
  input  logic        uart_rx,

  // Switches for configuration
  input  logic [3:0]  mode_switch,
  input  logic [7:0]  rate_switch,
  input  logic        test_mode
);

  // I/O buffers
  IBUF ecg_ibuf (.I(ecg_lead_i), .O(ecg_lead_internal));
  OBUF pace_obuf (.I(pace_pulse_internal), .O(pace_pulse_o));

  // Debounce switches
  debounce #(.DEPTH(16)) mode_sw0 (
    .clk(clk), .rst_n(rst_n),
    .sig_in(mode_switch[0]), .sig_out(mode_debounced[0])
  );

  // LED driver
  assign status_leds = {state, timer_running, pace_active};
  assign fault_led = fault_flag;
  assign battery_led = battery_alert;

endmodule
```

## 4. Prototype Validation

### 4.1 Hardware-in-the-Loop Testing

```systemverilog
// Hardware-in-the-loop test controller
module hil_test_controller (
  input  logic        clk,
  input  logic        rst_n,
  input  logic        start_test,
  output logic        test_running,
  output logic [31:0] test_results
);

  typedef enum logic [2:0] {
    HIL_IDLE,
    HIL_CONFIGURE,
    HIL_RUN,
    HIL_COLLECT,
    HIL_REPORT
  } hil_state_t;

  hil_state_t state;
  int test_count;
  int pass_count;
  int fail_count;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      state <= HIL_IDLE;
      test_count <= 0;
      pass_count <= 0;
      fail_count <= 0;
    end else begin
      case (state)
        HIL_IDLE:
          if (start_test) state <= HIL_CONFIGURE;
        HIL_CONFIGURE:
          state <= HIL_RUN;
        HIL_RUN: begin
          if (test_complete) begin
            if (test_passed)
              pass_count <= pass_count + 1;
            else
              fail_count <= fail_count + 1;
            test_count <= test_count + 1;
            state <= HIL_COLLECT;
          end
        end
        HIL_COLLECT:
          if (all_tests_done) state <= HIL_REPORT;
          else state <= HIL_CONFIGURE;
        HIL_REPORT:
          state <= HIL_IDLE;
      endcase
    end
  end

  assign test_running = (state != HIL_IDLE);
  assign test_results = {pass_count, fail_count, test_count};

endmodule
```

### 4.2 Clinical Scenario Testing

```systemverilog
// Clinical scenario test sequences
class clinical_scenario_test;
  // Normal sinus rhythm test
  task test_normal_sinus();
    // Configure for VVI mode at 72 BPM
    write_reg(8'h00, 32'h0000_0006); // VVI
    write_reg(8'h04, 32'h0000_0048); // 72 BPM

    // Simulate normal sinus rhythm
    apply_cardiac_stimulus(NORMAL_SINUS, 72);
    run_for_duration(30_000); // 30 seconds

    // Verify correct pacing behavior
    verify_pace_count(30); // ~30 paces in 30s at 72bpm
    verify_no_faults();
    verify_rate_accuracy(72, 2);
  endtask

  // Bradycardia response test
  task test_bradycardia_response();
    write_reg(8'h00, 32'h0000_0006); // VVI
    write_reg(8'h04, 32'h0000_003C); // 60 BPM

    // Simulate bradycardia (40 BPM intrinsic)
    apply_cardiac_stimulus(BRADYCARDIA, 40);
    run_for_duration(10_000);

    // Verify pacemaker takes over
    verify_pace_count(10); // Should pace at 60 BPM
    verify_rate_accuracy(60, 2);
  endtask

  // Fault recovery test
  task test_fault_recovery();
    write_reg(8'h00, 32'h0000_0006); // VVI

    // Normal operation
    apply_cardiac_stimulus(NORMAL_SINUS, 72);
    run_for_duration(5_000);

    // Inject lead fault
    set_lead_impedance(16'hFFFF); // Open circuit
    run_for_duration(1_000);

    // Verify fault detection
    verify_fault_detected();
    verify_safe_mode_entered();

    // Clear fault
    set_lead_impedance(16'h01F4); // Nominal
    run_for_duration(5_000);

    // Verify recovery
    verify_normal_operation_resumed();
  endtask
endclass
```

## 5. Prototype Debug

### 5.1 Logic Analyzer Integration

```systemverilog
// ILA (Integrated Logic Analyzer) for prototype debug
module prototype_debug_ila (
  input  logic        clk,
  input  logic [7:0]  probe_state,
  input  logic        probe_pace_pulse,
  input  logic [7:0]  probe_amplitude,
  input  logic        probe_fault_flag,
  input  logic [15:0] probe_lead_impedance
);

  // ILA instantiation (Xilinx)
  ila_0 u_ila (
    .clk(clk),
    .probe0(probe_state),
    .probe1(probe_pace_pulse),
    .probe2(probe_amplitude),
    .probe3(probe_fault_flag),
    .probe4(probe_lead_impedance)
  );

endmodule
```

### 5.2 Virtual I/O

```systemverilog
// Virtual I/O for remote debug
module virtual_io (
  input  logic        clk,
  input  logic        rst_n,
  input  logic [31:0] cmd_from_host,
  output logic [31:0] status_to_host,
  output logic [31:0] debug_data
);

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      status_to_host <= 0;
      debug_data <= 0;
    end else begin
      case (cmd_from_host[31:24])
        8'h01: debug_data <= {state, timer_cnt};     // Read state
        8'h02: debug_data <= pace_amplitude;          // Read amplitude
        8'h03: debug_data <= lead_impedance;          // Read impedance
        8'h04: debug_data <= {fault_flag, alert_code}; // Read fault
        8'hFF: debug_data <= 32'hDEAD_BEEF;          // Heartbeat
      endcase
      status_to_host <= debug_data;
    end
  end

endmodule
```

## 6. Prototype Board Interface

### 6.1 Medical Equipment Interface

```systemverilog
// Medical equipment interface for prototype
module medical_equipment_interface (
  input  logic        clk,
  input  logic        rst_n,

  // ECG input (simulated)
  input  logic        ecg_pacer_spike_i,
  output logic        ecg_signal_o,

  // Pacing output
  input  logic        pace_pulse_i,
  input  logic [7:0]  pace_amplitude_i,
  output logic        pace_detected_o,

  // Lead impedance measurement
  output logic        z_measure_o,
  input  logic [15:0] z_result_i,

  // Power supply monitoring
  input  logic [7:0]  battery_voltage_i,
  output logic        power_enable_o
);

  // ECG signal generation
  assign ecg_signal_o = pace_pulse_i ? 1'b1 : ecg_pacer_spike_i;

  // Pace detection
  edge_detector pace_det (
    .clk(clk), .rst_n(rst_n),
    .sig_in(pace_pulse_i),
    .rise(pace_detected_o)
  );

  // Impedance measurement control
  assign z_measure_o = (state == MEASURE_Z);

  // Power management
  assign power_enable_o = (battery_voltage_i > 8'h32);

endmodule
```

## 7. Prototype Validation Matrix

### 7.1 Test Coverage

```
Test Category          Simulation    Prototype    Coverage
────────────────────────────────────────────────────────────
Functional             ✓             ✓            100%
Timing                 ✓             ✓            100%
Power                  -             ✓            New
EMI/EMC                -             ✓            New
Real-world Noise       -             ✓            New
Clinical Scenarios     Limited       ✓            Full
Long Duration          -             ✓            Full
```

## 8. Summary

FPGA prototyping methodology for the iPACE-CHIP pacemaker provides:

| Capability | Benefit | Validation |
|------------|---------|------------|
| Real Hardware | Actual I/O behavior | Medical interface |
| Real-time | Accurate timing | Clinical scenarios |
| Long Duration | Extended testing | Reliability |
| Power Analysis | Real consumption | Battery life |
| EMI Testing | Radiation compliance | Safety |
| Clinical Prep | Pre-silicon validation | Regulatory |

Key prototyping benefits:
- **Real-world validation** with actual hardware interfaces
- **Clinical scenario testing** before silicon
- **Power analysis** at real operating conditions
- **EMI/EMC pre-compliance** testing
- **Software development** platform for firmware
- **Regulatory evidence** for design verification
