# Floorplanning for iPACE-CHIP ASIC

## 1. Introduction

Floorplanning defines the physical arrangement of major blocks on the iPACE-CHIP die.
It establishes the die size, pad locations, power distribution network, and block
placement regions. For a medical implantable device, floorplanning must account for:

- **Analog-digital isolation** to prevent digital switching noise from corrupting
  sensitive cardiac sensing signals (µV-level)
- **Thermal distribution** across the die (even though thermal is not a constraint)
- **ESD protection** of all I/O pads connected to external electrodes
- **Hermetic packaging** compatibility with ceramic or titanium housings
- **Radiation hardness** through physical spacing and guard ring placement

## 2. Die Architecture

### 2.1 Die Dimensions

```
iPACE-CHIP Die Specifications:
═══════════════════════════════════════════════════════════════

  Die Size: 1.8 mm × 1.8 mm (3.24 mm² total)
  Core Area: 1.2 mm × 1.2 mm (1.44 mm²)
  Pad Ring Width: 0.3 mm per side

  ┌────────────────────────────────────────────────────────────┐
  │  PAD RING (0.3 mm width all sides)                        │
  │  ┌──────────────────────────────────────────────────────┐ │
  │  │  1.8 mm × 1.8 mm DIE (including pad ring)           │ │
  │  │                                                       │ │
  │  │  ┌─────────────────────────────────────────────────┐ │ │
  │  │  │           CORE AREA (1.2 × 1.2 mm)              │ │ │
  │  │  │                                                  │ │ │
  │  │  │  ┌──────────────┐    ┌──────────────────────┐  │ │ │
  │  │  │  │   ANALOG     │    │    DIGITAL CORE      │  │ │ │
  │  │  │  │   SUBSYSTEM  │    │                      │  │ │ │
  │  │  │  │   0.4×0.8mm  │    │   0.8×0.8mm          │  │ │ │
  │  │  │  │   0.32mm²    │    │   0.64mm²            │  │ │ │
  │  │  │  │              │    │                      │  │ │ │
  │  │  │  │  LNA         │    │  Pacing Engine       │  │ │ │
  │  │  │  │  VGA         │    │  Sensing Engine      │  │ │ │
  │  │  │  │  BPF         │    │  AES-128 Engine      │  │ │ │
  │  │  │  │  SAR ADC     │    │  Telemetry Unit      │  │ │ │
  │  │  │  │  Output Drv  │    │  Watchdog Timer      │  │ │ │
  │  │  │  │  Bandgap     │    │  Parameter Store     │  │ │ │
  │  │  │  │  LDO         │    │  Power Manager       │  │ │ │
  │  │  │  │  Telem Coil  │    │  CRC-16 Engine       │  │ │ │
  │  │  │  └──────────────┘    └──────────────────────┘  │ │ │
  │  │  │                                                  │ │ │
  │  │  │  ┌──────────────────────────────────────────┐   │ │ │
  │  │  │  │           MEMORY BLOCK                     │   │ │ │
  │  │  │  │  SRAM (2KB) │ SRAM (2KB) │ ROM (1KB)     │   │ │ │
  │  │  │  └──────────────────────────────────────────┘   │ │ │
  │  │  └─────────────────────────────────────────────────┘ │ │
  │  └──────────────────────────────────────────────────────┘ │
  └────────────────────────────────────────────────────────────┘

  Floorplan Dimensions:
    Total die:     1.8 mm × 1.8 mm = 3.24 mm²
    Core:          1.2 mm × 1.2 mm = 1.44 mm²
    Pad ring:      0.3 mm × 4 sides
    Analog block:  0.4 mm × 0.8 mm = 0.32 mm²
    Digital block: 0.8 mm × 0.8 mm = 0.64 mm²
    Memory block:  0.8 mm × 0.2 mm = 0.16 mm²
```

### 2.2 Placement Regions

