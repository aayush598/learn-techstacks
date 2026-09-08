# Carrier Mobility & Scattering - Concepts

## Mobility Definition

### Basic Concept
- Drift velocity per unit electric field
- μ = vd/E (cm²/V·s)
- Measure of carrier transport efficiency

### Types
- **Electron mobility (μn)**: typically higher
- **Hole mobility (μp)**: typically lower

### Typical Values (300K, Low Doping)
| Material | μn (cm²/V·s) | μp (cm²/V·s) |
|----------|--------------|--------------|
| Si | 1350 | 480 |
| Ge | 3900 | 1900 |
| GaAs | 8500 | 400 |
| InP | 4600 | 150 |
| GaN | 1000 | 200 |

---

## Drift Velocity

### Linear Region (Low Field)
$$v_d = \mu E$$

### Saturation Region (High Field)
$$v_{sat} \approx 10^7 \text{ cm/s (for Si)}$$

### Field Dependence
```
vd
│
│         vsat ───────────────
│        /
│       /
│      /
│     /
│    /
│   /
│  /
│ /
│/
└──────────────────────────── E
```

### Critical Field
$$E_{sat} = \frac{2v_{sat}}{\mu_n} \approx 3 \times 10^4 \text{ V/cm (for Si)}$$

---

## Scattering Mechanisms

### 1. Lattice (Phonon) Scattering
- Caused by thermal vibrations of crystal lattice
- Dominant at high temperatures
- μL ∝ T⁻³/²

### 2. Ionized Impurity Scattering
- Caused by Coulomb interaction with ionized dopants
- Dominant at low temperatures
- μI ∝ T³/²/NI

### 3. Neutral Impurity Scattering
- Interaction with neutral atoms
- Important at very high doping
- μN ∝ 1/NN

### 4. Surface Scattering
- Carriers scattered at Si-SiO₂ interface
- Important in MOSFETs
- Reduces effective mobility

### 5. Alloy Scattering
- In compound semiconductors (GaAs, InGaN)
- Random distribution of atoms
- Limits mobility in alloys

---

## Mobility-Temperature Relation

### Matthiessen's Rule
$$\frac{1}{\mu} = \frac{1}{\mu_L} + \frac{1}{\mu_I} + \frac{1}{\mu_N} + ...$$

### Temperature Dependence
| Mechanism | Temperature Dependence |
|-----------|------------------------|
| Lattice | μL ∝ T⁻³/² |
| Impurity | μI ∝ T³/² |
| Surface | μS ∝ T⁻¹/² |

### Combined Behavior
- High T: lattice scattering dominates (μ ∝ T⁻³/²)
- Low T: impurity scattering dominates (μ ∝ T³/²)
- Room T: mixed behavior

---

## Mobility-Doping Relation

### Empirical Formula
$$\mu = \frac{\mu_0}{1 + \left(\frac{N}{N_{ref}}\right)^\gamma}$$

### Parameters for Si at 300K
| Carrier | μ₀ (cm²/V·s) | Nref (cm⁻³) | γ |
|---------|--------------|-------------|---|
| Electrons | 92 | 1.3 × 10¹⁷ | 0.91 |
| Holes | 54 | 2.35 × 10¹⁷ | 0.88 |

### Key Points
- Mobility decreases with doping
- More degradation at high doping
- Electrons always faster than holes

---

## Saturation Velocity

### Definition
- Maximum drift velocity at high electric fields
- Independent of mobility
- Due to optical phonon emission

### Values at 300K
| Material | vsat (×10⁷ cm/s) |
|----------|-------------------|
| Si | 1.0 |
| GaAs | 0.8 |
| Ge | 0.6 |
| InP | 1.0 |
| GaN | 2.5 |

### Field Dependence (Empirical)
$$v_d = \frac{\mu E}{1 + \mu E/v_{sat}}$$

---

## Effective Mobility

### Definition
- Mobility measured in MOSFET channel
- Lower than bulk mobility

### Factors Reducing Effective Mobility
1. Surface roughness scattering
2. Coulomb scattering from oxide charges
3. Phonon scattering at interface
4. High vertical field

### Typical Values (MOSFET)
| Material | μeff (cm²/V·s) |
|----------|----------------|
| Si (electrons) | 300-500 |
| Si (holes) | 100-200 |

---

## Einstein Relation

### Fundamental
$$\frac{D}{\mu} = \frac{kT}{q} = V_T$$

### Diffusion Coefficients
$$D_n = \mu_n V_T$$
$$D_p = \mu_p V_T$$

### At 300K
$$D_n = 0.026 \mu_n \quad \text{(cm²/s)}$$
$$D_p = 0.026 \mu_p \quad \text{(cm²/s)}$$

---

## High-Field Transport

### Velocity Overshoot
- Transient effect in short channels
- Carriers overshoot steady-state velocity
- Important in sub-micron devices

### Ballistic Transport
- In very short channels (< 100 nm)
- Carriers traverse without scattering
- Velocity approaches thermal velocity

### Thermal Velocity
$$v_{th} = \sqrt{\frac{3kT}{m^*}} \approx 10^7 \text{ cm/s}$$

---

## Temperature Coefficient of Mobility

### Lattice Scattering
$$\frac{d\mu_L}{dT} = -\frac{3}{2}\frac{\mu_L}{T}$$

### Impurity Scattering
$$\frac{d\mu_I}{dT} = \frac{3}{2}\frac{\mu_I}{T}$$

### Net Effect
- At room temperature: dμ/dT < 0 (lattice dominates)
- Mobility decreases with temperature

---

## Strained Silicon

### Concept
- Strain modifies band structure
- Reduces effective mass
- Increases mobility

### Benefits
- NMOS: 70-100% μn improvement
- PMOS: 20-50% μp improvement
- Used in modern CMOS

---

## ISRO Key Points
- μn > μp (electrons faster than holes)
- Mobility decreases with doping and temperature
- vsat ≈ 10⁷ cm/s for Si
- Lattice scattering: μ ∝ T⁻³/²
- Impurity scattering: μ ∝ T³/²
- Einstein relation: D/μ = VT = 26 mV
- Effective mobility in MOSFET < bulk mobility
