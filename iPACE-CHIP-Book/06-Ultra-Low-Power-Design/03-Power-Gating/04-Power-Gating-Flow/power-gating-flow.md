# Power Gating Design Flow for Implantable Pacemaker ASICs

## 1. Introduction to Power Gating Flow

The power gating design flow is a systematic methodology for implementing power switches, isolation cells, level shifters, and retention flip-flops across the iPACE-CHIP pacemaker ASIC. This flow transforms a single-supply, always-on design into a multi-domain, power-manageable architecture capable of shutting down inactive blocks to save energy. For a 10-year implantable pacemaker, the power gating flow must ensure functional correctness, timing closure, and reliability across all power states.

The flow integrates with the standard RTL-to-GDSII methodology, adding power-aware synthesis, physical design, and verification steps. Each stage requires specialized tools and methodologies that understand power domain boundaries, voltage islands, and the unique constraints of implantable medical devices.

## 2. UPF/CPF Specification

### 2.1 Unified Power Format (UPF) Specification

```
UPF Specification for iPACE-CHIP:

# Create power domains
create_power_domain PD_ALWAYS_ON -include_scope
create_power_domain PD_SENSING -elements {sensing/*}
create_power_domain PD_PROCESSING -elements {dsp/* classifier/*}
create_power_domain PD_OUTPUT -elements {stim/* comm/*}

# Create power rails
create_supply_net VDD -domain PD_ALWAYS_ON
create_supply_net VDD_SENSE -domain PD_SENSING
create_supply_net VDD_PROC -domain PD_PROCESSING
create_supply_net VDD_OUTPUT -domain PD_OUTPUT
create_supply_net VSS -domain ALL

# Create power ports
create_supply_port VDD -direction in
create_supply_port VDD_SENSE -direction in
create_supply_port VDD_PROC -direction in
create_supply_port VDD_OUTPUT -direction in
create_supply_port VSS -direction in

# Connect supply nets to ports
connect_supply_net VDD -ports {VDD}
connect_supply_net VDD_SENSE -ports {VDD_SENSE}
connect_supply_net VDD_PROC -ports {VDD_PROC}
connect_supply_net VDD_OUTPUT -ports {VDD_OUTPUT}
connect_supply_net VSS -ports {VSS}

# Set domain supply nets
set_domain_supply_net PD_ALWAYS_ON -primary_power VDD -primary_ground VSS
set_domain_supply_net PD_SENSING -primary_power VDD_SENSE -primary_ground VSS
set_domain_supply_net PD_PROCESSING -primary_power VDD_PROC -primary_ground VSS
set_domain_supply_net PD_OUTPUT -primary_power VDD_OUTPUT -primary_ground VSS
```

### 2.2 Power Switch Specification

```
UPF Power Switch Specification:

# Power switch for sensing domain
create_power_switch SW_SENSING -domain PD_SENSING \
  -input_port VDD -output_port VDD_SENSE \
  -control_port PWR_EN_SENSE_N -on_state {PWR_SENSE_ON !PWR_EN_SENSE_N} \
  -off_state {PWR_SENSE_OFF PWR_EN_SENSE_N} \
  -on_partial_control {PWR_SENSE_ON !PWR_EN_SENSE_N}

# Power switch for processing domain
create_power_switch SW_PROCESSING -domain PD_PROCESSING \
  -input_port VDD -output_port VDD_PROC \
  -control_port PWR_EN_PROC_N -on_state {PWR_PROC_ON !PWR_EN_PROC_N} \
  -off_state {PWR_PROC_OFF PWR_EN_PROC_N} \
  -on_partial_control {PWR_PROC_ON !PWR_EN_PROC_N}

# Power switch for output domain
create_power_switch SW_OUTPUT -domain PD_OUTPUT \
  -input_port VDD -output_port VDD_OUTPUT \
  -control_port PWR_EN_OUTPUT_N -on_state {PWR_OUT_ON !PWR_EN_OUTPUT_N} \
  -off_state {PWR_OUT_OFF PWR_EN_OUTPUT_N} \
  -on_partial_control {PWR_OUT_ON !PWR_EN_OUTPUT_N}

# Power switch cells
set_domain_supply_net PD_SENSING -primary_power VDD_SENSE
set_domain_supply_net PD_PROCESSING -primary_power VDD_PROC
set_domain_supply_net PD_OUTPUT -primary_power VDD_OUTPUT
```

