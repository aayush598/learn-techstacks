# Sensitivity Layout Rules

## Overview

Sensitivity layout rules define special design constraints for analog and mixed-signal circuits in the iPACE-CHIP pacemaker ASIC. These rules go beyond standard DRC to address performance-sensitive requirements such as matching, noise, leakage, and reliability that are critical for implantable medical device operation.

## Sensitivity Classification

### Block Sensitivity Levels

```python
# Sensitivity classification for iPACE-CHIP blocks
sensitivity_levels = {
    'CRITICAL': {
        'blocks': ['heart_signal_adc', 'sense_amplifier', 'bandgap_ref'],
        'description': 'Directly affects patient safety',
        'rules': ['tightest_matching', 'minimum_noise', 'maximum_isolation'],
    },
    'HIGH': {
        'blocks': ['impedance_adc', 'charge_pump', 'sample_hold'],
        'description': 'Affects measurement accuracy',
        'rules': ['tight_matching', 'low_noise', 'good_isolation'],
    },
    'MODERATE': {
        'blocks': ['ldo_regulator', 'voltage_reference', 'analog_mux'],
        'description': 'Affects circuit performance',
        'rules': ['standard_matching', 'moderate_noise'],
    },
    'LOW': {
        'blocks': ['digital_controller', 'timing_engine', 'comm_interface'],
        'description': 'Digital logic, standard rules apply',
        'rules': ['standard_drc'],
    },
}

print("Sensitivity Classification:")
for level, data in sensitivity_levels.items():
    print(f"\n{level} ({len(data['blocks'])} blocks):")
    print(f"  Description: {data['description']}")
    print(f"  Blocks: {', '.join(data['blocks'])}")
    print(f"  Rules: {', '.join(data['rules'])}")
```

## Critical Sensitivity Rules

### Rule S1: Matching Precision

```tcl
# S1: Matching precision rules for differential pairs
# Critical for sense amplifier and ADC

# Rule: Differential pair transistors must be within 20 um of each other
# Rule: Same orientation (no mirroring)
# Rule: Common-centroid or interdigitated layout
# Rule: Minimum 10 um dummy devices on all sides

# Implementation
proc check_matching_rules {cell_name} {
    set diff_pair [get_diff_pair $cell_name]
    set device1 [lindex $diff_pair 0]
    set device2 [lindex $diff_pair 1]

    # Check distance
    set loc1 [get_db $device1 .location]
    set loc2 [get_db $device2 .location]
    set distance [expr {sqrt(([lindex $loc1 0] - [lindex $loc2 0])**2 +
                             ([lindex $loc1 1] - [lindex $loc2 1])**2)}]

    if {$distance > 20.0} {
        puts "VIOLATION: $cell_name diff pair distance = $distance um > 20 um"
        return 0
    }

    # Check orientation
    set orient1 [get_db $device1 .orient]
    set orient2 [get_db $device2 .orient]
    if {$orient1 ne $orient2} {
        puts "VIOLATION: $cell_name diff pair orientation mismatch"
        return 0
    }

    puts "PASS: $cell_name matching rules satisfied"
    return 1
}
```

### Rule S2: Noise Floor

```python
# S2: Noise floor requirements for sensitive analog blocks
noise_floor_requirements = {
    'heart_signal_adc': {
        'input_referred_noise_uv': 5.0,
        'snr_db': 60,
        'enob_bits': 10,
    },
    'sense_amplifier': {
        'input_referred_noise_uv': 2.0,
        'snr_db': 70,
        'enob_bits': 11.5,
    },
    'impedance_adc': {
        'input_referred_noise_uv': 10.0,
        'snr_db': 50,
        'enob_bits': 8.5,
    },
}

# Layout rules for noise:
# 1. Minimum 20 um spacing from digital blocks
# 2. Shield all sensitive inputs
# 3. Dedicated substrate taps
# 4. No digital signal routing within 30 um
# 5. Guard ring on all sensitive nodes

print("Noise Floor Requirements:")
for block, specs in noise_floor_requirements.items():
    print(f"\n{block}:")
    for spec, value in specs.items():
        print(f"  {spec}: {value}")
```

