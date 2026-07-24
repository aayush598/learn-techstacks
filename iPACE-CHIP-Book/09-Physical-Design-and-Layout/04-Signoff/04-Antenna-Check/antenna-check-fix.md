# Antenna Check and Fix

## Overview

Antenna effects occur during manufacturing when long metal traces accumulate charge from plasma etching processes. This charge can damage thin gate oxides in connected transistors. For iPACE-CHIP, antenna violations must be zero — a damaged gate oxide could cause latent defects that manifest years after implantation.

## Antenna Effect Fundamentals

### How Antenna Damage Occurs

```
Manufacturing Process:

1. Metal layer deposition
   - Long metal trace connected to transistor gate
   - Trace acts as antenna, collecting charge from plasma

2. Charge accumulation
   - Charge builds up on metal trace
   - No path to discharge (transistor gate is isolated oxide)

3. Gate oxide damage
   - Charge punches through thin gate oxide
   - Creates trapped charge or oxide breakdown
   - Results in: threshold voltage shift, leakage, or failure

4. Recovery (partial)
   - Subsequent metal layers can provide discharge path
   - But damage from earlier layers may already be done
```

### Antenna Ratio

```python
# Antenna ratio calculation
# Ratio = Metal area connected to gate / Gate oxide area

def antenna_ratio(metal_area_um2, gate_width_um, gate_length_um,oxide_thickness_nm):
    """Calculate antenna ratio"""
    gate_area = gate_width_um * gate_length_um
    
    # For thin oxide: max ratio depends on process
    # BCD 180nm: max ratio = 100 for metal, 500 for via
    
    ratio = metal_area_um2 / gate_area
    max_ratio = 100  # for M1-M6 connected to gates
    
    return {
        'ratio': ratio,
        'max_allowed': max_ratio,
        'violation': ratio > max_ratio,
        'severity': 'VIOLATION' if ratio > max_ratio else 'OK'
    }

# Example: long M3 net connected to a flip-flop gate
result = antenna_ratio(
    metal_area_um2=50000,    # 50,000 um^2 metal trace
    gate_width_um=0.36,      # minimum width transistor
    gate_length_um=0.18,     # 180nm gate length
    oxide_thickness_nm=4.0   # thin oxide
)

print(f"Antenna ratio: {result['ratio']:.0f}")
print(f"Max allowed: {result['max_allowed']}")
print(f"Status: {result['severity']}")
# Ratio: 771,605 >> 100 = VIOLATION
```

## Antenna Check Flow

### Setup and Execution

```tcl
# Antenna check configuration
set_db design_process_node 180

# Set antenna rules per technology
set_antenna_rule -layer M1 -ratio 100
set_antenna_rule -layer M2 -ratio 100
set_antenna_rule -layer M3 -ratio 100
set_antenna_rule -layer M4 -ratio 100
set_antenna_rule -layer M5 -ratio 100
set_antenna_rule -layer M6 -ratio 100
set_antenna_rule -via VIA12 -ratio 500
set_antenna_rule -via VIA23 -ratio 500
set_antenna_rule -via VIA34 -ratio 500
set_antenna_rule -via VIA45 -ratio 500
set_antenna_rule -via VIA56 -ratio 500

# Run antenna check
verifyProcessAntenna -report reports/antenna_check.rpt

# Results
set antenna_violations [get_db designs .antenna_violation_count]
puts "Antenna violations: $antenna_violations"
```

### Antenna Check Results

```python
# Antenna check results for iPACE-CHIP
antenna_results = {
    'pre_fix': {
        'total_violations': 47,
        'metal_violations': 35,
        'via_violations': 12,
        'worst_ratio': 2850,
        'affected_nets': 42,
    },
    'post_fix': {
        'total_violations': 0,
        'diode_insertions': 52,
        'buffer_insertions': 8,
        'metal_jumps': 15,
        'worst_remaining_ratio': 85,
    }
}

print("Antenna Check Results (Pre-Fix):")
print(f"  Total violations: {antenna_results['pre_fix']['total_violations']}")
print(f"  Metal violations: {antenna_results['pre_fix']['metal_violations']}")
print(f"  Via violations: {antenna_results['pre_fix']['via_violations']}")
print(f"  Worst ratio: {antenna_results['pre_fix']['worst_ratio']}")

print("\nAntenna Check Results (Post-Fix):")
print(f"  Total violations: {antenna_results['post_fix']['total_violations']}")
print(f"  Diode insertions: {antenna_results['post_fix']['diode_insertions']}")
print(f"  Buffer insertions: {antenna_results['post_fix']['buffer_insertions']}")
print(f"  Metal jumps: {antenna_results['post_fix']['metal_jumps']}")
```

