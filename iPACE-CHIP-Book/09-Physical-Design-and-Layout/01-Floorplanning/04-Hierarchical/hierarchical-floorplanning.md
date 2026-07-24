# Hierarchical Floorplanning

## Overview

Hierarchical floorplanning decomposes the iPACE-CHIP pacemaker ASIC into manageable blocks, each planned independently before integration. This approach is essential when the design exceeds flat floorplanning capacity or when different blocks have distinct physical requirements — as is the case with the mixed-signal pacemaker architecture.

## Why Hierarchical for iPACE-CHIP

The iPACE-CHIP contains fundamentally different circuit types that benefit from separate planning:

```
Digital Blocks:
- Standard cell based
- Automated placement and routing
- Dense utilization (65-75%)
- Clock tree synthesis required

Analog Blocks:
- Custom/semi-custom layout
- Matching and symmetry constraints
- Low utilization (40-50%)
- Sensitive to noise coupling

Memory Macros:
- Hard macros with fixed dimensions
- Specific pin access patterns
- Dedicated power supply requirements
- Physical-only cells (no logical rearrangement)
```

## Hierarchy Decomposition

### iPACE-CHIP Module Hierarchy

```
iPACE_CHIP_top
|
+-- digital_subsystem
|   +-- timing_engine
|   |   +-- interval_counter
|   |   +-- rate_adaptation
|   |   +-- refractory_period
|   |   +-- blanking_logic
|   |
|   +-- pulse_controller
|   |   +-- pulse_width_mod
|   |   +-- amplitude_control
|   |   +-- output_driver
|   |   +-- safety_monitor
|   |
|   +-- digital_comm
|   |   +-- uart_controller
|   |   +-- spi_master
|   |   +-- i2c_controller
|   |   +-- telem_encoder
|   |
|   +-- dsp_core
|       +-- fir_filter
|       +-- peak_detector
|       +-- arrhythmia_detector
|       +-- classifier
|
+-- analog_subsystem
|   +-- heart_signal_adc
|   |   +-- saramd_adc
|   |   +-- sample_hold
|   |   +-- reference_buffer
|   |   +-- digital_correction
|   |
|   +-- impedance_adc
|   |   +-- excitation_gen
|   |   +-- sense_amplifier
|   |   +-- demodulator
|   |   +-- calibration_dac
|   |
|   +-- power_analog
|       +-- charge_pump
|       +-- bandgap_ref
|       +-- ldo_regulator
|       +-- brownout_detector
|
+-- memory_subsystem
|   +-- pace_config_ram
|   +-- egm_buffer_sram
|   +-- lut_array
|   +-- fifo_buffer
|
+-- io_subsystem
    +-- pad_ring
    +-- esd_protection
    +-- level_shifters
    +-- bond_pad_array
```

## Block-Level Floorplanning

### Floorplanning Constraints per Block

Each hierarchical block has specific constraints:

```tcl
# Define block shapes and aspect ratios
set block_constraints {
    timing_engine {
        aspect_ratio 1.2
        utilization 0.70
        pin_side {north south}
        macro_keepout 5.0
    }
    pulse_controller {
        aspect_ratio 1.0
        utilization 0.65
        pin_side {east west}
        macro_keepout 10.0
    }
    heart_signal_adc {
        aspect_ratio 1.5
        utilization 0.45
        pin_side {north}
        macro_keepout 20.0
        isolation_ring true
    }
    impedance_adc {
        aspect_ratio 1.3
        utilization 0.40
        pin_side {south}
        macro_keepout 20.0
        isolation_ring true
    }
}
```

### Block Pin Assignment

```tcl
# Assign block pins for timing_engine
setPinAssignMode -minLayer M3 -maxLayer M5

# Group pins by function
set pins_data {
    {north {clk rst_n config_data[*] start}}
    {south {interval_done rate_out[*] status[*]}}
    {east  {refractory_req blanking_flag}}
    {west  {pulse_trigger width_req[*]}}
}

# Auto-assign with constraints
editPin -fixed -pinLength 20.0 -layer M5 \
    -side north -spreadType range \
    -start {10.0 0.0} -end {200.0 0.0} \
    -net {clk rst_n}

# Report pin locations
reportPin -file reports/timing_engine_pins.rpt
```