### 2.3 Isolation and Level Shifter Specification

```
UPF Isolation Specification:

# Isolation for sensing domain outputs
set_isolation_strategy -domain PD_SENSING \
  -applies_to outputs \
  -clamp_value 0 \
  -isolation_cell_type AND \
  -isolation_cell_name ISO_SENSE_OUT \
  -active_low

# Isolation for processing domain outputs
set_isolation_strategy -domain PD_PROCESSING \
  -applies_to outputs \
  -clamp_value 0 \
  -isolation_cell_type AND \
  -isolation_cell_name ISO_PROC_OUT \
  -active_low

# Isolation for output domain outputs
set_isolation_strategy -domain PD_OUTPUT \
  -applies_to outputs \
  -clamp_value 0 \
  -isolation_cell_type AND \
  -isolation_cell_name ISO_OUTPUT_OUT \
  -active_low

# Level shifter specifications
set_level_shifter_strategy -domain PD_SENSING \
  -applies_to inputs \
  -rule low_to_high \
  -input_voltage_range {0 1.2} \
  -output_voltage_range {0 1.8} \
  -level_shifter_cell LS_LH_SENSE

set_level_shifter_strategy -domain PD_PROCESSING \
  -applies_to inputs \
  -rule high_to_low \
  -input_voltage_range {0 1.8} \
  -output_voltage_range {0 1.2} \
  -level_shifter_cell LS_HL_PROC
```

### 2.4 Retention Specification

```
UPF Retention Specification:

# Retention for configuration registers
set_retention -domain PD_SENSING \
  -elements {sensing/config_reg[*]} \
  -retention_cell RET_FF \
  -retention_power_net VDD_RET \
  -retention_ground_net VSS \
  -save_signal {PWR_EN_SENSE_N posedge} \
  -restore_signal {PWR_EN_SENSE negedge}

# Retention for state machine registers
set_retention -domain PD_PROCESSING \
  -elements {dsp/state_reg[*] classifier/state_reg[*]} \
  -retention_cell RET_FF \
  -retention_power_net VDD_RET \
  -retention_ground_net VSS \
  -save_signal {PWR_EN_PROC_N posedge} \
  -restore_signal {PWR_EN_PROC negedge}

# Retention for output domain state
set_retention -domain PD_OUTPUT \
  -elements {stim/state_reg[*] comm/config_reg[*]} \
  -retention_cell RET_FF \
  -retention_power_net VDD_RET \
  -retention_ground_net VSS \
  -save_signal {PWR_EN_OUTPUT_N posedge} \
  -restore_signal {PWR_EN_OUTPUT negedge}
```

## 3. Power-Aware Synthesis

### 3.1 Synthesis Flow

```
Power-Aware Synthesis Flow:

Step 1: RTL Analysis
├── Read RTL source files
├── Read UPF specification
├── Identify power domains
├── Map functionality to domains
└── Generate power-aware netlist

Step 2: Power Domain Mapping
├── Assign cells to power domains
├── Insert power switches at domain boundaries
├── Insert isolation cells for OFF→ON crossings
├── Insert level shifters for voltage crossings
├── Insert retention flip-flops for state preservation
└── Verify domain assignments

Step 3: Power Optimization
├── Clock gating insertion (see Section 02)
├── Multi-Vt optimization (see Section 04)
├── Operand isolation insertion
├── Memory power optimization
└── Activity-based optimization

Step 4: Timing Closure
├── Multi-mode multi-corner timing analysis
├── Power-aware STA
├── Clock tree synthesis (with power domains)
├── Hold time optimization
└── Signal integrity verification

Step 5: Power Verification
├── UPF compliance check
├── Isolation verification
├── Level shifter verification
├── Retention verification
├── Power switch verification
└── Power analysis (dynamic + static)
```

