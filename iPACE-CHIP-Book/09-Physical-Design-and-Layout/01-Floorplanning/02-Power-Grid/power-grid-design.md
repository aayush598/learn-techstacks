# Power Grid Design

## Overview

The power distribution network (PDN) is the backbone of any ASIC, delivering stable voltage to every transistor on the chip. For iPACE-CHIP, the power grid design is mission-critical: a voltage drop on a pacing output circuit could directly affect patient therapy delivery.

## Power Delivery Requirements

### Voltage Domains in iPACE-CHIP

| Domain | Voltage | Purpose | Max Current |
|--------|---------|---------|-------------|
| VDD_CORE | 1.2V | Digital logic core | 2.5 mA |
| VDD_IO | 1.8V | IO buffers, communication | 1.0 mA |
| VDD_ANA | 1.8V | Analog circuits, ADCs | 0.8 mA |
| VDD_PLL | 1.2V | PLL clock generator | 0.3 mA |
| VSS | 0V | Common ground | Return path |

### IR Drop Budget

The total IR drop budget must be partitioned across the PDN:

```
Total IR Drop Budget = VDD × 5% = 60 mV (for 1.2V core)

Allocation:
- Package bonding wire: 10 mV
- Board-level drops: 5 mV
- Chip-level PDN: 45 mV
  - Global grid: 15 mV
  - Local grid: 15 mV
  - Standard cell internal: 15 mV
```

## PDN Architecture

### Hierarchical Power Grid

The iPACE-CHIP power grid follows a four-level hierarchy:

```
Level 1: Pad Ring → Package connections
Level 2: Top Metal (M6) → Global horizontal straps
Level 3: Upper Metal (M5) → Global vertical straps
Level 4: Lower Metal (M3-M4) → Local distribution
Level 5: Standard Cell Rails → Direct transistor supply
```

### Grid Topology Selection

For iPACE-CHIP, a uniform mesh topology is preferred:

```
Advantages:
- Predictable IR drop across the die
- Simplified PDN modeling
- Easier to verify electromigration compliance
- Consistent current density

Disadvantages:
- More metal resource consumed
- May over-design low-current regions
```

## Global Power Grid Design

### Top Metal Strapping

```tcl
# Innovus PDN configuration
# Level 2: M6 horizontal straps
addRing -nets {VDD VSS} \
    -type core_rings \
    -layer {M6 M6} \
    -width {20.0 20.0} \
    -spacing {8.0 8.0} \
    -offset {5.0 5.0}

# Level 3: M5 vertical straps
addStripe -nets {VDD VSS} \
    -layer M5 \
    -width 16.0 \
    -spacing 8.0 \
    -set_to_set_distance 100.0 \
    -start_offset 50.0

# Level 2: M6 horizontal straps
addStripe -nets {VDD VSS} \
    -layer M6 \
    -width 16.0 \
    -spacing 8.0 \
    -set_to_set_distance 120.0 \
    -start_offset 60.0
```

### Via Stack Requirements

Power vias connecting the global grid to the local distribution:

```tcl
# Via density rule for power vias
# Minimum 1 via per 10 um of power strap width
# Use via arrays for better current handling

sroute -connect {blockPin corePin floatingStripe} \
    -nets {VDD VSS} \
    -allowJogging true \
    -allowLayerChange true \
    -crossoverViaLayerRange {M1 M6} \
    -nets {VDD VSS}
```

### Current Density Calculation

The current each power strap must carry:

```python
# Power grid current density analysis
import math

# Total core current
I_total_core = 2.5e-3  # 2.5 mA for core domain

# Grid parameters
strap_width_m6 = 16.0e-6  # 16 um width on M6
strap_pitch_m6 = 120.0e-6  # 120 um pitch on M6
num_straps_m6 = 40  # number of horizontal straps

# Current per strap
I_per_strap = I_total_core / num_straps_m6
# 62.5 uA per strap

# M6 current density limit (BCD 180nm)
J_max_m6 = 1.0e6  # 1.0 mA/um² for M6 at 105°C

# Required minimum width
W_min = I_per_strap / (J_max_m6 * 1.0e-6)
# Well below 16 um design width - safe
```

## Local Power Distribution

### Standard Cell Rail Design

Standard cell power rails run on M1, perpendicular to cell orientation:

```tcl
# Standard cell rail configuration
sroute -connect {corePin} \
    -nets {VDD VSS} \
    -allowJogging true \
    -allowLayerChange true \
    -crossoverViaLayerRange {M1 M2} \
    -nets {VDD VSS}

# Target: at least 80% of cells directly connected to rails
# without requiring additional routing
```

### Rail Width Calculations

