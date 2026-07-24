# 14.2.1 Hermetic Packaging for iPACE-CHIP

## Overview

The iPACE-CHIP implantable medical device requires hermetic packaging that maintains a
sealed internal environment for 20+ years while implanted in the human body. Any ingress
of body fluids into the package cavity will cause immediate corrosion and functional
failure of the semiconductor die. This chapter defines the hermetic packaging requirements,
design architecture, sealing processes, and verification methods that ensure the
iPACE-CHIP achieves its lifetime reliability target in the most hostile operating
environment — the human body.

## Hermeticity Requirements

### Definition of Hermeticity

Hermeticity refers to the ability of a package to prevent gas or liquid permeation
through the package walls, seals, or feedthroughs. For medical implants, the standard
is defined by MIL-STD-883, Method 1014:

**Fine Leak Rate (He)**: < 1 × 10⁻⁹ atm·cc/sec at 1 atm He overpressure
**Gross Leak**: No bubbles observed during fluorocarbon immersion within 60 seconds

### Why Hermeticity Matters for iPACE-CHIP

The human body presents a uniquely aggressive environment:

| Parameter | Value | Impact |
|-----------|-------|--------|
| Body Temperature | 37°C ± 1°C | Accelerates corrosion and diffusion |
| Saline Concentration | 0.9% NaCl | Electrolyte enhances galvanic corrosion |
| pH | 7.4 ± 0.1 | Mildly alkaline, attacks some metals |
| Oxygen Partial Pressure | 40 mmHg (venous) | Oxidizes exposed metal |
| Protein Adsorption | Continuous | Can create pathways for ion transport |
| Mechanical Stress | Pulsatile, 1-10 Hz | Fatigue on seal interfaces |

Without hermetic sealing, moisture ingress rates in the body would cause die
failure within weeks to months, far below the 20-year requirement.

### Leakage Rate Lifetime Projection

The iPACE-CHIP uses a conservative lifetime model based on the Arrhenius equation:

```
t_failure = Q₀ × exp(Ea / kT)

Where:
  t_failure = time to critical moisture level
  Q₀        = pre-exponential constant (derived from accelerated testing)
  Ea        = activation energy (0.7 eV typical for hermetic seal failure)
  k         = Boltzmann constant (8.617 × 10⁻⁵ eV/K)
  T         = absolute temperature (310K for body temperature)
```

For a fine leak rate of 1 × 10⁻⁹ atm·cc/sec at 37°C, the projected time to
critical internal humidity (> 500 ppm H₂O) exceeds 50 years, providing a 2.5×
margin over the 20-year requirement.

## Package Architecture

### Package Cross-Section

The iPACE-CHIP uses a ceramic-titanium hybrid hermetic package:

```
                  Titanium Lid (0.3mm)
              ═══════════════════════════
             ║  Laser Weld Seam (360°)  ║
         ┌───╨───────────────────────────╨───┐
         │                                    │
         │     Alumina Ceramic Ring           │
         │     (96% Al₂O₃, 1.5mm height)     │
         │                                    │
    ═════╪════════════════════════════════════╪═══  ← TiN/Au plating
         │                                    │
         │     ┌──────────────────────┐      │
         │     │                      │      │
         │     │   iPACE-CHIP Die     │      │
         │     │   (Eutectic Attach)  │      │
         │     │                      │      │
         │     └──────────────────────┘      │
         │                                    │
         │     Titanium Package Base          │
         │     (Grade 1 Ti, 0.5mm thick)      │
         │                                    │
         │  ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐   │
         │  │FT│  │FT│  │FT│  │FT│  │FT│   │  ← Feedthroughs
         └──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘
              │    │    │    │    │
              ▼    ▼    ▼    ▼    ▼
         ┌─────────────────────────────────┐
         │  Platinum/Iridium Lead Wires    │
         │  (connected to electrodes)      │
         └─────────────────────────────────┘
```

### Materials Selection

| Component | Material | Rationale |
|-----------|----------|-----------|
| Package Base | Grade 1 Titanium (CP Ti) | Biocompatible, weldable, low modulus |
| Package Lid | Grade 1 Titanium (CP Ti) | Matches base for laser welding |
| Ceramic Ring | 96% Alumina (Al₂O₃) | Hermetic, biocompatible, rigid |
| Feedthrough Alumina | 99.6% Alumina | Higher purity for better seal |
| Feedthrough Conductor | Pt/Ir (90/10) | Biocompatible, corrosion resistant |
| Die Attach | Au/Sn eutectic (80/20) | Hermetic, high-temperature stable |
| Wire Bond | Au (99.99%) | Thermocompression bonding |
| Lid Seal | Au/Sn preform | Eutectic brazing |
| Internal Plating | TiN/Au | Adhesion and biocompatibility |