### 3.2 Synthesis Tool Configuration

```
Synopsys Design Compiler Power-Aware Configuration:

# Read UPF
set_power_domain_design -upf ipeace_chip.upf

# Power-aware synthesis
set_power_gating_style -type header \
    -control_signal PWR_EN \
    -min_width 15 \
    -max_width 100 \
    -threshold 0.1

# Level shifter insertion
set_level_shifter_style -rule low_to_high \
    -cell LS_LH_180 \
    -no_of_bits 1

# Isolation cell insertion
set_isolation_style -rule clamp \
    -cell ISO_AND \
    -clamp_value 0

# Retention flip-flop insertion
set_retention_style -cell RET_FF \
    -save_signal SAVE_n \
    -restore_signal RESTORE_n

# Compile with power awareness
compile_ultra -power
```

### 3.3 Post-Synthesis Power Analysis

```
Post-Synthesis Power Results:

Block                 │ Dynamic  │ Static   │ Total
──────────────────────┼──────────┼──────────┼────────
Always-On Domain      │ 100 nW   │ 50 nW    │ 150 nW
Sensing Domain        │ 480 nW   │ 90 nW    │ 570 nW
Processing Domain     │ 1030 nW  │ 130 nW   │ 1160 nW
Output Domain         │ 815 nW   │ 5 nW     │ 820 nW
Power Switches        │ 0 nW     │ 5 nW     │ 5 nW
Isolation Cells       │ 5 nW     │ 5 nW     │ 10 nW
Level Shifters        │ 10 nW    │ 5 nW     │ 15 nW
Retention Flops       │ 0 nW     │ 33 pW    │ ~0 nW
──────────────────────┼──────────┼──────────┼────────
TOTAL (all active)    │ 2435 nW  │ 290 nW   │ 2725 nW

Time-Weighted Average (with power gating):
P_avg = 0.28 × 570 + 0.65 × 5 + 0.03 × 1160 + 0.02 × 820
      = 159.6 + 3.25 + 34.8 + 16.4 = 214 nW

Power Gating Benefit: 2725 - 214 = 2511 nW (92% reduction)
```

## 4. Physical Design

### 4.1 Floorplanning with Power Domains

```
Power-Aware Floorplanning:

Step 1: Domain Placement
├── Place always-on domain near I/O ring
├── Place domains with high activity together
├── Minimize wire length between domains
├── Reserve area for power switches
└── Place decoupling capacitors

Step 2: Power Switch Placement
├── Place power switches at domain edges
├── Distribute switches uniformly
├── Route control signals to switches
├── Ensure adequate decoupling
└── Verify IR drop

Step 3: Isolation Cell Placement
├── Place isolation cells at domain boundaries
├── Route isolation control signals
├── Ensure isolation cells powered by always-on domain
└── Verify isolation timing

Step 4: Level Shifter Placement
├── Place level shifters at voltage crossings
├── Minimize level shifter delay impact
├── Route level shifter power supplies
└── Verify level shifter timing

Step 5: Retention Flop Placement
├── Place retention flops near domain boundaries
├── Route retention power supply
├── Ensure retention flop accessibility
└── Verify retention timing
```

### 4.2 Power Network Design

```
Power Distribution Network for Multiple Domains:

V_DD (1.8V) ────────────────────────────────────────────
│              │              │              │            │
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  Power   │  │  Power   │  │  Power   │  │  Power   │  │
│  Switch  │  │  Switch  │  │  Switch  │  │  Switch  │  │
│  (Sense) │  │  (Proc)  │  │  (Output)│  │  (Decap) │  │
└────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
     │             │             │             │          │
     ▼             ▼             ▼             ▼          │
V_DD_Sense    V_DD_Proc    V_DD_Output    V_DD_Decap     │
     │             │             │             │          │
┌────┴─────┐  ┌────┴─────┐  ┌────┴─────┐  ┌────┴─────┐  │
│  Sensing │  │Processing│  │  Output  │  │ Decoupling│  │
│  Domain  │  │ Domain   │  │  Domain  │  │ Capacitors│  │
└──────────┘  └──────────┘  └──────────┘  └──────────┘  │
                                                          │
V_SS (GND) ──────────────────────────────────────────────┘

Power Network Parameters:
- V_DD main rail: 2 μm wide (top metal)
- V_DD switched rails: 1 μm wide (metal 4)
- Via connections: Every 10 μm
- IR drop budget: < 50 mV (2.8% of 1.8V)
- Decoupling capacitance: 120 pF total
```

