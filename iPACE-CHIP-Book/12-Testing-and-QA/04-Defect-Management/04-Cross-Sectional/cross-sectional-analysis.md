# Cross-Sectional Analysis

## Overview

Cross-sectional analysis is the definitive physical failure analysis (PFA) technique for the iPACE-CHIP, providing nanometer-resolution imaging of internal device structures to identify root causes of electrical failures. By precisely cutting through the die at the diagnosed fault location and imaging the cross-section with scanning electron microscopy (SEM) or transmission electron microscopy (TEM), engineers can directly observe defects that are invisible to electrical testing alone. For a medical-grade IC, cross-sectional analysis is the ultimate truth source for defect characterization, process validation, and reliability assessment.

---

## 1. Cross-Sectional Analysis Principles

### 1.1 Why Cross-Sectioning Is Necessary

```
Cross-sectional analysis provides:
  Direct visualization of physical defects
    ├── Confirms or refutes fault diagnosis results
    ├── Reveals defect morphology (shape, size, location)
    └── Identifies defect composition through EDX
    
  Process characterization
    ├── Film thickness measurement
    ├── Profile verification (etch, deposition)
    ├── Interface quality assessment
    └── Dimensional compliance verification
    
  Reliability investigation
    ├── Electromigration void visualization
    ├── Stress migration crack detection
    ├── Corrosion path identification
    └── Delamination observation
    
  Design verification
    ├── Critical dimension (CD) measurement
    ├── Overlay verification
    ├── Via landing pad alignment
    └── Metal spacing verification
```

### 1.2 Cross-Section Types

| Section Type | Method | Resolution | Application |
|-------------|--------|------------|-------------|
| Vertical cross-section | FIB or mechanical | 5-50 nm | Defect imaging, profile measurement |
| Planar cross-section | Delayering + SEM | 1-10 nm | Layer-by-layer defect inspection |
| Angled cross-section | FIB at angle | 5-20 nm | Via/interface inspection |
| TEM lamella | FIB lift-out + TEM | 0.1-1 nm | Atomic-level defect analysis |
| 3D tomography | Serial sectioning + SEM | 10-50 nm | 3D defect reconstruction |

### 1.3 Sample Preparation Requirements

```
Cross-section sample requirements for iPACE-CHIP:
  Minimum sample size: 5um x 5um (for localized defect)
  Maximum sample size: Full die (for process characterization)
  Substrate: Silicon die (conducting, no charging)
  Surface preparation: Mirror polish (for mechanical section)
  Coating: Conductive coating (for insulating layers)
  
  ESD protection: Handle with ESD-safe tools
  Contamination control: Cleanroom preparation
  Documentation: Record coordinates and orientation
```

---

## 2. Focused Ion Beam (FIB) Cross-Sectioning

### 2.1 FIB Principle

```
Focused Ion Beam operation:
  Ion source: Gallium (Ga+) liquid metal ion source
  Ion energy: 5-30 keV
  Beam current: 1 pA to 20 nA (for different operations)
  Spot size: 5-20 nm (at low current)
  
  Material removal: Sputtering by high-energy ions
  Material deposition: Precursor gas + ion beam
  Imaging: Secondary electrons from ion beam interaction
  
  Dual-beam FIB-SEM:
    ├── Ion beam for cutting/milling
    ├── Electron beam for imaging
    └── Simultaneous cut and image capability
```

### 2.2 FIB Cross-Section Procedure

```
FIB cross-section procedure for iPACE-CHIP:
  Step 1: Navigate to fault location
    ├── Load die into FIB-SEM chamber
    ├── Use reference features for alignment
    ├── Navigate to (x, y) coordinates from diagnosis
    └── Verify location with SEM imaging
    
  Step 2: Define cross-section plane
    ├── Select cutting orientation (perpendicular to defect)
    ├── Define section width (typically 10-20 um)
    ├── Define section depth (typically 5-10 um)
    └── Define polishing parameters
    
  Step 3: Rough milling
    ├── High beam current (5-10 nA) for material removal
    ├── Remove bulk material around section
    ├── Time: 10-30 minutes depending on depth
    └── Monitor with SEM imaging
    
  Step 4: Fine polishing
    ├── Low beam current (50-200 pA) for smooth surface
    ├── Remove ~100 nm per pass
    ├── Achieve surface roughness less than 5 nm RMS
    └── Time: 30-60 minutes
    
  Step 5: SEM imaging
    ├── Image at multiple magnifications
    ├── Capture defect morphology
    ├── Measure dimensions
    └── Compare with reference (good device)
```

### 2.3 FIB Cross-Section Parameters

