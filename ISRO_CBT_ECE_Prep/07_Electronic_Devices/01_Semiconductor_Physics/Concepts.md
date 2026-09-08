# Semiconductor Physics - Concepts

## Energy Bands in Solids

### Formation of Energy Bands
- Isolated atoms have discrete energy levels
- When N atoms come close, each level splits into N closely spaced levels
- These groups of closely spaced levels form **energy bands**
- Energy gap between bands = **forbidden energy gap (Eg)**

### Types of Energy Bands
| Band | Description |
|------|-------------|
| Valence Band (VB) | Highest energy band occupied by electrons at 0K |
| Conduction Band (EB) | Lowest empty band at 0K |
| Forbidden Gap | Energy difference between CB bottom and VB top |
| Fermi Level | Average energy level, probability = 0.5 |

### Classification Based on Eg
| Material | Eg (eV) at 300K | Example |
|----------|-----------------|---------|
| Conductor | 0 (overlapping bands) | Cu, Ag, Al |
| Semiconductor | 0.1 - 3.0 | Si (1.12), Ge (0.67), GaAs (1.43) |
| Insulator | > 3.0 | Diamond (5.5), SiO₂ (9) |

### Temperature Dependence of Eg
$$E_g(T) = E_g(0) - \frac{\alpha T^2}{T + \beta}$$
- Si: α = 4.73×10⁻⁴ eV/K, β = 636 K
- Eg decreases with temperature
- At T=0K, Eg(0) = 1.17 eV for Si

---

## Crystal Structure

### Silicon Crystal
- Diamond cubic structure
- Each Si atom covalently bonded to 4 neighbors
- Bond energy = 1.12 eV per bond
- Lattice constant a = 5.43 Å

### Covalent Bonding
- 4 valence electrons of Si form 4 covalent bonds
- At T=0K: all bonds complete → no free electrons → insulator behavior
- At T>0K: thermal energy breaks bonds → electron-hole pairs created

---

## Intrinsic Semiconductors

### Definition
Pure semiconductor with no intentional doping. Conductivity determined by thermally generated carriers.

### Carrier Generation
- Thermal agitation breaks covalent bonds
- Creates electron-hole pair (EHP)
- Rate of generation = Rate of recombination (thermal equilibrium)

### Intrinsic Carrier Concentration
$$n_i = \sqrt{N_c N_v} \exp\left(-\frac{E_g}{2kT}\right)$$

At T=300K:
| Material | ni (cm⁻³) |
|----------|-----------|
| Si | 1.5 × 10¹⁰ |
| Ge | 2.4 × 10¹³ |
| GaAs | 1.8 × 10⁶ |

### Temperature Dependence of ni
- ni doubles for every 11°C rise in Si
- ni is very sensitive to temperature (exponential)

### neutrality condition (intrinsic)
n = p = ni

---

## Extrinsic Semiconductors

### N-type Semiconductor
- Doped with pentavalent impurity (P, As, Sb)
- Majority carriers: **electrons** (n ≈ ND)
- Minority carriers: **holes** (p = ni²/ND)
- Donor energy level ED is just below EC (~0.01-0.05 eV)
- At room temperature, all donors are ionized (exhaustion range)

### P-type Semiconductor
- Doped with trivalent impurity (B, Ga, In)
- Majority carriers: **holes** (p ≈ NA)
- Minority carriers: **electrons** (n = ni²/NA)
- Acceptor energy level EA is just above EV
- At room temperature, all acceptors are ionized

### Compensation
- When both donor and acceptor impurities are present
- Net doping = |ND - NA|
- If ND > NA → n-type, n ≈ ND - NA

---

## Carrier Concentration (Law of Mass Action)

### Mass Action Law
$$n \cdot p = n_i^2$$

- Product of electron and hole concentrations is constant at given temperature
- Independent of doping level
- Applies under thermal equilibrium

### Electroneutrality Condition
$$n + N_A^- = p + N_D^+$$

Where NA⁻ = ionized acceptors, ND⁺ = ionized donors

### Complete Equations
For n-type (ND >> NA, complete ionization):
$$n \approx N_D - N_A + \frac{n_i^2}{N_D - N_A}$$

$$p = \frac{n_i^2}{N_D - N_A}$$

---

## Conductivity and Resistivity

### Conductivity
$$\sigma = q(n\mu_n + p\mu_p)$$

### Resistivity
$$\rho = \frac{1}{\sigma} = \frac{1}{q(n\mu_n + p\mu_p)}$$