## Top-Level Floorplan Assembly

### Chip-Level Floorplan

```tcl
# Top-level floorplan setup
# Die size: 1140 um x 1140 um (including IO ring)

# Core area (excluding IO ring)
floorPlan -site core_site \
    -r 1.0 1.0 \
    -left 80.0 -right 80.0 \
    -top 80.0 -bottom 80.0

# Core dimensions: 980 um x 980 um

# Place hierarchical blocks
createInstGroup -name digital_group \
    -region {0 0 600 980} \
    -cell {digital_subsystem}

createInstGroup -name analog_group \
    -region {600 0 980 500} \
    -cell {analog_subsystem}

createInstGroup -name memory_group \
    -region {0 500 600 980} \
    -cell {memory_subsystem}

# Power ring around each group
addRing -nets {VDD VSS} \
    -type block_rings \
    -around digital_group \
    -layer {M6 M6} \
    -width {15.0 15.0} \
    -spacing {6.0 6.0} \
    -offset {8.0 8.0}

addRing -nets {VDD_ANA VSS} \
    -type block_rings \
    -around analog_group \
    -layer {M6 M6} \
    -width {15.0 15.0} \
    -spacing {6.0 6.0} \
    -offset {12.0 12.0}
```

### Block Placement Visualization

```
+--------------------------------------------------+
|  [IO Ring - M6 Power Rails]                       |
| +----------------------------------------------+ |
| |              Digital Subsystem                | |
| | +------------------+  +-------------------+ | |
| | |  Timing Engine   |  | Pulse Controller  | | |
| | |  180x150 um      |  |  160x160 um       | | |
| | +------------------+  +-------------------+ | |
| | +------------------+  +-------------------+ | |
| | |   DSP Core       |  | Digital Comm      | | |
| | |  220x200 um      |  |  140x120 um       | | |
| | +------------------+  +-------------------+ | |
| |                                             | |
| | +----------------------------------------+ | |
| | |         Memory Subsystem               | | |
| | | +----------+ +----------+ +---------+ | | |
| | | | Pace RAM | | EGM Buf  | |  LUTs   | | | |
| | | +----------+ +----------+ +---------+ | | |
| | |         FIFO Buffer                    | | |
| | +----------------------------------------+ | |
| +----------------------------------------------+ |
| +----------------------------------------------+ |
| |            Analog Subsystem                   | |
| | +------------------+  +-------------------+ | |
| | |  Heart Signal ADC |  | Impedance ADC     | | |
| | |  180x200 um       |  |  160x180 um       | | |
| | +------------------+  +-------------------+ | |
| | +------------------+  +-------------------+ | |
| | |  Charge Pump     |  | Bandgap + LDO     | | |
| | |  120x100 um      |  |  100x80 um        | | |
| | +------------------+  +-------------------+ | |
| +----------------------------------------------+ |
+--------------------------------------------------+
```

## Macro Placement

### Memory Macro Placement Rules

```tcl
# Place memory macros before standard cells
# Fixed placement with orientation control

# SRAM macro placement
placeInst egm_buffer_sram 50 500 0
placeInst pace_config_ram 50 600 0
placeInst lut_array 200 500 0
placeInst fifo_buffer 200 620 0

# Orient macros for optimal pin access
# All macros face north (pins on bottom)
setDb [get_db inst egm_buffer_sram] .orient R0
setDb [get_db inst pace_config_ram] .orient R0

# Create halo around each macro
createHalo -cell egm_buffer_sram -left 5.0 -right 5.0 \
    -top 5.0 -bottom 5.0
```

### Macro Placement Constraints