```
Typical FIB cross-section parameters for iPACE-CHIP:
  Ion beam energy: 30 keV (for cutting), 5 keV (for final polish)
  Ion beam current:
    Rough cut: 5 nA (material removal rate ~1 um^3/s)
    Fine cut: 500 pA (material removal rate ~0.1 um^3/s)
    Polish: 50 pA (material removal rate ~0.01 um^3/s)
    
  Gas assistance:
    XeF2 for enhanced etching (dielectric removal)
    Pt deposition for sample protection (200nm cap)
    
  Section dimensions:
    Width: 15 um (typical)
    Depth: 8 um (typical)
    Surface roughness: less than 5 nm RMS
    
  Total preparation time:
    Rough milling: 15 minutes
    Fine milling: 30 minutes
    Polishing: 30 minutes
    Total: 75 minutes (typical)
```

---

## 3. Mechanical Cross-Sectioning

### 3.1 Mechanical Sectioning Method

```
Mechanical cross-section procedure:
  Step 1: Encapsulate sample
    ├── Mount die in epoxy resin
    ├── Ensure proper orientation for desired cross-section
    └── Cure epoxy at 60 deg-C for 4 hours
    
  Step 2: Section cutting
    ├── Diamond wafering blade (100 um thickness)
    ├── Coolant: Deionized water
    ├── Feed rate: 0.5 mm/min
    └── Cut through defect location
    
  Step 3: Grinding
    ├── Progressive SiC paper: 240, 400, 600, 1200 grit
    ├── Final grind: 0.05 um alumina suspension
    └── Achieve mirror finish
    
  Step 4: Polishing
    ├── Diamond paste: 1 um, 0.25 um, 0.05 um
    ├── Final polish: Colloidal silica (0.02 um)
    └── Surface roughness: less than 1 nm RMS
    
  Step 5: Imaging
    ├── Optical microscopy (initial inspection)
    ├── SEM imaging (detailed analysis)
    └── EDX analysis (composition identification)
```

### 3.2 Mechanical vs. FIB Sectioning

| Parameter | Mechanical | FIB |
|-----------|-----------|-----|
| Precision | Lower (um-level) | Higher (nm-level) |
| Speed | Faster for large areas | Faster for small areas |
| Sample size | Large (full die) | Small (5-20 um) |
| Cost | Lower | Higher |
| Automation | Manual or semi-auto | Fully automated |
| Application | Process characterization | Defect localization |
| Material removal | Abrasive grinding | Ion sputtering |
| Surface quality | Mirror finish possible | Near-mirror finish |

### 3.3 Polish Quality Assessment

```
Polish quality verification:
  Surface roughness measurement:
    Method: AFM (Atomic Force Microscopy)
    Requirement: Ra less than 2 nm for SEM imaging
    Measurement area: 1um x 1um
    
  Contamination check:
    Method: SEM imaging at high magnification
    Requirement: No scratches, smearing, or debris
    Verification: 50,000x magnification
    
  Structural integrity:
    Method: SEM imaging
    Requirement: No delamination, cracking, or pull-out
    Verification: Interface integrity visible
```

---

## 4. SEM Imaging and Analysis

### 4.1 SEM Imaging Modes

```
SEM imaging modes for iPACE-CHIP cross-sections:
  Secondary electron (SE) imaging:
    ├── Topographic contrast
    ├── Surface morphology visualization
    ├── Resolution: 1-5 nm
    └── Primary mode for defect imaging
    
  Backscattered electron (BSE) imaging:
    ├── Compositional contrast (Z-contrast)
    ├── Material identification (heavy vs. light elements)
    ├── Resolution: 5-10 nm
    └── Useful for material interface analysis
    
  Energy-dispersive X-ray (EDX):
    ├── Elemental composition analysis
    ├── Spot analysis at defect location
    ├── Mapping of elemental distribution
    └── Detection limit: ~0.1% by weight
    
  Electron beam-induced current (EBIC):
    ├── Carrier lifetime mapping
    ├── Junction identification
    ├── Defect activity detection
    └── Useful for junction leakage characterization
```

### 4.2 SEM Imaging Parameters

```
SEM imaging parameters for iPACE-CHIP:
  Accelerating voltage: 1-20 keV (depending on application)
    Low voltage (1-3 keV): Surface detail, charging reduction
    Medium voltage (5-10 keV): General imaging
    High voltage (15-20 keV): Penetration, BSE imaging
    
  Working distance: 5-15 mm
    Short WD (5mm): High resolution
    Long WD (15mm): Large depth of field
    
  Probe current: 1 pA to 10 nA
    Low current: High resolution, low damage
    High current: Fast imaging, EDX analysis
    
  Chamber vacuum: less than 10^-5 Torr
    For insulating samples: Low vacuum mode (10^-3 Torr)
```

### 4.3 EDX Analysis

