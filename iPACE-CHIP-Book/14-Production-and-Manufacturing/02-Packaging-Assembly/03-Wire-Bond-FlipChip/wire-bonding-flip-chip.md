# 14.2.3 Wire Bonding and Flip Chip for iPACE-CHIP

## Overview

Die-to-package interconnection is a critical step in iPACE-CHIP assembly that directly
impacts reliability, electrical performance, and long-term implant survival. This chapter
evaluates both wire bonding and flip chip technologies for the iPACE-CHIP application,
provides detailed process specifications for the selected approach, and establishes
quality requirements supporting zero-defect manufacturing.

## Interconnect Technology Comparison

### Wire Bonding vs. Flip Chip

| Parameter | Wire Bonding | Flip Chip |
|-----------|-------------|-----------|
| Maturity | 60+ years | 40+ years |
| Medical Track Record | Extensive (pacemakers) | Growing (cochlear) |
| Maximum I/O Count | 200+ per die | 1000+ per die |
| Minimum Pitch | 50 um | 40 um |
| Loop Height | 100-200 um | 0 um (direct) |
| Inductance per Connection | 1-3 nH | < 0.1 nH |
| Resistance per Connection | 50-200 mOhm | 10-50 mOhm |
| Thermal Resistance | Higher (wire path) | Lower (direct path) |
| Rework Capability | Yes (re-bond) | Difficult |
| Die Size Flexibility | Yes (any pad arrangement) | Requires matching BGA |
| Underfill Required | No | Yes (for reliability) |
| Cost | Lower | Higher |
| Reliability (Thermal Cycling) | Good | Excellent |
| Reliability (Vibration) | Moderate | Excellent |

### iPACE-CHIP Selection

**Current Generation (Gen 1)**: Wire bonding is selected due to:
- 24 I/O count well within wire bonding capability
- Proven reliability in implantable medical devices
- Lower assembly cost and easier rework during development
- Extensive existing qualification data for medical applications

**Future Generation (Gen 3+)**: Flip chip adoption when:
- I/O count exceeds 100 (128+ channel neural interface)
- Higher bandwidth digital interfaces required
- Thermal management requires direct die-to-lid heat path
- Die area constraints demand maximum I/O density

## Wire Bonding Technology

### Gold Wire Thermosonic Bonding

The iPACE-CHIP uses gold wire thermosonic bonding, the most established interconnect
method for implantable medical devices.

**Wire Specification**:

| Parameter | Specification | Rationale |
|-----------|--------------|-----------|
| Material | 99.99% Au (4N) | Corrosion resistance, biocompatibility |
| Diameter | 25 um (1.0 mil) | Adequate current capacity |
| Elongation | 2-6% | Consistent ball formation |
| Tensile Strength | 90-140 MPa | Mechanical reliability |
| Break Load | > 4.5 g minimum | Survives thermal cycling |
| Dopant | None (un-doped) | No contamination risk |

### First Bond: Ball Bond on Die Pad

**Bond Formation Process**:

1. Gold wire melted at capillary tip using electronic flame-off (EFO) spark
2. Ball diameter controlled to 2.5x wire diameter (62.5 um for 25 um wire)
3. Capillary descends pressing ball onto aluminum bond pad with ultrasonic energy

**Ball Bond Cross-Section**:

```
    Capillary Tip
    +===========+
    |   \   /   |
    |    \ /    |
    +====|=====+
         |
    +----+----+
    |  Gold   |  Ball (62.5 um diameter)
    |  Ball   |
    +---------+
    | Al Pad  |  1 um Al / TiW barrier
    +---------+
    | SiO2    |
    +---------+
    | Si Die  |
    +---------+
```

**Ball Bond Parameters**:

| Parameter | Value | Tolerance |
|-----------|-------|-----------|
| Bond Force | 25-35 g | +/-5 g |
| Ultrasonic Power | 50-80 mW | +/-10 mW |
| Bond Time | 15-25 ms | +/-5 ms |
| Bond Temperature | 150 C | +/-5 C |
| Ball Diameter | 55-70 um | +/-5 um |
| Ball Height | 15-25 um | +/-5 um |
| Pad Opening | > 70% of ball over pad | 100% inspection |

