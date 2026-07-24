# 14.4.2 OSAT Partners for iPACE-CHIP

## Overview

Outsourced Semiconductor Assembly and Test (OSAT) partners perform the critical
post-fabrication steps that transform tested silicon die into fully packaged, tested,
and marked iPACE-CHIP devices ready for sterilization and implantation. For a medical
device with zero-defect requirements, OSAT partner selection demands careful evaluation
of quality systems, process capabilities, and regulatory compliance. This chapter
defines the OSAT partner selection criteria, evaluates candidate partners, and
establishes the quality framework for assembly operations.

## OSAT Services Required

### iPACE-CHIP Assembly Process Flow

```
Die Receipt (from foundry, KGD tested)
    |
    v
Die Bonder (Eutectic attach to Ti package base)
    |
    v
Wire Bonder (Au thermosonic, 24 bonds)
    |
    v
AOI Inspection (100% wire bond inspection)
    |
    v
Hermetic Sealing (Laser weld, lid attach)
    |
    v
Hermeticity Test (MIL-STD-883, Method 1014)
    |
    v
Encapsulation (Ti shell assembly, laser weld)
    |
    v
Final Test (Electrical, functional, telemetry)
    |
    v
X-ray Inspection (Internal structure verification)
    |
    v
Laser Marking (Lot, serial number, UDI)
    |
    v
Visual Inspection (Final cosmetic check)
    |
    v
Packaging (Sterile barrier, labeling)
    |
    v
Ship to Sterilization Facility
```

### Service Categories

| Service | Description | Criticality |
|---------|------------|-------------|
| Die Attach | Eutectic Au/Sn die bonding to Ti package | Critical |
| Wire Bonding | Au thermosonic ball-stitch bonding | Critical |
| Hermetic Sealing | Laser welding of Ti lid to package | Critical |
| Encapsulation | Ti outer shell assembly and welding | Critical |
| Electrical Test | Parametric and functional test | Critical |
| X-ray Inspection | Internal structure verification | High |
| Laser Marking | Device identification and UDI | Medium |
| Clean Room Assembly | ISO 5 environment for all steps | Critical |
| Moisture Sensitivity | Handling per MSL requirements | High |

## OSAT Partner Evaluation

### Candidate OSATs

| Company | HQ | Revenue | Medical Track Record | Facilities |
|---------|------|---------|---------------------|------------|
| ASE Group | Taiwan | $18B | Extensive | Global |
| Amkor Technology | USA | $7B | Strong | Global |
| JCET Group | China | $5B | Limited | Asia |
| Chipbond Technology | Taiwan | $1B | Moderate | Taiwan |
| Tongfu Microelectronics | China | $3B | Limited | China |
| Carsem (TDK) | Malaysia | $1B | Strong | Malaysia |
| Custom Assembly (US) | USA | $50M | Specialized | USA |

### Medical Device Qualification Requirements

| Requirement | ASE | Amkor | Carsem | Custom Assembly |
|------------|-----|-------|--------|-----------------|
| ISO 13485 | Yes | Yes | Yes | Yes |
| ISO 9001 | Yes | Yes | Yes | Yes |
| FDA Registered | Yes | Yes | Yes | Yes |
| ITAR Compliant | Yes | Yes | No | Yes |
| DSCSA Compliant | Yes | Yes | Yes | Yes |
| Class III Experience | Yes | Yes | Yes | Yes |
| Biocompatible Process | Yes | Yes | Yes | Yes |
| Hermetic Packaging | Yes | Yes | Yes | Specialized |
| Laser Welding | Yes | Yes | Limited | Specialized |

### Evaluation Scorecard

| Criterion (Weight) | ASE | Amkor | Carsem | Custom Assembly |
|-------------------|-----|-------|--------|-----------------|
| Quality System (25%) | 9.0 | 9.0 | 8.5 | 9.5 |
| Medical Device Experience (25%) | 9.0 | 8.5 | 7.5 | 9.0 |
| Hermetic Packaging (20%) | 8.5 | 8.0 | 7.0 | 9.5 |
| Process Capability (15%) | 9.0 | 8.5 | 7.5 | 8.0 |
| Supply Chain Security (10%) | 7.0 | 8.0 | 7.0 | 9.5 |
| Cost (5%) | 8.0 | 7.5 | 8.5 | 6.0 |
| **Weighted Score** | **8.68** | **8.40** | **7.63** | **8.88** |

### Selection Decision

**Primary OSAT**: Custom Assembly (USA) — Specialized medical device assembly
- Highest score driven by specialized medical device expertise
- US-based facility provides supply chain security and ITAR compliance
- Small company provides dedicated attention and flexibility
- Specialized in hermetic packaging for implantable devices

**Secondary OSAT**: ASE Group (Taiwan) — High-volume backup
- Largest OSAT with extensive capability
- Provides volume surge capacity if needed
- Multiple qualified sites for risk diversification

## Primary OSAT: Detailed Specifications

### Facility Requirements