### Resistivity Values at 300K
| Material | ρ (Ω-cm) |
|----------|----------|
| Cu (conductor) | 1.7 × 10⁻⁶ |
| Intrinsic Si | 2.3 × 10⁵ |
| Doped Si (10¹⁶ cm⁻³) | 0.5 |

### Conductivity of N-type
$$\sigma_n \approx q N_D \mu_n$$

### Conductivity of P-type
$$\sigma_p \approx q N_A \mu_p$$

---

## Mobility and Diffusion

### Mobility (μ)
- Drift velocity per unit electric field
- μ = vd/E (cm²/V-s)
- Depends on: temperature, doping, crystal defects

### Typical Mobility Values (300K)
| Material | μn (cm²/V-s) | μp (cm²/V-s) |
|----------|--------------|--------------|
| Si | 1350 | 480 |
| Ge | 3900 | 1900 |
| GaAs | 8500 | 400 |

### Einstein Relation
$$\frac{D}{\mu} = \frac{kT}{q} = V_T$$

VT = 26 mV at 300K

### Diffusion Constant
$$D_n = \mu_n V_T, \quad D_p = \mu_p V_T$$

---

## Types of Carrier Transport

### 1. Drift
- Motion of carriers due to applied electric field
- Drift current density: J = σE
- Contributes to current in resistors, etc.

### 2. Diffusion
- Motion of carriers from high to low concentration
- Due to concentration gradient
- Fick's law: J = -qD(dn/dx)

### 3. Thermal Motion
- Random motion at finite temperature
- Average kinetic energy = 3kT/2
- No net current (statistically cancels)

---

## Fermi-Dirac Distribution

### Probability Function
$$f(E) = \frac{1}{1 + \exp\left(\frac{E - E_F}{kT}\right)}$$

### Key Properties
- f(EF) = 1/2 (at any temperature)
- At T=0K: f(E) = 1 for E < EF, f(E) = 0 for E > EF
- At high energies: f(E) ≈ exp(-(E-EF)/kT) (Maxwell-Boltzmann approx)

### Boltzmann Approximation
Valid when (E - EF) >> kT:
$$f(E) \approx \exp\left(-\frac{E - E_F}{kT}\right)$$

---

## Density of States

### Effective Density of States
$$N_c = 2\left(\frac{2\pi m_n^* kT}{h^2}\right)^{3/2}$$

$$N_v = 2\left(\frac{2\pi m_p^* kT}{h^2}\right)^{3/2}$$

### At 300K
| Material | Nc (cm⁻³) | Nv (cm⁻³) |
|----------|-----------|-----------|
| Si | 2.8 × 10¹⁹ | 1.04 × 10¹⁹ |
| Ge | 1.04 × 10¹⁹ | 6.0 × 10¹⁸ |
| GaAs | 4.7 × 10¹⁷ | 7.0 × 10¹⁸ |

### Effective Mass
- mn* ≈ 1.08mn for Si
- mp* ≈ 0.81mn for Si
- mn* ≈ 0.067mn for GaAs (light electrons → high mobility)

---

## Recombination Mechanisms

### 1. Direct (Band-to-Band)
- Electron falls directly from CB to VB
- Energy released as photon (LED principle)
- Dominant in direct bandgap (GaAs, InP)

### 2. Indirect (Shockley-Read-Hall - SRH)
- Via trap/defect level in forbidden gap
- Two-step process involving phonon
- Dominant in indirect bandgap (Si, Ge)

### 3. Auger Recombination
- Energy transferred to third carrier
- Dominant at high carrier concentrations
- Important in heavily doped regions

### Recombination Rate
$$R = \frac{np - n_i^2}{\tau_p(n + n_1) + \tau_n(p + p_1)}$$

---

## Semiconductor Examples (ISRO Frequent)

| Parameter | Si | Ge | GaAs |
|-----------|-----|-----|------|
| Eg (eV) | 1.12 | 0.67 | 1.43 |
| Type | Indirect | Indirect | Direct |
| ni (cm⁻³) | 1.5×10¹⁰ | 2.4×10¹³ | 1.8×10⁶ |
| μn (cm²/V-s) | 1350 | 3900 | 8500 |
| μp (cm²/V-s) | 480 | 1900 | 400 |
| Application | ICs, MOSFETs | Detectors | LEDs, lasers |

---

## ISRO Key Points
- Si is most used in IC fabrication due to stable SiO₂
- GaAs preferred for high-frequency and optoelectronic devices
- At T=0K, semiconductor behaves as insulator
- Extrinsic range: all dopants ionized, n or p constant with T
- Intrinsic range: ni >> doping, semiconductor behaves intrinsic
