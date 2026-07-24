# 14.2.2 Titanium Encapsulation for iPACE-CHIP

## Overview

Titanium encapsulation provides the outermost protective barrier for the iPACE-CHIP
implant, directly interfacing with human body tissue for the device's entire operational
lifetime. Unlike the internal hermetic seal that protects the die, the encapsulation
system manages biocompatibility, mechanical protection, RF transparency for telemetry,
and long-term corrosion resistance. This chapter covers titanium alloy selection,
encapsulation design, surface treatment, joining processes, and quality verification
specific to the iPACE-CHIP implantable neural interface.

## Titanium Alloy Selection

### Grade 1 CP Titanium vs. Alloy Options

| Property | Grade 1 Ti | Ti-6Al-4V (Grade 5) | Ti-6Al-7Nb (Grade 19) |
|-----------|-----------|---------------------|-----------------------|
| UTS (MPa) | 240 | 950 | 900 |
| Yield (MPa) | 170 | 880 | 830 |
| Elongation (%) | 24 | 14 | 14 |
| Density (g/cm³) | 4.51 | 4.43 | 4.52 |
| Elastic Modulus (GPa) | 105 | 114 | 105 |
| Corrosion Rate (mpy) | 0.001 | 0.002 | 0.001 |
| Biocompatibility | Excellent | Good (Al/V concerns) | Excellent |
| Weldability | Excellent | Good | Good |
| MRI Artifacts | Minimal | Moderate | Minimal |
| FDA Master File | Yes (Multiple) | Yes (Multiple) | Limited |
| Cost (per kg) | $15-25 | $30-50 | $80-120 |

### iPACE-CHIP Selection: Grade 1 CP Titanium

**Rationale for Grade 1 over alloys**:

1. **No alloying element concerns**: Ti-6Al-4V contains aluminum (neurotoxicity
   concerns at elevated leaching levels) and vanadium (cytotoxicity concerns).
   Grade 1 CP titanium is elemental titanium with no alloying additions.

2. **Superior corrosion resistance**: CP titanium forms a more stable and uniform
   TiO₂ passive layer than alloys, which contain second-phase particles that can
   create micro-galvanic cells.

3. **Superior weldability**: Critical for the laser welding process used in lid
   sealing. Grade 1 provides the widest process window with no risk of
   martensitic transformation or embrittlement.

4. **Sufficient mechanical strength**: At 240 MPa UTS, Grade 1 titanium provides
   more than adequate strength for implant encapsulation. The implant is not
   load-bearing, so the higher strength of alloys is unnecessary.

5. **MRI compatibility**: Grade 1 titanium produces minimal MRI artifacts due to
   its paramagnetic behavior and low magnetic susceptibility (χ = 1.8 × 10⁻⁵).

### Material Specification

| Parameter | Specification | Test Standard |
|-----------|--------------|---------------|
| Composition | Ti ≥ 99.5% | ASTM E2371 |
| Fe max | 0.20% | ASTM E2371 |
| O max | 0.18% | ASTM E1409 |
| N max | 0.03% | ASTM E1409 |
| C max | 0.08% | ASTM E1409 |
| H max | 0.015% | ASTM E1409 |
| Grain Size | ASTM 7-10 | ASTM E112 |
| Surface Finish | Ra < 0.4 μm | ISO 4287 |
| Form | Sheet/Plate, 0.3-2.0 mm | - |

## Encapsulation Architecture

### External Shell Design

The iPACE-CHIP encapsulation consists of two major titanium shell components:

```
         External Encapsulation Cross-Section

         ┌────────────────────────────────────────┐
         │          Titanium Top Shell             │
         │          (0.4mm wall thickness)         │
         │                                         │
    ═════╪═════════════════════════════════════════╪═══
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░░░░░░░░░░  TiN Plasma-Enhanced Coating  ░░░░░░░░░░
    ═════╪═════════════════════════════════════════╪═══
         │                                         │
         │  ┌─────────────────────────────────┐   │
         │  │     Hermetic Package            │   │
         │  │  (from Section 14.2.1)          │   │
         │  │                                 │   │
         │  │  ┌─────────────────────────┐   │   │
         │  │  │    iPACE-CHIP Die       │   │   │
         │  │  │                         │   │   │
         │  │  └─────────────────────────┘   │   │
         │  │                                 │   │
         │  │  Au/Sn Epoxy Underfill         │   │
         │  └─────────────────────────────────┘   │
         │                                         │
         │          Titanium Bottom Shell          │
         │          (0.4mm wall thickness)         │
         └───┬────┬────┬────┬────┬────┬────┬──────┘
             │    │    │    │    │    │    │
             ▼    ▼    ▼    ▼    ▼    ▼    ▼
         ┌────────────────────────────────────────┐
         │    Electrode Lead Extensions            │
         │    (Pt/Ir, silicone-insulated)          │
         └────────────────────────────────────────┘
```