### Rule S3: Leakage Control

```tcl
# S3: Leakage current control for high-impedance nodes
# Critical for sample-and-hold circuits

# Rule: Maximum leakage current = 1 pA at 25C
# Rule: Guard all high-impedance nodes
# Rule: No poly-to-diffusion overlap near sensitive nodes
# Rule: Minimum 50 um from high-voltage nodes

# Implementation for sample-and-hold
proc check_leakage_rules {node_name} {
    # Find high-impedance node
    set node [get_db nets $node_name]

    # Check guard ring
    set has_guard [check_guard_ring $node]
    if {!$has_guard} {
        puts "VIOLATION: $node_name missing guard ring"
        return 0
    }

    # Check distance from high-voltage nodes
    set min_distance [find_min_distance_to_hv $node]
    if {$min_distance < 50.0} {
        puts "VIOLATION: $node_name too close to HV node ($min_distance um)"
        return 0
    }

    puts "PASS: $node_name leakage rules satisfied"
    return 1
}
```

## Layout Rule Definitions

### Rule S4: Symmetry

```python
# S4: Symmetry rules for analog layout
symmetry_rules = {
    'axial_symmetry': {
        'description': 'Mirror symmetry along one axis',
        'application': 'Differential amplifiers, current mirrors',
        'tolerance_um': 0.5,
    },
    'point_symmetry': {
        'description': 'Rotational symmetry around center point',
        'application': 'Current steering DACs, charge redistribution ADCs',
        'tolerance_um': 0.5,
    },
    'translational_symmetry': {
        'description': 'Identical repeated structures',
        'application': 'Resistor ladders, capacitor arrays',
        'tolerance_um': 1.0,
    },
}

# Symmetry verification
def check_symmetry(device_group, symmetry_type):
    """Verify symmetry of device group"""
    if symmetry_type == 'axial':
        # Check mirror symmetry
        center = find_center(device_group)
        for device in device_group:
            mirror = find_mirror_position(device, center)
            if not is_device_at(mirror, device_group):
                return False, f"Asymmetric device at {device.location}"
    return True, "Symmetry satisfied"
```

### Rule S5: Orientation

```tcl
# S5: Device orientation rules
# Rule: All matched devices same orientation
# Rule: No mixing of N/P orientation in matched pairs
# Rule: Clockwise and counterclockwise placement alternating

# Orientation matrix for iPACE-CHIP analog blocks
set orientation_rules {
    heart_signal_adc {
        diff_pair: N          ;# All North
        current_mirror: N     ;# All North
        load_devices: N       ;# All North
    }
    impedance_adc {
        diff_pair: N          ;# All North
        current_mirror: N     ;# All North
        dac_elements: N       ;# All North
    }
    bandgap_ref {
        pnp_devices: N        ;# All North
        resistors: N          ;# All North
        opamp_inputs: N       ;# All North
    }
}
```

### Rule S6: Spacing

```tcl
# S6: Enhanced spacing rules for sensitive nodes
# Rule: Minimum 20 um from any digital signal
# Rule: Minimum 10 um from power supply lines
# Rule: Minimum 5 um from other analog signals (non-matched)
# Rule: Minimum 2 um from matched partner

# Spacing check
proc check_spacing_rules {sensitive_node} {
    set rules {
        {digital_signal 20.0}
        {power_supply 10.0}
        {analog_signal 5.0}
        {matched_partner 2.0}
    }

    foreach rule $rules {
        set type [lindex $rule 0]
        set min_dist [lindex $rule 1]

        set nearest [find_nearest $sensitive_node $type]
        set distance [get_distance $sensitive_node $nearest]

        if {$distance < $min_dist} {
            puts "VIOLATION: $sensitive_node too close to $type"
            puts "  Distance: $distance um, Required: $min_dist um"
            return 0
        }
    }
    return 1
}
```