**Bond Quality Requirements**:

| Test | Method | Accept Criteria |
|------|--------|-----------------|
| Ball Shear | MIL-STD-883 Method 2011 | > 15 g (25 um wire) |
| Ball Bond Pull | Per bond (destructive) | > 4.5 g |
| Ball Diameter | Optical measurement | 55-70 um |
| Pad Overhang | Optical/AOI | Zero overhang |
| Intermetallic Coverage | SAM or X-ray | > 90% |

### Second Bond: Stitch Bond on Package Pad

**Bond Formation Process**:

Wire routed from ball bond on die to package pad where capillary creates a
wedge-shaped stitch bond.

**Stitch Bond Parameters**:

| Parameter | Value | Tolerance |
|-----------|-------|-----------|
| Bond Force | 30-45 g | +/-5 g |
| Ultrasonic Power | 60-100 mW | +/-10 mW |
| Bond Time | 20-30 ms | +/-5 ms |
| Stitch Length | 75-100 um | +/-10 um |
| Tail Length | 25-50 um | Before EFO for next ball |

### Wire Loop Profile

The wire loop between first and second bond must satisfy mechanical and electrical
requirements.

**Loop Parameters**:

| Parameter | Specification | Reason |
|-----------|--------------|--------|
| Loop Height | 100-150 um | Clearance for lid closing |
| Neck Angle | 40-50 degrees | Prevents kinking at first bond |
| Span Angle | 5-15 degrees | Consistent profile |
| Sweep Allowance | 25% of loop height | For capillary flow during encapsulation |
| Minimum Bend Radius | > 2x wire diameter | Prevents work hardening |

```
Wire Loop Profile:

         Loop Peak
            |
            v
    +-------+-------+
    |       |       |
    |   /---+---\   |
    |  /    |    \  |
    + /     |     \ +
    First    |    Second
    Bond     |    Bond
             |
    ---------+-------- Die Surface

    Loop Height: 100-150 um
    Neck Angle: 40-50 degrees
```

### Intermetallic Compound Formation

Over time gold and aluminum form intermetallic compounds at the bond interface:

| IMC Phase | Composition | Color | Reliability |
|-----------|------------|-------|-------------|
| Au5Al2 | Gold-rich | White | Good |
| Au2Al | Mixed | Cream | Good |
| AuAl2 | Aluminum-rich | Purple plague | Poor at high T |
| AuAl | Mixed | White | Moderate |

The purple plague (AuAl2) is brittle. To minimize risk:
- Bond temperature limited to 150 C (reduces IMC growth rate)
- Un-doped gold wire used consistently
- Accelerated life testing at 175 C validates IMC stability through 20-year lifetime

**IMC Growth at Body Temperature**:

After 20 years at 37 C the estimated IMC layer thickness is 1.3 um, well within
acceptable limits for a 25 um wire bond diameter.

## Bond Pad Design

### Die Bond Pad Layout

| Parameter | Specification |
|-----------|--------------|
| Pad Material | TiW/Al (50 nm / 1 um) |
| Pad Size | 80 x 80 um |
| Pad Pitch | 120 um center-to-center |
| Passivation Opening | 60 x 60 um |
| Pad Array | Staggered 2 rows |

```
Die Bond Pad Layout:

    Passivation Opening (60x60 um)
    +----------+
    |  +----+  |  Pad Opening
    |  |    |  |
    |  | ** |  |  Wire Bond Landing Zone
    |  |    |  |
    |  +----+  |
    +----------+
    80 um width

    Pad Pitch = 120 um
    -------------------------
    Row 1:  *--------*--------*----
    Row 2:     *--------*--------*  (staggered)
```

### Package Pad Layout

