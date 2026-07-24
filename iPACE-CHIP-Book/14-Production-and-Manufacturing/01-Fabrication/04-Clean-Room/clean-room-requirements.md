# 14.1.4 Clean Room Requirements for iPACE-CHIP Fabrication

## Overview

The iPACE-CHIP semiconductor fabrication requires stringent clean room environmental
control to achieve the zero-defect manufacturing objective. Particle contamination as
small as 0.1 micrometers can cause killer defects in 180 nm features, resulting in
functional failures or latent reliability defects that may not manifest until years
after implantation. This chapter defines the clean room classification, monitoring
protocols, contamination control strategies, and qualification requirements specific
to iPACE-CHIP production.

## Clean Room Classification

### ISO 14644-1 Classification

The iPACE-CHIP fabrication requires different cleanliness levels for different process
areas. The ISO 14644-1 classification system defines maximum allowable particle
concentrations per cubic meter:

| ISO Class | 0.1 μm | 0.2 μm | 0.3 μm | 0.5 μm | 1.0 μm | 5.0 μm |
|-----------|--------|--------|--------|--------|--------|--------|
| ISO 1 | 10 | - | - | - | - | - |
| ISO 2 | 100 | 24 | 10 | - | - | - |
| ISO 3 | 1,000 | 237 | 102 | 35 | - | - |
| ISO 4 | 10,000 | 2,370 | 1,020 | 352 | 83 | - |
| ISO 5 | 100,000 | 23,700 | 10,200 | 3,520 | 832 | 29 |
| ISO 6 | - | 237,000 | 102,000 | 35,200 | 8,320 | 293 |
| ISO 7 | - | - | - | 352,000 | 83,200 | 2,930 |
| ISO 8 | - | - | - | 3,520,000 | 832,000 | 29,300 |

### iPACE-CHIP Fab Area Requirements

| Process Area | ISO Class | Rationale |
|-------------|-----------|-----------|
| Lithography | ISO 3 | 0.18 μm features require sub-0.5 μm particle control |
| Etch (Dry/Wet) | ISO 4 | Post-etch defects directly impact device yield |
| Deposition (CVD/PVD) | ISO 4 | Thin film defects cause reliability failures |
| Ion Implantation | ISO 5 | Particle contamination during implant causes junction defects |
| CMP | ISO 5 | Post-CMP particles cause metal bridging defects |
| Diffusion/Oxidation | ISO 5 | High-temperature process, moderate contamination risk |
| Wet Processing | ISO 6 | Chemical cleaning reduces particle adhesion |
| Metrology | ISO 5 | Measurement accuracy requires clean environment |
| Wafer Sorting | ISO 6 | Post-fab testing, less sensitive to particle defects |
| Packaging/Assembly | ISO 5 | Wire bond and die attach require low particle counts |

### FED-STD 209E Correlation

For reference to the older US Federal Standard:

| ISO Class | FED-STD 209E Equivalent |
|-----------|------------------------|
| ISO 3 | Class 1 |
| ISO 4 | Class 10 |
| ISO 5 | Class 100 |
| ISO 6 | Class 1,000 |
| ISO 7 | Class 10,000 |
| ISO 8 | Class 100,000 |

## Air Handling Systems

### HEPA and ULPA Filtration

The clean room uses a combination of filter technologies:

**HEPA (High Efficiency Particulate Air) Filters**:
- Efficiency: 99.97% at 0.3 μm (DOP test method)
- Used in: ISO 5-8 areas
- Face velocity: 0.3-0.5 m/s
- Filter media: Borosilicate glass microfiber

**ULPA (Ultra-Low Penetration Air) Filters**:
- Efficiency: 99.9995% at 0.12 μm
- Used in: ISO 3-4 areas (lithography, etch)
- Required for iPACE-CHIP critical layers
- More expensive but essential for sub-0.5 μm particle control

### Airflow Design

The iPACE-CHIP clean room uses a unidirectional (laminar) airflow design in critical
areas and turbulent airflow in support areas:

**Unidirectional Flow (Critical Areas)**:
```
┌─────────────────────────────────────┐
│  ULPA Filter Plenum                  │
│  ══════════════════════════════════  │
│  ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓  │  ← 0.45 m/s uniform velocity
│  ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓  │
│  ┌──────────┐    ┌──────────┐      │
│  │ Wafer    │    │ Equipment│      │  ← Equipment positioned to not
│  │ Process  │    │          │      │    block airflow
│  └──────────┘    └──────────┘      │
│  ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓  │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  ← Raised floor with return grilles
└─────────────────────────────────────┘
```

