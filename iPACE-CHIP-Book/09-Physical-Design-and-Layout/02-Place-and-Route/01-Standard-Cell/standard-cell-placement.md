# Standard Cell Placement

## Overview

Standard cell placement positions every logical cell in the iPACE-CHIP pacemaker ASIC onto the physical floorplan. This step transforms the netlist into a geometric representation, balancing timing, congestion, power, and routability. For a medical device like iPACE-CHIP, placement quality directly impacts timing closure and reliability.

## Standard Cell Library for iPACE-CHIP

### Cell Height and Track Pitch

```tcl
# BCD 180nm standard cell library parameters
set_db rdl_track_pitch 0.1    ;# um (track pitch)
set_db std_cell_height 4.32   ;# um (12-track library)
set_db site_name core_site     ;# placement site name

# Cell width is multiples of unit width (0.36 um)
# BUFX1 = 0.72 um (2 unit widths)
# AND2X1 = 1.08 um (3 unit widths)
# AOI21X1 = 1.44 um (4 unit widths)
```

### Cell Orientation Convention

```
Standard cell orientation for 12-track library:

Row 1 (Bottom): R0    - pins on top, VDD on top, VSS on bottom
Row 2:          MX    - pins on bottom, VDD on bottom, VSS on top
Row 3:          R0    - alternating
Row 4:          MX    - alternating

Power rail sharing:
- Adjacent rows share VDD or VSS rail
- Rail width: 0.96 um (2.5x minimum metal width)
- Ensures low-impedance power delivery
```

## Placement Flow

### Complete Innovus Placement Script

```tcl
proc run_placement {} {
    # Step 1: Read floorplan
    read_def iPACE_chip_floorplan.def

    # Step 2: Read synthesized netlist
    read_netlist iPACE_chip_synth.v -top iPACE_CHIP_top
    read_netlist iPACE_chip_stdcell.v -celltype standardcell

    # Step 3: Initialize design
    init_design

    # Step 4: Set placement constraints
    set_db place_global_place_detail_cells true
    set_db place_global_cong_effort high
    set_db place_global_timing_effort med
    set_db place_detail_check_cut_spacing true

    # Step 5: Global placement
    place_design -report_file reports/placement_global.rpt

    # Step 6: Optimize placement
    setOptMode -fixFanoutLoad true
    optDesign -preCTS -timing

    # Step 7: Detail placement
    place_detail -incremental

    # Step 8: Report results
    report_placement -file reports/placement_final.rpt
    reportCongestion -file reports/congestion_post_place.rpt
    reportTimingSummary -file reports/timing_post_place.rpt
}
```

### Placement Quality Checks

```tcl
# Verify placement quality
check_place -reportFile reports/check_place.rpt

# Common issues to check:
# - Cell overlap
# - Cells outside core boundary
# - Macro overlap
# - Pin access violations
# - Antenna violations

# Report cell density
reportGateDensity -file reports/gate_density.rpt
# Target: 65-70% in standard cell areas
# < 60% = underutilized (waste area)
# > 80% = congestion risk
```

## Timing-Driven Placement

### Setup for Timing Awareness

```tcl
# Enable timing-driven placement
setOptMode -effort high
set_db place_global_timing_effort high
setOptMode -optimizeFF true
setOptMode -repairDesign true
setOptMode -repairMinFanout 4

# Define clock
create_clock -name CLK -period 10.0 -waveform {0 5.0} [get_ports clk]

# False paths and exceptions
set_false_path -from [get_ports reset_n]
set_multicycle_path 2 -from [get_designs dsp_core/*]

# Max transition constraints
set_max_transition 0.5 [current_design]
```

### Timing-Driven Placement Execution

```tcl
# Run timing-driven placement
setPlaceMode -place_detail_legalization_inst_gap 1
setPlaceMode -place_global_place_io_pins true

place_design

# Check timing after placement
report_timing -max_paths 20 -delay_type max > reports/setup_timing_place.rpt
report_timing -max_paths 10 -delay_type min > reports/hold_timing_place.rpt

# Critical path analysis
report_timing -from [get_ports sense_rv] -to [get_ports pace_a_out] \
    > reports/critical_path.rpt
```

## Congestion-Driven Placement

### Congestion Map Generation

```tcl
# Generate congestion heatmap
reportCongestion -hotSpot -output reports/congestion_map.rpt
reportCongestion -overflow -output reports/overflow.rpt

# Congestion thresholds
# Green: 0-60% - good
# Yellow: 60-75% - acceptable
# Orange: 75-85% - needs attention
# Red: >85% - must optimize

# For iPACE-CHIP, target max congestion < 75%
```

### Congestion Mitigation

```tcl
# If congestion is high, apply these techniques:

# 1. Cell density reduction in congested areas
set_db place_global_max_density 0.7

# 2. Increase routing layers availability
setNanoRouteMode -routeWithTimingDriven true
setNanoRouteMode -routeWithViaInPin true

# 3. Add routing blockages in worst areas
createRouteBlk -box {300 200 500 400} -layer {M3}

# 4. Spread cells in congested regions
set_db place_global_max_density_limit 0.75
setOptMode -fixFanoutLoad true
optDesign -preCTS
```

## Placement Optimization

### Cell Sizing