```
Standard cell rail current capacity:

M1 rail width: 0.5 um (minimum DRC width)
M1 current density: 0.3 mA/um² (at 105°C)
Current per rail: 0.5 × 0.3 = 0.15 mA

Number of cells per rail segment: ~50 cells
Average cell current: 2.5 mA / 8,423 cells = 0.297 uA per cell
Rail capacity per segment: 50 × 0.297 uA = 14.9 uA

M1 rail capacity >> required current → Safe
```

## Decoupling Capacitance Strategy

### On-Chip Decap Requirements

Decoupling capacitors (decaps) suppress high-frequency noise on the power rails:

```
Total decap needed = I_transient × dt / dV_tolerance

For iPACE-CHIP:
- Maximum transient current: 500 uA (clock switching)
- Transition time: 1 ns
- Allowed voltage noise: 30 mV

C_decap = 500e-6 × 1e-9 / 30e-3 = 16.7 pF
```

### Decap Cell Distribution

```tcl
# Insert decap cells
addDecap -cells {DCAP60BWP180} \
    -prefix DEC \
    -incision 0.5

# Fill gaps with decap cells at 8% area density
addFiller -cells {DEC60BWP180 DEC30BWP180 DEC15BWP180} \
    -prefix FILL \
    -markFixed

# Decap budget: 8% of core area = 75,446 um²
# Available from fill cells in routing channels
```

### Decap Placement Rules

- Decaps must be placed within 200 um of every high-switching block
- PLL supply requires dedicated decap cluster (minimum 5 pF)
- Analog supply decaps separated from digital decaps
- No decaps in timing-critical routing channels

## Power Grid Analysis

### Static IR Drop Analysis

```tcl
# Innovus static IR drop analysis
set_power_analysis_mode -method static \
    -create_binary_db true \
    -write_static_currents true

# Run power analysis
report_power -analysis_effort high \
    -cell_type all \
    -output reports/power_analysis.rpt

# Static IR drop check
set_pg_library_mode -celltype techonly \
    -extraction_tech_file {tech/qrc_180nm.tch}

report_pg -method voltage -output reports/ir_drop_static.rpt
```

### Dynamic IR Drop Analysis

Dynamic analysis captures instantaneous voltage droops during switching:

```tcl
# Dynamic IR drop requires switching activity
read_vcd {sim/activity.vcd} -strip_path iPACE_CHIP_top

set_dynamic_power_analysis -method dynamic \
    -start_time 0 \
    -end_time 100e-9 \
    -time_step 1e-12

report_dynamic_power -output reports/ir_drop_dynamic.rpt

# Key concern: switching activity during pace pulse delivery
# Verify < 45 mV droop during critical timing windows
```

### IR Drop Contour Maps

```tcl
# Generate voltage contour plots
report_power -method heat_map \
    -resolution 10.0 \
    -output reports/ir_drop_map.rpt

# Contour thresholds for iPACE-CHIP:
# Green: < 20 mV drop
# Yellow: 20-35 mV drop
# Red: > 35 mV drop (requires optimization)
```

## Power Grid for Analog Blocks

### Dedicated Analog Supply Routing

Analog circuits require isolated, low-noise power delivery:

```tcl
# Dedicated analog power ring
addRing -nets {VDD_ANA VSS_ANA} \
    -type block_rings \
    -around {adc_subsystem heart_adc} \
    -layer {M5 M5} \
    -width {12.0 12.0} \
    -spacing {6.0 6.0} \
    -offset {4.0 4.0}

# Separate via connections to global grid
sroute -connect {blockPin} \
    -nets {VDD_ANA VSS_ANA} \
    -allowJogging true \
    -crossoverViaLayerRange {M3 M6} \
    -fixedBondLayerAllow {M6} \
    -allowLayerChange true
```

### Analog PDN Noise Budget

```
Total analog noise budget: 10 mV peak-to-peak

Sources of noise coupling:
- Digital switching: 3 mV (through substrate)
- Power supply coupling: 4 mV (through PDN)
- Coupled signal routing: 2 mV (through capacitive coupling)
- Substrate noise: 1 mV

Isolation techniques:
- Guard rings on all analog supply rails
- Dedicated analog power pins (separate from digital)
- Ferrite bead model at package level
- Deep N-well isolation where available
```

## Electromigration Considerations

### Current Density Limits

```tcl
# EM rules for power grid metals
# BCD 180nm process

# M6 (Top metal): Jmax = 1.0 mA/um² at 105°C
# M5: Jmax = 0.8 mA/um² at 105°C
# M4: Jmax = 0.6 mA/um² at 105°C
# M3: Jmax = 0.4 mA/um² at 105°C
# M2: Jmax = 0.3 mA/um² at 105°C
# M1: Jmax = 0.2 mA/um² at 105°C

# Via current limits
# Via56: 2.0 uA per via
# Via45: 1.5 uA per via
# Via34: 1.0 uA per via
# Via23: 0.8 uA per via
# Via12: 0.5 uA per via
```

