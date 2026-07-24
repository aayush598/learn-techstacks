# 14.2.4 Biocompatible Packaging Materials for iPACE-CHIP

## Overview

Every material that contacts human tissue or body fluids during the iPACE-CHIP implant
lifetime must demonstrate biocompatibility as defined by ISO 10993. This chapter catalogs
all packaging materials, their biocompatibility test status, chemical composition limits,
leachables and extractables profiles, and long-term degradation behavior in the implant
environment. Material selection directly impacts patient safety and regulatory approval.

## Material Selection Framework

### ISO 10993 Biological Evaluation Hierarchy

The ISO 10993 standard series provides a systematic approach to biocompatibility
evaluation:

| Part | Title | Application to iPACE-CHIP |
|------|-------|--------------------------|
| ISO 10993-1 | Evaluation and testing within a risk management process | Overall framework |
| ISO 10993-2 | Animal welfare requirements | Test protocol design |
| ISO 10993-3 | Genotoxicity, carcinogenicity, reprotoxicity | Material screening |
| ISO 10993-4 | Selection of tests for interactions with blood | Blood-contact assessment |
| ISO 10993-5 | Tests for in vitro cytotoxicity | Initial biocompatibility screen |
| ISO 10993-6 | Tests for local effects after implantation | Tissue response evaluation |
| ISO 10993-10 | Tests for skin sensitization and irritation | Surface material testing |
| ISO 10993-11 | Tests for systemic toxicity | Full systemic evaluation |
| ISO 10993-12 | Sample preparation and reference materials | Test material preparation |
| ISO 10993-13 | Identification and quantification of degradation products | Degradation assessment |
| ISO 10993-14 | Identification and quantification of degradation products from ceramics | Ceramic evaluation |
| ISO 10993-15 | Identification and quantification of degradation products from metals | Metal leaching |
| ISO 10993-17 | Toxicological risk assessment of medical device constituents | Risk assessment |
| ISO 10993-18 | Chemical characterization of materials | Extractables/leachables |

### iPACE-CHIP Material Categories

| Category | Materials | Tissue Contact | ISO 10993 Tests Required |
|----------|----------|----------------|-------------------------|
| Metallic (implant) | Ti, Pt/Ir, Au | Long-term implant (> 30 days) | Parts 3,4,5,6,10,11,15,17 |
| Ceramic | Al2O3 | Long-term implant | Parts 3,5,6,10,11,14,17 |
| Polymer (encapsulation) | PDMS silicone | Long-term implant | Parts 3,5,6,10,11,17 |
| Polymer (insulation) | Parylene C | Long-term implant | Parts 3,5,6,10,11,17 |
| Solder/Braze | AuSn | Internal (no contact) | Parts 3,5 (precautionary) |
| Adhesive | Medical epoxy | Internal | Parts 3,5 (precautionary) |

## Metallic Materials

### Grade 1 Commercially Pure Titanium

**Chemical Composition (ASTM F67)**:

| Element | Maximum (%) | Actual (typical) |
|---------|------------|-------------------|
| Ti | Balance (>= 99.5) | 99.7 |
| Fe | 0.20 | 0.12 |
| O | 0.18 | 0.14 |
| C | 0.08 | 0.04 |
| N | 0.03 | 0.01 |
| H | 0.015 | 0.005 |

**Biocompatibility Profile**:

Titanium is the gold standard for biocompatible implant metals:
- Forms stable TiO2 passive layer (2-10 nm) immediately upon air exposure
- TiO2 layer is insoluble in body fluids (pH 7.4, 37 C)
- Ion release rate: < 0.1 ug/cm2/year (measured in simulated body fluid)
- No known allergenicity (unlike nickel, cobalt, chromium)
- No cytotoxicity, no genotoxicity, no carcinogenicity
- Excellent osseointegration capability (bone bonding)

**Leachables Analysis**:

| Species | Detection Limit | Result (20-year equivalent) | Limit |
|---------|----------------|---------------------------|-------|
| Ti ions | 0.01 ppb | < 0.5 ppb | 100 ppb |
| Fe ions | 0.01 ppb | < 0.3 ppb | 50 ppb |
| Total organic carbon | 0.1 ppb | < 1 ppb | 10 ppb |

### Platinum/Iridium (90/10)

**Chemical Composition (ASTM F560)**:

| Element | Specification | Purpose |
|---------|--------------|---------|
| Pt | 90 +/- 2% | Base metal |
| Ir | 10 +/- 2% | Strengthening, corrosion resistance |
| Rh | < 0.5% | Impurity |
| Pd | < 0.2% | Impurity |
| Au | < 0.1% | Impurity |
| Base metals | < 0.1% total | Impurities |