```tcl
# Replace cells with optimal drive strength
# Larger cells for long nets, smaller for short nets

setOptMode -fixDRC true
setOptMode -optimizeFF true
optDesign -preCTS

# Report cell sizing changes
report_cell_usage -file reports/cell_sizing.rpt

# Typical optimization results:
# - 5-10% cells upsized (timing critical paths)
# - 15-20% cells downsized (non-critical paths, saves power)
# - Net result: timing improved, area neutral or reduced
```

### Logic Restructuring

```tcl
# Enable logic restructuring during placement
setOptMode -restructure true
setOptMode -mergeSeriesViaEffort high

# Common restructurings:
# - Buffer insertion for long nets
# - Logic duplication for high-fanout
# - Gate resizing
# - Path balancing
# - Redundant cell removal

optDesign -preCTS -logic
```

### Pin Swap Optimization

```tcl
# Swap pins on symmetric gates to improve timing
setOptMode -swapPin true
optDesign -preCTS

# Example: AOI21X1 pin swap
# Before: A=path1, B=path2, C=path3
# After:  A=path3, B=path1, C=path2 (if path3 has worst arrival)
```

## Placement for Medical Device Reliability

### Guard Ring Insertion

```tcl
# Add guard rings around sensitive blocks
# Prevents latch-up in pacemaker circuits

# Timing engine guard ring
addRing -nets {VSS} -type block_rings \
    -around {timing_engine} \
    -layer {M2 M3} \
    -width {3.0 3.0} -spacing {2.0 2.0} \
    -offset {8.0 8.0}

# Pulse controller guard ring
addRing -nets {VSS} -type block_rings \
    -around {pulse_controller} \
    -layer {M2 M3} \
    -width {3.0 3.0} -spacing {2.0 2.0} \
    -offset {8.0 8.0}
```

### Fill Cell Insertion

```tcl
# Insert filler cells for density uniformity
addFiller -cells {FILL64BWP180 FILL32BWP180 FILL16BWP180 \
                 FILL8BWP180 FILL4BWP180 FILL2BWP180 FILL1BWP180} \
    -prefix FILL -markFixed

# Decap filler for power integrity
addDecap -cells {DCAP60BWP180 DCAP30BWP180} \
    -prefix DEC -markFixed

# Verify density
reportGateDensity -from 0.0 -to 1.0 -step 0.05 \
    -file reports/density_check.rpt
```

## Placement Constraints for Analog

### Keep-Out Zones

```tcl
# Define keep-out zones around analog blocks
# No digital standard cells within these areas

createPlaceBlockage -box {600 0 980 500} -type soft -density 0.5
createPlaceBlockage -box {610 10 970 490} -type hard

# Allow only analog cells in analog region
set_db place_global_allow_cells {analog_* ldo_* bandgap_* charge_*}
```

### Analog Cell Placement

```tcl
# Manual placement for critical analog cells
placeInst sample_hold_core 650 150 N
placeInst saramd_core 750 150 N
placeInst ref_buffer 850 150 N

# Fix placement
set_db [get_db inst sample_hold_core] .place_status fixed
set_db [get_db inst saramd_core] .place_status fixed
set_db [get_db inst ref_buffer] .place_status fixed
```

## Placement Reports

### Critical Report Generation

```tcl
proc generate_placement_reports {} {
    # Timing report
    report_timing -max_paths 50 -delay_type max \
        > reports/placement_timing_setup.rpt

    # Hold timing
    report_timing -max_paths 20 -delay_type min \
        > reports/placement_timing_hold.rpt

    # Congestion
    reportCongestion -hotSpot -output reports/placement_congestion.rpt

    # Cell usage
    report_cell_usage -file reports/placement_cell_usage.rpt

    # Placement summary
    report_placement -summary > reports/placement_summary.rpt

    # Net length distribution
    report_net_length -distribution \
        > reports/net_length_dist.rpt

    # Power estimate
    report_power -cell_type all \
        > reports/placement_power.rpt
}
```

### Placement Statistics

| Metric | iPACE-CHIP Target | Typical |
|--------|-------------------|---------|
| Total cells | 8,423 | 8,423 |
| Sequential cells | 2,321 | 2,321 |
| Combinational cells | 6,102 | 6,102 |
| Cell density | 65-70% | 68.3% |
| Max congestion | < 75% | 71.2% |
| Total wirelength | < 50,000 um | 47,200 um |
| WNS (setup) | > 0 ns | +0.23 ns |
| TNS (setup) | 0 ns | 0 ns |
| WNS (hold) | > -0.1 ns | -0.05 ns |

## Incremental Placement

### Post-Optimization Placement

```tcl
# After initial placement optimization, run incremental
setOptMode -fixFanoutLoad true
setOptMode -repairDesign true
setOptMode -addInst true
setOptMode -deleteInst true

# Incremental placement for timing closure
place_detail -incremental

# Verify no overlaps after detail placement
check_place -reportFile reports/incremental_check.rpt
```

## Summary

Standard cell placement for iPACE-CHIP employs timing-driven and congestion-aware algorithms in Innovus. The flow progresses from global placement through optimization to detail placement, with guard rings for reliability and fill cells for density uniformity. Post-placement metrics target 65-70% cell density, sub-75% congestion, and positive setup slack across all timing paths.
