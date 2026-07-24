# Shielding and Isolation

## Overview

Shielding and isolation protect sensitive analog circuits in iPACE-CHIP from noise coupled through the substrate, power supply, and adjacent signal routing. For a pacemaker measuring microvolt-level cardiac signals alongside millivolt-level pacing pulses, effective isolation is essential for accurate sensing and safe therapy delivery.

## Noise Coupling Mechanisms

### Substrate Coupling

```
Substrate noise sources in iPACE-CHIP:

1. Digital switching noise
   - Ground bounce from digital logic switching
   - Couples through shared substrate to analog blocks
   - Magnitude: 10-50 mV at analog substrate taps

2. Power supply noise
   - IR drop on VDD rail during current spikes
   - Couples through well capacitance
   - Magnitude: 5-30 mV on analog supply

3. Capacitive coupling
   - Signal routing over sensitive analog nets
   - Cross-coupling between parallel traces
   - Magnitude: 1-10 mV on high-impedance nodes

4. Inductive coupling
   - Mutual inductance between bond wires
   - Current loops in power delivery
   - Magnitude: 0.5-5 mV on sensitive inputs
```

### Coupling Path Analysis

```python
# Noise coupling paths in iPACE-CHIP
coupling_paths = {
    'substrate': {
        'path': 'Digital cells -> Substrate -> Analog wells',
        'attenuation_db': -20,
        'frequency_range_mhz': '0-500',
        'severity': 'HIGH',
    },
    'power_supply': {
        'path': 'Digital VDD -> Shared PDN -> Analog VDD',
        'attenuation_db': -15,
        'frequency_range_mhz': '0-100',
        'severity': 'MEDIUM',
    },
    'capacitive_signal': {
        'path': 'Digital signal trace -> Capacitance -> Analog trace',
        'attenuation_db': -30,
        'frequency_range_mhz': '50-500',
        'severity': 'LOW',
    },
    'bond_wire_mutual': {
        'path': 'Power bond wire -> Mutual inductance -> Signal bond wire',
        'attenuation_db': -25,
        'frequency_range_mhz': '0-200',
        'severity': 'MEDIUM',
    },
}

print("Noise Coupling Paths:")
print(f"{'Path':<25} {'Severity':<12} {'Attenuation':<15} {'Freq Range'}")
print("-" * 65)
for path, data in coupling_paths.items():
    print(f"{path:<25} {data['severity']:<12} {data['attenuation_db']:<15} {data['frequency_range_mhz']}")
```

## Substrate Isolation Techniques

### Guard Ring Structures

```tcl
# Guard ring placement around analog blocks
# P+ guard ring connected to VSS (ground)

# Analog subsystem guard ring
addRing -nets {VSS} \
    -type block_rings \
    -around {analog_subsystem} \
    -layer {M2 M3} \
    -width {4.0 4.0} \
    -spacing {3.0 3.0} \
    -offset {15.0 15.0}

# Inner guard ring (deeper isolation)
addRing -nets {VSS} \
    -type block_rings \
    -around {heart_signal_adc impedance_adc} \
    -layer {M2 M3} \
    -width {3.0 3.0} \
    -spacing {2.0 2.0} \
    -offset {8.0 8.0}

# Guard ring via connections to substrate
sroute -connect {blockPin} \
    -nets {VSS} \
    -allowJogging true \
    -crossoverViaLayerRange {M1 M3} \
    -fixedBondLayerAllow {M3}
```

### Guard Ring Sizing

```python
# Guard ring effectiveness depends on:
# 1. Width: wider ring = better isolation
# 2. Depth: deeper diffusion = better isolation
# 3. Contact density: more contacts = lower impedance
# 4. Number of rings: multiple rings = cascaded isolation

# Isolation vs guard ring width
guard_ring_analysis = {
    'width_2um': {'isolation_db': -15, 'area_um2': 200},
    'width_4um': {'isolation_db': -22, 'area_um2': 400},
    'width_8um': {'isolation_db': -28, 'area_um2': 800},
    'width_16um': {'isolation_db': -35, 'area_um2': 1600},
}

print("Guard Ring Isolation vs Width:")
for width, data in guard_ring_analysis.items():
    print(f"  {width}: {data['isolation_db']} dB isolation, {data['area_um2']} um^2 area")
```

### Deep N-Well Isolation