**Biocompatibility Profile**:

Pt/Ir is the standard electrode material for neural implants:
- Extremely noble (E0 = +1.2 V for Pt)
- Corrosion rate in body fluid: < 0.001 ug/cm2/year
- No known allergic reaction (Pt allergy is extremely rare)
- High charge injection capacity for neural stimulation
- Radiopaque (visible on X-ray for implant localization)

**Charge Injection Limits (for stimulation electrodes)**:

| Parameter | Value | Note |
|-----------|-------|------|
| Cathodic Charge Capacity | 150 uC/cm2 | Without Faradaic damage |
| Anodic Charge Capacity | 100 uC/cm2 | Lower than cathodic |
| Charge Density (iPACE-CHIP) | 20 uC/cm2 | Well within safe limits |
| Stimulation Frequency | 100 Hz maximum | Prevents charge accumulation |

### Gold (Au)

**Chemical Composition (ASTM F2063 or equivalent)**:

| Element | Specification |
|---------|--------------|
| Au | >= 99.99% (4N) |
| Ag | < 10 ppm |
| Cu | < 5 ppm |
| Fe | < 5 ppm |
| Total impurities | < 100 ppm |

**Biocompatibility Profile**:

Gold is used for wire bonding and plating in iPACE-CHIP:
- Extremely inert in biological environment
- No ion release at body temperature in neutral pH
- No cytotoxicity
- No genotoxicity
- Historical use in dental and orthopedic implants

**Note**: Gold particles from wire bonding or plating are encapsulated within the
hermetic package and do not contact tissue. Gold biocompatibility testing is performed
as a precautionary measure.

## Ceramic Materials

### Alumina (Al2O3)

**Material Grade**: 96% or 99.6% alumina depending on application

| Property | 96% Alumina | 99.6% Alumina |
|----------|------------|---------------|
| Application | Package structure | Feedthrough insulator |
| Density | 3.7 g/cm3 | 3.9 g/cm3 |
| Flexural Strength | 345 MPa | 380 MPa |
| Thermal Conductivity | 24 W/mK | 28 W/mK |
| Dielectric Constant | 9.4 | 9.8 |
| CTE | 6.4 ppm/C | 7.2 ppm/C |
| Surface Finish | Ra < 0.4 um | Ra < 0.2 um |

**Biocompatibility Profile**:

Alumina is one of the most established bioceramics:
- Chemically inert in body fluids (no dissolution)
- No ion release (ionic crystal, no metal ions)
- Excellent tribological properties (low wear)
- No cytotoxicity
- FDA-approved for decades in dental and orthopedic implants
- High compressive strength (2000 MPa) resists fracture

**Degradation Assessment**:

Alumina shows no measurable degradation in simulated body fluid over 20-year
equivalent testing. Mass change: < 0.001 mg/cm2/year. Surface chemistry
unchanged by XPS analysis after accelerated aging.

## Polymer Materials

### Medical-Grade Silicone (PDMS)

**Material Specification**:

| Property | Specification | Test Method |
|----------|--------------|-------------|
| Base Polymer | Polydimethylsiloxane | - |
| Hardness | 30-50 Shore A | ASTM D2240 |
| Tensile Strength | > 8 MPa | ASTM D412 |
| Elongation at Break | > 400% | ASTM D412 |
| Tear Strength | > 20 kN/m | ASTM D624 |
| CTE | 300 ppm/C | TMA |
| Volume Resistivity | > 10^14 Ohm-cm | ASTM D257 |
| Dielectric Constant | 2.8 at 1 MHz | ASTM D150 |
| Extractables | < 0.5% by weight | USP <661> |

**Biocompatibility Testing**:

| Test | Standard | Result |
|------|----------|--------|
| Cytotoxicity | ISO 10993-5 | Pass (Grade 0) |
| Sensitization | ISO 10993-10 | Pass (No sensitization) |
| Irritation | ISO 10993-10 | Pass (Negligible) |
| Acute Systemic | ISO 10993-11 | Pass (No effects) |
| Implantation | ISO 10993-6 | Pass (Minimal response) |
| Hemocompatibility | ISO 10993-4 | Not required (no blood contact) |
| Genotoxicity | ISO 10993-3 | Pass (Negative Ames, micronucleus) |

**Extractables and Leachables Profile**:

| Extractable | Concentration | Toxicity Assessment |
|------------|--------------|---------------------|
| D4 (octamethylcyclotetrasiloxane) | < 10 ppm | No significant toxicity |
| D5 (decamethylcyclopentasiloxane) | < 5 ppm | No significant toxicity |
| Low MW siloxanes | < 20 ppm total | Below NOAEL thresholds |
| Metals (total) | < 1 ppm | Below toxicity thresholds |

### Parylene C (Poly-para-xylylene)

**Material Properties**:

| Property | Value | Application |
|----------|-------|-------------|
| Dielectric Strength | 220 V/um | Insulation coating |
| Dielectric Constant | 3.1 at 1 kHz | Consistent over frequency |
| Dissipation Factor | 0.013 at 1 kHz | Low dielectric loss |
| Water Absorption | 0.06% at 24 hr | Excellent moisture barrier |
| Tensile Strength | 40 MPa | Adequate for coating |
| CTE | 35 ppm/C | Moderate |
| Pinhole Density | < 0.1/cm2 at 12.5 um | Conformal coverage |
| Biocompatibility | ISO 10993 compliant | Well-established |

**Application in iPACE-CHIP**:

Parylene C coats the electrode lead extensions that contact body tissue:
- Conformal coating (CVD process, no solvent)
- Pinhole-free at > 10 um thickness
- Chemical inertness in body fluid
- Long-term stability (> 20 years documented)
- UL 746B Class F biocompatibility rating

**Deposition Process**:

```
Gordac Process (Typical):

Step 1: Dimer Vaporization
    Parylene C dimer heated to 150 C in vacuum

Step 2: Pyrolysis
    Dimer cracked to monomer at 680 C

Step 3: Deposition
    Monomer condenses on room-temperature surfaces
    Uniform, conformal coating

Step 4: Polymerization
    Monomer polymerizes on surface (no initiator needed)
    Final thickness: 10-25 um
```

## Sealant and Adhesive Materials

### Medical-Grade Epoxy

**Application**: Die attach adhesive, underfill, lid seal reinforcement

| Property | Specification |
|----------|--------------|
| Base Chemistry | Bisphenol-A or aliphatic epoxy |
| Hardener | Anhydride or amine (medical grade) |
| Cure Temperature | 150 C for 1 hour |
| Tg | > 150 C |
| CTE | 30-50 ppm/C (below Tg) |
| Modulus | 3-5 GPa |
| Lap Shear Strength | > 15 MPa (Ti to ceramic) |
| Biocompatibility | ISO 10993-5 (cytotoxicity) |
| Outgassing | < 0.1% TML, < 0.01% CVCM (ASTM E595) |

### Au/Sn Eutectic Solder (80/20)

**Application**: Die attach, lid seal

| Property | Value |
|----------|-------|
| Composition | 80% Au, 20% Sn (by weight) |
| Melting Point | 280 C |
| Density | 14.5 g/cm3 |
| Tensile Strength | 33 MPa |
| CTE | 16 ppm/C |
| Electrical Resistivity | 15 uOhm-cm |
| Biocompatibility | Encapsulated (no tissue contact) |

The Au/Sn solder is fully encapsulated within the hermetic package and titanium
encapsulation, so it does not require full ISO 10993 implant testing. Precautionary
cytotoxicity testing (ISO 10993-5) is performed to ensure safety in case of
hypothetical primary seal breach.

## Material Compatibility Matrix

### Galvanic Corrosion Assessment

When dissimilar metals are in electrical contact in an electrolyte (body fluid),
galvanic corrosion can occur. The iPACE-CHIP material combinations are assessed:

| Material Pair | Potential Difference | Corrosion Risk | Mitigation |
|--------------|---------------------|----------------|------------|
| Ti vs Pt/Ir | 0.3 V | Low | Ti is passive (noble in body fluid) |
| Ti vs Au | 0.4 V | Low | Both are noble, minimal driving force |
| Pt/Ir vs Au | 0.1 V | Negligible | Very small potential difference |
| Ti vs Al (die pad) | 0.8 V | Moderate | Al protected by passivation, no exposure |
| Au vs Al (internal) | 1.0 V | Low | No electrolyte (encapsulated, hermetic) |

**Key Finding**: All metallic material combinations in the iPACE-CHIP have
acceptable galvanic corrosion risk, primarily because the noble metals (Ti, Pt/Ir, Au)
have very small potential differences between them.

### CTE Mismatch Assessment

Thermal expansion mismatch between adjacent materials creates mechanical stress
during temperature changes:

| Material | CTE (ppm/C) | Paired With | Delta CTE | Stress Level |
|----------|------------|-------------|-----------|--------------|
| Si die | 2.6 | Au/Sn solder | 13.4 | Moderate |
| Au/Sn solder | 16 | Ti base | 10 | Moderate |
| Ti base | 8.6 | Alumina ring | 2.2 | Low |
| Alumina ring | 6.4 | Ti lid | 2.2 | Low |
| Ti lid | 8.6 | PDMS fill | 291 | Low (compliant) |

The compliant PDMS fill material absorbs CTE mismatch stress between the titanium
shell and internal components, preventing fatigue failure.

## Degradation and Aging Studies

### Accelerated Aging Protocol

To project 20-year material behavior, the iPACE-CHIP uses the following accelerated
aging protocol:

| Test | Conditions | Duration | Acceleration Factor |
|------|-----------|----------|-------------------|
| Static Soak | SBF at 85 C | 5000 hr | ~15 years at 37 C |
| HAST | 130 C, 85% RH | 96 hr | ~5 years at 37 C |
| Thermal Aging | 100 C, N2 ambient | 10000 hr | ~10 years at 37 C |
| UV Exposure | 30 hr (sterilization) | 30 hr | 1x (actual) |

### Material-Specific Aging Results

**Titanium (after 15-year equivalent soak)**:
- Mass loss: < 0.001 mg/cm2/year
- Surface chemistry: Unchanged (TiO2 passive layer maintained)
- Mechanical properties: No measurable degradation

**Pt/Ir (after 15-year equivalent soak)**:
- Mass loss: < 0.0001 mg/cm2/year
- Surface chemistry: Unchanged
- Electrochemical impedance: No change

**Alumina (after 15-year equivalent soak)**:
- Mass loss: < 0.0005 mg/cm2/year
- Flexural strength: > 95% of original
- Surface: No detectable degradation

**PDMS Silicone (after 15-year equivalent soak)**:
- Hardness change: < 2 Shore A points
- Tensile strength retention: > 90%
- Volume change: < 3%
- Extractables: No increase from baseline

**Parylene C (after 15-year equivalent soak)**:
- Thickness retention: > 95%
- Dielectric strength: > 90% of original
- Adhesion: No delamination

## Regulatory Documentation

### Material Master File (MAF)

For FDA submission, each packaging material requires a Material Master File
containing:

1. Material composition and manufacturing process
2. Characterization data (physical, chemical, mechanical)
3. Biocompatibility test reports (ISO 10993 series)
4. Extractables and leachables data
5. Shelf life and storage conditions
6. Change control procedures
7. Supplier qualifications and audits

### Supplier Qualification

| Supplier | Material | Qualification Status |
|----------|----------|---------------------|
| TIMET | Grade 1 Ti sheet | Qualified (Audit 2024) |
| Heraeus | Pt/Ir wire and sheet | Qualified (Audit 2024) |
| Tanaka Kikinzoku | Au wire | Qualified (Audit 2024) |
| CoorsTek | Alumina components | Qualified (Audit 2024) |
| Dow Corning/Medical | Medical PDMS | Qualified (Audit 2024)
| Specialty Coating | Parylene C | Qualified (Audit 2024)
| Epoxy Technology | Medical epoxy | Qualified (Audit 2024)

### Change Control Process

Any material change requires:
1. Risk assessment per ISO 14971
2. Biocompatibility re-testing per ISO 10993
3. Process validation at assembly level
4. FDA notification (for Class III PMA devices)
5. Internal design history file (DHF) update

## Summary

The iPACE-CHIP packaging material selection prioritizes patient safety through
comprehensive biocompatibility evaluation per ISO 10993. All materials have demonstrated
chemical stability, minimal leachables, and long-term durability in the implant
environment through accelerated aging testing equivalent to 20+ years. The material
portfolio including Grade 1 titanium, Pt/Ir, gold, alumina, PDMS silicone, and
Parylene C represents a well-characterized, FDA-accepted set of implant materials
with extensive historical clinical data supporting their safety and efficacy.

## References

1. ISO 10993-1:2018, "Biological Evaluation of Medical Devices."
2. ASTM F67-13, "Standard Specification for Commercially Pure Titanium."
3. ASTM F560-14, "Standard Specification for Unalloyed Tantalum."
4. ISO 10993-18:2020, "Chemical characterization of medical device materials."
5. USP <661>, "Plastic Packaging Systems."
6. iPACE-CHIP Material Specification, Internal Document, Rev 3.0.
7. S. Tavakoli, "Biocompatibility of Packaging Materials for Implantable Devices," 2023.
8. FDA Guidance: Use of ISO 10993-1, 2020.
