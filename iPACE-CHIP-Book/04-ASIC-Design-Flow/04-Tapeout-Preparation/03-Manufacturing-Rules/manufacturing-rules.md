# Manufacturing Rules for iPACE-CHIP ASIC

## 1. Introduction

Manufacturing rules define the geometric and electrical constraints that the foundry
requires for reliable fabrication of the iPACE-CHIP. These rules go beyond DRC — they
encompass process-specific requirements for yield optimization, reliability assurance,
and foundry-specific manufacturing capabilities.

For a medical implantable device, manufacturing rule compliance directly impacts patient
safety: a single manufacturing defect can cause chip failure, potentially endangering
the patient's life.

## 2. Process Technology Manufacturing Rules

### 2.1 TSMC 180nm Design Rules Summary

```
TSMC 180nm (T180G) Manufacturing Rules:
═══════════════════════════════════════════════════════════════

  Technology: TSMC 180nm CMOS (1P5M + top thick metal)
  Minimum Feature Size: 180 nm (poly gate)
  Design Grid: 0.01 µm (10 nm resolution)

  ┌──────────────┬────────────────────────────────────────────┐
  │ Layer        │ Key Manufacturing Rules                    │
  ├──────────────┼────────────────────────────────────────────┤
  │ Poly         │ • Min width: 0.18 µm                      │
  │              │ • Min length: 0.18 µm (Lmin)              │
  │              │ • Min spacing: 0.18 µm                    │
  │              │ • Poly must cross active (gate formation)  │
  │              │ • No poly cuts within active region        │
  ├──────────────┼────────────────────────────────────────────┤
  │ Active       │ • Min width: 0.22 µm                      │
  │ (Diffusion)  │ • Min spacing: 0.28 µm (N+ to N+)        │
  │              │ • Min spacing: 0.50 µm (N+ to P+)        │
  │              │ • Well enclosure: 0.60 µm                 │
  ├──────────────┼────────────────────────────────────────────┤
  │ N-Well       │ • Min width: 0.80 µm                      │
  │              │ • Min spacing: 1.00 µm (N+ to P-sub)     │
  │              │ • Must enclose all PMOS devices            │
  │              │ • Deep N-well available for isolation      │
  ├──────────────┼────────────────────────────────────────────┤
  │ Contact      │ • Size: 0.20 µm × 0.20 µm                │
  │              │ • Min spacing: 0.25 µm                    │
  │              │ • Min enclosure (poly): 0.09 µm           │
  │              │ • Min enclosure (M1): 0.05 µm             │
  │              │ • One contact per transistor terminal      │
  ├──────────────┼────────────────────────────────────────────┤
  │ M1           │ • Min width: 0.18 µm (signal)             │
  │              │ • Min width: 0.30 µm (power rails)        │
  │              │ • Min spacing: 0.18 µm                    │
  │              │ • Min area: 0.10 µm²                     │
  │              │ • Preferred direction: Horizontal          │
  ├──────────────┼────────────────────────────────────────────┤
  │ M2-M5        │ • Min width: 0.20 µm                      │
  │              │ • Min spacing: 0.20 µm                    │
  │              │ • Min area: 0.12 µm²                     │
  │              │ • Min via enclosure: 0.05 µm              │
  │              │ • Preferred: M2/M4=Vertical, M3/M5=Horiz  │
  ├──────────────┼────────────────────────────────────────────┤
  │ M6 (thick)   │ • Min width: 0.40 µm                      │
  │              │ • Min spacing: 0.40 µm                    │
  │              │ • Thickness: 0.80 µm (2× standard)        │
  │              │ • Sheet resistance: 0.022 Ω/sq            │
  │              │ • Used for power rings, inductors          │
  ├──────────────┼────────────────────────────────────────────┤
  │ Via          │ • Size: 0.22 µm × 0.22 µm                 │
  │ (Via1-Via5)  │ • Min spacing: 0.25 µm                   │
  │              │ • Min enclosure: 0.05 µm per layer        │
  │              │ • No stacked vias > 3 high (RC limit)     │
  └──────────────┴────────────────────────────────────────────┘
```

### 2.2 Transistor-Level Rules

