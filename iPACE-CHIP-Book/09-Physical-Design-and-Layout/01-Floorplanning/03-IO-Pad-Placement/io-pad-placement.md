# IO Pad Placement

## Overview

IO pad placement defines how the iPACE-CHIP pacemaker ASIC interfaces with external components — the pacing leads, sensing electrodes, battery, telemetry antenna, and programming interface. Poor pad placement can introduce noise coupling, signal integrity issues, and packaging difficulties that compromise the entire implant.

## IO Pad Architecture

### Pad Types in iPACE-CHIP

| Pad Type | Count | Function | Special Requirements |
|----------|-------|----------|---------------------|
| VDD Power | 4 | Core supply | Low inductance, decap |
| VSS Ground | 4 | Return path | Multiple connections |
| VDD_ANA | 2 | Analog supply | Isolated from digital |
| Pace Output | 2 | Therapy delivery | High current, ESD |
| Sense Input | 2 | EGM acquisition | Low noise, high impedance |
| Impedance Meas | 2 | Lead impedance | 4-wire Kelvin |
| Telemetry | 2 | RF communication | 50 ohm match, isolated |
| SPI | 4 | Programming | Standard SPI interface |
| Test/DFT | 6 | Manufacturing test | Multiplexed functions |
| GPIO | 4 | General purpose | Configurable |
| NC/Reserved | 4 | Future use | Leave floating |
| **Total** | **36** | | |

### Pad Cell Library

```tcl
# Pad cell naming convention for BCD 180nm
# Format: PADTYPE_CELLNAME

set pad_cells {
    PAD_VDD33      ;# 3.3V tolerant power pad
    PAD_VSS        ;# Ground pad
    PAD_VDDIO      ;# 1.8V IO supply pad
    PAD_INOUT      ;# Bidirectional IO pad
    PAD_INPUT      ;# Input-only pad with ESD
    PAD_OUTPUT     ;# Output-only pad with ESD
    PAD_BIDIR      ;# Bidirectional with tri-state
    PAD_PACE       ;# High-current pace output
    PAD_SENSE      ;# Low-noise analog input
    PAD_RF         ;# RF antenna pad with matching
    PAD_SPI        ;# SPI dedicated pad
    PAD_TEST       ;# Test/DFT pad
    PAD_Filler     ;# Non-functional filler pad
}
```

## Pad Placement Constraints

### ESD Protection Requirements

Every pad must include electrostatic discharge protection rated for the iPACE-CHIP specifications:

```
ESD Rating Requirements:
- HBM (Human Body Model): >= 4 kV (medical implant standard)
- CDM (Charged Device Model): >= 500 V
- System-level ESD: >= 8 kV per IEC 61000-4-2

ESD Clamp Structure:
- Primary clamp: GCMOS diode clamp (50 pF, 1.5 kOhm)
- Secondary clamp: SCR-based clamp (fast turn-on)
- Series resistance: 200 Ohm on sensitive inputs
```

### Pad Size and Pitch

```tcl
# Pad dimensions for wire-bond package
# BCD 180nm pad library

set pad_width 80.0      ;# um
set pad_height 80.0     ;# um
set pad_pitch 100.0     ;# um (center-to-center)
set bond_pad_size 60.0  ;# um bond pad opening
set esd_area 2000.0     ;# um^2 per pad for ESD

# Total IO ring area estimate
# 36 pads x 100 um pitch = 3,600 um perimeter
# Core area: 1,070 x 1,070 um
# IO ring area: ~1,140,000 - 1,070^2 = ~147,000 um^2
```

## Pad Placement Strategy

### Quadrant-Based Placement

```
              North (Top)
         +--------------------+
         |  SPI   VDD   GPIO  |
West     |  Test  VSS   Test  |  East
(Left)   |  RF    VDD   Sense |  (Right)
         |  Pace  VSS   Pace  |
         +--------------------+
              South (Bottom)
         +--------------------+
         |  Sense VDD_ANA     |
         |  Imped VSS         |
         |  Sense VDD_ANA     |
         +--------------------+
```

