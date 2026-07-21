# Synthesis Constraints for iPACE-CHIP ASIC

## 1. Introduction

Synthesis constraints define the mapping objectives that guide the logic synthesis tool
(Design Compiler or Genus) to convert RTL into a gate-level netlist meeting iPACE-CHIP
specifications. Constraints encode timing, area, power, and design rule requirements into
a format the synthesis tool can optimize against.

For the iPACE-CHIP, constraints are uniquely shaped by:
- Ultra-low clock frequency (32.768 kHz) vs. standard cell speed
- Reduced core voltage (1.5V) affecting cell delay
- Safety-critical paths requiring specific derating
- Medical-grade reliability requiring conservative margins

## 2. Timing Constraints

### 2.1 Clock Definitions

```tcl
#==========================================================================
# Clock Definitions for iPACE-CHIP
#==========================================================================

# Primary clock: 32.768 kHz crystal oscillator
create_clock -name clk_core -period 30518 \
    [get_ports clk_core]
# Period = 1/32768 = 30.518 us = 30518 ns

# Telemetry clock: 1.048576 MHz (PLL-derived, active only during tele)
create_clock -name clk_tele -period 953.7 \
    [get_ports clk_tele]
# Period = 1/1048576 = 953.7 ns

# Clock uncertainty (jitter + skew)
set_clock_uncertainty -setup 0.5 [get_clocks clk_core]
set_clock_uncertainty -hold  0.2 [get_clocks clk_core]
set_clock_uncertainty -setup 0.1 [get_clocks clk_tele]
set_clock_uncertainty -hold  0.05 [get_clocks clk_tele]

# Clock latency (estimated)
set_clock_latency -source 0.5 [get_clocks clk_core]
set_clock_latency 0.2 [get_clocks clk_core]

# Clock transition (rise/fall time)
set_input_transition 5.0 [get_ports clk_core]
set_input_transition 2.0 [get_ports clk_tele]

# False paths between clock domains
set_false_path -from [get_clocks clk_core] \
               -to   [get_clocks clk_tele]
set_false_path -from [get_clocks clk_tele] \
               -to   [get_clocks clk_core]

# Generated clocks (internal clock dividers)
create_generated_clock -name clk_div2 \
    -source [get_ports clk_core] \
    -divide_by 2 \
    [get_pins u_clk_div/clk_out]
```

### 2.2 Input/Output Timing

```tcl
#==========================================================================
# Input/Output Delay Constraints
#==========================================================================

# AFE inputs (analog interface, slow signals)
set_input_delay -clock clk_core -max 100.0 [get_ports {sense_atrial* sense_vent*}]
set_input_delay -clock clk_core -min 0.0   [get_ports {sense_atrial* sense_vent*}]

# Output to electrode driver (pace command)
set_output_delay -clock clk_core -max 50.0  [get_ports {pace_*}]
set_output_delay -clock clk_core -min 0.0   [get_ports {pace_*}]

# Telemetry interface (fast domain)
set_input_delay -clock clk_tele -max 100.0 [get_ports {tele_rx_data}]
set_input_delay -clock clk_tele -min 0.0   [get_ports {tele_rx_data}]
set_output_delay -clock clk_tele -max 50.0 [get_ports {tele_tx_data}]
set_output_delay -clock clk_tele -min 0.0  [get_ports {tele_tx_data}]

# Asynchronous inputs (require synchronizers)
set_max_delay 200.0 -from [get_ports reset_b] \
                     -to   [get_pins u_rst_sync/rst_ff1/D]
set_max_delay 200.0 -from [get_ports watchdog_in] \
                     -to   [get_pins u_wdog_sync/ff1/D]

# Test mode timing (relaxed)
set_case_analysis 0 [get_ports test_mode_b]
```

### 2.3 Multicycle Paths

```tcl
#==========================================================================
# Multicycle Path Constraints
#==========================================================================

# Parameter registers: only written during telemetry sessions
# These are slow-changing signals, allow 10 cycles for setup
set_multicycle_path -setup 10 \
    -from [get_pins u_param_store/*/Q] \
    -to   [get_pins u_pacing_engine/*/D]
set_multicycle_path -hold 9 \
    -from [get_pins u_param_store/*/Q] \
    -to   [get_pins u_pacing_engine/*/D]

# ADC output data: sampled at 1 kHz, clock at 32.768 kHz
# Allow 30 cycles for ADC data to settle
set_multicycle_path -setup 30 \
    -from [get_pins u_adc/data_out*] \
    -to   [get_pins u_sensing_engine/*/D]
set_multicycle_path -hold 29 \
    -from [get_pins u_adc/data_out*] \
    -to   [get_pins u_sensing_engine/*/D]

# Telemetry CRC: computed over entire frame (many cycles)
set_multicycle_path -setup 100 \
    -from [get_pins u_tele_rx/data_reg*] \
    -to   [get_pins u_crc16/*/D]
set_multicycle_path -hold 99 \
    -from [get_pins u_tele_rx/data_reg*] \
    -to   [get_pins u_crc16/*/D]
```