```
SRAM Placement Rules:
1. All macros aligned to grid (aligned on 0.1 um multiples)
2. Minimum 10 um halo on all sides for routing
3. No standard cells within 5 um of macro edge
4. Power straps must cross macro power pins
5. Macros on same row share power rails
6. Clock pin accessible from clock tree insertion point
7. No macro overlap (obvious but verify)
```

### Analog Macro Placement

```tcl
# Analog blocks require special placement
# Fixed placement with isolation constraints

placeInst heart_signal_adc 620 100 0
placeInst impedance_adc 620 320 0
placeInst charge_pump 850 100 0
placeInst bandgap_ref 850 220 0

# Isolation ring around analog area
addRing -nets {VSS} \
    -type block_rings \
    -around analog_subsystem \
    -layer {M2 M3} \
    -width {3.0 3.0} \
    -spacing {2.0 2.0} \
    -offset {5.0 5.0}

# Deep N-well boundary for analog isolation
createRouteBlk -box {600 0 980 500} -layer {M1 M2}
```

## Block Pin Planning

### Pin Location Optimization

```tcl
# Automated pin placement with timing awareness
setPinAssignMode -pinLengthOnBoundary 15

# For each hierarchical block
foreach block {timing_engine pulse_controller dsp_core digital_comm} {
    # Get critical nets
    set critical_nets [get_critical_nets -from $block]

    # Assign pins on opposite sides for flow-through
    editPin -inst $block -fixed -pinLength 15 -layer M5 \
        -side north -spreadType center \
        -nets $critical_nets
}

# Report block pin locations
reportBlockPins -file reports/block_pins.rpt
```

### Inter-Block Connectivity

```tcl
# Define top-level routes between blocks
# These are pre-routed channels

# Digital to Memory channel
createRouteBlk -box {0 480 600 500} -layer {M3 M4 M5}

# Digital to Analog channel
createRouteBlk -box {580 0 600 500} -layer {M4 M5 M6}

# Global clock routing channel
createRouteBlk -box {0 0 980 20} -layer {M6}
createRouteBlk -box {0 960 980 980} -layer {M6}
```

## Channel Routing

### Inter-Block Routing Channels

```tcl
# Channel between digital and analog subsystems
# Width: 20 um
# Available layers: M3, M4, M5, M6

# Pre-route power in channel
addStripe -nets {VDD VSS} \
    -layer M6 \
    -width 12.0 \
    -spacing 6.0 \
    -set_to_set_distance 80.0 \
    -start_offset 40.0 \
    -area {580 0 600 500}

# Route signal nets through channel
routeDesign -selectedNet -channel
```

### Channel Capacity Analysis

```python
# Channel routing capacity calculation
def channel_capacity(channel_width, num_layers, wire_width, wire_spacing):
    """
    Calculate maximum wires that fit in a routing channel
    """
    wires_per_layer = int(channel_width / (wire_width + wire_spacing))
    total_wires = wires_per_layer * num_layers
    
    return {
        'wires_per_layer': wires_per_layer,
        'total_wires': total_wires,
        'utilization': 0.7  # target utilization
    }

# Digital-Analog channel
result = channel_capacity(
    channel_width=20.0,  # 20 um
    num_layers=3,        # M3, M4, M5 (M6 reserved for power)
    wire_width=0.5,      # minimum width
    wire_spacing=0.5     # minimum spacing
)
# Wires per layer: 20
# Total wires: 60
# Available after utilization: 42 wires
```

## Power Domain Partitioning

### Power Domain Definition

```tcl
# Define power domains for iPACE-CHIP
createPowerDomain -name PD_DIGITAL -elements {
    timing_engine pulse_controller dsp_core digital_comm
}

createPowerDomain -name PD_ANALOG -elements {
    heart_signal_adc impedance_adc charge_pump bandgap_ref
}

createPowerDomain -name PD_MEMORY -elements {
    pace_config_ram egm_buffer_sram lut_array fifo_buffer
}

# Isolation between domains
addIsolationCell -domain PD_ANALOG -lib_cell ISO_BUF -clamp 0
addIsolationCell -domain PD_MEMORY -lib_cell ISO_BUF -clamp 0

# Level shifters between voltage domains
addLevelShifter -domain PD_MEMORY -lib_cell LSCH2 -rule both
```