### Via Array Requirements

```tcl
# Ensure adequate via density on power connections
# Rule: minimum 4 vias per power pin connection

editAddRoute -net VDD -via {VIA65} -point {100 200}
editAddRoute -net VSS -via {VIA65} -point {150 200}

# For via arrays on power straps
addViaRow -cell VIA65 -origin {100 50} -direction horizontal \
    -width 16 -height 8 -spacing 4 -nets {VDD VSS}
```

## Power Switches and Islands

### Power Gating Architecture

For iPACE-CHIP, power gating reduces idle power in non-essential blocks:

```tcl
# Create power domain for communication block
create_power_domain -name PD_COMM \
    -elements {uart_controller spi_master i2c_controller}

# Insert power switches
insertPowerSwitch -type header \
    -prefix PSW \
    -cell {PWR_SW2BWP180} \
    -powerDomain PD_COMM \
    -nets {VDD VDD_SW}

# Power switch array: 8 switches in parallel
# Drive strength: 2x per switch (total 16x)
```

### Isolation Strategy

```tcl
# Insert isolation cells at power domain boundaries
addIsolationCell -lib_cell {ISO_BUFBWP180} \
    -domain PD_COMM \
    -clamp_value 0 \
    -appliesTo inputs

# Level shifter requirements between voltage domains
addLevelShifter -domain PD_COMM \
    -lib_cell {LSCH2BWP180} \
    -rule both
```

## Power Grid Verification

### Design Rule Checks for PDN

```tcl
# Verify power grid connectivity
verifyConnectivity -type special -net {VDD VSS} \
    -error 100 -report reports/connectivity.rpt

# Check for floating power vias
verify_drc -limit 1000

# Metal density check (important for PDN)
verifyMetalDensity -report reports/metal_density.rpt
```

### PDN Frequency Response

```tcl
# AC analysis of power grid
# Ensures low impedance up to switching frequency

# Self-resonance frequency of decap network
# f_self = 1 / (2π × √(L_parasitic × C_decap))

# Target: low impedance below 500 MHz (5× clock frequency)
# iPACE-CHIP clock: 100 MHz → analyze up to 500 MHz
```

## Power Grid Summary for iPACE-CHIP

### Final PDN Specifications

| Parameter | Value |
|-----------|-------|
| Core voltage | 1.2V ± 5% |
| Global strap width (M6) | 16 um |
| Global strap pitch (M6) | 120 um |
| Local strap width (M5) | 12 um |
| Local strap pitch (M5) | 100 um |
| Decap density | 8% |
| Total decap capacitance | 18 pF |
| Static IR drop (max) | 30 mV |
| Dynamic IR drop (max) | 45 mV |
| EM compliance margin | 1.5× rule minimum |
| Via density per power pin | ≥ 4 vias |

## TCL Power Grid Setup Script

```tcl
# Complete PDN setup for iPACE-CHIP
proc setup_pdn {} {
    # Define power nets
    set power_nets {VDD VDD_ANA VDD_IO VDD_PLL}
    set ground_nets {VSS}

    # Core ring
    addRing -nets {VDD VSS} \
        -type core_rings \
        -layer {M6 M6} \
        -width {20.0 20.0} \
        -spacing {8.0 8.0} \
        -offset {5.0 5.0}

    # Block rings for analog
    addRing -nets {VDD_ANA VSS} \
        -type block_rings \
        -around {heart_adc impedance_adc} \
        -layer {M5 M5} \
        -width {12.0 12.0} \
        -spacing {6.0 6.0}

    # Vertical stripes (M5)
    addStripe -nets {VDD VSS} \
        -layer M5 \
        -width 16.0 \
        -spacing 8.0 \
        -set_to_set_distance 100.0 \
        -start_offset 50.0

    # Horizontal stripes (M6)
    addStripe -nets {VDD VSS} \
        -layer M6 \
        -width 16.0 \
        -spacing 8.0 \
        -set_to_set_distance 120.0 \
        -start_offset 60.0

    # Connect everything
    sroute -connect {blockPin corePin floatingStripe} \
        -nets {VDD VSS} \
        -allowJogging true \
        -crossoverViaLayerRange {M1 M6}

    # Add decaps
    addDecap -cells {DCAP60BWP180} -prefix DEC -incision 0.5

    puts "PDN setup complete"
}
```

## Summary

The iPACE-CHIP power grid employs a hierarchical mesh on M5/M6 with dedicated analog supply isolation, 8% decap density, and rigorous IR drop verification. The design targets 30 mV static and 45 mV dynamic IR drop, ensuring stable operation for all pacemaker functions including pacing pulse delivery and sensing.