| Parameter | Specification |
|-----------|--------------|
| Pad Material | Au-plated Pt/Ir feedthrough pad |
| Au Plating Thickness | 3-5 um |
| Pad Size | 150 x 200 um |
| Pad Pitch | 500 um |
| Surface Roughness | Ra < 0.2 um |
| Wire Bondable Area | 120 x 180 um (after margin) |

### Wire Routing Rules

| Rule | Specification | Rationale |
|------|--------------|-----------|
| Minimum Wire Length | 200 um | Prevents short looping |
| Maximum Wire Length | 5000 um | Limits inductance and sag |
| Minimum Wire Spacing | 2x wire diameter | Prevents electrical shorts |
| Wire Crossing | Not permitted | Risk of short circuit |
| Adjacent Wire Angle | > 30 degrees | Prevents parallel contact |
| Max Wires per Pad | 1 | One wire per bond pad |
| Wire Count per Die | 24 | Matches I/O count |

## Wire Bond Reliability for Implants

### Thermal Cycling

The iPACE-CHIP must survive thermal cycling from storage (-40 C) to body temperature
(37 C) and sterilization temperatures (up to 55 C for EtO):

**Test Protocol**:

| Parameter | Value |
|-----------|-------|
| Temperature Range | -40 C to +85 C |
| Dwell Time | 15 minutes at each extreme |
| Transition Time | < 10 seconds |
| Number of Cycles | 1000 |
| Sample Size | 30 units |
| Accept Criteria | 0 bond failures, < 10% pull strength degradation |

**Failure Mechanisms**:

1. **Wire fatigue**: Cyclic thermal stress causes work hardening and eventual fracture
   at the heel of the ball bond or stitch bond
2. **Pad cratering**: CTE mismatch between die and package creates stress that can
   crack the silicon beneath the bond pad
3. **Delamination**: Intermetallic growth can create voids (Kirkendall effect) that
   weaken the bond interface

### Accelerated Life Testing

| Condition | Temperature | Duration | Equivalence |
|-----------|-------------|----------|-------------|
| HTOL | 125 C, powered | 2000 hr | ~15 years at 37 C |
| TC (High Stress) | -55 C to +125 C | 1000 cycles | ~20 years mechanical |
| HAST | 130 C, 85% RH | 96 hr | ~5 years at 37 C |
| Thermal Aging | 150 C, N2 ambient | 5000 hr | ~20 years IMC growth |

### Bond Pull Test Results (Typical)

| Aging Condition | Average Pull Force | Min Pull Force | Failure Mode |
|----------------|-------------------|---------------|--------------|
| As-bonded | 7.2 g | 5.8 g | Wire break |
| After 1000 TC | 6.8 g | 5.2 g | Wire break |
| After 2000 hr HTOL | 6.5 g | 4.9 g | Wire break |
| After 5000 hr 150C | 5.8 g | 4.2 g | Ball lift (rare) |

All results exceed the minimum 4.5 g requirement through the full test duration.

## AOI (Automated Optical Inspection)

### Inspection System

The iPACE-CHIP wire bonds are inspected using a high-resolution AOI system:

| Parameter | Specification |
|-----------|--------------|
| Resolution | 1.0 um/pixel |
| Illumination | Multi-angle LED (dark + bright field) |
| Inspection Time | < 5 seconds per die |
| Defect Detection | > 99.5% for critical defects |
| False Alarm Rate | < 0.1% |

### Inspection Criteria

| Defect Type | Severity | Accept Criteria |
|------------|----------|-----------------|
| Missing bond | Critical | Zero tolerance |
| Ball off-pad | Critical | Zero tolerance |
| Stich off-pad | Critical | Zero tolerance |
| Wire sag | Major | > 25 um below nominal profile |
| Wire sweep | Major | > 25 um lateral displacement |
| Broken wire | Critical | Zero tolerance |
| Short (wire-to-wire) | Critical | Zero tolerance |
| Ball too large | Minor | > 75 um diameter |
| Ball too small | Minor | < 50 um diameter |
| Neck crack | Critical | Zero tolerance |
| Tail too long | Minor | > 75 um length |