```
EDX analysis for iPACE-CHIP defect characterization:
  Typical defect compositions:
    Metallic particle: Al, Cu, Ti, W (from process equipment)
    Silicon particle: Si (from wafer handling)
    Organic residue: C, O (from photoresist or clean chemistry)
    Oxide defect: Si, O (from gate oxide process)
    Corrosion product: Al, O, Cl, F (from environmental exposure)
    
  EDX spectrum analysis:
    Identify peaks: Match with elemental database
    Quantify composition: ZAF correction method
    Spatial mapping: Elemental distribution map
    
  Example EDX result:
    Defect: Particle at (1250, 800) um
    Spectrum: Strong Al peak, weak O peak
    Conclusion: Aluminum particle from sputtering target
    Source: Metal sputtering chamber contamination
```

---

## 5. TEM Analysis

### 5.1 TEM Sample Preparation

```
TEM lamella preparation for iPACE-CHIP:
  Step 1: Identify region of interest (from SEM analysis)
    ├── Defect location: (1250, 800) um
    ├── Size of interest: 2um x 0.2um (width x depth)
    └── Orientation: Perpendicular to defect plane
    
  Step 2: FIB lift-out
    ├── Protect surface with Pt cap (200nm)
    ├── Mill trenches on both sides of lamella
    ├── Cut lamella free from substrate
    ├── Lift out with micromanipulator
    └── Mount on TEM grid (copper or molybdenum)
    
  Step 3: FIB thinning
    ├── Initial thinning: 30 keV, 500 pA
    ├── Final thinning: 5 keV, 50 pA
    ├── Target thickness: 50-100 nm
    └── Verify with electron transparency
    
  Step 4: TEM imaging
    ├── Bright-field imaging
    ├── Dark-field imaging
    ├── High-resolution TEM (HRTEM)
    └── Selected area electron diffraction (SAED)
```

### 5.2 TEM Analysis Capabilities

```
TEM capabilities for iPACE-CHIP analysis:
  Resolution: 0.1 nm (atomic resolution possible)
  
  Imaging modes:
    ├── HRTEM: Lattice imaging, crystal structure
    ├── STEM: High-angle annular dark field (HAADF)
    ├── EELS: Electron energy loss spectroscopy
    └── SAED: Crystal structure identification
    
  Measurement capabilities:
    ├── Film thickness: +/-0.1 nm accuracy
    ├── Lattice spacing: +/-0.01 nm accuracy
    ├── Interface roughness: +/-0.5 nm accuracy
    └── Defect dimensions: +/-1 nm accuracy
    
  Application examples:
    ├── Gate oxide thickness measurement
    ├── Barrier metal integrity assessment
    ├── Via fill quality verification
    └── Crystal defect identification
```

---

## 6. Application Examples

### 6.1 Gate Oxide Defect Analysis

```
Case study: IDDQ failure from gate oxide defect
  Electrical signature:
    IDDQ = 8.5 uA (spec: less than 5 uA)
    Failing vector: #452
    Diagnosis: NMOS transistor M456 in comparator
    
  Cross-section preparation:
    FIB cross-section through M456 gate region
    Section orientation: Perpendicular to gate channel
    
  SEM imaging results:
    Normal gate oxide: 5.0 nm thickness, uniform
    Defect region: 3.2 nm thickness (36% thinning)
    Defect length: 120 nm along gate width
    Defect morphology: Local thinning, not particle
    
  Root cause:
    Gate oxide thinning due to local etch non-uniformity
    Source: Micro-loading effect at pattern edge
    Corrective action: Adjust oxidation recipe for uniformity
```

### 6.2 Metal Bridging Defect

```
Case study: Scan failure from metal bridging
  Electrical signature:
    Pattern 452 fails on Chain 3, Cell 847
    Diagnosis: Possible bridging between M1 nets
    
  Cross-section preparation:
    FIB cross-section through suspected bridge location
    Section orientation: Parallel to metal lines
    
  SEM imaging results:
    Normal spacing: 180 nm (design rule: 180 nm)
    Defect location: 0 nm spacing (bridged)
    Bridge material: Metal residue (EDX: Al-Cu alloy)
    Bridge length: 250 nm
    
  Root cause:
    Incomplete etch-back of metal residue
    Source: Etch endpoint detection failure
    Corrective action: Optimize etch recipe, add post-etch clean
```

### 6.3 Via Void Defect

```
Case study: Signal integrity failure from via void
  Electrical signature:
    Timing failure on critical path
    Diagnosis: High resistance via
    
  Cross-section preparation:
    FIB cross-section through failing via
    Section orientation: Vertical through via stack
    
  SEM imaging results:
    Normal via: Complete fill, no voids
    Defect via: 60% void (incomplete fill)
    Void morphology: Center void (keyhole type)
    Void size: 0.15 um diameter in 0.20 um via
    
  Root cause:
    Via fill deposition non-uniformity
    Source: High aspect ratio via fill challenge
    Corrective action: Optimize PVD deposition, add reflow step
```