**Turbulent Flow (Support Areas)**:
```
┌─────────────────────────────────────┐
│  HEPA Filter Panels (Ceiling)       │
│  ══════════════════════════════════  │
│     ↘   ↓   ↙   ↓   ↘   ↓   ↙    │
│       ↘ ↓ ↙     ↘ ↓ ↙     ↘ ↓    │
│         ↓    Equipment    ↓         │  ← 50-70% ceiling coverage
│         ↓   ↗   ↓   ↖   ↓         │
│    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  ← Return air plenum
└─────────────────────────────────────┘
```

### Air Change Rates

| Area Type | Air Changes/Hour | Recirculation Rate |
|-----------|-----------------|-------------------|
| ISO 3 Lithography | 600-900 | 80% recirculated |
| ISO 4 Process | 300-600 | 70% recirculated |
| ISO 5 Support | 150-300 | 60% recirculated |
| ISO 6-7 Utility | 60-150 | 40% recirculated |

### Temperature and Humidity Control

**Temperature**: 21.0°C ± 0.5°C throughout the clean room
- Tighter control (±0.1°C) in lithography areas due to CD sensitivity to temperature
- HVAC system redundancy: N+1 configuration with automatic failover

**Relative Humidity**: 45% ± 5% nominal
- Lithography areas: 42% ± 2% (photoresist sensitivity)
- Wet processing areas: 50% ± 5% (chemical compatibility)
- Electrostatic discharge prevention: Minimum 30% RH required

**Pressure Cascades**: Positive pressure maintained between areas:
```
Pressure Hierarchy (relative to exterior):
Lithography:     +15 Pa  (highest priority)
Etch:            +12 Pa
Deposition:      +10 Pa
Ion Implant:     +8 Pa
CMP:             +6 Pa
Wet Processing:  +4 Pa
Service Corridor: +2 Pa
Subfab:          -5 Pa  (negative, prevents backstreaming)
Building Exterior: 0 Pa (reference)
```

## Particle Contamination Control

### Particle Budget for 180 nm iPACE-CHIP

A killer defect occurs when a particle lands on a critical feature and causes a
short, open, or parametric failure. The maximum allowable particle density is
calculated from the target yield:

```
Yield = e^(-D × A)

Where:
  Y    = target yield (0.98 for iPACE-CHIP)
  D    = defect density (defects/cm²)
  A    = critical area per die (cm²)

Solving for D:
  D = -ln(Y) / A = -ln(0.98) / 0.1 cm² = 0.202 defects/cm²
```

This maximum allowable defect density of 0.2 defects/cm² must be distributed
across all process layers:

| Process Layer | Defect Budget (def/cm²) | Critical Area (mm²) | Expected Defects |
|--------------|------------------------|---------------------|------------------|
| Active (OD) | 0.02 | 4.5 | 0.009 |
| Poly Gate | 0.03 | 3.2 | 0.010 |
| Contact | 0.04 | 2.8 | 0.011 |
| Metal 1 | 0.03 | 5.1 | 0.015 |
| Via 1 | 0.02 | 3.5 | 0.007 |
| Metal 2 | 0.02 | 4.2 | 0.008 |
| Via 2 | 0.02 | 3.0 | 0.006 |
| Metal 3 | 0.02 | 3.8 | 0.008 |
| Via 3 | 0.01 | 2.5 | 0.003 |
| Metal 4 | 0.02 | 4.0 | 0.008 |
| Passivation | 0.02 | 6.0 | 0.012 |
| **Total** | **0.23** | - | **0.089** |

### Particle Sources and Mitigation

**People**: The dominant source of particle generation in a clean room

| Activity | Particles Generated (>0.5 μm) |
|----------|-------------------------------|
| Standing/Walking | 100,000/min |
| Sitting | 50,000/min |
| Hand Movement | 40,000/min |
| Talking | 25,000/min |
| Operating Equipment | 10,000-100,000/min |

Mitigation strategies:
- Minimize personnel in critical areas (2-3 max during processing)
- Strict gowning protocol (see Gowning Protocol section)
- Personnel monitoring via particle counters
- Training and certification program with annual recertification

**Equipment**: Process equipment generates particles during wafer handling, chemical
delivery, and plasma processing:

- Equipment-specific particle qualification required before production use
- In-situ particle monitoring during processing
- Preventive maintenance schedules based on particle accumulation rates
- Wafer run qualification (test wafers run before production lots)

**Chemicals and Gases**: Ultra-pure chemicals and gases are essential:

| Contaminant | Maximum Allowable | Test Method |
|------------|-------------------|-------------|
| Particles in DI water | < 1/mL (> 0.05 μm) | Liquid particle counter |
| Particles in chemicals | < 25/mL (> 0.1 μm) | Liquid particle counter |
| Metallic impurities in DI water | < 10 ppt | ICP-MS |
| Metallic impurities in chemicals | < 100 ppt | ICP-MS |
| Particle in process gases | < 1/ft³ (> 0.003 μm) | Condensation counter |
| TOC in DI water | < 1 ppb | UV oxidation |

### Deionized Water Quality

DI water is the most heavily used chemical in semiconductor fabrication. iPACE-CHIP
requires ultra-high purity DI water:

| Parameter | Specification | Test Frequency |
|-----------|--------------|----------------|
| Resistivity | > 18.2 MΩ·cm | Continuous |
| Particles (> 0.05 μm) | < 1/mL | Daily |
| Dissolved O₂ | < 1 ppb | Daily |
| Total Organic Carbon | < 1 ppb | Daily |
| Silica (dissolved) | < 0.1 ppb | Weekly |
| Sodium (Na⁺) | < 0.05 ppb | Weekly |
| Chloride (Cl⁻) | < 0.1 ppb | Weekly |
| Bacteria | < 1 CFU/L | Weekly |
| Endotoxin | < 0.001 EU/mL | Monthly |

## Gowning Protocol

### Personnel Entry Procedure

The iPACE-CHIP clean room gowning protocol follows a 7-stage process:

```
Stage 1: Street Clothes Removal
         → Enter changing room, remove all personal items
         → Store in personal locker

Stage 2: Bunny Suit Base Layer
         → Don clean room undergarments
         → Don shoe covers (first layer)

Stage 3: Head Covering
         → Don bouffant cap (full head coverage)
         → Don face mask (covers nose and mouth)
         → Don safety glasses (prescription or clean room rated)

Stage 4: Upper Body
         → Don clean room smock or coverall
         → Ensure all personal clothing is fully covered

Stage 5: Hands
         → Don first pair of nitrile gloves
         → Apply glove powder-free protocol

Stage 6: Lower Body
         → Don boot covers (second layer, over shoe covers)
         → Ensure no skin exposure at wrist or ankle

Stage 7: Final Check
         → Air shower (15-second cycle, 25 m/s air velocity)
         → Mirror check for exposed skin or hair
         → Enter clean room through interlocked door
```

### Gowning Materials

| Item | Material | Particle Rating | Replacement Frequency |
|------|----------|-----------------|----------------------|
| Coverall | Polyester, low-lint | < 0.5 μm, ISO Class 4 | After 3 uses or contamination |
| Bouffant Cap | Spun-bond polyester | < 0.5 μm | Single use |
| Face Mask | melt-blown polypropylene | < 0.3 μm | Single use |
| Gloves | Nitrile, powder-free | < 0.5 μm | Every 30 min or upon contamination |
| Boot Covers | Polyester, ESD-rated | < 1.0 μm | Single use |
| Safety Glasses | Polycarbonate | N/A | Reusable, daily cleaning |

### Gowning Qualification

All personnel must pass a gowning qualification before entering the iPACE-CHIP
production clean room:

1. **Written Examination**: Contamination control principles, gowning procedure,
   emergency protocols (score ≥ 90%)
2. **Practical Demonstration**: Correct gowning sequence observed by qualified inspector
3. **Particle Count Test**: Person-level particle counter test after gowning:
   - Must generate < 35 particles/ft³ at > 0.5 μm while standing still
   - Must generate < 100 particles/ft³ at > 0.5 μm while performing basic movements
4. **Annual Recertification**: Repeat practical demonstration and particle count test

## Particle Monitoring Systems

### Real-Time Airborne Particle Counters

**Locations**: Particle counters are installed at each work station and at strategic
points throughout the clean room:

| Location | Counter Type | Sample Rate | Alert Threshold |
|----------|-------------|-------------|-----------------|
| Lithography Bay | Optical, 0.1 μm sensitivity | Continuous | 5 particles/ft³ at 0.1 μm |
| Etch Bay | Optical, 0.1 μm sensitivity | Continuous | 10 particles/ft³ at 0.1 μm |
| Each Wet Bench | Liquid particle counter | Per bath cycle | 5 particles/mL at 0.1 μm |
| Personnel Entry | Optical, 0.3 μm sensitivity | Per entry | 100 particles/ft³ at 0.3 μm |
| Supply Air Duct | Optical, 0.1 μm sensitivity | Continuous | 1 particle/ft³ at 0.1 μm |