### Package Dimensions

| Parameter | Specification | Tolerance |
|-----------|--------------|-----------|
| Overall Length | 12.0 mm | ±0.1 mm |
| Overall Width | 10.0 mm | ±0.1 mm |
| Overall Height | 3.5 mm | ±0.15 mm |
| Ceramic Ring ID | 8.0 mm | ±0.05 mm |
| Ceramic Ring Height | 1.5 mm | ±0.05 mm |
| Ti Base Thickness | 0.5 mm | ±0.03 mm |
| Ti Lid Thickness | 0.3 mm | ±0.03 mm |
| Cavity Volume | ~96 mm³ | ±5 mm³ |
| Feedthrough Count | 24 | - |
| Feedthrough Pitch | 0.5 mm | ±0.025 mm |

## Titanium Package Fabrication

### Titanium Base Manufacturing

**Raw Material**: Grade 1 commercially pure titanium per ASTM F67
- Composition: Ti ≥ 99.5%, Fe < 0.20%, O < 0.18%
- Sheet thickness: 0.5 mm ± 0.03 mm
- Surface finish: Ra < 0.4 μm (as-received)

**Forming Process**:

1. **Blanking**: Laser-cut titanium blanks from coil stock
2. **Deep Drawing**: Progressive die forming the cavity shape
   - Draw ratio: < 2.0 (to avoid excessive thinning)
   - Draw speed: 50 mm/min
   - Lubricant: Chlorine-free drawing oil (removed post-forming)
3. **Trimming**: CNC trimming of drawn edges to final dimensions
4. **Machining**: CNC milling of feedthrough holes and alignment features
5. **Surface Treatment**: 
   - Alkaline cleaning (NaOH, 60°C, 10 min)
   - Acid etch (HF/HNO₃, room temperature, 30 sec)
   - Deionized water rinse (3 cycles)
   - Vacuum bake (200°C, 10⁻⁶ Torr, 2 hours)
6. **Plating**: TiN adhesion layer (50 nm) + Au barrier layer (2 μm) in feedthrough
   bond areas

### Titanium Lid Manufacturing

**Fabrication Steps**:

1. **Blanking**: Laser-cut lids from 0.3 mm Ti sheet
2. **Forming**: Shallow draw for lid curvature (adds structural rigidity)
3. **Surface Preparation**: Same as base
4. **Weld Zone Preparation**: 
   - Localized Au plating (5 μm) at weld seam interface
   - Surface roughness: Ra < 0.2 μm at weld zone
5. **Optional**: Laser-engraved lot tracking information on lid exterior

### Ceramic Ring Manufacturing

**Material**: 96% alumina (CoorsTek or equivalent)
- Density: 3.7 g/cm³
- Flexural strength: 345 MPa
- Thermal conductivity: 24 W/m·K
- Dielectric constant: 9.4 at 1 MHz
- CTE: 6.4 × 10⁻⁶ /°C (25-300°C)

**Fabrication Steps**:

1. **Green Machining**: CNC machining of alumina green body
2. **Sintering**: 1600°C, 2 hours in air
3. **Diamond Grinding**: Final dimensional adjustment to ±0.05 mm tolerance
4. **Metallization**: Mo/Mn metallization on seal surfaces
5. **Nickel Plating**: 5 μm Ni over metallization for braze wetting
6. **Gold Plating**: 2 μm Au over Ni for Au/Sn braze compatibility

## Feedthrough Design and Fabrication

### Feedthrough Requirements

The iPACE-CHIP feedthroughs carry electrical signals between the interior package
cavity (die) and exterior (body tissue/electrodes). Each feedthrough must:

- Maintain hermetic seal (Leak rate < 1 × 10⁻⁹ atm·cc/sec He)
- Provide electrical isolation between adjacent conductors (> 100 MΩ at 500V)
- Withstand 37°C saline environment for 20+ years
- Support stimulation currents up to 20 mA per conductor
- Be MRI-compatible (non-ferromagnetic)

### Feedthrough Types