| Requirement | Specification |
|------------|--------------|
| Clean Room Class | ISO 5 (minimum for all assembly) |
| ESD Control | ANSI/ESD S20.20 compliant |
| Temperature | 21 C +/- 0.5 C |
| Humidity | 45% +/- 5% RH |
| Nitrogen Supply | > 99.999% purity |
| DI Water | 18.2 MOhm-cm |
| Fire Suppression | Inert gas (N2 or IG-541) |
| Security | 24/7 surveillance, restricted access |
| Backup Power | UPS + diesel generator |

### Equipment List

| Equipment | Quantity | Capability | Calibration |
|-----------|----------|-----------|-------------|
| Die Bonder (Eutectic) | 2 | Au/Sn, 280C, < 1 um accuracy | Monthly |
| Wire Bonder | 3 | 25 um Au, thermosonic | Weekly |
| AOI System | 2 | 1.0 um resolution, < 5 sec/die | Daily |
| Laser Welder | 2 | Nd:YAG, 1064 nm, pulsed | Weekly |
| He Leak Detector | 2 | Sensitivity < 10^-12 atm-cc/sec | Monthly |
| X-ray System | 1 | 2D/CT, 1 um resolution | Monthly |
| Electrical Tester | 3 | 4-ch SMU, 500 MHz counter | Monthly |
| Laser Marker | 1 | Fiber laser, 50 um spot | Quarterly |
| Vision System (Final) | 2 | 5x-50x zoom, automated | Daily |

### Personnel Requirements

| Role | Count | Qualification |
|------|-------|--------------|
| Program Manager | 1 | PMP, ASQ CQE |
| Quality Engineer | 2 | ASQ CQE, ISO 13485 Lead Auditor |
| Process Engineer | 2 | Semiconductor packaging background |
| Reliability Engineer | 1 | JEDEC familiarity, 5+ years |
| Production Operators | 8 | Trained and certified per SOP |
| Inspection Operators | 4 | Vision inspection certified |
| Test Engineers | 2 | ATE programming, medical device |
| Metrology | 1 | CMM, optical measurement |
| **Total** | **21** | |

## Quality Framework

### Incoming Material Verification

| Material | Verification Method | Frequency | Accept Criteria |
|---------|-------------------|-----------|-----------------|
| KGD Die | Electrical re-screen | 100% of die | All 48 parametric + functional pass |
| Ti Package Base | Visual + dimensional | 100% of trays | Per mechanical drawing |
| Ti Lid | Visual + dimensional | 100% of trays | Per mechanical drawing |
| Ceramic Ring | Visual + dimensional | 100% of trays | Per mechanical drawing |
| Au Wire | Certificate of conformance | Per lot | ASTM B417 compliant |
| Au/Sn Preform | Certificate of conformance | Per lot | 80/20 composition verified |
| Medical Silicone | Certificate + extractables | Per lot | ISO 10993 compliant |

### In-Process Quality Controls

| Process Step | Control | Method | Frequency |
|-------------|---------|--------|-----------|
| Die Attach | Coverage > 95% | Scanning Acoustic Microscopy | 100% |
| Die Attach | Shear strength > 25N | Die shear tester | 3 per wafer |
| Wire Bond | Ball shear > 15g | Wire bond tester | 3 per die |
| Wire Bond | Pull strength > 4.5g | Wire pull tester | 3 per die |
| Wire Bond | Visual inspection | AOI system | 100% of die |
| Laser Weld | Visual inspection | Stereo microscope | 100% of units |
| Hermeticity | Fine leak < 10^-9 | He mass spectrometer | 100% of units |
| Hermeticity | Gross leak test | Fluorocarbon immersion | 100% of units |
| Electrical Test | Full parametric + functional | ATE | 100% of units |
| X-ray | Internal structure | 2D X-ray | 100% of units |
| Visual (Final) | Cosmetic + dimensional | 10x microscope | 100% of units |
| Laser Mark | Readability + accuracy | Barcode verifier | 100% of units |

### Nonconforming Material Control

```
Nonconforming Material Handling Flow:

Detection of Nonconformity
    |
    v
Immediate Containment
    +---> Quarantine affected units
    +---> Notify Quality Engineer
    +---> Halt affected production (if systematic)
    |
    v
Disposition Decision (MRB - Material Review Board)
    |
    +---> Use As-Is (with documented justification)
    +---> Rework (re-work per approved procedure)
    +---> Return to Supplier (die or material supplier)
    +---> Scrap (destroy and document)
    |
    v
Root Cause Analysis
    +---> 5-Why analysis
    +---> Fishbone diagram
    +---> 8D report (if customer-affecting)
    |
    v
Corrective Action
    +---> Process change
    +---> Training update
    +---> Supplier corrective action
    +---> CAPA record (if significant)
    |
    v
Effectiveness Verification
    +---> Monitor 10 lots post-change
    +---> Verify nonconformity does not recur
    +---> Close CAPA record
```

## Assembly Process Specifications

### Die Attach Specification