### Wafer Surface Inspection

**Brightfield Inspection**: After critical process steps, wafers are inspected
using automated optical inspection (AOI):

| Inspection Point | Tool Example | Sensitivity | Sample Size |
|-----------------|-------------|-------------|-------------|
| After Poly Etch | KLA 28xx | 0.05 μm | 5 wafers/lot |
| After Metal 1 Dep | KLA 28xx | 0.08 μm | 3 wafers/lot |
| After Via 1 Etch | KLA 28xx | 0.06 μm | 5 wafers/lot |
| After Final Metal | KLA Surfscan SP7 | Unpatterned | 2 wafers/lot |
| Post-Passivation | KLA 28xx | 0.1 μm | 100% wafer scan |

**Darkfield Laser Scanning**: For unpatterned wafer surfaces, the KLA Surfscan
SP7 provides defect density mapping:

```
Defect Density Map Example:
┌─────────────────────────────┐
│    ·  ·                     │
│  ·    ·  ·    ·            │
│    ·  ·  ·  ·    ·        │  Legend: · = 1-2 defects/cm²
│  ·  ·    ·  ·  ·  ·      │          ● = 3-5 defects/cm²
│    ·  ·  ·  ·  ·  ·      │          ○ = > 5 defects/cm²
│  ·  ·  ·    ·  ·  ·      │
│    ·  ·  ·  ·  ·    ·    │
│  ·    ·  ·  ·    ·  ·    │
│    ·  ·    ·  ·  ·       │
│                          │
│ Overall D0: 0.15 def/cm² │
│ Yield Prediction: 98.5%  │
└─────────────────────────────┘
```

### E-Beam Inspection for Latent Defects

For iPACE-CHIP reliability requirements, e-beam inspection detects latent defects
that may not cause immediate failure but could lead to reliability failures over the
20-year implant lifetime:

- **Charged particle detection**: Identifies latent oxide defects
- **Voltage contrast**: Detects high-resistance contacts and vias
- **Floating gate integrity**: Verifies EEPROM cell charge retention

E-beam inspection sample size: 2 wafers per lot, focusing on reliability-critical
structures (stimulation output transistors, EEPROM cells, high-voltage devices).

## Static Electricity Control

### ESD Requirements

Electrostatic discharge can damage or destroy iPACE-CHIP devices. The clean room
implements comprehensive ESD control:

**Grounding**:
- All personnel grounded via conductive shoe covers and ESD flooring
- Equipment grounded via dedicated ESD ground bus
- Ground resistance: < 1 × 10⁹ Ω (personnel), < 1 Ω (equipment)

**Ionizers**:
- Overhead ionizing blowers in all process areas
- Point-of-use ionizers at each workstation
- Ion balance: ±25V offset maximum
- Decay time: < 20 seconds from ±1000V to ±100V

**ESD-Safe Materials**:
- All wafer carriers, FOUPs, and cassettes made from ESD-dissipative materials
- Surface resistivity: 1 × 10⁶ to 1 × 10⁹ Ω/square
- Clean room mats: ESD-dissipative with surface resistivity < 1 × 10⁹ Ω/square

### ESD Monitoring

| Measurement | Method | Frequency | Limit |
|------------|--------|-----------|-------|
| Person grounding | Wrist strap/heel strap tester | Every entry | < 10 MΩ |
| Flooring resistance | Parallel bar method | Monthly | 1 × 10⁶ - 1 × 10⁹ Ω |
| Work surface resistance | Surface resistance meter | Weekly | 1 × 10⁶ - 1 × 10⁹ Ω |
| Ionizer performance | Charged plate monitor | Weekly | ±25V balance, < 20s decay |
| FOUP/smotherer resistance | Surface resistance meter | Per lot | 1 × 10⁶ - 1 × 10⁹ Ω |

## Clean Room Qualification and Certification

### Initial Qualification Protocol

Before iPACE-CHIP production begins, the clean room must pass a comprehensive
qualification program:

**Airborne Particle Count Certification**:
- All locations measured per ISO 14644-1
- Minimum 9 measurement locations per zone (more for larger areas)
- At least 5 sample volumes per location (minimum 1 ft³ per sample)
- All results must meet classification limits with 95% confidence

**Air Velocity and Uniformity**:
- Unidirectional flow: 0.45 m/s ± 20%
- Measured at HEPA filter face and work height
- Uniformity coefficient < 0.25 (ratio of max to min velocity)