### Dimensional Specifications

| Parameter | Specification | Tolerance |
|-----------|--------------|-----------|
| Outer Length | 14.0 mm | ±0.15 mm |
| Outer Width | 12.0 mm | ±0.15 mm |
| Outer Height | 4.5 mm | ±0.20 mm |
| Wall Thickness | 0.4 mm | ±0.05 mm |
| Corner Radius | 0.5 mm | ±0.1 mm |
| Internal Cavity | 11.0 × 10.0 × 3.0 mm | ±0.15 mm |
| Total Encapsulated Weight | < 3.0 g | - |
| Surface Area | ~4.5 cm² | - |

### Internal Cavity Fill

The internal cavity surrounding the hermetic package is filled with a biocompatible
underfill material:

**Material**: Medical-grade silicone (polydimethylsiloxane, PDMS)
- Shore A hardness: 30-40
- Dielectric constant: 2.8 at 1 MHz
- Thermal conductivity: 0.2 W/m·K
- Volume resistivity: > 1 × 10¹⁴ Ω·cm
- Biocompatibility: ISO 10993 Class VI certified

**Purpose**:
- Mechanical shock and vibration damping
- Moisture barrier (secondary to hermetic package)
- Elimination of internal voids that could collect fluid if primary seal fails
- Thermal conduction path from die to external shell

## Surface Treatment

### TiO₂ Passive Layer Management

Titanium's biocompatibility derives from its stable TiO₂ passive layer (2-10 nm thick).
The iPACE-CHIP encapsulation requires controlled growth and maintenance of this layer:

**As-Manufactured Surface**:
- Native TiO₂: 2-5 nm
- Roughness: Ra < 0.4 μm (as-polished)

**Acid Etch Treatment**:
```
Solution: 1% HF + 10% HNO₃ in DI water
Temperature: 25°C ± 2°C
Duration: 60 seconds
Rinse: 3 × DI water (18.2 MΩ·cm)
Drying: Nitrogen blow-off + vacuum bake (100°C, 1 hr)
```

This treatment removes the native oxide and contaminants, then regrows a uniform,
high-quality TiO₂ layer approximately 3-5 nm thick.

**Anodization (Optional)**:
For enhanced biocompatibility, the external surface can be anodized to grow a thicker
TiO₂ layer:

```
Electrolyte: 0.5 M H₃PO₄
Voltage: 10-20V (controlled to ±0.1V)
Current Density: 1 mA/cm²
Duration: 30 minutes
Resulting Oxide: 20-40 nm TiO₂ (rutile phase)
```

The anodized surface provides:
- Enhanced protein adsorption (promotes tissue integration)
- Increased corrosion resistance (> 10× improvement)
- Reduced ion release rate
- Color change (interference colors) useful for identification

### Hydroxyapatite Coating (Future Generation)

For tissue-integrated placement, a hydroxyapatite (HA) coating may be applied:

| Parameter | Specification |
|-----------|--------------|
| Composition | Ca₁₀(PO₄)₆(OH)₂, Ca/P = 1.67 |
| Coating Thickness | 50-75 μm |
| Crystallinity | > 65% |
| Adhesion Strength | > 15 MPa (ASTM F1147) |
| Deposition Method | Plasma spray or biomimetic |
| Porosity | 10-20% (interconnected) |

Note: HA coating is NOT used in the current iPACE-CHIP generation due to concerns
about coating delamination and particle generation in the chronic implant environment.

## Titanium Joining Processes

### Laser Welding for Encapsulation

The encapsulation shells are joined by laser welding, creating a continuous hermetic
seal around the entire device perimeter:

**Process Parameters**:

