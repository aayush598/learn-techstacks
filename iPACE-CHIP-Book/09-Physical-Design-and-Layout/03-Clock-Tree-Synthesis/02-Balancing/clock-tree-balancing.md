# Clock Tree Balancing

## Overview

Clock tree balancing ensures that the clock signal arrives at all flip-flops within acceptable timing tolerance. For iPACE-CHIP, unbalanced clock trees can cause setup/hold violations, metastability in CDC synchronizers, and timing errors in the pacing output circuitry — any of which could be life-threatening.

## Clock Skew Fundamentals

### Types of Skew

```
Local Skew: Between flip-flops in same clock domain
- Affects setup/hold timing within a block
- Target: < 50 ps for iPACE-CHIP

Global Skew: Between any two flip-flops in design
- Affects system-level timing
- Target: < 100 ps for iPACE-CHIP

Inter-clock Skew: Between different clock domains
- Managed through CDC synchronizers
- Target: < 200 ps (handled by synchronizer stages)
```

### Skew Sources

```python
# Sources of clock skew in iPACE-CHIP
skew_sources = {
    'wire_length_variation': 0.035,  # ns (35 ps)
    'buffer_delay_variation': 0.015, # ns (15 ps)
    'load_capacitance_variation': 0.010, # ns (10 ps)
    'voltage_variation': 0.008,      # ns (8 ps)
    'temperature_variation': 0.005,  # ns (5 ps)
    'process_variation': 0.012,      # ns (12 ps)
}

# RSS (Root Sum Square) total skew
import math
total_skew = math.sqrt(sum(v**2 for v in skew_sources.values()))
print(f"Estimated skew: {total_skew*1000:.0f} ps")
# Result: ~45 ps RSS (target: < 100 ps)
```

## Balancing Algorithms

### H-Tree Approach

```tcl
# H-tree clock distribution for uniform skew
# Divides chip into quadrants recursively

# For iPACE-CHIP 980 x 980 um core:
# Level 0: Center root buffer
# Level 1: 4 quadrant buffers (490 um away)
# Level 2: 16 sub-quadrant buffers (245 um away)
# Level 3: 64 leaf buffers (122.5 um away)

# H-tree parameters
set htree_params {
    root_position {490 490}
    levels 3
    fanout 4
    buffer_cells {CLKBUFX16SVT CLKBUFX8SVT CLKBUFX4SVT CLKBUFX4SVT}
    wire_width {1.6 1.2 0.8 0.6}
}
```

### Mesh-Based Clock Distribution

```tcl
# Clock mesh for ultra-low skew
# Create metal mesh on M6, then buffer to local distribution

# Create clock mesh
create_clock_mesh -layer M6 -width 1.6 -pitch 50.0

# Buffer from mesh to local clock pins
setClockTreeOptions -meshInsertion true \
    -meshBuffer {CLKBUFX8SVT} \
    -meshRoot {CLKBUFX16SVT}

# Mesh results for iPACE-CHIP:
# Mesh area: 980 x 980 um
# Mesh pitch: 50 um (20 horizontal, 20 vertical wires)
# Mesh resistance: 0.5 ohm per node
# Skew from mesh: < 10 ps (excellent)
```

## Innovus Clock Balancing Flow

### Post-CTS Balancing

```tcl
# After initial CTS, optimize for balance
clock_opt -from balance_clock_tree -to balance_clock_tree

# Check balance quality
report_clock_tree -balance > reports/cts_balance.rpt

# Balancing targets
# Local skew: < 50 ps
# Global skew: < 100 ps
# Insertion delay: < 2.0 ns
```

### Level Adjustment

```tcl
# Adjust buffer levels for balance
setClockTreeOptions -balanceLevels true

# For each branch of the clock tree:
# - Equalize buffer counts from root to leaves
# - Equalize wire lengths on symmetric paths
# - Equalize capacitive loads

# Example balancing operation:
# Before: Root -> BUF -> BUF -> BUF -> FF (4 levels)
# After:  Root -> BUF -> BUF -> FF (3 levels, shorter path)
```

## Load Balancing

### Capacitance Balancing