## Antenna Fix Techniques

### Diode Protection

```tcl
# Add protection diodes to gate-connected nets
# Diodes provide discharge path during manufacturing

# Antenna diode cell from standard cell library
set antenna_diode ANTENNA_NW2HD

# Auto-insert antenna diodes
ecoAddDiode -cell $antenna_diode -net {violating_net}

# For each violation, insert diode at gate connection point
proc fix_antenna_diode {net} {
    # Find gate connection point
    set gate_pin [get_db $net .driver_pins]

    # Insert diode between gate and metal
    ecoAddInst -cell ANTENNA_NW2HD -inst "ant_diode_${net}" \
        -location [get_db $gate_pin .location]

    # Connect diode to net
    ecoRoute -selectedNet -net $net
}

# Apply to all violations
set violations [get_violating_nets]
foreach net $violations {
    fix_antenna_diode $net
}
```

### Buffer Insertion

```tcl
# Insert buffers to break long antenna paths
# Buffer creates a new gate connection point, resetting ratio

proc fix_antenna_buffer {net max_ratio} {
    # Calculate where to insert buffer
    set metal_area [get_net_metal_area $net]
    set gate_area [get_net_gate_area $net]
    set current_ratio [expr {$metal_area / $gate_area}]

    if {$current_ratio > $max_ratio} {
        # Find midpoint of net
        set midpoint [find_net_midpoint $net]

        # Insert buffer
        ecoAddInst -cell BUFX4 -inst "ant_buf_${net}" \
            -location $midpoint

        # Reconnect net
        ecoRoute -selectedNet -net $net

        puts "Buffer inserted on $net at $midpoint"
    }
}

# Apply buffer insertion
foreach net [get_antenna_violating_nets] {
    fix_antenna_buffer $net 100
}
```

### Metal Layer Jumps

```tcl
# Add metal layer jumps to break antenna paths
# Route to higher layer and back down

proc fix_antenna_layer_jump {net} {
    # Find long metal segment
    set long_segment [find_longest_segment $net]

    # Add via up to higher layer
    set via_point [lindex $long_segment [expr {[llength $long_segment] / 2}]]

    # Jump to M5 (higher layer with larger ratio limit)
    editRoute -net $net -via {VIA45} -point $via_point
    editRoute -net $net -layer M5 -point $via_point

    # Jump back down after some distance
    set return_point [expr {[lindex $via_point 0] + 50}]
    editRoute -net $net -via {VIA45} -point [list $return_point [lindex $via_point 1]]
    editRoute -net $net -layer M4 -point [list $return_point [lindex $via_point 1]]
}
```

## Antenna Fix Automation

### Complete Fix Script

```tcl
proc fix_all_antenna_violations {} {
    set fix_pass 0
    set max_passes 5

    while {$fix_pass < $max_passes} {
        incr fix_pass
        puts "=== Antenna Fix Pass $fix_pass ==="

        # Run antenna check
        verifyProcessAntenna -report reports/antenna_pass_${fix_pass}.rpt

        set violations [get_db designs .antenna_violation_count]
        puts "Violations found: $violations"

        if {$violations == 0} {
            puts "All antenna violations fixed!"
            break
        }

        # Fix strategy per pass:
        switch $fix_pass {
            1 {
                # Pass 1: Add diodes
                puts "Adding antenna protection diodes..."
                ecoAddDiode -cell ANTENNA_NW2HD -allViolation
            }
            2 {
                # Pass 2: Insert buffers on worst violations
                puts "Inserting buffers for worst violations..."
                set worst [get_worst_antenna_violations -count 10]
                foreach net $worst {
                    ecoAddInst -cell BUFX4 -inst "ant_buf_${net}" \
                        -location [find_net_midpoint $net]
                }
            }
            3 {
                # Pass 3: Metal layer jumps
                puts "Adding metal layer jumps..."
                set remaining [get_antenna_violating_nets]
                foreach net $remaining {
                    fix_antenna_layer_jump $net
                }
            }
            4 {
                # Pass 4: Wire widening
                puts "Widening narrow wires..."
                set remaining [get_antenna_violating_nets]
                foreach net $remaining {
                    set width [get_db $net .min_width]
                    editRoute -net $net -width [expr {$width * 2}]
                }
            }
            5 {
                # Pass 5: Last resort - re-route
                puts "Re-routing remaining violations..."
                set remaining [get_antenna_violating_nets]
                foreach net $remaining {
                    editRoute -net $net -route
                }
            }
        }

        # Re-route after fixes
        ecoRoute

        # Verify DRC after fixes
        verify_drc -limit 100 -report reports/antenna_fix_drc_${fix_pass}.rpt
    }

    # Final check
    verifyProcessAntenna -report reports/antenna_final.rpt
    set final_violations [get_db designs .antenna_violation_count]
    puts "Final antenna violations: $final_violations"
}

fix_all_antenna_violations
```

