# ISRO EDC Shortcuts

## Quick-Value Constants (Given/Required for ISRO)

| Quantity | Value |
|----------|-------|
| VT (300K) | 25.85 mV ≈ 26 mV |
| kT (300K) | 0.02585 eV |
| q | 1.6×10⁻¹⁹ C |
| k | 8.617×10⁻⁵ eV/K |
| Si Eg | 1.12 eV |
| Ge Eg | 0.67 eV |
| GaAs Eg | 1.43 eV |
| ni(Si) 300K | 1.5×10¹⁰ cm⁻³ |
| Nc(Si) | 2.8×10¹⁹ cm⁻³ |
| Nv(Si) | 1.04×10¹⁹ cm⁻³ |
| μn(Si) | 1350 cm²/V·s |
| μp(Si) | 480 cm²/V·s |

---

## Bandgap Temperature Coefficient Problems

### dEg/dT
- Si: -0.27 meV/K
- Eg(300K) = Eg(0) - 0.045 (Si)
- Eg(0) = 1.17 eV (Si)

### Method
$$E_g(T) = E_g(0) - \frac{\alpha T^2}{T + \beta}$$

**Quick approach:** Eg(300K) ≈ Eg(0) - 0.045 (for Si)
- For every 100K above 300: Eg drops ~5-8 meV
- Approximate: dEg/dT ≈ -0.3 meV/K

### Example
Q: Eg of Si at 400K?
Eg(400K) ≈ 1.12 - 0.27×10⁻³×(400-300) = 1.12 - 0.027 = 1.093 eV

---

## Fermi Level Calculations - Fast Method

### Formula
$$E_F - E_i = kT \ln\left(\frac{N_D}{n_i}\right)$$

### Use kT = 0.026 eV @ 300K
| ND/ni | ln ratio | EF-Ei (eV) |
|--------|----------|------------|
| 10⁵ | 11.5 | 0.30 |
| 10⁶ | 13.8 | 0.36 |
| 10⁷ | 16.1 | 0.42 |
| 10⁸ | 18.4 | 0.48 |

### Convert EF position from EC:
EF from EC = kT·ln(Nc/n) = 0.026·ln(Nc/n)

| n (cm⁻³) | EC - EF (eV) |
|-----------|--------------|
| 10¹⁵ | 0.26 |
| 10¹⁶ | 0.21 |
| 10¹⁷ | 0.15 |
| 10¹⁸ | 0.09 |

---

## MOSFET Current Calculation - Fast Method

### Saturation
$$I_D = \frac{1}{2} k_n' \frac{W}{L}(V_{GS} - V_T)^2$$

- If kn'(W/L) known: ID = (1/2)kn'(W/L)·Vov²
- If ID and Vov known: gm = 2ID/Vov

### Quick gm
| ID (μA) | Vov (V) | gm (μS) |
|---------|---------|---------|
| 100 | 0.5 | 400 |
| 400 | 0.5 | 1600 |
| 100 | 0.2 | 1000 |

---

## BJT Beta/Alpha Conversions

### Conversions (memorize)
$$β = \frac{α}{1-α}, \quad α = \frac{β}{1+β}$$

| α | β |
|---|----|
| 0.95 | 19 |
| 0.98 | 49 |
| 0.99 | 99 |
| 0.995 | 199 |
| 0.999 | 999 |

### gm for BJT
gm = IC/VT = 40×IC(mA) mS
- IC=1mA → gm=40mS
- IC=2mA → gm=80mS
- IC=0.5mA → gm=20mS

---

## Diode DC Operation - Quick Values

### Forward voltage drops
| Diode | VF |
|-------|-----|
| Si | 0.7V |
| Ge | 0.3V |
| Schottky | 0.3V |
| LED red | 1.8V |
| LED blue | 3.0V |

### Dynamic resistance
rd = 26mV/ID(mA) (Ω)
- ID=1mA → 26Ω
- ID=10mA → 2.6Ω
- ID=100mA → 0.26Ω

### Current change per mV
Each 60 mV forward → current ×10 (at n=1, 300K)

---

## Capacitance Quick Values

### Junction Capacitance
Cj = Cj0/√(1+VR/Vbi) (abrupt)

- VR=3Vbi → Cj = Cj0/2
- VR=8Vbi → Cj = Cj0/3
- VR=15Vbi → Cj = Cj0/4

### Diffusion Capacitance
Cd = τ·gm = τI/VT

---

## Region Determination - Quick Flow

### BJT
```
VBE < 0.5V (Si forward) ? 
  No → Cutoff
  Yes → VCE > VCE(sat)?
     Yes → Active
     No → Saturation
```

### MOSFET (NMOS)
```
VGS < VT ? → Cutoff
VGS > VT and VDS < VGS-VT ? → Linear
VGS > VT and VDS ≥ VGS-VT ? → Saturation
```

---

## Breakdown Mechanism Quick Check

| VBR | Mechanism | Temp coef |
|-----|-----------|-----------|
| < 5V | Zener | Negative |
| 5-6V | Combined | ≈ 0 |
| > 6V | Avalanche | Positive |
| ~5.6V | Balanced | ≈ 0 |

---

## ISRO Numerical Surprises

### Thermal voltage at different T
VT = 25.85×(T/300) mV
- 200K: 17.2mV
- 400K: 34.5mV
- 500K: 43mV

### ni at different T (Si)
ni(T) ≈ 4.5×10¹⁵ × T^1.5 × exp(-0.56/kT... )
- 300K: 1.5×10¹⁰
- 400K: ~4.5×10¹²
- 500K: ~2×10¹⁴

### Mobility approximation
μ(T) ≈ μ(300)×(300/T)^1.5 (lattice only)

---

## Unit Conversion Helpers

- 1 eV = 1.6×10⁻¹⁹ J
- VT·ln(N) → use 26 mV × ln ratio
- λ(mn) = 1240/Eg(eV)
- ni² = np (always)
- μ units: cm²/V·s
- D units: cm²/s

---

## Fast Selection Tips
1. Mass action law: n·p = ni² (any doping)
2. gm BJT = 40×IC(absolute)
3. gm MOSFET = 2ID/Vov
4. rd diode = 26mV/I
5. β = α/(1-α)
6. Defer: don't compute ln, recall from table
7. Einstein: D = μ×0.026
8. L = √(Dτ)
