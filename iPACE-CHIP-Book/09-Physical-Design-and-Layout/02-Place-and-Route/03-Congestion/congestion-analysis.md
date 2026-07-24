# Congestion Analysis

## Overview

Congestion analysis identifies routing hotspots where wire demand exceeds available routing resources. For iPACE-CHIP, congestion analysis must account for the mixed-signal nature of the design — digital blocks with dense standard cells alongside analog blocks with restrictive routing rules.

## Congestion Fundamentals

### What Causes Congestion

```
Primary Causes:
1. High cell density in localized regions
2. Many nets crossing a small area
3. Macro blockages forcing routes through narrow channels
4. Power grid consuming routing resources
5. Restrictive layer assignments for analog nets

Secondary Causes:
6. Poorly placed high-fanout nets
7. Clock tree nets with many destinations
8. Bus-style interconnects in narrow corridors
9. Power/ground shielding consuming tracks
10. Guard ring routing requirements
```

### Congestion Metric Definition

```
Congestion = Demand / Supply

Where:
- Demand = number of wires needing to pass through a Gcell
- Supply = number of available routing tracks in the Gcell
- Gcell = Global routing cell (typically 5-10 um square)

Congestion Ratio:
- 0.0 - 0.6: Low congestion (green)
- 0.6 - 0.75: Moderate congestion (yellow)
- 0.75 - 0.85: High congestion (orange)
- 0.85 - 1.0: Critical congestion (red)
- > 1.0: Overflow (routing impossible without adjustment)
```

## Gcell Grid Setup

### iPACE-CHIP Gcell Configuration

```tcl
# Configure Gcell grid for analysis
setNanoRouteMode -routeWithTimingDriven true

# Gcell size determination
# Chip core: 980 um x 980 um
# Target Gcell size: 10 um x 10 um
# Grid: 98 x 98 = 9,604 Gcells

# Layer routing capacity per Gcell
set gcell_capacity {
    M3: 16 tracks  ;# horizontal routing
    M4: 16 tracks  ;# vertical routing
    M5: 10 tracks  ;# partial routing (power sharing)
    M6: 6 tracks   ;# minimal signal routing
}

# Total tracks per Gcell: 48
# Usable for signals (80%): 38 tracks
```

### Generate Gcell Grid

```tcl
# Create Gcell grid
createGcellGrid -origin {0 0} \
    -direction horizontal \
    -pitch {10.0 10.0} \
    -extent {0 0 980 980}

# Verify grid
reportGcellGrid -file reports/gcell_grid.rpt
```

## Pre-Route Congestion Analysis

### Placement-Based Estimate

```tcl
# Analyze congestion before routing
reportCongestion -overflow -output reports/pre_route_congestion.rpt
reportCongestion -hotSpot -output reports/pre_route_hotspot.rpt

# Generate congestion map
reportCongestion -congestedMap reports/congestion_map.txt

# Congestion summary
puts "Max overflow: [get_db designs .max_overflow]"
puts "Average overflow: [get_db designs .avg_overflow]"
puts "Overflow count: [get_db designs .overflow_count]"
```

### Layer-by-Layer Analysis

```python
# Layer congestion breakdown for iPACE-CHIP
layer_analysis = {
    'M3': {
        'tracks_per_gcell': 16,
        'demand_avg': 10.4,
        'demand_max': 14.2,
        'utilization_avg': 0.65,
        'utilization_max': 0.887,
        'overflow_gcells': 12,
    },
    'M4': {
        'tracks_per_gcell': 16,
        'demand_avg': 11.8,
        'demand_max': 15.1,
        'utilization_avg': 0.737,
        'utilization_max': 0.944,
        'overflow_gcells': 23,
    },
    'M5': {
        'tracks_per_gcell': 10,
        'demand_avg': 4.2,
        'demand_max': 7.8,
        'utilization_avg': 0.42,
        'utilization_max': 0.78,
        'overflow_gcells': 0,
    },
    'M6': {
        'tracks_per_gcell': 6,
        'demand_avg': 1.8,
        'demand_max': 3.2,
        'utilization_avg': 0.30,
        'utilization_max': 0.533,
        'overflow_gcells': 0,
    }
}

for layer, data in layer_analysis.items():
    overflow = data['overflow_gcells']
    status = "OVERFLOW" if overflow > 0 else "OK"
    print(f"{layer}: {data['utilization_max']*100:.1f}% max util, "
          f"{overflow} overflow Gcells [{status}]")
```

## Congestion Hotspot Analysis

### Identifying Hotspots