```
Block Placement Constraints:
═══════════════════════════════════════════════════════════════

  ┌──────────────────┬───────────┬────────────────────────────┐
  │ Block            │ Area      │ Placement Rule             │
  ├──────────────────┼───────────┼────────────────────────────┤
  │ Analog Subsystem │ 0.32 mm²  │ Top-left quadrant          │
  │ (AFE, Output Drv)│           │ Away from digital          │
  │                  │           │ Guard ring isolation        │
  ├──────────────────┼───────────┼────────────────────────────┤
  │ Digital Core     │ 0.64 mm²  │ Right half of core         │
  │ (FSM, AES, UART)│           │ Away from analog           │
  │                  │           │ Clock tree from center      │
  ├──────────────────┼───────────┼────────────────────────────┤
  │ SRAM (2KB)       │ 0.12 mm²  │ Bottom center              │
  │ Parameters       │           │ Accessible from digital    │
  │                  │           │ and analog sides           │
  ├──────────────────┼───────────┼────────────────────────────┤
  │ SRAM (2KB)       │ 0.06 mm²  │ Next to param SRAM         │
  │ Data Buffer      │           │ Shared power rails         │
  ├──────────────────┼───────────┼────────────────────────────┤
  │ ROM (1KB)        │ 0.03 mm²  │ Bottom-right               │
  │                  │           │ Lowest priority            │
  ├──────────────────┼───────────┼────────────────────────────┤
  │ Pad Ring         │ 0.3mm     │ Perimeter, all sides       │
  │                  │ width     │ ESD clamps at power pads   │
  └──────────────────┴───────────┴────────────────────────────┘
```

## 3. Power Distribution Network

### 3.1 Power Ring Architecture

```
Power Distribution Network for iPACE-CHIP:
═══════════════════════════════════════════════════════════════

  Power Nets:
    VDD_IO  = 3.3V (I/O and high-voltage drivers)
    VDD_CORE = 1.5V (digital core)
    VDD_A   = 1.5V (analog, filtered)
    VSS     = 0V   (ground)

  Power Ring Structure:
  ┌────────────────────────────────────────────────────────────┐
  │  VDD_IO ring (outermost, 10 µm wide)                       │
  │  ┌──────────────────────────────────────────────────────┐ │
  │  │  VDD_CORE ring (inner, 8 µm wide)                    │ │
  │  │  ┌──────────────────────────────────────────────────┐ │ │
  │  │  │  VDD_A ring (analog only, 6 µm wide, guarded)    │ │ │
  │  │  │  ┌──────────────────────────────────────────────┐ │ │ │
  │  │  │  │                CORE AREA                       │ │ │ │
  │  │  │  │                                               │ │ │ │
  │  │  │  └──────────────────────────────────────────────┘ │ │ │
  │  │  │  VSS ring (6 µm wide, under VDD rings)           │ │ │
  │  │  └──────────────────────────────────────────────────┘ │ │
  │  └──────────────────────────────────────────────────────┘ │
  └────────────────────────────────────────────────────────────┘

  Power Straps (M6 top metal, horizontal):
    VDD_IO:  every 100 µm, 4 µm wide
    VDD_CORE: every 80 µm, 3 µm wide
    VDD_A:   every 60 µm, 2 µm wide (denser for lower noise)
    VSS:     every 60 µm, 3 µm wide

  Power Rails (M1-M5, vertical):
    VDD_CORE: every 50 µm, 1 µm wide
    VSS:      every 50 µm, 1 µm wide
    VDD_A:    every 40 µm, 0.8 µm wide
```

### 3.2 Power Grid Analysis

```
Power Grid Resistance Analysis:
═══════════════════════════════════════════════════════════════

  VDD_CORE power distribution:
    Ring resistance (M6): R_ring = ρ × L / (W × t)
      ρ = 0.022 Ω·µm (aluminum, 180nm)
      L = 4 × 1200 µm = 4800 µm (perimeter)
      W = 8 µm (ring width)
      t = 0.8 µm (M6 thickness)
      R_ring = 0.022 × 4800 / (8 × 0.8) = 16.5 Ω

    IR drop (worst case):
      Peak current: 80 µA (during pacing pulse)
      R_drop = R_ring / 4 = 4.125 Ω (quarter-ring worst case)
      V_drop = 80 µA × 4.125 Ω = 0.33 mV
      VDD_actual = 1.500 - 0.00033 = 1.49967 V ✓

    Power noise (dynamic):
      C_total (on-chip decoupling) ≈ 50 pF
      ΔI = 80 µA (peak switching current)
      Δt = 30 µs (clock period)
      ΔV = ΔI × Δt / C = 80µ × 30µ / 50p = 48 mV
      This is ~3.2% of VDD (acceptable for digital logic)

  VDD_A power distribution (analog):
    Separate power ring with LC filtering:
      L_filter = 100 nH (on-chip spiral inductor)
      C_filter = 10 pF (MIM capacitor)
      f_resonant = 1 / (2π√(LC)) = 159 kHz
      This filters digital switching noise above 159 kHz
```

## 4. Analog-Digital Isolation

### 4.1 Isolation Strategy