| Parameter | Value | Notes |
|-----------|-------|-------|
| Laser Type | Pulsed Nd:YAG | 1064 nm, TEM₀₀ mode |
| Pulse Energy | 1.0-3.0 J | Depends on wall thickness |
| Pulse Duration | 3-8 ms | Square wave profile |
| Weld Speed | 3-8 mm/sec | Continuous wave mode |
| Spot Diameter | 0.4 mm | Focused at weld plane |
| Shielding Gas | Argon | 20 L/min, coaxial |
| Preheat | 150°C | Reduces thermal stress |
| Interpass Temperature | < 300°C | Prevents grain coarsening |

**Weld Joint Design**:

```
    Lap Joint Configuration (Cross-Section)

    Top Shell
    ─────────────────────┐
                         │  ← 0.4mm overlap
    Bottom Shell ────────┘
                         │
    ← Laser Beam →       │
         ↓               │
         ●               │  ← Weld pool (0.4mm × 0.4mm)
         │               │
    ─────┴───────────────┘
```

The lap joint provides:
- Self-aligning assembly (top shell nests into bottom shell)
- 0.4 mm overlap zone for weld bead placement
- Adequate joint strength (> 200 N/cm, far exceeding requirements)

### Weld Quality Monitoring

**Real-Time Monitoring**:
- Photodiode monitors reflected laser light (weld pool stability indicator)
- Infrared pyrometer tracks surface temperature (target: 1650°C ± 100°C)
- Acoustic emission sensor detects spatter or porosity formation

**Post-Weld Inspection**:
- 100% visual inspection under 10× magnification
- 100% X-ray inspection for internal porosity
- 100% leak test per MIL-STD-883, Method 1014

### Microplasma Arc Welding (Alternative)

For prototype and low-volume production, microplasma arc welding provides an
alternative joining method:

| Parameter | Value |
|-----------|-------|
| Plasma Gas | Argon (99.999%) |
| Shielding Gas | Argon/Hydrogen (95/5) |
| Current | 2-5 A |
| Arc Length | 0.5-1.0 mm |
| Weld Speed | 2-4 mm/sec |
| Nozzle Diameter | 0.5 mm |

Advantages: Lower thermal input, narrower HAZ, better for thin-wall sections
Disadvantages: Lower throughput, higher operator skill requirement

## Biocompatibility Testing

### ISO 10993 Test Matrix for Encapsulation

| Test | Standard | Duration | Sample Size | Accept Criteria |
|------|----------|----------|-------------|-----------------|
| Cytotoxicity | ISO 10993-5 | 24-72 hr | 3 extracts | Grade 0-1 reactivity |
| Sensitization | ISO 10993-10 | 14 days | 10 animals | No sensitization |
| Irritation | ISO 10993-10 | 14 days | 10 animals | Negligible irritation |
| Acute Systemic Toxicity | ISO 10993-11 | 72 hr | 5 animals | No systemic effects |
| Subchronic Toxicity | ISO 10993-11 | 90 days | 20 animals | No adverse effects |
| Genotoxicity | ISO 10993-3 | In vitro + vivo | Per standard | Negative ( Ames, micronucleus) |
| Implantation | ISO 10993-6 | 12 weeks | 10 animals | Minimal tissue response |
| Chronic Toxicity | ISO 10993-11 | 6+ months | 20 animals | No long-term adverse effects |

### Corrosion Testing

**Electrochemical Impedance Spectroscopy (EIS)**:

The encapsulation resistance to corrosion is characterized by EIS in simulated body
fluid at 37°C:

| Frequency Range | Measurement | Accept Criteria |
|----------------|-------------|-----------------|
| 100 kHz - 10 mHz | Impedance magnitude | |Z| > 10⁷ Ω·cm² at 1 Hz |
| 100 kHz - 10 mHz | Phase angle | > 80° at 1 Hz (capacitive behavior) |

A high impedance magnitude and near-capacitive phase angle indicate an intact,
protective passive layer.

**Potentiodynamic Polarization**:

| Parameter | Value | Accept Criteria |
|-----------|-------|-----------------|
| Corrosion Potential (Ecorr) | Measured vs. SCE | > -200 mV (noble) |
| Breakdown Potential (Eb) | Measured vs. SCE | > +200 mV (no pitting) |
| Corrosion Current (Icorr) | Derived from Tafel | < 0.01 μA/cm² |

## RF Transparency Considerations

### Telemetry Frequency

The iPACE-CHIP operates at 13.56 MHz for wireless telemetry. The titanium encapsulation
must be RF-transparent enough to allow adequate signal coupling:

**Skin Depth in Titanium at 13.56 MHz**:

```
δ = √(2ρ / ωμμ₀)

Where:
  ρ   = resistivity of Ti (54 × 10⁻⁸ Ω·m)
  ω   = 2π × 13.56 × 10⁶ rad/s
  μ   = relative permeability (1.0 for Ti)
  μ₀  = 4π × 10⁻⁷ H/m

δ = √(2 × 54 × 10⁻⁸) / (2π × 13.56 × 10⁶ × 4π × 10⁻⁷)
δ = √(108 × 10⁻⁸) / (214.6 × 10⁻¹)
δ = 31.3 μm
```

At 31.3 μm skin depth, a 0.4 mm (400 μm) wall provides approximately 13 skin
depths of attenuation:

```
Attenuation = 20 × log₁₀(e) × t/δ = 8.686 × 400/31.3 = 111 dB
```

### RF Transparency Solutions

The 111 dB attenuation of solid titanium is far too high for practical telemetry.
The iPACE-CHIP uses strategic openings in the encapsulation:

**Antenna Window Design**:

```
    Encapsulation Top View

    ┌──────────────────────────────┐
    │                              │
    │   ┌──────────────────────┐  │
    │   │                      │  │
    │   │   RF Window          │  │
    │   │   (No Titanium)      │  │
    │   │   Filled with        │  │
    │   │   Ceramic Composite  │  │
    │   │                      │  │
    │   └──────────────────────┘  │
    │                              │
    │   Titanium Shell            │
    │   (Solid, Hermetic)         │
    │                              │
    └──────────────────────────────┘
```

**RF Window Material**: Alumina-filled PEEK (polyetheretherketone)
- Dielectric constant: 3.5 at 13.56 MHz
- Loss tangent: 0.003 at 13.56 MHz
- Biocompatibility: ISO 10993 compliant
- Coefficient of thermal expansion: 20 × 10⁻⁶ /°C (CTE-matched to titanium)
- Sealed to titanium by laser welding of surrounding titanium frame

**Window Dimensions**:
- Size: 6.0 × 4.0 mm
- Thickness: 1.0 mm
- RF attenuation through window: < 3 dB
- Hermetic seal maintained by Ti frame weld around window perimeter

### Antenna Design for Through-Encapsulation Telemetry

The iPACE-CHIP includes an internal coil antenna behind the RF window:

```
    Antenna Geometry (Top View)

    ┌───────────────────────┐
    │  ┌─────────────────┐  │
    │  │  ┌───────────┐  │  │
    │  │  │  ┌─────┐  │  │  │
    │  │  │  │     │  │  │  │
    │  │  │  │ IC  │  │  │  │
    │  │  │  └─────┘  │  │  │
    │  │  │           │  │  │
    │  │  └───────────┘  │  │
    │  │    5-turn coil   │  │
    │  └─────────────────┘  │
    │     8mm × 5mm          │
    └───────────────────────┘
```

| Antenna Parameter | Value |
|-------------------|-------|
| Number of Turns | 5 |
| Trace Width | 200 μm |
| Trace Spacing | 100 μm |
| Inductance | ~2.5 μH |
| Q Factor (in package) | ~15 at 13.56 MHz |
| Coupling Distance | 5-15 mm through tissue |

## Mechanical Design Verification

### Finite Element Analysis (FEA)

The encapsulation is analyzed under worst-case mechanical loads:

| Load Case | Description | Safety Factor Required |
|-----------|------------|----------------------|
| Implantation | Surgical insertion force | > 3.0 |
| Chronic Loading | Tissue pressure (0-50 kPa) | > 5.0 |
| Impact | Accidental blow (100G, 1 ms) | > 2.0 |
| Compression | External body force (500 N) | > 2.0 |
| Fatigue | Cardiac pulsation (10⁸ cycles) | > 10.0 |

### FEA Results Summary

```
Von Mises Stress Distribution (100G Impact):

    ┌────────────────────────────────┐
    │  12 MPa    45 MPa    12 MPa   │
    │     ╲         │         ╱     │
    │       28 MPa ─┤─ 28 MPa      │
    │          ╲    │    ╱          │
    │            ───┤───            │
    │          ╱    │    ╲          │
    │       15 MPa ─┤─ 15 MPa      │
    │     ╱         │         ╲     │
    │  8 MPa     20 MPa     8 MPa   │
    └────────────────────────────────┘

    Maximum Stress: 45 MPa (at corner)
    Yield Strength: 170 MPa
    Safety Factor: 170/45 = 3.8 (> 2.0 required) ✓
```