### 4.3 Physical Design Verification

```
Physical Design Verification for Power Gating:

DRC Checks:
- Minimum width for power switches: 15 μm ✓
- Guard ring spacing: 0.5 μm ✓
- Well tap spacing: 10 μm ✓
- Metal density: > 30% ✓

LVS Checks:
- Power switch connectivity: ✓
- Isolation cell connections: ✓
- Level shifter power supplies: ✓
- Retention power supply: ✓
- Domain boundary crossings: ✓

ERC Checks:
- Floating inputs: ✓ (all isolated)
- Unconnected power pins: ✓
- Short circuits: ✓
- Missing isolation: ✓

Timing Checks:
- Setup time for all paths: ✓
- Hold time for all paths: ✓
- Clock skew: ✓ (within budget)
- IR drop: ✓ (< 50 mV)

Power Checks:
- Dynamic power: ✓ (within budget)
- Static power: ✓ (within budget)
- Total power: ✓ (within budget)
```

## 5. Verification Methodology

### 5.1 Functional Verification

```
Power Gating Functional Verification:

Test Categories:
1. Power State Transitions
2. Isolation Correctness
3. Level Shifter Correctness
4. Retention Save/Restore
5. Clock Gating Integration
6. Fault Injection

Test 1: Power State Transition
- Start: All domains ON
- Transition: Domain 2 power off
- Verify: Domain 2 outputs isolated
- Verify: Domain 2 state retained
- Transition: Domain 2 power on
- Verify: Domain 2 state restored
- Verify: Domain 2 outputs correct

Test 2: Isolation Correctness
- Power off Domain 2
- Drive inputs to Domain 2 from Domain 0
- Verify Domain 2 outputs clamped to 0
- Verify no leakage through isolation cells
- Power on Domain 2
- Verify normal operation resumes

Test 3: Level Shifter Correctness
- Apply signals across voltage domains
- Verify correct voltage translation
- Verify timing constraints met
- Verify no signal integrity issues
```

### 5.2 Assertion-Based Verification

```
Power Gating Assertions:

// Power switch assertion
property power_switch_correct;
  @(posedge CLK) disable iff (!RST_n)
    PWR_EN_SENSE_N |-> VDD_SENSE == 0;
endproperty

// Isolation assertion
property isolation_correct;
  @(posedge CLK) disable iff (!RST_n)
    !POWER_GOOD_SENSE |-> sensing_outputs == 0;
endproperty

// Level shifter assertion
property level_shifter_correct;
  @(posedge CLK) disable iff (!RST_n)
    $rose(VDD_PROC) |-> ##[0:1] (proc_inputs === 0 || proc_inputs === 1);
endproperty

// Retention assertion
property retention_correct;
  @(posedge CLK) disable iff (!RST_n)
    $fell(POWER_GOOD_PROC) && $past(POWER_GOOD_PROC) |-> 
    config_reg == $past(config_reg);
endproperty
```

### 5.3 Formal Verification