```
Analog-Digital Isolation Techniques:
═══════════════════════════════════════════════════════════════

  Physical Separation:
  ┌────────────────────────────────────────────────────────────┐
  │  ┌──────────┐    ┌──────┐    ┌──────────────────────┐    │
  │  │ ANALOG   │    │GUARD │    │     DIGITAL           │    │
  │  │          │◄──►│ RING │◄──►│                       │    │
  │  │ 0.4×0.8mm│    │50µm  │    │  0.8×0.8mm            │    │
  │  │          │    │      │    │                       │    │
  │  └──────────┘    └──────┘    └──────────────────────┘    │
  │                                                            │
  │  Minimum separation: 50 µm between analog and digital     │
  │  Guard ring width: 5 µm (n+ in p-sub, p+ around n-well)  │
  │  Deep n-well isolation: under entire analog block         │
  └────────────────────────────────────────────────────────────┘

  Guard Ring Structure:
  ┌────────────────────────────────────────────────────────────┐
  │                                                            │
  │  Analog │  N+ guard  │  P+ guard  │  N-well  │  Digital  │
  │  region │  (grounded)│  (VDD)     │  (VDD)   │  region   │
  │         │            │            │          │           │
  │  ───────┼────────────┼────────────┼──────────┼──────────  │
  │         │  5 µm      │  5 µm      │  10 µm   │           │
  │         │            │            │          │           │
  └────────────────────────────────────────────────────────────┘

  Substrate Noise Isolation:
    • Deep n-well under analog transistors (traps minority carriers)
    • Separate analog and digital substrate ties
    • Analog substrate tie: every 20 µm near sensitive circuits
    • Digital substrate tie: every 50 µm (less critical)
```

### 4.2 Signal Routing Rules

```
Signal Routing Isolation Rules:
═══════════════════════════════════════════════════════════════

  ┌────┬─────────────────────────────────┬────────────────────┐
  │ #  │ Rule                            │ Implementation     │
  ├────┼─────────────────────────────────┼────────────────────┤
  │  1 │ No digital signals routed over  │ Physical DRC rule  │
  │    │ sensitive analog circuits        │ in P&R tool        │
  ├────┼─────────────────────────────────┼────────────────────┤
  │  │  │ Analog signals stay on M1-M3   │ Routing constraint │
  │  2 │ only (avoid M6 power straps)    │                    │
  ├────┼─────────────────────────────────┼────────────────────┤
  │  3 │ No switching signals on M1       │ Shield on M1       │
  │    │ adjacent to analog signal on M2  │ under analog       │
  ├────┼─────────────────────────────────┼────────────────────┤
  │  4 │ Clock signals routed on M4-M5    │ Away from analog   │
  │    │ only (away from analog on M1-M3)│ routing            │
  ├────┼─────────────────────────────────┼────────────────────┤
  │  5 │ Analog output to digital input   │ Must use CDC sync  │
  │    │ crosses via synchronizer         │                    │
  ├────┼─────────────────────────────────┼────────────────────┤
  │  6 │ No metal bridges across analog- │ Top-metal layer    │
  │    │ digital boundary on same layer   │ restriction        │
  └────┴─────────────────────────────────┴────────────────────┘
```

## 5. Pad Placement

### 5.1 Pad Ring Layout

```
iPACE-CHIP Pad Placement:
═══════════════════════════════════════════════════════════════

  Pad count: 16
  Pad pitch: 150 µm (minimum for 180nm)
  Pad size: 80 µm × 80 µm (bond pad)
  Seal ring: 50 µm around entire die

  ┌──────────────────────────────────────────────────────────┐
  │  TOP SIDE (analog pads closest to analog block)          │
  │                                                          │
  │  ○ VDD_A  ○ VSS_A  ○ A_IN+  ○ A_IN-  ○ V_OUT+  ○ V_OUT- │
  │                                                          │
  │  ┌──────────────────────────────────────────────────────┐│
  │  │                  DIE CORE                            ││
  │  │                                                       ││
  │  │  ┌────────┐    ┌──────────────────────┐             ││
  │  │  │ANALOG  │    │     DIGITAL          │             ││
  │  │  │BLOCK   │    │                      │             ││
  │  │  └────────┘    └──────────────────────┘             ││
  │  │                                                       ││
  │  │  ┌──────────────────────────────────────────────┐   ││
  │  │  │              MEMORY                           │   ││
  │  │  └──────────────────────────────────────────────┘   ││
  │  └──────────────────────────────────────────────────────┘│
  │                                                          │
  │  BOTTOM SIDE (digital/control pads closest to digital)  │
  │                                                          │
  │  ○ VDD_D  ○ VSS_D  ○ TEST_CLK  ○ TEST_EN  ○ RESET_B  ○ IRQ │
  └──────────────────────────────────────────────────────────┘

  LEFT SIDE: ○ A_OUT+  ○ A_OUT-  ○ TELE_TX  ○ TELE_RX
  RIGHT SIDE: (power and ground straps)

  Pad Assignment Rationale:
    • A_IN+/A_IN- near analog block (short routing)
    • V_OUT+/V_OUT- near output drivers (high current)
    • A_OUT+/A_OUT- near atrial driver
    • TELE_TX/TELE_RX near coil driver
    • TEST pins grouped together (factory only)
    • RESET_B and IRQ near digital core (control signals)
```