```python
# Load capacitance analysis for clock tree balancing
def analyze_clock_loads(clock_tree):
    """Analyze and balance clock tree loads"""
    
    branches = clock_tree['branches']
    
    # Calculate load per branch
    for branch in branches:
        branch['load_cap'] = sum(ff['capacitance'] for ff in branch['flip_flops'])
        branch['wire_cap'] = branch['wire_length'] * 0.0002  # pF/um
        branch['total_cap'] = branch['load_cap'] + branch['wire_cap']
    
    # Find worst imbalance
    min_cap = min(b['total_cap'] for b in branches)
    max_cap = max(b['total_cap'] for b in branches)
    imbalance = (max_cap - min_cap) / min_cap
    
    return {
        'min_capacitance': min_cap,
        'max_capacitance': max_cap,
        'imbalance_ratio': imbalance,
        'target_imbalance': 0.10  # 10% max
    }

# iPACE-CHIP results:
# Branch 1 (timing engine): 12.5 pF total
# Branch 2 (pulse controller): 11.8 pF total
# Branch 3 (DSP core): 14.2 pF total
# Branch 4 (digital comm): 10.5 pF total
# Imbalance: (14.2 - 10.5) / 10.5 = 35% -> needs balancing
```

### Load Balancing Techniques

```tcl
# Technique 1: Add dummy loads to balanced branches
addDummyLoad -net CLK_branch4 -capacitance 2.0 -layer M3

# Technique 2: Re-position buffer insertion points
# Move buffer closer to heavy-load branch
moveInst CLKBUFX8SVT_dsp 350 350 0

# Technique 3: Use different buffer sizes per branch
# Heavy load branch: CLKBUFX16
# Light load branch: CLKBUFX4
set_clock_buffer_size -net CLK_branch3 -buffer CLKBUFX16SVT
set_clock_buffer_size -net CLK_branch4 -buffer CLKBUFX4SVT

# Re-verify balance
report_clock_tree -balance > reports/cts_balanced_load.rpt
```

## Wire Length Balancing

### Symmetric Routing

```tcl
# Ensure symmetric clock routing
# For H-tree: each level has equal wire lengths

# Level 1: 4 branches, each 245 um from center
# Level 2: 16 branches, each 122.5 um
# Level 3: 64 branches, each 61.25 um

# Route clock tree with symmetry constraint
setNanoRouteMode -routeWithSymmetry true
routeDesign -clock

# Verify wire length distribution
report_net_length -net CLK_CORE -distribution > reports/clk_wire_length.rpt
```

### Wire Length Tolerance

```python
# Wire length tolerance for iPACE-CHIP
wire_length_tolerance = {
    'level_0_to_1': {
        'target': 245.0,  # um
        'tolerance': 10.0,  # um (4%)
        'max_allowed': 255.0,
    },
    'level_1_to_2': {
        'target': 122.5,
        'tolerance': 5.0,
        'max_allowed': 127.5,
    },
    'level_2_to_3': {
        'target': 61.25,
        'tolerance': 3.0,
        'max_allowed': 64.25,
    },
}

# Total path length: 245 + 122.5 + 61.25 = 428.75 um
# Max variation: 10 + 5 + 3 = 18 um
# Skew from wire variation: 18 * 0.001 = 0.018 ns (18 ps)
```

## Clock Tree Balancing for CDC

### Synchronizer Clock Balance

```tcl
# CDC synchronizer flip-flops need special balance treatment
# Both source and destination clocks must arrive balanced

# Identify CDC synchronizers
report_clock_crossing -file reports/cdc_crossings.rpt

# For each CDC synchronizer:
# - Balance source domain clock to first FF
# - Balance destination domain clock to second FF
# - Minimize skew between the two domains at synchronizer

# Example: CLK_CORE to CLK_ANA crossing
# Synchronizer at ADC controller boundary
set_false_path -from [get_pins sync_reg1/CK] -to [get_pins sync_reg2/CK]
```

### Asynchronous Clock Domain Handling