---

## 7. Automated Cross-Sectional Analysis

### 7.1 Automated FIB-SEM Systems

```
Automated cross-section systems for production PFA:
  FEI Helios 5 UX (or equivalent):
    Dual-beam FIB-SEM
    Automated cross-section recipes
    Image stitching for large areas
    Automated defect detection
    
  Capabilities:
    ├── Navigate from (x,y) coordinates to defect
    ├── Automated cross-section cutting
    ├── Multiple section angles
    ├── Automated SEM imaging
    └── EDX mapping
    
  Throughput:
    Single cross-section: 1-2 hours
    Multiple sections: 4-8 hours
    Full analysis report: 1-2 days
```

### 7.2 3D Tomography

```
3D cross-section analysis:
  Serial sectioning and imaging:
    ├── FIB cuts thin slice (50 nm)
    ├── SEM images exposed surface
    ├── Repeat for 100-200 slices
    └── Reconstruct 3D volume
    
  Applications for iPACE-CHIP:
    ├── 3D visualization of defect morphology
    ├── Via fill characterization (3D void shape)
    ├── Interconnect reliability assessment
    └── Process optimization feedback
    
  Data volume:
    200 slices x 1um x 1um = 200 um^3 volume
    Pixel size: 5nm x 5nm x 50nm
    Total data: ~1 GB per analysis
```

---

## 8. Quality and Reporting

### 8.1 Measurement Uncertainty

```
Cross-section measurement uncertainty:
  SEM magnification calibration: +/-2%
  Stage positioning: +/-50 nm
  FIB cutting accuracy: +/-20 nm
  Film thickness measurement: +/-0.5 nm (SEM), +/-0.1 nm (TEM)
  EDX composition: +/-2% relative
  
  Total measurement uncertainty budget:
    Film thickness: +/-0.5 nm (95% confidence)
    Feature dimension: +/-5 nm (95% confidence)
    Composition: +/-3% (95% confidence)
```

### 8.2 Cross-Section Analysis Report

```
Cross-section analysis report structure:
  1. Summary
     ├── Device and failure information
     ├── Cross-section location and orientation
     ├── Key findings
     └── Root cause conclusion
    
  2. Sample preparation
     ├── Method (FIB or mechanical)
     ├── Section orientation
     ├── Preparation parameters
    .
    └── Quality verification
    
  3. Imaging results
     ├── SEM images at multiple magnifications
     ├── Defect identification and measurement
     ├── Comparison with reference
    .
    └── EDX analysis results
    
  4. Analysis
     ├── Defect morphology description
     ├── Dimension measurements
     ├── Material composition
     ├── Process step identification
    .
    └── Comparison with design specification
    
  5. Root cause
     ├── Defect mechanism
     ├── Process step of origin
     ├── Systematic vs. random assessment
    .
    └── Corrective action recommendation
```

### 8.3 Archive and Traceability

```
Cross-section analysis data management:
  Image storage: TIFF format, 16-bit, uncompressed
  Metadata: Device ID, coordinates, parameters
  Archive: Network storage with 15-year retention
  Backup: Off-site redundant backup
  Access: Role-based permissions
  
  Traceability:
    Device serial number linked to analysis
    Analysis date and operator recorded
    Equipment serial number and calibration status
    Software version and settings documented
```

---

## 9. Summary

Cross-sectional analysis is the definitive physical failure analysis technique for the iPACE-CHIP, providing nanometer-resolution visualization of internal defects that cause electrical failures. FIB-based cross-sectioning offers precise targeting at diagnosed fault locations, while SEM and TEM imaging reveal defect morphology, composition, and root cause. The combination of automated FIB-SEM systems, EDX composition analysis, and 3D tomography provides comprehensive defect characterization that drives process improvement and ensures the zero-defect quality standard for this implantable medical device. Each cross-section analysis generates actionable root cause information that directly contributes to yield improvement, reliability assessment, and patient safety assurance.

---

## References

- Giannuzzi, L.A. & Stevie, F.A. *Introduction to Focused Ion Beams*. Springer, 2005.
- Orloff, J., Utlaut, M., & Swanson, L. *High Resolution Focused Ion Beams*. Kluwer, 2003.
- Goldstein, J. et al. *Scanning Electron Microscopy and X-Ray Microanalysis*. Springer, 2003.
- Williams, D.B. & Carter, C.B. *Transmission Electron Microscopy*. Springer, 2009.
- MIL-STD-883: Test Methods for Microelectronics (Method 2012 - Physical Dimensions)
- IEC 60747-1: Semiconductor Devices - General
- ASTM F1260: Standard Test Method for Examination of Cross-Section of Thin Film head