## 3. Design Rule Constraints

### 3.1 Maximum Transition/Fanout

```tcl
#==========================================================================
# Design Rule Constraints (DRC)
#==========================================================================

# Maximum transition (slew) on all nets
set_max_transition 50.0 [current_design]
# 50 ns max rise/fall at 33 kHz (generous due to low freq)

# Maximum capacitance per net
set_max_capacitance 0.5 [current_design]
# 0.5 pF max load on any net (180nm guideline)

# Maximum fanout
set_max_fanout 32 [current_design]
# 32 inputs maximum per driver

# Minimum transition (prevents too-fast edges causing ringing)
set_min_transition 0.5 [current_design]

# Maximum bit width for buses (linting)
# No synthesis constraint needed; handled in RTL lint
```

### 3.2 Floorplan-Based Constraints

```tcl
#==========================================================================
# Physical Constraints (for synthesis planning)
#==========================================================================

# Target die area
set_max_area 2.0e6
# 2.0 mm^2 target (core only, excluding pads)

# Target utilization
set_max_utilization 0.70
# 70% target cell density

# Power budget
set_max_dynamic_power 50.0e-6
# 50 uW max dynamic power
set_max_leakage_power 5.0e-6
# 5 uW max leakage power (at 25C, typical corner)
```

## 4. Power Constraints

### 4.1 Power Attributes

```tcl
#==========================================================================
# Power Attributes and Settings
#==========================================================================

# Toggle rate on inputs (for power estimation)
set_toggle_rate 0.01 [get_ports sense_atrial*]
# 1% toggle rate (cardiac signals: ~1 Hz vs 33 kHz clock)
set_toggle_rate 0.01 [get_ports sense_vent*]
set_toggle_rate 0.001 [get_ports tele_rx_data]
# Very low activity (telemetry duty-cycled)
set_toggle_rate 0.5  [get_ports clk_core]
# 50% for clock

# Clock gating setup
set_clock_gating_style -sequential_cell latch \
    -minimum_bitwidth 4 \
    -max_fanout 16 \
    -positive_edge_logic {integrated}

# Switching activity annotation (SAIF-based)
# read_saif ./simulations/ipace_toggle.saif -strip_path iPACE_CHIP

# Power analysis mode
set_power_analysis_mode -method static \
    -create_binary_db true \
    -write_static_currents true
```

## 5. Optimization Directives

### 5.1 Area Optimization

```tcl
#==========================================================================
# Area Optimization Strategy
#==========================================================================

# Phase 1: High-performance synthesis (area not primary concern)
compile_ultra -area_high_effort_script

# Phase 2: Area recovery
compile_ultra -area_high_effort_script
# -remap to smaller cells where timing allows

# Phase 3: Manual area optimization
# Focus on high-area blocks:
#   - AES-128 engine (~10K gates): optimize S-box implementation
#   - Parameter store (SRAM): use compiler for density
#   - Output drivers: minimum transistors for required drive

# Area budget per block:
set_block_max_area pacing_engine 100000
set_block_max_area sensing_engine 150000
set_block_max_area aes128_engine 200000
set_block_max_area telemetry_unit 80000
set_block_max_area watchdog_timer 30000
set_block_max_area param_store 50000
set_block_max_area crc16_engine 10000
# Total: 620,000 um^2 = 0.62 mm^2 (core only)
# With 70% utilization: 0.89 mm^2 (including routing)
```

### 5.2 Timing Optimization Strategy

```tcl
#==========================================================================
# Timing Optimization Strategy
#==========================================================================

# Given the ultra-low clock frequency (33 kHz), timing closure is
# straightforward. The focus is on:
#   1. No violations on any path
#   2. Minimal buffer insertion (power savings)
#   3. HVT cell preference (leakage reduction)

# Set operating conditions
set_operating_conditions \
    -library tcbn180ghpwc \
    -max BEST \
    -max_library tcbn180ghpwc \
    -min WORST \
    -min_library tcbn180ghpwcl

# Wire load model
set_wire_load_model -name TSMC180_5K -library tcbn180ghpwc
set_wire_load_mode top

# Apply timing derating for safety
set_timing_derate -late 0.95 [current_design]
# 5% derating = 95% of timing allowed (conservative)
# For safety-critical paths:
set_timing_derate -late 0.90 -to [get_pins u_wdog_timer/*]
# 10% derating on watchdog timer

# Critical path budget (at 33 kHz = 30,518 ns period)
# Available slack per path: 30,518 ns - 500 ns (uncertainty) = 30,018 ns
# Typical path delay: ~200 ns (2-3 gate delays)
# Slack: ~29,818 ns (enormous margin)
```