| Parameter | Specification | Tolerance |
|-----------|--------------|-----------|
| Die Attach Material | Au/Sn 80/20 preform | Per ASTM B840 |
| Preform Thickness | 25 um | +/- 3 um |
| Preform Size | Die size + 0.2 mm | +/- 0.05 mm |
| Attach Temperature | 280 C | +/- 5 C |
| Attach Atmosphere | Forming gas (95% N2/5% H2) | O2 < 10 ppm |
| Reflow Time | 60 sec at peak | +/- 5 sec |
| Cooling Rate | < 5 C/sec | Monitored |
| Bond Coverage | > 95% | SAM measurement |
| Max Void Size | < 50 um | SAM measurement |
| Die Shear Strength | > 25 N | Destructive test |

### Wire Bond Specification

| Parameter | First Bond (Die) | Second Bond (Package) |
|-----------|-----------------|----------------------|
| Bond Type | Ball | Stitch |
| Wire Material | Au 99.99% | Au 99.99% |
| Wire Diameter | 25 um | 25 um |
| Bond Temperature | 150 C | 150 C |
| Bond Force | 25-35 g | 30-45 g |
| Ultrasonic Power | 50-80 mW | 60-100 mW |
| Bond Time | 15-25 ms | 20-30 ms |
| Ball Diameter | 55-70 um | N/A |
| Stitch Length | N/A | 75-100 um |
| Ball Shear | > 15 g | N/A |
| Pull Strength | > 4.5 g | > 4.5 g |

### Laser Welding Specification

| Parameter | Lid Seal | Encapsulation |
|-----------|---------|---------------|
| Laser Type | Pulsed Nd:YAG | Pulsed Nd:YAG |
| Wavelength | 1064 nm | 1064 nm |
| Pulse Energy | 0.5-2.0 J | 1.0-3.0 J |
| Pulse Duration | 2-5 ms | 3-8 ms |
| Weld Speed | 5 mm/sec | 3-8 mm/sec |
| Shielding Gas | Argon, 15 L/min | Argon, 20 L/min |
| Penetration | 70-90% of wall | 70-90% of wall |
| Weld Width | 0.4-0.6 mm | 0.4-0.6 mm |
| Cracks | Zero tolerance | Zero tolerance |
| Porosity | No interconnected | No interconnected |

### Hermeticity Test Specification

| Test | Method | Limit | Sample |
|------|--------|-------|--------|
| Fine Leak | MIL-STD-883, Method 1014 | < 1 x 10^-9 atm-cc/sec He | 100% |
| Gross Leak | Fluorocarbon, 125 C | No bubbles in 60 sec | 100% |
| Post-Test Verification | Functional test | Full function | 100% |

## Production Capacity Planning

### Capacity Requirements

| Phase | Annual Volume | Assembly Time/Unit | Total Assembly Hours | OSAT Capacity |
|-------|-------------|-------------------|---------------------|---------------|
| Launch (Year 1) | 5,000 | 2.5 hr | 12,500 hr | 1,500 hr/mo |
| Growth (Year 2) | 20,000 | 2.0 hr | 40,000 hr | 5,000 hr/mo |
| Maturity (Year 3+) | 50,000-100,000 | 1.5 hr | 75,000-150,000 hr | 10,000-20,000 hr/mo |

### Capacity Allocation Agreement

The OSAT partner commits dedicated capacity:

| Resource | Dedicated Capacity | Shared Pool | Total |
|---------|-------------------|-------------|-------|
| Die Bonder | 1 unit | 0.5 unit | 1.5 units |
| Wire Bonder | 1 unit | 0.5 unit | 1.5 units |
| Laser Welder | 1 unit | 0.5 unit | 1.5 units |
| He Leak Detector | 1 unit | 0 | 1 unit |
| Electrical Tester | 1 unit | 0.5 unit | 1.5 units |
| Operators | 4 dedicated | 2 shared | 6 total |

## Summary

The iPACE-CHIP OSAT partner strategy identifies a specialized US-based medical
device assembly house as the primary partner, leveraging their deep expertise in
hermetic packaging for implantable devices. The comprehensive quality framework
includes incoming material verification, 100% in-process inspection, and full
electrical and hermeticity testing. Nonconforming material procedures ensure that
no defective units escape to the sterilization and shipping stages. The capacity
allocation agreement provides guaranteed resources while maintaining flexibility
for volume ramp.

## References

1. iPACE-CHIP Assembly Specification, Internal Document, Rev 2.3.
2. ISO 13485:2016, "Medical Devices — Quality Management Systems."
3. MIL-STD-883, "Test Methods and Procedures for Microelectronics."
4. iPACE-CHIP OSAT Audit Report, Internal Document, 2024.
5. SEMI G30, "KGD Handling and Testing Standards."
6. IPC-A-610, "Acceptability of Electronic Assemblies."
7. iPACE-CHIP Supply Chain Plan, Internal Document, Rev 1.5.
8. ASQ, "Quality Management for Medical Devices," 2023.