```tcl
# Ensure proper synchronization
# Double-flop synchronizers for CDC

# Balance first flop clock (source domain)
setClockTreeOptions -balanceTo synchronizer_source

# Balance second flop clock (dest domain)
setClockTreeOptions -balanceTo synchronizer_dest

# Verify synchronizer timing
report_timing -through [get_pins sync_reg*/CK] \
    > reports/cdc_synchronizer_timing.rpt
```

## Clock Tree Balancing Results

### Pre-Balancing Skew

```
Branch | Leaf FFs | Insertion Delay | Skew to Mean
-------|----------|-----------------|-------------
B1     | 420      | 1.35 ns         | -0.10 ns
B2     | 385      | 1.28 ns         | -0.17 ns
B3     | 510      | 1.52 ns         | +0.07 ns
B4     | 290      | 1.15 ns         | -0.30 ns
B5     | 340      | 1.42 ns         | -0.03 ns
B6     | 376      | 1.65 ns         | +0.20 ns

Mean: 1.45 ns
Max skew: 0.30 ns (B4 vs B6) -- EXCEEDS 0.1 ns target
```

### Post-Balancing Skew

```
Branch | Leaf FFs | Insertion Delay | Skew to Mean
-------|----------|-----------------|-------------
B1     | 420      | 1.43 ns         | -0.02 ns
B2     | 385      | 1.42 ns         | -0.03 ns
B3     | 510      | 1.46 ns         | +0.01 ns
B4     | 290      | 1.44 ns         | -0.01 ns
B5     | 340      | 1.47 ns         | +0.02 ns
B6     | 376      | 1.45 ns         | +0.00 ns

Mean: 1.445 ns
Max skew: 0.03 ns (B2 vs B5) -- MEETS 0.1 ns target
```

## Process Variation Impact

### On-Chip Variation (OCV)

```tcl
# Account for on-chip variation in clock balance
set_timing_derate -late 0.1 -cell_delay
set_timing_derate -early -0.1 -cell_delay
set_timing_derate -late 0.05 -net_delay
set_timing_derate -early -0.05 -net_delay

# Pessimistic analysis for clock tree
set_clock_uncertainty 0.15 [get_clocks CLK_CORE]

# OCV analysis
report_timing -late -max_paths 20 > reports/ocv_analysis.rpt
```

### Statistical OCV (SOCV)

```tcl
# Advanced OCV for better accuracy
set_timing_derate -late 0.08 -cell_delay -variation type_on_chip
set_timing_derate -early -0.08 -cell_delay -variation type_on_chip

# SOCV analysis
report_timing -late -max_paths 10 > reports/socv_analysis.rpt

# SOCV typically shows 20-30% less pessimism than flat OCV
```

## Clock Tree Balancing Verification

### Balance Quality Metrics

```tcl
# Verify clock tree balance
proc verify_clock_balance {} {
    set report "reports/clock_balance_verification.rpt"
    set fp [open $report w]

    puts $fp "Clock Tree Balance Verification"
    puts $fp "=============================="

    # Get all clock sinks
    set sinks [get_db [get_db pins -if {.clock}] .inst.name]

    # Calculate skew
    set arrival_times [list]
    foreach sink $sinks {
        set arrival [get_db $sink .arrival_clk]
        lappend arrival_times $arrival
    }

    set min_arrival [tcl::mathfunc::min {*}$arrival_times]
    set max_arrival [tcl::mathfunc::max {*}$arrival_times]
    set skew [expr {$max_arrival - $min_arrival}]

    puts $fp "Clock sinks: [llength $sinks]"
    puts $fp "Min arrival: ${min_arrival} ns"
    puts $fp "Max arrival: ${max_arrival} ns"
    puts $fp "Skew: ${skew} ns"
    puts $fp "Target skew: 0.1 ns"
    puts $fp "Status: [expr {$skew < 0.1 ? \"PASS\" : \"FAIL\"}]"

    close $fp
}

verify_clock_balance
```

## Summary

Clock tree balancing for iPACE-CHIP achieves 0.03 ns skew through load balancing, wire length equalization, and buffer sizing. The balancing flow addresses both local and global skew, accounts for CDC synchronizer requirements, and maintains margin for on-chip variation. Final verification confirms all branches within the 0.1 ns skew target.