## 6. Process Corner Analysis

### 6.1 Corner Definitions

```tcl
#==========================================================================
# Process Corner Analysis for iPACE-CHIP
#==========================================================================

# Six analysis corners:
set corners {
    {SS_0P9V_125C  tcbn180ghpsl  0.9   125}
    {SS_1P0V_125C  tcbn180ghpsl  1.0   125}
    {TT_1P5V_025C  tcbn180ghpwc  1.5   25}
    {TT_1P5V_075C  tcbn180ghpwc  1.5   75}
    {FF_1P8V_M40C  tcbn180ghpff  1.8  -40}
    {FF_1P8V_025C  tcbn180ghpff  1.8   25}
}

# iPACE-CHIP operating point:
# Nominal: TT, 1.5V, 37C (body temperature)
# Best-case (fast): FF, 1.8V, -40C (storage cold)
# Worst-case (slow): SS, 0.9V, 125C (aging + thermal)

# Signoff requires ALL corners to meet timing
# iPACE-CHIP adds: reliability corner (aged models, 10-year)

# Aging models (NBTI/PBTI degradation after 10 years)
# Available from TSMC as additional library sets
set aging_derate 0.05  # 5% additional delay from aging
```

### 6.2 Corner-by-Corner Timing

```
Timing Results by Corner (simulated):
═══════════════════════════════════════════════════════════════

┌──────────────────┬──────────┬──────────┬────────┬──────────┐
│ Corner           │ Period   │ WNS      │ TNS    │ Leakage  │
│                  │ (ns)     │ (ns)     │ (ns)   │ (uW)     │
├──────────────────┼──────────┼──────────┼────────┼──────────┤
│ SS_0P9V_125C     │ 30518    │ +30100   │ 0      │ 1.2      │
│ (worst-case)     │          │          │        │          │
├──────────────────┼──────────┼──────────┼────────┼──────────┤
│ SS_1P0V_125C     │ 30518    │ +30150   │ 0      │ 1.8      │
├──────────────────┼──────────┼──────────┼────────┼──────────┤
│ TT_1P5V_025C     │ 30518    │ +30350   │ 0      │ 3.5      │
│ (nominal)        │          │          │        │          │
├──────────────────┼──────────┼──────────┼────────┼──────────┤
│ TT_1P5V_075C     │ 30518    │ +30300   │ 0      │ 4.2      │
├──────────────────┼──────────┼──────────┼────────┼──────────┤
│ FF_1P8V_M40C     │ 30518    │ +30420   │ 0      │ 8.5      │
│ (best-case)      │          │          │        │          │
├──────────────────┼──────────┼──────────┼────────┼──────────┤
│ FF_1P8V_025C     │ 30518    │ +30400   │ 0      │ 7.2      │
└──────────────────┴──────────┴──────────┴────────┴──────────┘

  WNS = Worst Negative Slack (positive = meeting timing)
  TNS = Total Negative Slack (0 = no violations)
  Note: All corners show massive positive slack due to 33kHz clock
  This is expected and desirable for ultra-low power design.
```

## 7. Synthesis Script Structure

### 7.1 Top-Level Synthesis Flow