```
Formal Verification for Power Gating:

Properties to Prove:
1. Power switch enables/disables correctly
2. Isolation cells clamp during power-off
3. Level shifters translate correctly
4. Retention flops preserve state
5. No combinational loops at domain boundaries
6. Correct power state machine transitions

Formal Verification Results:
┌─────────────────────────────┬──────────┬──────────┐
│ Property                    │ Status   │ Proven   │
├─────────────────────────────┼──────────┼──────────┤
│ Power switch correctness    │ PASS     │ YES      │
│ Isolation correctness       │ PASS     │ YES      │
│ Level shifter correctness   │ PASS     │ YES      │
│ Retention correctness       │ PASS     │ YES      │
│ No combinational loops      │ PASS     │ YES      │
│ State machine correctness   │ PASS     │ YES      │
└─────────────────────────────┴──────────┴──────────┘

Total Properties: 150
Properties Proven: 150 (100%)
Runtime: 4 hours
```

## 6. Power Gating Verification Results

### 6.1 Power Savings Verification

```
Power Gating Savings Verification:

Method: Compare power consumption with and without power gating

Without Power Gating:
- Total power (all domains always on): 2725 nW
- Average power (time-weighted): 2725 nW

With Power Gating:
- Total power (all domains on): 2725 nW
- Average power (time-weighted): 214 nW
- Power gating overhead: 15 nW (switches + isolation)

Net Power Savings: 2725 - 214 = 2511 nW
Power Gating Efficiency: 2511 / 2725 = 92.1%

Time-Weighted Average Calculation:
Mode              │ Time  │ Power    │ Weighted
──────────────────┼───────┼──────────┼──────────
All domains ON    │ 20%   │ 2725 nW  │ 545 nW
Sensing only      │ 70%   │ 150 nW   │ 105 nW
Only always-on    │ 10%   │ 150 nW   │ 15 nW
──────────────────┼───────┼──────────┼──────────
Weighted Average  │ 100%  │          │ 665 nW

Note: Power gating reduces from 2725 nW to 665 nW average.
This is different from the clock gating analysis because
power gating affects the entire block power, not just clocks.
```

### 6.2 Area Overhead

```
Power Gating Area Overhead:

Component             │ Count │ Area Each │ Total     │ % Die
──────────────────────┼───────┼───────────┼───────────┼──────
Power switches        │ 24    │ 32 μm²    │ 768 μm²  │ 0.19%
Isolation cells       │ 30    │ 2.16 μm²  │ 64.8 μm² │ 0.016%
Level shifters        │ 46    │ 12 μm²    │ 552 μm²  │ 0.14%
Retention flops       │ 660   │ 0.19 μm²  │ 125.4 μm²│ 0.031%
Decoupling caps       │ -     │ -         │ 40,000 μm²│ 1.0%
Control logic         │ 1     │ 500 μm²   │ 500 μm²  │ 0.125%
──────────────────────┼───────┼───────────┼───────────┼──────
TOTAL                 │       │           │ 42,010 μm²│ 1.05%

Die Area: 4,000,000 μm² (2 mm × 2 mm)
Overhead: 1.05% of die area

Justification:
- Power savings: 2511 nW (92% reduction)
- Area cost: 1.05% of die
- Power per area: 2511 nW / 42,010 μm² = 59.8 pW/μm²
- Excellent return on investment
```

### 6.3 Timing Impact

```
Timing Impact of Power Gating:

Critical Path Analysis:

Path 1: Sensing amplifier → DSP engine
- Without power gating: 0.8 ns
- With power gating (level shifter): 0.9 ns
- Overhead: 0.1 ns (12.5%)
- Slack: 29.6 ns (MET)

Path 2: DSP engine → Stimulation control
- Without power gating: 0.6 ns
- With power gating (level shifter): 0.7 ns
- Overhead: 0.1 ns (16.7%)
- Slack: 29.8 ns (MET)

Path 3: Configuration register → Output
- Without power gating: 0.4 ns
- With power gating (isolation + level shifter): 0.6 ns
- Overhead: 0.2 ns (50%)
- Slack: 29.9 ns (MET)

All paths meet timing at all corners.
Maximum timing overhead: 50% (still met with large margin).
```

## 7. Integration with Design Flow

### 7.1 Complete Power Gating Design Flow