**Containment Recovery Test**:
- Generate particle event (powder dispersion)
- Measure time for particle count to return to baseline
- Recovery time < 20 minutes for ISO 3 areas
- Recovery time < 30 minutes for ISO 4-5 areas

**Temperature Stability**:
- Ramp rate: < 0.5°C/minute
- Uniformity: ±0.5°C across the zone
- Recovery: Within 5 minutes of equipment door opening

### Ongoing Certification Schedule

| Test | Frequency | Standard | Accept Criteria |
|------|-----------|----------|-----------------|
| Airborne particles | Monthly | ISO 14644-1 | Meets class limits |
| HEPA filter integrity | Annually | IEST-RP-CC001 | > 99.97% at 0.3 μm |
| Air velocity | Quarterly | ISO 14644-3 | Within ±20% of spec |
| Temperature/Humidity | Continuous | - | Within control limits |
| Pressurization | Weekly | - | Positive cascade maintained |
| ESD flooring | Monthly | ANSI/ESD S20.20 | Within spec range |
| AMC (Airborne Molecular) | Quarterly | ISO 14644-8 | Below threshold limits |

### Airborne Molecular Contamination (AMC)

In addition to particles, molecular contamination affects iPACE-CHIP yield:

| AMC Type | Source | Maximum Allowable | Impact |
|----------|--------|-------------------|--------|
| Organic | Outgassing, solvents | < 10 ppb | Photoresist defects |
| Acid | Process gases, cleaning | < 1 ppb | Metal corrosion |
| Base | Cleaners, personnel | < 1 ppb | Photoresist sensitivity change |
| Dopant | Phosphorus, boron sources | < 0.01 ppb | Unintentional doping |
| Metallic | Equipment, chemicals | < 0.001 ppb | Gate oxide reliability |

## Contamination Control During iPACE-CHIP Process Steps

### Critical Process Steps

**Lithography**: Most particle-sensitive step
- BARC and photoresist application must occur within 30 seconds of wafer exposure to air
- Mask/reticle handling: 100% pellicle protection, zero-contact handling
- Environmental control: ±0.1°C temperature, 42% RH ± 2%
- Particle alert triggers immediate wafer hold and investigation

**Gate Oxide Growth**: Cleanest process step required
- Pre-oxide clean: SC1, SC2, HF dip sequence
- Particle count on dummy wafer before production run
- Furnace tube purge: 2 hours minimum before loading
- Post-oxide: Zero particle addition verified on monitor wafer

**Metal Deposition**: Stress-sensitive to contamination
- Chamber base pressure < 5 × 10⁻⁸ Torr
- Target life monitoring: Change target when particle count increases > 50%
- Post-deposition particle inspection: 100% of wafers for Metal 1

### Post-Clean Hold Times

Maximum time between cleaning and next process step:

| Clean Type | Maximum Hold Time | Environment |
|-----------|-------------------|-------------|
| SC1/SC2 (pre-gate) | 4 hours | N₂ purged FOUP |
| HF last (pre-gate) | 2 hours | N₂ purged FOUP |
| Piranha (pre-metal) | 8 hours | N₂ purged FOUP |
| Post-CMP clean | 4 hours | N₂ purged FOUP |
| Post-etch strip | 24 hours | Standard clean room |

## Summary

The iPACE-CHIP clean room requirements encompass ISO 14644-1 classified environments
with ULPA filtration in critical areas, comprehensive particle monitoring, rigorous
gowning protocols, and molecular contamination control. The 180 nm fabrication process
demands particle control to 0.1 μm sensitivity with a defect density budget of
0.2 defects/cm² to achieve the 98% yield target. Combined with ESD protection, water
purity standards, and ongoing certification programs, these clean room requirements
provide the contamination-free environment essential for zero-defect iPACE-CHIP
manufacturing.

## References

1. ISO 14644-1:2015, "Cleanrooms and associated controlled environments — Part 1."
2. ISO 14644-3:2019, "Cleanrooms — Part 3: Test methods."
3. IEST-RP-CC006.3, "Testing Cleanrooms."
4. IEST-RP-CC012.2, "Considerations for Cleanroom Design."
5. SEMI E10-0304, "Standard for Definition and Measurement of Equipment Reliability."
6. ANSI/ESD S20.20-2021, "Development of an ESD Control Program."
7. iPACE-CHIP Clean Room Specification, Internal Document, Rev 2.0.
8. KLA Corporation, "Defect Reduction in Semiconductor Manufacturing," Technical Report, 2023.
9. SEMI F21-1102, "Classification of Airborne Molecular Contaminant Levels."