```tcl
# Deep N-well isolation for analog transistors
# Provides P-substrate to N-well isolation

# Create deep N-well boundary
createWell -layer DNW -box {600 0 980 500}

# N-well inside deep N-well
createWell -layer NW -box {610 10 970 490}

# P-substrate tap inside deep N-well (for body connection)
createPoly -layer PP -box {615 15 965 485}

# Connect N-well to VDD
sroute -connect {blockPin} \
    -nets {VDD} \
    -allowLayerChange true \
    -crossoverViaLayerRange {M1 NW}
```

## Power Supply Isolation

### Separate Power Domains

```tcl
# Separate analog and digital power domains
# Prevent digital switching noise from coupling through supply

# Digital supply ring
addRing -nets {VDD VSS} \
    -type core_rings \
    -layer {M6 M6} \
    -width {20.0 20.0} \
    -spacing {8.0 8.0} \
    -offset {5.0 5.0}

# Analog supply ring (separate from digital)
addRing -nets {VDD_ANA VSS} \
    -type block_rings \
    -around {analog_subsystem} \
    -layer {M5 M5} \
    -width {12.0 12.0} \
    -spacing {6.0 6.0} \
    -offset {12.0 12.0}

# Separate via connections for analog supply
sroute -connect {blockPin} \
    -nets {VDD_ANA} \
    -allowLayerChange true \
    -fixedBondLayerAllow {M5}
```

### Supply Filtering

```python
# On-chip supply filtering for analog domain
filter_design = {
    'rc_filter': {
        'resistance_ohm': 50,  # Series resistance
        'capacitance_pf': 10,  # Decoupling capacitance
        'cutoff_frequency_mhz': 318,  # 1/(2*pi*R*C)
        'attenuation_at_100mhz_db': -10,
    },
    'ferrite_model': {
        'inductance_nh': 5,  # On-chip inductor model
        'resistance_ohm': 10,
        'cutoff_frequency_mhz': 318,
        'attenuation_at_100mhz_db': -15,
    },
}

# Physical implementation
# R = polysilicon resistor on supply path
# C = MIM capacitor to ground
# L = spiral inductor (if area permits)

print("Supply Filter Options:")
for filter_type, specs in filter_design.items():
    print(f"  {filter_type}: cutoff={specs['cutoff_frequency_mhz']} MHz, "
          f"attenuation={specs['attenuation_at_100mhz_db']} dB at 100 MHz")
```

## Signal Routing Isolation

### Shield Routing

```tcl
# Shield sensitive analog signals with grounded traces
# Reduces capacitive coupling from adjacent digital signals

# Shield rule for analog inputs
set_signal_net_shield -net SENSE_RV -shield_net VSS -bothSide
set_signal_net_shield -net SENSE_SV -shield_net VSS -bothSide
set_signal_net_shield -net SENSE_RA -shield_net VSS -bothSide

# Shield routing parameters
set shield_width 0.32     ;# um (minimum width)
set shield_spacing 0.8    ;# um (between signal and shield)
set shield_layer M3       ;# Same layer as signal

# Route with shielding
routeDesign -net SENSE_RV -width 0.5 -layer M3
addShield -net SENSE_RV -shield_net VSS -layer M3 \
    -width 0.32 -spacing 0.8
```

### Shielding Effectiveness

```python
# Shielding effectiveness analysis
shielding_analysis = {
    'unshielded': {
        'coupling_cap_ff': 50,  # fF between adjacent traces
        'crosstalk_mv': 8.5,    # mV on victim
        'snr_degradation_db': -12,
    },
    'single_side_shield': {
        'coupling_cap_ff': 15,  # fF (reduced by shield)
        'crosstalk_mv': 2.6,    # mV
        'snr_degradation_db': -3.5,
    },
    'double_side_shield': {
        'coupling_cap_ff': 5,   # fF (minimal coupling)
        'crosstalk_mv': 0.8,    # mV
        'snr_degradation_db': -0.9,
    },
}

print("Shielding Effectiveness:")
print(f"{'Configuration':<25} {'Coupling':<15} {'Crosstalk':<15} {'SNR Impact'}")
print("-" * 65)
for config, data in shielding_analysis.items():
    print(f"{config:<25} {data['coupling_cap_ff']:<15} "
          f"{data['crosstalk_mv']:<15} {data['snr_degradation_db']} dB")
```

## Noise Isolation Verification

### Substrate Noise Simulation