```tcl
# Generate hotspot report
reportCongestion -hotSpot -output reports/hotspots.rpt

# Detailed hotspot analysis
proc analyze_hotspots {report_file} {
    set fp [open $report_file w]
    puts $fp "=========================================="
    puts $fp "Congestion Hotspot Analysis"
    puts $fp "=========================================="

    # Get congested Gcells
    set congested [get_db -quiet designs .overflow_gcells]

    foreach gcell $congested {
        set x [lindex $gcell 0]
        set y [lindex $gcell 1]
        set overflow [lindex $gcell 2]

        puts $fp "Gcell ($x, $y): overflow = $overflow"

        # Identify nets in this Gcell
        set nets [get_nets_in_gcell $x $y]
        puts $fp "  Nets: [llength $nets]"

        # Top contributors
        foreach net $nets {
            set weight [get_net_weight $net]
            puts $fp "    [get_db $net .name] : weight = $weight"
        }
    }
    close $fp
}
```

### Hotspot Location Mapping

```
iPACE-CHIP Congestion Heatmap:

Y (um)
980 +----------------------------------------------+
    | [DSP]    [Pulse]     | [Memory]              |
800 | [Core]   [Control]   | [SRAMs]              |
    |                                              |
600 | [Timing] [Engine]    | [FIFO]  [LUT]        |
    |                                              |
400 |              ROUTING  | [Analog]              |
    |              CHANNEL  | [ADC]                 |
200 | [Comm]    [Digital]   | [Charge] [Bandgap]   |
    |                                              |
  0 +----------------------------------------------+
    0        200       400       600       800  980
                        X (um)

Hotspot Regions:
- (350-450, 350-450): Digital-Analog transition zone
  Cause: High fanout nets crossing routing channel
  Severity: Orange (0.78-0.82)

- (100-200, 600-700): DSP core area
  Cause: Dense arithmetic logic
  Severity: Yellow (0.72-0.78)
```

## Congestion Mitigation Techniques

### Cell Density Reduction

```tcl
# Reduce max density in congested areas
set_db place_global_max_density 0.65

# Create density constraint regions
createDensityConstraint -region {300 300 500 500} \
    -maxDensity 0.60 -weight 1.0

# Re-place with constraints
setOptMode -fixFanoutLoad true
place_design -incremental
```

### Routing Resource Optimization

```tcl
# Add routing blockages to redirect traffic
createRouteBlk -box {350 350 450 450} -layer {M3}

# Enable additional routing layers
setNanoRouteMode -routeWithViaInPin true
setNanoRouteMode -routeWithViaOnlyForStandardCellPin auto

# Allow jog routing
setNanoRouteMode -routeWithJog true
setNanoRouteMode -routeWithMinimizeViaCountEffort high
```

### Cell Spreading

```tcl
# Spread cells in congested regions
setSpreadMode -region {350 350 450 450} -spreadFactor 1.3

# Or manually spread specific cells
set cells_to_spread [get_cells -of_objects [get_nets -of_objects \
    [get_timing_paths -max_paths 10]]]

spreadInst $cells_to_spread -direction horizontal -spacing 2.0
```

### Net Restructuring

```tcl
# Re-route high-congestion nets
set congested_nets [get_congested_nets -threshold 0.85]

foreach_in_collection net $congested_nets {
    # Try alternative routing
    setPreferredNet -net $net -layer {M4 M5}
    routeDesign -selectedNet -net $net
}

# Report improvement
reportCongestion -overflow -output reports/post_mitigation.rpt
```

## Channel Congestion

### Routing Channel Analysis

```tcl
# Define routing channels
set channels {
    {name digital_analog_channel box {580 0 620 500} layer {M3 M4 M5}}
    {name memory_digital_channel box {0 480 600 500} layer {M3 M4 M5}}
    {name clock_channel box {0 0 980 20} layer {M6}}
}

# Analyze each channel
foreach ch $channels {
    set name [dict get $ch name]
    set box [dict get $ch box]
    set layers [dict get $ch layer]

    set width [expr {[lindex $box 2] - [lindex $box 0]}]
    set height [expr {[lindex $box 3] - [lindex $box 1]}]

    # Count nets crossing channel
    set crossing_nets [get_nets_crossing_box $box]

    puts "Channel: $name"
    puts "  Size: ${width} x ${height} um"
    puts "  Layers: $layers"
    puts "  Crossing nets: [llength $crossing_nets]"

    # Available tracks
    set available [calculate_available_tracks $width $layers]
    puts "  Available tracks: $available"
    puts "  Utilization: [expr {[llength $crossing_nets] / double($available) * 100}]%"
}
```

### Channel Widening

```tcl
# If channel is congested, widen it
# Move adjacent blocks to create more space

# Original: 20 um channel
# Widened: 30 um channel
moveInstGroup digital_subsystem -shift {0 15}
moveInstGroup memory_subsystem -shift {0 15}

# Re-analyze
reportCongestion -box {580 0 620 500} -output reports/channel_widened.rpt
```

## Bus Routing Congestion

### Identifying Bus Congestion