```
MOSFET Manufacturing Rules:
═══════════════════════════════════════════════════════════════

  NMOS Transistor:
  ┌──────────────────────────────────────────────────────────┐
  │          Poly (Gate)                                      │
  │    ┌──────┼──────────┼──────┐                             │
  │    │      │          │      │                             │
  │  ──┼──────┼──────────┼──────┼──  M1 (Drain/Source)       │
  │    │   ┌──┴──────────┴──┐   │                             │
  │    │   │    Channel      │   │                             │
  │    │   │   (Active)      │   │                             │
  │    │   └─────────────────┘   │                             │
  │    │      │          │      │                             │
  │    │      │   N+Impl │      │                             │
  │    │      │          │      │                             │
  │    │   ┌──┴──────────┴──┐   │                             │
  │    │   │   P-Substrate   │   │                             │
  │    │   └─────────────────┘   │                             │
  └──────────────────────────────────────────────────────────┘

  Minimum NMOS Dimensions:
    Lmin = 0.18 µm (gate length)
    Wmin = 0.22 µm (minimum active width)
    Poly extension beyond active: 0.09 µm
    Contact inside active: min 0.10 µm from poly edge
```

## 3. Yield Enhancement Rules

### 3.1 Design-for-Manufacturing (DFM)

```
DFM Rules for Yield Optimization:
═══════════════════════════════════════════════════════════════

  ┌──────────────────────┬──────────────────────────────────────┐
  │ DFM Rule             │ Implementation                       │
  ├──────────────────────┼──────────────────────────────────────┤
  │ Redundant vias       │ All signal vias have at least 1     │
  │                      │ redundant via (2 vias minimum)      │
  │                      │ Increases via reliability by 10×     │
  ├──────────────────────┼──────────────────────────────────────┤
  │ Metal filling        │ Dummy metal fill added to achieve   │
  │                      │ 35-65% density on all metal layers  │
  │                      │ Non-functional fill (not connected)  │
  ├──────────────────────┼──────────────────────────────────────┤
  │ Wire spreading       │ Wires spread apart where possible   │
  │                      │ to reduce bridging defects           │
  ├──────────────────────┼──────────────────────────────────────┤
  │ Via redundancy       │ Critical vias (clock, power) have   │
  │                      │ 2x-4x redundancy                     │
  ├──────────────────────┼──────────────────────────────────────┤
  │ Poly corner rounding │ Poly corners rounded where possible │
  │                      │ to prevent hot spots                 │
  ├──────────────────────┼──────────────────────────────────────┤
  │ Keep-out zones       │ No minimum-feature-size geometry    │
  │                      │ near well edges or implant edges     │
  ├──────────────────────┼──────────────────────────────────────┤
  │ ESD design rules     │ All I/O pads have dedicated ESD     │
  │                      │ protection devices                   │
  └──────────────────────┴──────────────────────────────────────┘
```

### 3.2 Redundancy Requirements

```
Redundancy Requirements for iPACE-CHIP:
═══════════════════════════════════════════════════════════════

  Via Redundancy:
  ┌──────────────────┬───────────┬──────────┬────────────────┐
  │ Net Category     │ Vias Used │ Redundant│ Rationale      │
  ├──────────────────┼───────────┼──────────┼────────────────┤
  │ Clock nets       │ 2 per via │ Yes (2×) │ Reliability    │
  │ Power nets       │ 4 per via │ Yes (4×) │ EM, reliability│
  │ Pace outputs     │ 3 per via │ Yes (3×) │ High current   │
  │ Signal (general) │ 1 per via │ Yes (2×) │ DFM            │
  │ Analog signals   │ 1 per via │ Optional │ Noise concern  │
  └──────────────────┴───────────┴──────────┴────────────────┘

  Total via count: 12,400
  With redundancy: ~24,800 via cuts
  Via failure rate (with redundancy): <0.01 FIT per via
  Total via failure rate: <0.25 FIT (negligible)
```

## 4. Packaging Rules

### 4.1 Ceramic Package Requirements