## Antenna Fix Impact Analysis

### Area Overhead

```python
# Area impact of antenna fixes
area_impact = {
    'diode_insertions': {
        'count': 52,
        'area_per_diode_um2': 12.0,
        'total_area_um2': 624,
    },
    'buffer_insertions': {
        'count': 8,
        'area_per_buffer_um2': 14.4,
        'total_area_um2': 115.2,
    },
    'metal_jumps': {
        'count': 15,
        'area_overhead_per_jump_um2': 5.0,
        'total_area_um2': 75.0,
    },
    'wire_widening': {
        'count': 12,
        'area_overhead_per_net_um2': 25.0,
        'total_area_um2': 300.0,
    },
}

total_overhead = sum(d['total_area_um2'] for d in area_impact.values())
total_chip_area = 980 * 980  # um^2 core area
overhead_pct = total_overhead / total_chip_area * 100

print("Antenna Fix Area Impact:")
for technique, data in area_impact.items():
    print(f"  {technique}: {data['total_area_um2']:.1f} um^2 ({data['count']} instances)")
print(f"\nTotal overhead: {total_overhead:.1f} um^2")
print(f"Percentage of core: {overhead_pct:.3f}%")
```

### Timing Impact

```python
# Timing impact of antenna fixes
timing_impact = {
    'diode_leakage': {
        'additional_leakage_nA': 0.5,
        'total_leakage_uA': 0.026,
    },
    'buffer_delay': {
        'added_delay_ps': 80,
        'affected_paths': 8,
        'impact_on_critical_path': 'negligible',
    },
}

print("Timing Impact:")
print(f"  Additional leakage: {timing_impact['diode_leakage']['total_leakage_uA']:.3f} uA")
print(f"  Buffer delay: {timing_impact['buffer_delay']['added_delay_ps']} ps per insertion")
print(f"  Critical path impact: {timing_impact['buffer_delay']['impact_on_critical_path']}")
```

## Antenna Rules Summary

### iPACE-CHIP Antenna Specifications

| Parameter | Rule | Value |
|-----------|------|-------|
| Metal antenna ratio | Max ratio | 100:1 |
| Via antenna ratio | Max ratio | 500:1 |
| Thin oxide max ratio | Max ratio | 100:1 |
| Thick oxide max ratio | Max ratio | 200:1 |
| Protection diode | Minimum size | 2 um width |
| Buffer insertion | Minimum drive | BUFX2 |

### Worst-Case Violations (Pre-Fix)

| Net | Metal Layer | Ratio | Max Allowed | Over-Design |
|-----|-------------|-------|-------------|-------------|
| sense_rv_buf | M3 | 2,850 | 100 | 28.5x |
| pace_output | M6 | 1,200 | 100 | 12.0x |
| data_bus[15] | M4 | 950 | 100 | 9.5x |
| clk_core_drv | M5 | 820 | 100 | 8.2x |
| config_data[7] | M3 | 680 | 100 | 6.8x |

## Summary

Antenna check for iPACE-CHIP identifies 47 violations, all fixed through a combination of diode insertion (52 instances), buffer insertion (8 instances), metal layer jumps (15 instances), and wire widening (12 instances). Post-fix analysis confirms zero violations with 0.12% area overhead and negligible timing impact. All antenna rules are satisfied for the 180nm BCD process.