## Design Rule Manual

### iPACE-CHIP Sensitivity Rule Summary

| Rule | Description | Parameter | Value |
|------|-------------|-----------|-------|
| S1 | Diff pair matching | Max distance | 20 um |
| S2 | Noise floor | Input noise | < 5 uV |
| S3 | Leakage control | Max leakage | 1 pA |
| S4 | Symmetry tolerance | Position match | 0.5 um |
| S5 | Orientation | All matched same | N/A |
| S6 | Digital spacing | Min distance | 20 um |
| S7 | Supply spacing | Min distance | 10 um |
| S8 | Guard ring width | Minimum width | 4 um |
| S9 | Dummy device width | Minimum width | 2 um |
| S10 | Via enclosure | Metal enclosure | 2x standard |

### Rule Priority

```python
# Rule priority for conflict resolution
rule_priority = {
    1: 'S1 - Matching precision (affects accuracy)',
    2: 'S2 - Noise floor (affects SNR)',
    3: 'S3 - Leakage control (affects sample integrity)',
    4: 'S8 - Guard ring (affects isolation)',
    5: 'S6 - Spacing (affects crosstalk)',
    6: 'S4 - Symmetry (affects matching)',
    7: 'S5 - Orientation (affects matching)',
    8: 'S9 - Dummy devices (affects edge effects)',
    9: 'S7 - Supply spacing (affects noise)',
    10: 'S10 - Via enclosure (affects reliability)',
}

print("Rule Priority (highest first):")
for priority, rule in rule_priority.items():
    print(f"  {priority}. {rule}")
```

## Verification Flow

### Automated Rule Checking

```tcl
# Automated sensitivity rule checking
proc verify_sensitivity_rules {} {
    set results {}

    # Check each sensitive block
    foreach block {heart_signal_adc impedance_adc bandgap_ref
                   sense_amplifier sample_hold charge_pump} {

        puts "Checking $block..."

        # S1: Matching
        set s1 [check_matching_rules $block]
        lappend results [list $block S1 $s1]

        # S3: Leakage
        set s3 [check_leakage_rules $block]
        lappend results [list $block S3 $s3]

        # S6: Spacing
        set s6 [check_spacing_rules $block]
        lappend results [list $block S6 $s6]
    }

    # Report results
    set violations [lmap r $results {expr {[lindex $r 2] == 0 ? $r : {}}}]
    set violation_count [llength [lmap v $v {if {$v ne ""} {return 1} else {return 0}}]]

    puts "\nSensitivity Rule Check Results:"
    puts "Total checks: [llength $results]"
    puts "Violations: $violation_count"

    return $results
}

verify_sensitivity_rules
```

### Signoff Checklist

```tcl
proc sensitivity_signoff {} {
    set checks {
        "S1: All diff pairs matched within 20 um"
        "S2: Noise floor met for all analog blocks"
        "S3: Leakage < 1 pA on all high-impedance nodes"
        "S4: Symmetry tolerance < 0.5 um"
        "S5: All matched devices same orientation"
        "S6: Digital spacing > 20 um from sensitive nodes"
        "S7: Supply spacing > 10 um from sensitive nodes"
        "S8: Guard rings minimum 4 um wide"
        "S9: Dummy devices minimum 2 um wide"
        "S10: Via enclosure 2x standard minimum"
    }

    puts "Sensitivity Rule Signoff:"
    puts "========================="
    foreach check $checks {
        puts "  [x] $check"
    }
}

sensitivity_signoff
```

## Summary

Sensitivity layout rules for iPACE-CHIP define ten specific design constraints covering matching precision, noise floor, leakage control, symmetry, orientation, and spacing. These rules are verified through automated checking scripts and apply with priority to CRITICAL and HIGH sensitivity blocks. Compliance ensures the pacemaker's analog measurement circuits achieve the accuracy required for reliable cardiac sensing and therapy delivery.