**Type A — Standard Signal Feedthrough** (20 conductors):
- Conductor: Pt/Ir (90/10), 0.25 mm diameter
- Insulator: 99.6% Alumina, 0.5 mm OD
- Pitch: 0.5 mm (center-to-center)
- Hermetic seal: Glass-ceramic brazing

**Type B — Power Feedthrough** (2 conductors):
- Conductor: Pt/Ir (90/10), 0.4 mm diameter
- Insulator: 99.6% Alumina, 0.7 mm OD
- Pitch: 1.0 mm
- Hermetic seal: Glass-ceramic brazing
- Current rating: 50 mA continuous

**Type C — Optical Feedthrough** (2 channels):
- Conductor: None (optical fiber)
- Window: Sapphire, 0.3 mm diameter
- Insulator: 99.6% Alumina
- For future optical telemetry (not used in Gen 1)

### Glass-to-Metal Seal Process

The hermetic seal between Pt/Ir conductors and alumina insulator is achieved by
glass-ceramic brazing:

1. **Glass Preparation**: 
   - Composition: Al₂O₃-SiO₂-based glass (CTE matched to Pt/Ir and alumina)
   - Particle size: 10-44 μm
   - Transition temperature: 450°C

2. **Seal Formation**:
   - Apply glass preform around conductor in alumina sleeve
   - Fire in hydrogen atmosphere furnace at 850°C for 15 minutes
   - Glass flows and wets both metal and ceramic surfaces
   - Controlled cooling to manage residual stress

3. **Post-Fire Processing**:
   - Visual inspection for cracks or voids
   - Hermeticity testing (see Verification section)
   - Electrical testing (insulation resistance, DC resistance)

### Feedthrough Insulation Resistance

| Condition | Minimum Insulation Resistance |
|-----------|------------------------------|
| As-manufactured (dry) | > 10 GΩ |
| After HAST (130°C, 85% RH, 96 hr) | > 1 GΩ |
| After 20-year accelerated life test | > 100 MΩ |
| During stimulation (20 mA, 100 μs pulse) | > 10 MΩ |

## Die Attach and Wire Bonding

### Die Attach

The iPACE-CHIP die is attached to the titanium package base using Au/Sn eutectic
solder (80% Au, 20% Sn):

**Process Parameters**:
- Preform thickness: 25 μm
- Preform size: Matched to die footprint + 0.2 mm margin
- Reflow temperature: 280°C (Au/Sn eutectic point)
- Reflow atmosphere: Forming gas (95% N₂ / 5% H₂)
- Reflow time: 60 seconds at peak temperature
- Cooling rate: < 5°C/second to minimize thermal stress

**Quality Requirements**:
- Bond coverage > 95% (verified by scanning acoustic microscopy)
- No voids > 50 μm diameter within die footprint
- Die shear strength > 25 N (for 10 mm² die)
- Thermal resistance: < 5°C·cm²/W (die to package base)

### Wire Bonding

Gold wire bonds connect the die bond pads to the package feedthrough pads:

**Wire Specification**:
- Material: 99.99% Au
- Diameter: 25 μm (1 mil)
- Ball diameter after first bond: 62.5 μm (2.5× wire diameter)
- Stitch length: 75-100 μm

**Bond Parameters (Thermosonic)**:
- First bond (die pad): 150°C stage, 35 g force, 10 ms ultrasonic time
- Second bond (package pad): 150°C stage, 40 g force, 15 ms ultrasonic time
- Wire loop height: 100-150 μm above die surface
- Loop profile: Standard loop with 45° neck angle

**Quality Requirements**:
- Pull strength: > 3 g (minimum)
- Ball bond shear strength: > 15 g
- Ball bond diameter: 55-70 μm
- No neck cracks, no lifted bonds, no smeared ball bonds
- 100% visual inspection per MIL-STD-883, Method 2010

### Wire Bond Layout