### Signal Grouping Principles

Analog and digital signals must be physically separated:

```
Rule 1: No analog pad within 3 pads of a high-speed digital pad
Rule 2: Power pads distributed evenly (minimum 2 per side)
Rule 3: Pace outputs on opposite corners (current loop minimization)
Rule 4: Sense inputs adjacent to analog supply pads
Rule 5: Test pads grouped together (not on timing-critical signals)
Rule 6: RF pads isolated with guard ring and ground shielding
```

## Innovus Pad Placement Flow

### IO File Preparation

```tcl
# IO file format for Innovus
# Location orientation pad_name net_name

# File: iPACE_chip.io
# Side: Top (North)
PAD PAD_SPI_CLK_A  N  0  100.0  SPI_CLK     PAD_SPI
PAD PAD_SPI_MOSI   N  1  200.0  SPI_MOSI    PAD_SPI
PAD PAD_SPI_MISO   N  2  300.0  SPI_MISO    PAD_SPI
PAD PAD_VDD_CORE_N N  3  400.0  VDD         PAD_VDD33
PAD PAD_VSS_CORE_N N  4  500.0  VSS         PAD_VSS
PAD PAD_GPIO0      N  5  600.0  GPIO[0]     PAD_BIDIR
PAD PAD_GPIO1      N  6  700.0  GPIO[1]     PAD_BIDIR

# Side: Right (East)
PAD PAD_VDD_CORE_E E  0  100.0  VDD         PAD_VDD33
PAD PAD_SENSE_RV_E E  1  200.0  SENSE_RV    PAD_SENSE
PAD PAD_VDD_ANA_E  E  2  300.0  VDD_ANA     PAD_VDD33
PAD PAD_VSS_E      E  3  400.0  VSS         PAD_VSS
PAD PAD_TEST_TCK   E  4  500.0  TCK         PAD_TEST
PAD PAD_TEST_TMS   E  5  600.0  TMS         PAD_TEST

# Side: Bottom (South)
PAD PAD_SENSE_SV_S S  0  100.0  SENSE_SV    PAD_SENSE
PAD PAD_VDD_ANA_S  S  1  200.0  VDD_ANA     PAD_VDD33
PAD PAD_IMP_MEAS_S S  2  300.0  IMP_MEAS    PAD_SENSE
PAD PAD_VSS_S      S  3  400.0  VSS         PAD_VSS
PAD PAD_IMP_RET_S  S  4  500.0  IMP_RET     PAD_SENSE
PAD PAD_SENSE_RA_S S  5  600.0  SENSE_RA    PAD_SENSE

# Side: Left (West)
PAD PAD_VDD_CORE_W W  0  100.0  VDD         PAD_VDD33
PAD PAD_PACE_AO_W  W  1  200.0  PACE_AO     PAD_PACE
PAD PAD_PACE_TI_W  W  2  300.0  PACE_TI     PAD_PACE
PAD PAD_VSS_W      W  3  400.0  VSS         PAD_VSS
PAD PAD_RF_ANT_W   W  4  500.0  RF_ANT      PAD_RF
PAD PAD_RF_GND_W   W  5  600.0  RF_GND      PAD_VSS
PAD PAD_SPI_CS_W   W  6  700.0  SPI_CS      PAD_SPI
```

### Loading IO File

```tcl
# Load IO constraints into Innovus
loadIoFile iPACE_chip.io

# Verify pad placement
checkIoPlacer

# Report pad assignments
reportIo -file reports/io_placement.rpt
```

## Pad-Bump Mapping

### Wire Bond Package Mapping

For the iPACE-CHIP hermetic package, wire bonds connect pads to the lead frame:

```tcl
# Wire bond configuration
set bond_type ball_bond      ;# or wedge bond
set wire_material gold        ;# 25 um diameter
set wire_length_max 2000.0   ;# um maximum
set loop_height 150.0        ;# um above pad
set bond_pad_diameter 60.0   ;# um opening in passivation
```

### Bond Wire Inductance