```
iPACE-CHIP Synthesis Flow:
═══════════════════════════════════════════════════════════════

  ┌─────────────────────────────────────────────────────────────┐
  │  1. INITIALIZATION                                          │
  │     • Read TSMC 180nm PDK (lib, lef, verilog)             │
  │     • Read iPACE-CHIP RTL (all modules)                    │
  │     • Link design (check all modules resolved)             │
  │     • Check design (report violations)                     │
  └───────────────────────────┬─────────────────────────────────┘
                              │
  ┌───────────────────────────v─────────────────────────────────┐
  │  2. CONSTRAINTS                                             │
  │     • Read timing constraints (.sdc)                       │
  │     • Read power constraints                               │
  │     • Read design rules (.drc)                             │
  │     • Set operating conditions                             │
  └───────────────────────────┬─────────────────────────────────┘
                              │
  ┌───────────────────────────v─────────────────────────────────┐
  │  3. OPTIMIZATION (compile_ultra)                           │
  │     • Map RTL to standard cells                            │
  │     • Insert clock gating                                  │
  │     • Optimize timing                                      │
  │     • Optimize area                                        │
  │     • Optimize power                                       │
  └───────────────────────────┬─────────────────────────────────┘
                              │
  ┌───────────────────────────v─────────────────────────────────┐
  │  4. POST-SYNTHESIS VERIFICATION                            │
  │     • Timing analysis (STA)                                │
  │     • Design rule check                                    │
  │     • Power analysis                                       │
  │     • Equivalent checking (RTL vs netlist)                 │
  │     • DRC on netlist (schematic vs layout)                 │
  └───────────────────────────┬─────────────────────────────────┘
                              │
  ┌───────────────────────────v─────────────────────────────────┐
  │  5. OUTPUT GENERATION                                       │
  │     • Gate-level Verilog netlist                           │
  │     • Timing constraints (.sdf for sim, .sdc for P&R)     │
  │     • Power report (.saif for power sim)                   │
  │     • Area report                                          │
  │     • Design statistics                                    │
  └─────────────────────────────────────────────────────────────┘
```

### 7.2 Synthesis Commands

```tcl
#==========================================================================
# iPACE-CHIP Main Synthesis Script
#==========================================================================

# Technology setup
set target_library {tcbn180ghpwc.db tcbn180ghpff.db tcbn180ghpsl.db}
set link_library   "* tcbn180ghpwc.db tsmc180_std_cell.db"}
set symbol_library "tsmc180.sdb"

# Read RTL
read_file -format verilog {
    ./rtl/pacing_engine.v
    ./rtl/sensing_engine.v
    ./rtl/aes128_engine.v
    ./rtl/telemetry_unit.v
    ./rtl/watchdog_timer.v
    ./rtl/param_store.v
    ./rtl/crc16_engine.v
    ./rtl/power_state_ctrl.v
    ./rtl/ipace_chip_top.v
}

current_design ipace_chip_top
link
uniquify
check_design

# Read constraints
read_sdc ./constraints/ipace_timing.sdc

# Synthesis
compile_ultra -area_high_effort_script -gate_clock

# Reports
report_timing -max_paths 10 > ./reports/timing.rpt
report_area -hierarchy > ./reports/area.rpt
report_power -hierarchy > ./reports/power.rpt
report_resources > ./reports/resources.rpt
report_clock_gating > ./reports/clock_gating.rpt

# Write outputs
write -format verilog -hierarchy \
    -output ./netlist/ipace_chip_top.v
write_sdc -output ./constraints/ipace_chip_top.sdc
write_sdf -output ./timing/ipace_chip_top.sdf
write_script -output ./scripts/ipace_chip_top.tcl
```

## 8. Constraint Validation

```
Constraint Validation Checklist:
═══════════════════════════════════════════════════════════════

┌────┬────────────────────────────────┬──────┬────────────────┐
│ #  │ Check                          │ Pass │ Notes          │
├────┼────────────────────────────────┼──────┼────────────────┤
│  1 │ All clocks defined             │      │                │
│  2 │ All I/O delays set             │      │                │
│  3 │ All false paths declared       │      │                │
│  4 │ All multicycle paths declared  │      │                │
│  5 │ Operating conditions correct   │      │                │
│  6 │ Wire load model valid          │      │                │
│  7 │ DRC constraints meet foundry   │      │                │
│  8 │ Power budget achievable        │      │                │
│  9 │ Area budget achievable         │      │                │
│ 10 │ Timing met at all corners      │      │                │
│ 11 │ Clock gating insertion correct │      │                │
│ 12 │ No unintended CDC paths        │      │                │
│ 13 │ Safety derating applied        │      │                │
│ 14 │ Aging derating for 10-year     │      │                │
└────┴────────────────────────────────┴──────┴────────────────┘
```

## 9. Summary

Synthesis constraints for iPACE-CHIP leverage the extremely relaxed timing environment
(33 kHz clock) to aggressively optimize for power and area. Key strategies:

- HVT cell preference for 80% of logic (minimal leakage)
- Aggressive clock gating with 4-cycle minimum pulse width
- Multicycle paths on all slow-changing signals
- Conservative timing derating (5-10%) for safety margin
- Six-corner analysis including aged models for 10-year lifetime

---

*Previous: [RTL Coding Guidelines](../01-RTL-Coding-Guidelines/rtl-coding-guidelines.md)*