```
┌──────────────────────────────────────────────┐
│                   Package Top View             │
│                                                │
│    FT    FT    FT    FT    FT    FT           │
│    ●─────●─────●─────●─────●─────●           │
│    │╲   ╱│╲   ╱│╲   ╱│╲   ╱│╲   ╱│           │
│    │ ╲ ╱ │ ╲ ╱ │ ╲ ╱ │ ╲ ╱ │ ╲ ╱ │           │
│    │  ╲╱ │  ╲╱ │  ╲╱ │  ╲╱ │  ╲╱ │           │
│    │  ╱╲ │  ╱╲ │  ╱╲ │  ╱╲ │  ╱╲ │           │
│    │ ╱ ╲ │ ╱ ╲ │ ╱ ╲ │ ╱ ╲ │ ╱ ╲ │           │
│    │╱   ╲│╱   ╲│╱   ╲│╱   ╲│╱   ╲│           │
│    ●─────●─────●─────●─────●─────●           │
│    ┌─────────────────────────────┐            │
│    │                             │            │
│    │      iPACE-CHIP Die         │            │
│    │                             │            │
│    │   ○ ○ ○ ○ ○ ○ ○ ○ ○ ○     │ ← Bond pads│
│    │                             │            │
│    │   ○ ○ ○ ○ ○ ○ ○ ○ ○ ○     │            │
│    │                             │            │
│    └─────────────────────────────┘            │
│    ●─────●─────●─────●─────●─────●           │
│    │╲   ╱│╲   ╱│╲   ╱│╲   ╱│╲   ╱│           │
│    ●─────●─────●─────●─────●─────●           │
│    FT    FT    FT    FT    FT    FT           │
│                                                │
│    FT = Feedthrough Pad    ● = Package Pad     │
└──────────────────────────────────────────────┘
```

## Laser Welding

### Lid Sealing Process

The titanium lid is hermetically sealed to the package base by laser welding:

**Laser Parameters**:
- Laser type: Pulsed Nd:YAG, 1064 nm wavelength
- Pulse energy: 0.5-2.0 J (adjusted per weld seam geometry)
- Pulse duration: 2-5 ms
- Spot size: 0.3 mm diameter
- Weld speed: 5 mm/sec (continuous wave mode for seal seam)
- Shielding gas: Argon, 15 L/min flow rate
- Weld seam width: 0.4-0.6 mm

**Seal Sequence**:

1. **Pre-Weld Preparation**:
   - Package assembled with die, wire bonds, and internal components
   - Internal cavity purged with dry nitrogen (dew point < -60°C)
   - Lid placed on package with Au/Sn preform between lid and ceramic ring
   - Fixture holds assembly with 5 N downward force

2. **Eutectic Braze** (Lid to Ceramic):
   - Localized heating with defocused laser to 280°C
   - Au/Sn preform melts and wets ceramic metallization
   - Forms primary hermetic seal between lid and ceramic ring
   - 5-minute hold at temperature for complete wetting

3. **Laser Weld** (Ceramic to Titanium Base):
   - 360° continuous weld around package perimeter
   - Overlap start/end point by 0.5 mm
   - 12 segments, each with individual weld parameters
   - Post-weld: Visual inspection for cracks, porosity, or incomplete fusion

4. **Post-Weld Processing**:
   - Cool to room temperature over 30 minutes
   - Remove from fixture
   - Clean with isopropanol and DI water
   - External Au plating for biocompatibility (if required)

### Weld Quality Requirements

| Parameter | Requirement | Inspection Method |
|-----------|------------|-------------------|
| Weld Penetration | 70-90% of base material thickness | Cross-section metallography |
| Weld Width | 0.4-0.6 mm | Visual/optical measurement |
| Porosity | No interconnected porosity | X-ray inspection |
| Cracks | Zero cracks | Visual + dye penetrant |
| Misalignment | < 0.1 mm from designed path | Optical inspection |
| Undercut | < 0.05 mm | Optical profiling |
| Discoloration | Light straw color maximum | Visual (indicates oxidation) |

## Hermeticity Verification

### Fine Leak Test (MIL-STD-883, Method 1014)

**Test Procedure**:

1. **Pressurization**: Expose package to 1 atm He for 2 hours minimum
2. **Dwell Time**: Allow 1 hour for He to penetrate any leak paths
3. **Detection**: Place package in He mass spectrometer detector
4. **Measurement**: Record He leak rate
5. **Accept Criteria**: Leak rate < 1 × 10⁻⁹ atm·cc/sec

**Temperature Correction**: Test at 25°C, corrected for body temperature using:

```
L(37°C) = L(25°C) × exp[Ea/k × (1/298 - 1/310)]
```

### Gross Leak Test (MIL-STD-883, Method 1014)

**Test Procedure**:

1. Submerge package in fluorocarbon liquid (FC-72 or equivalent) at 125°C
2. Observe for 60 seconds
3. Accept: No stream of bubbles from any seal interface
4. Reject: Any continuous bubble stream indicates gross leak path

### Helium Leak Detection System