```python
# Bond wire inductance calculation
import math

def wire_inductance(length_um, diameter_um, height_um):
    """Calculate bond wire inductance in nH"""
    L = length = length_um * 1e-6
    d = diameter = diameter_um * 1e-6
    # Approximate formula for round wire
    L_nH = (length * 1e9) * (
        math.log(4 * length / d) + 0.25 * (height / length)
    ) * 0.2  # nH
    return L_nH

# Typical values for iPACE-CHIP
# Signal wire: 1.5 nH
# Power wire: 0.8 nH (wider wire, shorter length)
# Ground wire: 0.5 nH (direct, short path)
```

## Analog Pad Isolation

### Guard Ring Around Analog Pads

```tcl
# Add guard ring around analog pad group
createRouteBlk -box {780 100 1020 400} -layer {M1 M2 M3 M4 M5 M6}

addRing -nets {VSS} \
    -type block_rings \
    -around {PAD_SENSE_RV_E PAD_VDD_ANA_E} \
    -layer {M2 M3} \
    -width {3.0 3.0} \
    -spacing {2.0 2.0} \
    -offset {10.0 10.0}
```

### Noise Isolation Techniques

```
Between Analog and Digital Pad Groups:

1. Physical separation: Minimum 4 pad pitches
2. Ground guard ring: Continuous M2/M3 ring
3. Substrate tap ring: P+ taps connected to VSS
4. Deep N-well: Under analog pad group (if available)
5. Separate power returns: Dedicated VSS pad per domain
```

## High-Current Pad Design

### Pace Output Pad

The pace output delivers therapeutic pulses to the heart through the pacing leads:

```tcl
# Pace output pad requirements
# Current: up to 10 mA peak (1.5V into 150 Ohm lead impedance)
# Pulse width: 0.5 ms to 4 ms
# Slew rate control: prevent lead damage

# Wider metal routing for pace output
editRoute -selectedNetShape -net PACE_AO -width 12.0 -layer M6

# Additional vias for current capacity
addViaRow -cell VIA65 -origin {200 1050} -direction horizontal \
    -width 12 -height 4 -spacing 2 -nets {PACE_AO}
```

### Pace Output ESD Requirements

```
Pace Output Pad ESD:
- Must survive defibrillation pulse (up to 40 V for 5 ms)
- Series resistance: 1 kOhm (limits current)
- Back-to-back diode clamp to VDD and VSS
- Additional thick-oxide transistor for high-voltage tolerance
- Clamping voltage: < 3.6V (above 1.2V supply)
```

## Test Pad Configuration

### Scan Chain Test Pads

```tcl
# Test pad assignment for scan chain
# Multiplexed with functional signals where possible

set test_signals {
    {SCAN_EN    PAD_TEST_TMS  "Scan enable"        }
    {SCAN_IN    PAD_TEST_TDI  "Scan data in"       }
    {SCAN_OUT   PAD_TEST_TDO  "Scan data out"      }
    {SCAN_CLK   PAD_TEST_TCK  "Test clock"         }
    {BIST_DONE  PAD_TEST_TRST "BIST complete flag"  }
    {BIST_FAIL  PAD_TEST_BIST "BIST failure flag"   }
}
```

### Test Access Architecture

```
DFT Test Access:
- IEEE 1149.1 JTAG interface on dedicated pads
- Scan chain I/O shared with GPIO (mode select at power-up)
- Memory BIST on dedicated test pads
- Analog test via on-chip MUX to dedicated pads
- Boundary scan on all IO pads
```

## IO Placement in Innovus

### Complete IO Setup Script