```
iPACE-CHIP Package Specifications:
═══════════════════════════════════════════════════════════════

  Package Type: Ceramic hermetic (titanium housing)
  Bond Type: Gold wire bonding (25 µm diameter)
  Pin Count: 16

  ┌──────────────────┬────────────────────────────────────────┐
  │ Parameter        │ Specification                          │
  ├──────────────────┼────────────────────────────────────────┤
  │ Die attach       │ Conductive epoxy (biocompatible)       │
  │ Bond wire        │ Au, 25 µm diameter                     │
  │ Bond pad size    │ 80 µm × 80 µm (minimum)               │
  │ Bond pad pitch   │ 150 µm (minimum)                       │
  │ Bond pad finish  │ Aluminum pad + Ti/Pt/Au UBM            │
  │ Wire bond length │ < 2 mm (max)                           │
  │ Wire loop height │ 100-200 µm                             │
  │ Seal ring        │ 50 µm continuous around die            │
  │ Passivation      │ SiN with pad openings                  │
  │ Die thickness    │ 300 µm (standard) → 200 µm (thinned)  │
  │ Backside finish  │ Au plating for die attach              │
  └──────────────────┴────────────────────────────────────────┘

  Wire Bond Diagram (simplified):
  ┌──────────────────────────────────────────────────────────┐
  │  Package Pin Mapping                                      │
  │                                                          │
  │  Pin 1 ────── Bond wire ────── Die Pad (VDD_A)         │
  │  Pin 2 ────── Bond wire ────── Die Pad (VSS_A)         │
  │  Pin 3 ────── Bond wire ────── Die Pad (A_IN+)         │
  │  Pin 4 ────── Bond wire ────── Die Pad (A_IN-)         │
  │  Pin 5 ────── Bond wire ────── Die Pad (V_OUT+)        │
  │  Pin 6 ────── Bond wire ────── Die Pad (V_OUT-)        │
  │  Pin 7 ────── Bond wire ────── Die Pad (A_OUT+)        │
  │  Pin 8 ────── Bond wire ────── Die Pad (A_OUT-)        │
  │  Pin 9 ────── Bond wire ────── Die Pad (TELE_TX)       │
  │  Pin 10 ───── Bond wire ────── Die Pad (TELE_RX)       │
  │  Pin 11 ───── Bond wire ────── Die Pad (VDD_D)         │
  │  Pin 12 ───── Bond wire ────── Die Pad (VSS_D)         │
  │  Pin 13 ───── Bond wire ────── Die Pad (TEST_CLK)      │
  │  Pin 14 ───── Bond wire ────── Die Pad (TEST_EN)       │
  │  Pin 15 ───── Bond wire ────── Die Pad (RESET_B)       │
  │  Pin 16 ───── Bond wire ────── Die Pad (IRQ)           │
  └──────────────────────────────────────────────────────────┘
```

### 4.2 Hermeticity Requirements

```
Hermeticity Specifications:
═══════════════════════════════════════════════════════════════

  ┌──────────────────────────────┬────────────────────────────┐
  │ Parameter                    │ Specification              │
  ├──────────────────────────────┼────────────────────────────┤
  │ Helium leak rate             │ <= 10^-9 atm.cc/sec       │
  │ Fine leak rate (MIL-STD)     │ <= 5 x 10^-9 atm.cc/sec  │
  │ Gross leak rate              │ No bubbles in fluorocarbon│
  │ Seal method                  │ Laser welding (Ti housing)│
  │ Seal atmosphere              │ Nitrogen (dry, inert)     │
  │ Moisture content (内部)      │ <= 5000 ppm               │
  │ Hermeticity test standard    │ MIL-STD-883 Method 1014   │
  │ Burn-in before seal          │ 168 hours at 125°C        │
  └──────────────────────────────┴────────────────────────────┘

  Note: Hermeticity is a package-level specification, not a
  die-level DRC rule. However, the die must be designed to
  withstand the sealing process (temperature, pressure).
```

## 5. Cleanliness and Contamination

```
Manufacturing Cleanliness Requirements:
═══════════════════════════════════════════════════════════════

  ┌──────────────────────────────┬────────────────────────────┐
  │ Requirement                  │ Specification              │
  ├──────────────────────────────┼────────────────────────────┤
  │ Particle count (postFab)     │ <10 particles/cm² >0.5µm │
  │ Ionic contamination          │ < 1e10 atoms/cm² (Na+)   │
  │ Mobile ion cleanliness       │ < 5e9 atoms/cm²          │
  │ Moisture sensitivity         │ MSL 1 (unlimited)        │
  │ ESD handling                 │ Class 0 (<250V HBM)      │
  │ Floor cleanliness            │ Class 1000 cleanroom     │
  │ Packaging environment        │ Class 100 cleanroom      │
  └──────────────────────────────┴────────────────────────────┘

  For medical implantables, additional requirements:
  • ISO 10993 biocompatibility testing of all materials
  • No cytotoxic materials in contact with body tissue
  • Sterilization compatibility (EtO or gamma radiation)
  • Shelf life: 5 years minimum (sealed package)
```

## 6. Wafer-Level Manufacturing Specifications