```
┌─────────────────────────────────────────┐
│          He Leak Detection System         │
│                                           │
│  ┌──────────┐    ┌─────────────────┐     │
│  │ Package  │    │ Mass Spectrometer│     │
│  │ in Test  │───→│   Detector       │     │
│  │ Chamber  │    │ (Sensitivity:    │     │
│  │          │    │  10⁻¹² cc/sec)   │     │
│  └──────────┘    └────────┬────────┘     │
│                           │               │
│  ┌──────────┐    ┌───────┴────────┐      │
│  │ Vacuum   │    │  Display &     │      │
│  │ Pump     │←───│  Data Logger   │      │
│  │ System   │    │                │      │
│  └──────────┘    └────────────────┘      │
│                                           │
│  Test Cycle Time: ~3 minutes/package      │
│  Throughput: 200 packages/shift           │
└─────────────────────────────────────────┘
```

### Accelerated Life Testing

To verify hermeticity over the 20-year implant lifetime, accelerated life testing
uses elevated temperature and humidity:

| Test Condition | Temperature | Duration | Equivalence |
|---------------|-------------|----------|-------------|
| 85°C/85% RH, unpowered | 85°C | 2,000 hr | ~10 years at 37°C |
| 130°C/85% RH (HAST) | 130°C | 96 hr | ~5 years at 37°C |
| Boiling water test | 100°C | 1 hr | Screen for gross defects |
| Thermal cycling | -40°C to +85°C | 1,000 cycles | Mechanical stress screening |

Post-test verification includes:
- Fine leak rate measurement (must still meet 1 × 10⁻⁹ atm·cc/sec)
- Insulation resistance between feedthrough conductors
- Die functionality verification
- Internal humidity measurement (destructive, sample-based)

## Biocompatibility of Package Materials

### ISO 10993 Compliance

All materials in contact with body tissue must pass biocompatibility testing:

| Material | ISO 10993 Tests Required | Status |
|----------|-------------------------|--------|
| Grade 1 Ti | Cytotoxicity, sensitization, irritation, systemic toxicity, genotoxicity, implantation, chronic toxicity | Qualified |
| Pt/Ir (90/10) | Cytotoxicity, sensitization, implantation | Qualified |
| 96% Alumina | Cytotoxicity, sensitization, implantation | Qualified |
| Au/Sn solder | Cytotoxicity, sensitization | Qualified (encapsulated) |

### Corrosion Resistance

The titanium package must resist corrosion in simulated body fluid (SBF) at 37°C:

**SBF Composition** (per Kokubo):
- NaCl: 8.0 g/L
- NaHCO₃: 0.355 g/L
- KCl: 0.225 g/L
- K₂HPO₄: 0.230 g/L
- MgCl₂: 0.311 g/L
- CaCl₂: 0.292 g/L
- Na₂SO₄: 0.072 g/L
- Tris-HCl buffer to pH 7.4

**Test Results** (20-year equivalent at 85°C):
- Titanium mass loss: < 0.001 mg/cm²/year
- No pitting corrosion observed
- TiO₂ passive layer maintained throughout test
- Feedthrough conductor corrosion: None detected

## Summary

Hermetic packaging for the iPACE-CHIP achieves 20+ year lifetime reliability through
a titanium-alumina hybrid package with glass-to-metal feedthrough seals, Au/Sn eutectic
die attach, and laser-welded lid closure. The package meets MIL-STD-883 hermeticity
requirements (fine leak rate < 1 × 10⁻⁹ atm·cc/sec) and passes accelerated life
testing equivalent to 10× the intended implant duration. All package materials are
ISO 10993 biocompliant, and the non-ferromagnetic construction ensures MRI compatibility
in the post-implant clinical environment.

## References

1. MIL-STD-883, "Test Methods and Procedures for Microelectronics," Method 1014.
2. ISO 10993-1:2018, "Biological Evaluation of Medical Devices."
3. ASTM F67-13, "Standard Specification for Commercially Pure Titanium."
4. T. Kokubo, "Bioactive Glass Ceramics: Properties and Applications," Biomaterials, 1991.
5. H. Gray, "Hermetic Packaging for Implantable Medical Devices," IEEE ECTC, 2022.
6. iPACE-CHIP Package Specification, Internal Document, Rev 3.1.
7. SEMI G64, "Test Method for Hermeticity of Packages Using a Helium Leak Detector."
8. J. Lambrecht, "Titanium for Medical Implants," Springer, 2019.