### Power Domain Floorplan

```
+----------------------------------------------+
|           VDD Core (1.2V)                     |
|  +----------------------------------------+  |
|  |     PD_DIGITAL (VDD = 1.2V)            |  |
|  |  +-----------+  +-----------+          |  |
|  |  |  Timing   |  |  Pulse   |          |  |
|  |  |  Engine   |  |  Control |          |  |
|  |  +-----------+  +-----------+          |  |
|  |  +-----------+  +-----------+          |  |
|  |  |   DSP     |  | Digital  |          |  |
|  |  |   Core    |  |  Comm    |          |  |
|  |  +-----------+  +-----------+          |  |
|  +----------------------------------------+  |
|  |     PD_MEMORY (VDD = 1.2V)             |  |
|  |  +----------------------------------+  |  |
|  |  |  SRAMs and ROMs                  |  |  |
|  |  +----------------------------------+  |  |
|  +----------------------------------------+  |
|  |     PD_ANALOG (VDD_ANA = 1.8V)       |  |
|  |  +-----------+  +-----------+         |  |
|  |  |  Heart    |  | Impedance |         |  |
|  |  |  ADC      |  |   ADC     |         |  |
|  |  +-----------+  +-----------+         |  |
|  |  +-----------+  +-----------+         |  |
|  |  |  Charge   |  |  Bandgap  |         |  |
|  |  |  Pump     |  |  + LDO    |         |  |
|  |  +-----------+  +-----------+         |  |
|  +----------------------------------------+  |
+----------------------------------------------+
```

## Floorplan Constraints File

### SDC Constraints for Hierarchical Blocks

```tcl
# Hierarchical timing constraints

# Clock definitions
create_clock -name CLK_CORE -period 10.0 -waveform {0 5.0} [get_ports clk]
create_clock -name CLK_ANA  -period 20.0 -waveform {0 10.0} [get_ports clk_analog]

# Block-level timing exceptions
set_false_path -from [get_ports reset_n] -to [get_clocks CLK_CORE]

# Inter-block false paths (different clock domains)
set_false_path -from [get_clocks CLK_ANA] -to [get_clocks CLK_CORE]
set_false_path -from [get_clocks CLK_CORE] -to [get_clocks CLK_ANA]

# Max transition on critical timing engine paths
set_max_transition 0.5 [get_designs timing_engine]

# Max capacitance on pace output driver
set_max_capacitance 2.0 [get_ports pace_a_out]
```

### Physical Constraints

```tcl
# Physical design constraints per block

# Area constraints
set_max_area 0 [get_designs digital_subsystem]
set_max_area 80000 [get_designs analog_subsystem]

# Placement constraints
setPlacementConstraint -type soft -area {0 0 600 480} \
    [get_designs digital_subsystem]
setPlacementConstraint -type soft -area {600 0 980 500} \
    [get_designs analog_subsystem]

# Routing constraints
setNanoRouteMode -routeWithViaInPin true
setNanoRouteMode -routeWithViaOnlyForStandardCellPin auto

# Blockage for sensitive areas
createRouteBlk -box {600 0 980 500} -layer {M1 M2}
```

## Hierarchical Placement Flow

### Top-Level Placement Script