```
Wafer Specifications for iPACE-CHIP:
═══════════════════════════════════════════════════════════════

  ┌──────────────────────────────┬────────────────────────────┐
  │ Parameter                    │ Specification              │
  ├──────────────────────────────┼────────────────────────────┤
  │ Wafer size                   │ 200 mm (8 inch)           │
  │ Wafer material               │ CZ silicon, p-type        │
  │ Resistivity                  │ 10-20 Ω·cm               │
  │ Thickness                    │ 725 ± 25 µm              │
  │ Flat                        │ Primary flat (110)        │
  │ Process                     │ TSMC 180nm (1P5M)         │
  │ Yield target                 │ >90% (functional)        │
  │ Die size                     │ 1.8 mm × 1.8 mm           │
  │ Dies per wafer              │ ~9,000 (with scribe lines)│
  │ Scribe line width           │ 80 µm                     │
  │ Scribe line (kerf) content  │ Test structures, alignment│
  │ Package                     │ Wafer backgrind + die saw │
  │ Backgrind target            │ 200 µm (from 725 µm)     │
  └──────────────────────────────┴────────────────────────────┘

  Wafer Map (simplified, showing die placement):
  ┌────────────────────────────────────────────────────────┐
  │                                                        │
  │    ╔══════╦══════╦══════╦══════╦══════╦══════╗        │
  │    ║ Die  ║ Die  ║ Die  ║ Die  ║ Die  ║ Die  ║        │
  │    ║ 1,1  ║ 1,2  ║ 1,3  ║ 1,4  ║ 1,5  ║ 1,6  ║        │
  │    ╠══════╬══════╬══════╬══════╬══════╬══════╣        │
  │    ║ Die  ║ Die  ║ Die  ║ Die  ║ Die  ║ Die  ║        │
  │    ║ 2,1  ║ 2,2  ║ 2,3  ║ 2,4  ║ 2,5  ║ 2,6  ║        │
  │    ╠══════╬══════╬══════╬══════╬══════╬══════╣        │
  │    ║ Die  ║ Die  ║ Die  ║ Die  ║ Die  ║ Die  ║        │
  │    ║ 3,1  ║ 3,2  ║ 3,3  ║ 3,4  ║ 3,5  ║ 3,6  ║        │
  │    ╠══════╬══════╬══════╬══════╬══════╬══════╣        │
  │    ║      ║      ║      ║      ║      ║      ║        │
  │    ║ ...  ║ ...  ║ ...  ║ ...  ║ ...  ║ ...  ║        │
  │    ╚══════╩══════╩══════╩══════╩══════╩══════╝        │
  │                                                        │
  │    Each die: 1.8mm × 1.8mm + 80µm scribe = 1.96mm²   │
  │    Wafer area: π × 100² = 31,416 mm²                  │
  │    Dies per wafer: ~9,000 (after edge exclusion)       │
  └────────────────────────────────────────────────────────┘
```

## 7. Test Structure Requirements

```
On-Wafer Test Structures (in scribe line):
═══════════════════════════════════════════════════════════════

  Test structures placed in scribe lines for process monitoring:

  ┌──────────────────────┬────────────────────────────────────┐
  │ Structure            │ Purpose                            │
  ├──────────────────────┼────────────────────────────────────┤
  │ NMOS ID-VG           │ Threshold voltage, mobility        │
  │ PMOS ID-VG           │ Threshold voltage, mobility        │
  │ Poly line resistance │ Sheet resistance monitoring        │
  │ M1-M5 line resistance│ Metal resistance monitoring        │
  │ Contact resistance   │ Contact/via resistance             │
  │ Via chain (1000 vias)│ Via reliability                    │
  │ MOS capacitor        │ Oxide thickness monitoring         │
  │ Ring oscillator       │ Speed monitoring (D0/D1)          │
  │ SRAM test array       │ SRAM yield monitoring             │
  │ eFuse test structure  │ Fuse programming verification     │
  │ Antenna test structure│ Antenna rule verification         │
  │ ESD HBM structure    │ ESD protection verification       │
  └──────────────────────┴────────────────────────────────────┘
```

## 8. Summary

Manufacturing rules for iPACE-CHIP ensure:

1. **TSMC 180nm compatibility** with full DRC/LVS compliance
2. **DFM optimization** with redundant vias and metal fill
3. **Hermetic ceramic packaging** meeting MIL-STD-883
4. **200mm wafer processing** with ~9,000 dies per wafer
5. **ISO 10993 biocompatibility** for implant contact materials
6. **Test structures** in scribe lines for process monitoring

---

*Previous: [DRC/LVS Checks](../02-DRC-LVS-Checks/drc-lvs-checks.md)*