```tcl
proc setup_io_pads {} {
    # Load pad library
    set_db pad_libraries "pad_lib_180nm"

    # Load IO file
    loadIoFile iPACE_chip.io

    # Define pad ring constraints
    set_db io_place_h_layer M6
    set_db io_place_v_layer M5
    set_db io_place_h_width 20.0
    set_db io_place_v_width 20.0

    # Power pad connections
    connect_global_net VDD -type pad_rings \
        -netinst VDD -pad PAD_VDD*
    connect_global_net VSS -type pad_rings \
        -netinst VSS -pad PAD_VSS*

    # Create IO ring
    createIoRing -horizontal_layer M6 \
        -horizontal_width 20.0 \
        -vertical_layer M5 \
        -vertical_width 20.0 \
        -corner_width 30.0

    # Verify placement
    checkIoPlacer
    reportIo -file reports/io_check.rpt
}
```

## Signal Integrity at Pad Level

### Crosstalk Between Adjacent Pads

```tcl
# Minimize crosstalk on sensitive analog pads
# Set spacing constraints

set_db [get_db pads PAD_SENSE*] .pad_margin 3
set_db [get_db pads PAD_PACE*] .pad_margin 2

# Add shielding between pace and sense pads
# Place grounded filler pads between them
placeIoCell PAD_Filler -location {between PACE and SENSE pads}
```

### Impedance Matching for RF Pad

```tcl
# RF telemetry pad matching network
# Target: 50 Ohm at 402 MHz (MICS band)

# On-chip matching components
# L_match: 8.2 nH (on-chip spiral inductor)
# C_match: 1.8 pF (MIM capacitor)

# Layout constraints for RF pad
# - Minimum distance to digital pads: 500 um
# - Dedicated ground vias: minimum 8
# - Ground plane on M1/M2 beneath RF routing
# - No digital signal routing on layers M1-M2 within 200 um
```

## Package-Pad Coordination

### Lead Frame Compatibility

```
iPACE-CHIP Package: 36-pin Ceramic LCC

Pin Assignment Rules:
- Power pins at corners and center of each side
- No more than 2 signal pins between power pins
- Pace output pins on opposite sides (current loop)
- Sense input pins adjacent to analog power

Bond Pad to Package Pin Mapping:
- Package pin pitch: 0.5 mm (500 um)
- Die pad pitch: 100 um (requires bond wire fan-out)
- Maximum fan-out angle: 45 degrees
```

### Cross-Reference Table

| Die Pad | Pad Name | Package Pin | Function |
|---------|----------|-------------|----------|
| N0 | SPI_CLK | Pin 1 | SPI Clock |
| N1 | SPI_MOSI | Pin 2 | SPI Data Out |
| N2 | SPI_MISO | Pin 3 | SPI Data In |
| N3 | VDD | Pin 4 | Core Power |
| N4 | VSS | Pin 5 | Ground |
| E0 | VDD | Pin 9 | Core Power |
| E1 | SENSE_RV | Pin 10 | RV Sense |
| E2 | VDD_ANA | Pin 11 | Analog Power |
| W0 | VDD | Pin 28 | Core Power |
| W1 | PACE_AO | Pin 29 | Pace Output |
| W2 | PACE_TI | Pin 30 | Pace Return |
| S0 | SENSE_SV | Pin 19 | SV Sense |
| S1 | VDD_ANA | Pin 20 | Analog Power |

## Pad Placement Verification

### Connectivity Checks

```tcl
# Verify all pads connected correctly
verifyConnectivity -type regular -net {VDD VSS VDD_ANA} \
    -report reports/pad_connectivity.rpt

# Check for floating pads
reportFloatingNets -file reports/floating_nets.rpt

# Verify power pad to ring connections
verifyPowerVia -net {VDD VSS} \
    -report reports/power_via_check.rpt
```

### DRC on Pad Ring

```tcl
# Run DRC on IO ring area only
editSelect -area {0 0 1140 1140}
verify_drc -limit 500 -report reports/io_drc.rpt
editClearSelection
```

## Summary

IO pad placement for iPACE-CHIP follows a quadrant-based strategy that separates analog and digital domains, provides adequate ESD protection, and matches the 36-pin ceramic LCC package. The design allocates dedicated pads for pacing outputs with high-current capability, low-noise sense inputs with guard ring isolation, and RF telemetry with impedance matching. Verification ensures all pads meet connectivity, DRC, and signal integrity requirements.