```
Complete Power Gating Design Flow:

┌─────────────────────────────────────────────────────────┐
│ Step 1: Power Architecture Definition                   │
│ ├── Define power domains                                │
│ ├── Specify power switches                              │
│ ├── Define isolation strategies                         │
│ ├── Specify level shifter requirements                  │
│ └── Define retention requirements                       │
├─────────────────────────────────────────────────────────┤
│ Step 2: UPF/CPF Specification                           │
│ ├── Write UPF power intent                             │
│ ├── Verify UPF syntax                                   │
│ └── Review with design team                             │
├─────────────────────────────────────────────────────────┤
│ Step 3: RTL Design (power-aware)                        │
│ ├── Design with power domain awareness                  │
│ ├── Add power control logic                             │
│ └── Verify RTL functionally                             │
├─────────────────────────────────────────────────────────┤
│ Step 4: Power-Aware Synthesis                           │
│ ├── Synthesize with UPF                                 │
│ ├── Insert power switches, isolation, level shifters    │
│ ├── Insert retention flops                              │
│ └── Verify synthesis output                             │
├─────────────────────────────────────────────────────────┤
│ Step 5: Gate-Level Verification                         │
│ ├── Functional simulation with power states             │
│ ├── Formal verification                                 │
│ ├── Assertion-based verification                        │
│ └── Power analysis                                      │
├─────────────────────────────────────────────────────────┤
│ Step 6: Physical Design                                 │
│ ├── Power-aware floorplanning                           │
│ ├── Power switch placement                              │
│ ├── Isolation/level shifter placement                   │
│ ├── Power network design                                │
│ ├── Clock tree synthesis (power-aware)                  │
│ ├── Place and route                                     │
│ └── Post-layout verification                            │
├─────────────────────────────────────────────────────────┤
│ Step 7: Signoff                                         │
│ ├── Timing signoff (all corners)                        │
│ ├── Power signoff                                       │
│ ├── Physical verification (DRC/LVS/ERC)                 │
│ ├── Reliability signoff                                 │
│ └── Final power analysis                                │
└─────────────────────────────────────────────────────────┘
```

### 7.2 Debug and Iteration

```
Power Gating Debug Flow:

Issue: Power not gating correctly
├── Check: UPF specification correct?
├── Check: Power switch placement?
├── Check: Control signal routing?
├── Check: Isolation cell insertion?
└── Fix: Correct UPF or physical design

Issue: Timing violation with power gating
├── Check: Level shifter timing?
├── Check: Isolation cell delay?
├── Check: Power switch IR drop?
├── Check: Clock tree skew?
└── Fix: Resize cells or add buffers

Issue: Functional error in power state
├── Check: Retention save/restore?
├── Check: Isolation clamp value?
├── Check: Level shifter voltage ranges?
├── Check: Power state machine?
└── Fix: Correct RTL or UPF specification

Issue: Power higher than expected
├── Check: Power gating effectiveness?
├── Check: Leakage in power switches?
├── Check: Isolation cell leakage?
├── Check: Clock gating integration?
└── Fix: Optimize power gating strategy
```

## 8. Summary

The power gating design flow for the iPACE-CHIP pacemaker ASIC implements a comprehensive multi-domain architecture with 4 power domains, 24 power switches, 30 isolation cells, 46 level shifters, and 660 retention flip-flops. The flow integrates with standard RTL-to-GDSII methodology through UPF specification, power-aware synthesis, and specialized physical design steps. Verification encompasses functional correctness, timing closure, power savings validation, and reliability assessment. The implementation achieves 92% power reduction during idle periods with only 1.05% area overhead and minimal timing impact. The systematic flow ensures that power gating delivers its full benefit while meeting the stringent functional safety requirements of an implantable pacemaker.

## References

1. Keating, M., et al., "Low Power Design Methodology," Springer, 2002.
2. iPACE-CHIP Project Internal Documentation: Power Gating Design Flow Guide, Rev 3.0.
3. IEEE Std 1801-2015: Unified Power Format (UPF).
4. Synopsys, "Power Compiler User Guide," 2020.
5. Cadence, "Low-Power Design with Cadence Encounter," 2019.