### Inspection Flow

```
Wire Bond
    |
    v
AOI Inspection
    |
    +---> Pass ---> Next Bond
    |
    +---> Fail ---> Flag for Review
                     |
                     +---> Auto-Reject (Critical)
                     |
                     +---> Operator Review (Minor)
                              |
                              +---> Re-bond
                              +---> Scrap Die
```

## Flip Chip Technology (Future Generation)

### Flip Chip Process Overview

For iPACE-CHIP Gen 3 and beyond, flip chip technology offers superior electrical
and thermal performance:

**Process Flow**:

1. **Solder Bump Deposition**: Electroplated AuSn or Cu pillar bumps on die pads
2. **Flux Application**: Tacky flux for temporary die holding
3. **Die Flip and Placement**: Flip chip bonder aligns and places die on substrate
4. **Reflow**: Solder reflow at 280-300 C (eutectic AuSn)
5. **Underfill**: Capillary flow of medical-grade epoxy underfill
6. **Cure**: Thermal cure of underfill (150 C, 2 hours)

### Flip Chip Bump Specifications

| Parameter | Specification |
|-----------|--------------|
| Bump Material | AuSn (80/20 eutectic) |
| Bump Diameter | 80 um |
| Bump Height | 50 um |
| Bump Pitch | 150 um |
| Under-Bump Metallurgy | TiW/Cu/Au |
| Shear Strength | > 15 g per bump |
| Standoff After Reflow | 25-35 um |

### Underfill Material

| Property | Specification | Rationale |
|----------|--------------|-----------|
| Filler Content | 65% silica | CTE matching |
| CTE | 25 ppm/C | Between Si (3) and package (6-10) |
| Tg | 150 C | Above sterilization temp |
| Modulus | 8 GPa | Rigid enough for stress transfer |
| Adhesion (Si) | > 30 MPa | Prevent delamination |
| Adhesion (Au) | > 25 MPa | Bump interface integrity |
| Biocompatibility | ISO 10993 Class VI | Implant compatibility |
| Ionic Purity | < 10 ppm Na equivalent | Prevent corrosion |

### Flip Chip Reliability Advantages

| Parameter | Wire Bond | Flip Chip |
|-----------|-----------|-----------|
| Inductance | 1-3 nH | < 0.1 nH |
| Resistance | 50-200 mOhm | 10-50 mOhm |
| Thermal R (die to package) | 15-25 C/W | 3-8 C/W |
| Vibration Resistance | Moderate | Excellent |
| Thermal Cycling Life | ~3000 cycles | ~10000 cycles |

## Summary

Wire bonding with gold thermosonic bonding is the selected interconnect technology
for iPACE-CHIP Gen 1, providing proven reliability, cost-effective assembly, and
extensive qualification data for implantable medical devices. The 25 um gold wire
with 80 um bond pads at 120 um pitch delivers the 24 I/O connections required with
margin well beyond the 20-year lifetime. AOI inspection at 100% coverage ensures
zero-defect interconnect quality. Flip chip technology is planned for Gen 3 when
higher I/O density and improved electrical performance are required for 128+ channel
neural interface operation.

## References

1. MIL-STD-883, Method 2011, "Bond Strength (Destructive Bond Pull Test)."
2. K. Scholz, "Wire Bonding for Implantable Medical Devices," IEEE ECTC, 2021.
3. iPACE-CHIP Assembly Specification, Internal Document, Rev 2.3.
4. JEDEC JESD22-B111, "Board Level Cyclic Mechanical Shock Test."
5. H. Clode, "Gold Wire Bond Reliability in Medical Implants," IMAPS, 2022.
6. SEMI G64, "Test Method for Hermeticity of Packages."
7. iPACE-CHIP Wire Bond Qualification Report, Internal, Rev 1.0.
8. IPC-7093, "Design and Assembly Process Implementation for Flip Chip."