### Drop Test

Per ASTM F2052 (modified for implant context):

| Parameter | Specification |
|-----------|--------------|
| Drop Height | 1.0 m |
| Surface | Hardwood |
| Orientation | 6 orientations × 3 samples |
| Accept Criteria | No cracking, no hermeticity loss |
| Post-Test | Fine leak test, visual, functional |

### Vibration Test

Per IEC 60068-2-6:

| Parameter | Specification |
|-----------|--------------|
| Frequency Range | 10-2000 Hz |
| Acceleration | 20G |
| Duration | 2 hours per axis (3 axes) |
| Sweep Rate | 1 octave/minute |
| Post-Test | Fine leak test, visual inspection |

## Manufacturing Process Flow

### Encapsulation Assembly Sequence

```
Step 1: Incoming Inspection
    │  Verify hermetic package (from 14.2.1)
    │  Verify titanium shells (incoming QC)
    │  Verify RF window subassembly
    ▼
Step 2: Underfill Application
    │  Dispense medical-grade silicone into bottom shell
    │  Vacuum degas to remove bubbles
    │  Cure silicone (150°C, 1 hour)
    ▼
Step 3: Package Placement
    │  Place hermetic package into bottom shell
    │  Align feedthroughs with shell openings
    │  Verify alignment (automated vision system)
    ▼
Step 4: Top Shell Placement
    │  Apply silicone to top shell interior
    │  Place top shell onto bottom shell
    │  Verify nesting and alignment
    ▼
Step 5: Laser Welding
    │  Weld perimeter seam (automated laser welder)
    │  Weld RF window frame (if applicable)
    │  Real-time weld monitoring (IR + acoustic)
    ▼
Step 6: Post-Weld Processing
    │  Clean (isopropanol + DI water)
    │  Dry (nitrogen blow + vacuum)
    │  Surface treatment (acid etch or anodize)
    ▼
Step 7: Final Inspection
    │  Visual inspection (10× magnification)
    │  Dimensional measurement (CMM)
    │  X-ray inspection (internal structure)
    │  Hermeticity test (MIL-STD-883)
    │  Electrical test (feedthrough continuity)
    ▼
Step 8: Packaging for Sterilization
    │  Place in sterile barrier packaging
    │  Label with lot number, expiry date
    │  Ship to sterilization facility
```

### Process Controls

| Step | Critical Parameter | Control Method | Specification |
|------|-------------------|----------------|---------------|
| Silicone cure | Temperature, time | Thermocouple, timer | 150°C ± 5°C, 60 ± 2 min |
| Package alignment | X-Y position | Vision system | < 0.1 mm offset |
| Laser weld energy | Pulse energy, duration | Closed-loop control | Per qualified window |
| Surface treatment | HF concentration, time | Titration, timer | 1% ± 0.1%, 60 ± 2 sec |
| Hermeticity | He leak rate | Mass spectrometer | < 1 × 10⁻⁹ atm·cc/sec |

## Summary

The iPACE-CHIP titanium encapsulation system provides a biocompatible, mechanically
robust, and RF-transparent protective enclosure for 20+ year implantation. Grade 1 CP
titanium is selected for its superior corrosion resistance, MRI compatibility, and
absence of potentially toxic alloying elements. The encapsulation design incorporates
a ceramic-composite RF window for telemetry, laser-welded seams for hermeticity, and
medical-grade silicone underfill for mechanical protection. Comprehensive biocompatibility
testing per ISO 10993 and mechanical verification per ASTM/IEC standards ensure patient
safety throughout the device lifetime.

## References

1. ASTM F67-13, "Standard Specification for Commercially Pure Titanium."
2. ISO 10993-1:2018, "Biological Evaluation of Medical Devices."
3. ASTM F2052-15, "Standard Test Method for Measurement of Magnetically Induced Displacement Force."
4. IEC 60068-2-6, "Environmental Testing — Sinusoidal Vibration."
5. J. Black, "Biological Performance of Materials," CRC Press, 5th Ed., 2020.
6. R. Boyer, "Materials Properties Handbook: Titanium Alloys," ASM International.
7. iPACE-CHIP Encapsulation Design Document, Internal, Rev 2.5.
8. M. Long, "Titanium Alloys for Implantable Medical Devices," Biomaterials, 2022.