## 6. Floorplan Constraints (LEF)

### 6.1 Physical Constraints for P&R

```tcl
#==========================================================================
# iPACE-CHIP Floorplan Constraints (for P&R tool)
#==========================================================================

# Die size
set die_width 1800.0   ;# in microns
set die_height 1800.0

# Core area
set core_llx 300.0     ;# 0.3mm pad ring
set core_lly 300.0
set core_urx 1500.0
set core_ury 1500.0

# Create floorplan
create_floorplan -core_utilization 0.65 \
    -core_margins_by die \
    -left_io2core 300.0 \
    -right_io2core 300.0 \
    -top_io2core 300.0 \
    -bottom_io2core 300.0

# Placement blockages (no digital cells in analog area)
create_keepout_margin -type hard -outer {0 0 0 0} \
    [get_cells u_analog_frontend]
create_place_region -name analog_region \
    -coordinates {{0 600} {480 1400}}  ;# Analog block area
create_place_region -name digital_region \
    -coordinates {{580 600} {1500 1500}}  ;# Digital block area

# Pin placement (key analog pins near their blocks)
set_pin_physical -pin_name A_IN_P  -location {240 1600} -layer M2
set_pin_physical -pin_name A_IN_N  -location {300 1600} -layer M2
set_pin_physical -pin_name V_OUT_P -location {360 1600} -layer M2
set_pin_physical -pin_name V_OUT_N -location {420 1600} -layer M2
set_pin_physical -pin_name A_OUT_P -location {0 1200}   -layer M2
set_pin_physical -pin_name A_OUT_N -location {0 1100}   -layer M2

# Power planning
create_pg_ring_pattern pg_ring_core \
    -nets {VDD_CORE VSS} \
    -horizontal_layer M6 -horizontal_width 8.0 \
    -vertical_layer M5 -vertical_width 8.0

create_pg_ring_pattern pg_ring_io \
    -nets {VDD_IO VSS} \
    -horizontal_layer M6 -horizontal_width 10.0 \
    -vertical_layer M5 -vertical_width 10.0

create_pg_ring_pattern pg_ring_analog \
    -nets {VDD_A VSS} \
    -horizontal_layer M6 -horizontal_width 6.0 \
    -vertical_layer M5 -vertical_width 6.0

# Decap cells
create_stdcell_lib_group decap -cells {DCAPHD1 DCAPHD2} \
    -region {0 0 $die_width $die_height}
```

## 7. Floorplan Verification

```
Floorplan Verification Checklist:
═══════════════════════════════════════════════════════════════

┌────┬─────────────────────────────────┬──────┬────────────────┐
│ #  │ Check                           │ Pass │ Notes          │
├────┼─────────────────────────────────┼──────┼────────────────┤
│  1 │ Die area meets target           │      │ 3.24 mm²       │
│  2 │ Core utilization within budget   │      │ 65% target     │
│  3 │ All blocks within placement reg │      │                │
│  4 │ Analog-digital separation       │      │ 50 µm min      │
│  5 │ Guard rings placed correctly    │      │                │
│  6 │ Power rings connected to pads   │      │                │
│  7 │ No timing arcs blocked          │      │                │
│  8 │ Pin placement near blocks       │      │                │
│  9 │ Decap cells distributed         │      │                │
│ 10 │ Standard cell rows aligned      │      │                │
│ 11 │ No routing blockages over pins  │      │                │
│ 12 │ Seal ring integrity             │      │                │
│ 13 │ Corner cells placed             │      │                │
│ 14 │ ESD clamps on power pads        │      │                │
└────┴─────────────────────────────────┴──────┴────────────────┘
```

## 8. Summary

The iPACE-CHIP floorplan achieves:

1. **1.8mm × 1.8mm die** with 3.24 mm² total area
2. **Strict analog-digital isolation** with 50 µm guard ring separation
3. **Triple power domain** (VDD_IO, VDD_CORE, VDD_A) with independent rings
4. **16-pad ring** with analog pins near analog block, digital near digital
5. **65% core utilization** for efficient area use
6. **Power distribution** with <50 mV noise on VDD_CORE during pacing

---

*Previous: [Timing Analysis](../../02-RTL-Design-Synthesis/04-Timing-Analysis/timing-analysis.md)*