```tcl
proc place_hierarchical_blocks {} {
    # Step 1: Load all block netlists
    set blocks {timing_engine pulse_controller dsp_core digital_comm \
                heart_signal_adc impedance_adc charge_pump bandgap_ref \
                pace_config_ram egm_buffer_sram lut_array fifo_buffer}

    foreach block $blocks {
        read_netlist designs/${block}.v -cell $block
    }

    # Step 2: Define floorplan
    floorPlan -site core_site -r 1.0 1.0 \
        -left 80.0 -right 80.0 \
        -top 80.0 -bottom 80.0

    # Step 3: Place hard macros (memories)
    placeInst pace_config_ram 50 600 0
    placeInst egm_buffer_sram 50 500 0
    placeInst lut_array 200 500 0
    placeInst fifo_buffer 200 620 0

    # Step 4: Place analog blocks
    placeInst heart_signal_adc 620 100 0
    placeInst impedance_adc 620 320 0
    placeInst charge_pump 850 100 0
    placeInst bandgap_ref 850 220 0

    # Step 5: Create block halos
    foreach block $blocks {
        createHalo -cell $block \
            -left 5.0 -right 5.0 -top 5.0 -bottom 5.0
    }

    # Step 6: Define routing channels
    createRouteBlk -box {0 480 980 500} -layer {M3 M4}

    # Step 7: Place standard cell fillers
    addFiller -cells {FILLER64BWP180 FILLER32BWP180 FILLER16BWP180} \
        -prefix FILL -markFixed

    # Step 8: Verify floorplan
    reportFloorplan -file reports/floorplan.rpt
    checkFPlan -reportUtil
}
```

## Floorplan Iteration

### Metrics to Evaluate

```
Floorplan Quality Metrics:

1. Wirelength Estimate
   - HPWL (Half-Perimeter Wire Length)
   - Target: minimize global wirelength
   - iPACE-CHIP target: < 50,000 um HPWL

2. Congestion Estimate
   - Routing demand vs available resources
   - Target: max congestion < 80% utilization

3. Timing Estimate
   - Critical path delay from placement
   - Target: meet setup/hold for all paths

4. Power Distribution
   - IR drop estimate per block
   - Target: < 45 mV on any block

5. Thermal Profile
   - Power density per unit area
   - Target: < 5 W/cm^2 peak
```

### Iteration Script

```tcl
proc evaluate_floorplan {iteration} {
    set report_dir "reports/fp_iter_${iteration}"
    file mkdir $report_dir

    # Run quick placement
    set_db place_global_place_detail_cells false
    place_design

    # Evaluate metrics
    reportCongestion -file ${report_dir}/congestion.rpt
    reportTimingSummary -file ${report_dir}/timing.rpt
    report_power -file ${report_dir}/power.rpt

    # Check for violations
    set timing_slack [get_db [get_db timing_top_paths -1] .slack]
    set max_congestion [get_db designs .congestion_ratio]

    puts "Iteration $iteration: timing_slack=$timing_slack congestion=$max_congestion"

    # Decision logic
    if {$timing_slack < -0.5} {
        puts "WARN: Timing violation, restructure floorplan"
        return 0
    }
    if {$max_congestion > 0.8} {
        puts "WARN: High congestion, widen routing channels"
        return 0
    }

    return 1
}

# Run iterations
for {set i 1} {$i <= 5} {incr i} {
    if {[evaluate_floorplan $i]} {
        puts "Floorplan iteration $i passed"
        break
    }
    # Adjust floorplan for next iteration
   调整 placement or channel widths
}
```

## Floorplan Handoff

### Export Database

```tcl
# Save floorplan for downstream tools
write_def -floorplan -output iPACE_chip_floorplan.def
write_lef -output iPACE_chip_floorplan.lef

# Save constraints
write_sdc -output iPACE_chip_constraints.sdc

# Save power grid configuration
write_pg_netlist -output iPACE_chip_pg.v
```

### Floorplan Documentation

```tcl
# Generate floorplan documentation
reportFloorplan -file reports/floorplan_final.rpt
reportPowerGrid -file reports/powergrid.rpt
reportClockTree -file reports/ctree_est.rpt

# Create GDSII of floorplan for visualization
streamOut iCellStyle_chip_floorplan.gds \
    -mapFile technology/gds_map.txt \
    -mode ALL
```

## Summary

Hierarchical floorplanning for iPACE-CHIP separates digital, analog, and memory subsystems into independently planned blocks. The approach uses quadrant-based placement with dedicated power domains, macro-first placement flow, routing channel allocation, and iterative quality evaluation. The final floorplan passes timing, congestion, and power constraints before handoff to detailed placement and routing.