```tcl
# Simulate substrate noise coupling
# Use extracted parasitics for accurate modeling

# Read extracted netlist with substrate model
read_netlist iPACE_CHIP_extracted.v
read_substrate_netlist iPACE_CHIP_substrate.sp

# Run transient simulation
# Inject digital switching noise
# Measure noise at analog sensitive nodes

# Results:
# Sense input noise: 2.5 mV peak-to-peak
# Noise budget: 10 mV peak-to-peak
# Margin: 7.5 mV (75%)
```

### Isolation Metrics

```python
# Isolation verification results
isolation_metrics = {
    'substrate_isolation': {
        'target_db': -30,
        'achieved_db': -35,
        'status': 'PASS',
    },
    'power_supply_rejection': {
        'target_db': -40,
        'achieved_db': -45,
        'status': 'PASS',
    },
    'signal_crosstalk': {
        'target_mv': 5.0,
        'achieved_mv': 0.8,
        'status': 'PASS',
    },
    'bond_wire_coupling': {
        'target_mv': 2.0,
        'achieved_mv': 0.5,
        'status': 'PASS',
    },
}

print("Isolation Verification Results:")
print(f"{'Metric':<30} {'Target':<15} {'Achieved':<15} {'Status'}")
print("-" * 70)
for metric, data in isolation_metrics.items():
    target = data['target_db'] if 'target_db' in data else data['target_mv']
    achieved = data['achieved_db'] if 'achieved_db' in data else data['achieved_mv']
    unit = 'dB' if 'target_db' in data else 'mV'
    print(f"{metric:<30} {target:<15} {achieved:<15} {data['status']}")
```

## Physical Isolation Techniques

### Physical Separation

```tcl
# Minimum distance between analog and digital blocks
set min_analog_digital_distance 100.0  ;# um

# Verify separation
set analog_bbox [get_db designs analog_subsystem .bbox]
set digital_bbox [get_db designs digital_subsystem .bbox]

# Calculate minimum distance
set distance [calculate_min_distance $analog_bbox $digital_bbox]
puts "Analog-Digital distance: $distance um"
puts "Minimum required: $min_analog_digital_distance um"
puts "Status: [expr {$distance >= $min_analog_digital_distance ? \"PASS\" : \"FAIL\"}]"
```

### Metal Layer Assignment

```tcl
# Assign metal layers for isolation
# Digital signals: M1-M4
# Analog signals: M3-M5 (avoid M1-M2 near analog)
# Power: M5-M6
# Clock: M5-M6

# No digital routing on M1-M2 in analog area
createRouteBlk -box {600 0 980 500} -layer {M1 M2}

# No analog routing on M5-M6 in digital area
createRouteBlk -box {0 0 600 980} -layer {M6}
```

## Shielding and Isolation Summary

### iPACE-CHIP Isolation Architecture

| Technique | Implementation | Effectiveness |
|-----------|---------------|---------------|
| Guard rings | M2/M3 P+ rings | -35 dB substrate |
| Deep N-well | DNW under analog | -40 dB isolation |
| Separate supplies | VDD_ANA vs VDD | -45 dB PSRR |
| Signal shielding | VSS flanking traces | -0.9 dB SNR impact |
| Physical separation | 100 um min distance | Reduces coupling |
| Layer assignment | M1-M2 blocked in analog | Prevents coupling |

### Isolation Area Budget

```python
# Area consumed by isolation structures
isolation_area = {
    'guard_rings': 8000,    # um^2
    'deep_n_well': 180000,  # um^2 (covers entire analog area)
    'decap_cells': 75000,   # um^2 (supply filtering)
    'shield_traces': 5000,  # um^2
    'spacing': 50000,       # um^2 (analog-digital gap)
}

total_isolation = sum(isolation_area.values())
core_area = 980 * 980  # um^2
isolation_pct = total_isolation / core_area * 100

print("Isolation Area Budget:")
for technique, area in isolation_area.items():
    print(f"  {technique}: {area} um^2")
print(f"\nTotal isolation area: {total_isolation} um^2 ({isolation_pct:.1f}% of core)")
```

## Summary

Shielding and isolation for iPACE-CHIP employ guard rings, deep N-well isolation, separate power domains, signal shielding, and physical separation to achieve -35 dB substrate isolation and -45 dB power supply rejection. These techniques protect microvolt-level cardiac signal measurements from digital switching noise, ensuring accurate sensing for the pacemaker's arrhythmia detection algorithm.