```tcl
# Find bus structures in design
report_bus_nets -file reports/bus_analysis.rpt

# Bus nets often cause localized congestion
# Example: 32-bit data bus crossing digital-analog boundary

set bus_nets [get_db nets -if {.name == "data_bus[*]"}]
set bus_count [sizeof_collection $bus_nets]

puts "Bus width: $bus_count"
puts "Bus crossing region: need $bus_count parallel tracks"

# Available tracks in M3: 16 per Gcell
# If bus > 16 bits, need multi-layer routing
```

### Bus Routing Strategy

```tcl
# Assign bus to preferred layers
foreach_in_collection net $bus_nets {
    set bus_idx [get_bus_index $net]

    # Alternate layers for bus signals
    if {$bus_idx % 2 == 0} {
        setNetStat -net [get_db $net .name] -preferredLayer M3
    } else {
        setNetStat -net [get_db $net .name] -preferredLayer M4
    }
}

# Use wide vias for bus crossings
setNanoRouteMode -routeWithMinimizeViaCountEffort high
```

## Power Grid Impact on Congestion

### Power Routing Overhead

```tcl
# Analyze how power grid affects signal routing
report_pg_utilization -file reports/pg_utilization.rpt

# M5/M6 used heavily for power
# Leaves less capacity for signals on these layers

# Calculate effective signal capacity
set power_m5_util 0.40  ;# 40% of M5 used for power
set power_m6_util 0.30  ;# 30% of M6 used for power

# Remaining for signals
set signal_m5_capacity [expr {(1.0 - $power_m5_util) * 10}]
set signal_m6_capacity [expr {(1.0 - $power_m6_util) * 6}]

puts "M5 signal capacity: $signal_m5_capacity tracks/Gcell"
puts "M6 signal capacity: $signal_m6_capacity tracks/Gcell"
```

### Optimizing Power-Signal Tradeoff

```tcl
# If power grid is too dense, reduce it
# Move power straps to higher layers only

# Instead of M5+M6, use M6 only for power
# Frees up M5 for signal routing

# Remove M5 power stripes
editRoute -deleteStripe -net {VDD VSS} -layer M5

# Add more M6 power stripes instead
addStripe -nets {VDD VSS} -layer M6 \
    -width 20.0 -spacing 10.0 \
    -set_to_set_distance 80.0
```

## Congestion-Driven Placement Iteration

### Iterative Flow

```tcl
proc congestion_driven_flow {max_iterations} {
    for {set iter 1} {$iter <= $max_iterations} {incr iter} {
        puts "=== Iteration $iter ==="

        # Place
        set_db place_global_max_density [expr {0.7 - $iter * 0.02}]
        place_design

        # Analyze congestion
        set max_congestion [get_db designs .max_overflow]
        set overflow_count [get_db designs .overflow_count]

        puts "Max overflow: $max_congestion"
        puts "Overflow count: $overflow_count"

        # Decision
        if {$max_congestion < 0.8 && $overflow_count < 10} {
            puts "Congestion acceptable at iteration $iter"
            break
        }

        # Apply mitigation
        setDb place_global_max_density_limit [expr {0.65 - $iter * 0.02}]
        place_design -incremental

        # Report
        reportCongestion -output reports/congestion_iter_${iter}.rpt
    }
}

congestion_driven_flow 5
```

## Post-Route Congestion Verification

### Final Congestion Check

```tcl
# After routing, verify no congestion-induced violations
reportCongestion -file reports/final_congestion.rpt

# Check for DRC violations caused by congestion
verify_drc -limit 100 -report reports/congestion_drc.rpt

# Verify all nets routed
reportRoute -summary > reports/route_summary.rpt

# Check for open nets
verifyConnectivity -type regular -report reports/opens.rpt
```

## iPACE-CHIP Congestion Summary

### Final Congestion Metrics

| Layer | Max Util | Overflow Gcells | Status |
|-------|----------|----------------|--------|
| M3 | 88.7% | 12 | Resolved |
| M4 | 94.4% | 23 | Resolved |
| M5 | 78.0% | 0 | OK |
| M6 | 53.3% | 0 | OK |

### Mitigation Applied

| Technique | Iteration | Overflow Reduction |
|-----------|-----------|-------------------|
| Density reduction 0.7 to 0.65 | 1 | 45 → 28 |
| Routing blockage at channel | 2 | 28 → 15 |
| Cell spreading in DSP area | 3 | 15 → 8 |
| Bus layer assignment | 4 | 8 → 0 |

## Summary

Congestion analysis for iPACE-CHIP identifies routing hotspots primarily in the digital-analog transition zone and DSP arithmetic block. Four iterations of mitigation — density reduction, routing blockages, cell spreading, and bus layer assignment — resolve all overflow Gcells. Final congestion metrics show 0 overflow with maximum layer utilization below 95%, ensuring successful detailed routing.
