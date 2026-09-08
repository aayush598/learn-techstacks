# Fermi Level Calculations - Concepts

## Fermi-Dirac Statistics

### Distribution Function
$$f(E) = \frac{1}{1 + \exp\left(\frac{E - E_F}{kT}\right)}$$

### Key Properties
| Energy | f(E) |
|--------|------|
| E << EF | f ≈ 1 (filled) |
| E = EF | f = 0.5 |
| E >> EF | f ≈ 0 (empty) |
| E - EF = kT | f = 0.269 |
| E - EF = 3kT | f = 0.047 |

---

## Fermi Level Definition

### Physical Meaning
- Energy level with 50% probability of occupation
- Chemical potential of electrons
- Represents average electron energy

### At T = 0K
- f(E) = 1 for E < EF (all states filled)
- f(E) = 0 for E > EF (all states empty)
- Sharp boundary at EF

---

## Fermi Level in Different Materials

### Intrinsic Semiconductor
$$E_i = E_c - \frac{E_g}{2} + \frac{3kT}{4}\ln\left(\frac{m_p^*}{m_n^*}\right)$$

- Near midgap
- Slightly above midgap (if mn* > mp*)

### N-type
$$E_F = E_c - kT\ln\left(\frac{N_c}{N_D}\right)$$

- Moves closer to conduction band
- Higher doping → closer to EC

### P-type
$$E_F = E_v + kT\ln\left(\frac{N_v}{N_A}\right)$$

- Moves closer to valence band
- Higher doping → closer to EV

---

## Non-Degenerate Semiconductor

### Condition
$$(E_c - E_F) > 2kT$$

### Validity
- Boltzmann approximation valid
- f(E) ≈ exp(-(E-EF)/kT)
- Carrier concentration formulas simple

### Typical Doping
- N < 10¹⁸ cm⁻³ for Si at 300K
- Below degenerate limit

---

## Degenerate Semiconductor

### Condition
$$(E_c - E_F) \leq 2kT \text{ (or EF > Ec)}$$

### Characteristics
- EF approaches/enters band
- Boltzmann approximation invalid
- Fermi-Dirac statistics required
- Requires Fermi integral

### Heavy Doping Regime
- N > 10¹⁸-10¹⁹ cm⁻³ (Si)
- EF in conduction band

---

## Carrier Concentration Formulas

### Non-Degenerate
$$n = N_c \exp\left(-\frac{E_c - E_F}{kT}\right)$$

$$p = N_v \exp\left(-\frac{E_F - E_v}{kT}\right)$$

### In Terms of Intrinsic
$$n = n_i \exp\left(\frac{E_F - E_i}{kT}\right)$$

$$p = n_i \exp\left(\frac{E_i - E_F}{kT}\right)$$

### Mass Action Law
$$np = n_i^2$$

---

## Fermi Level Position Calculations

### From Doping
$$E_F - E_i = kT \ln\left(\frac{N_D}{n_i}\right) \quad \text{(N-type)}$$

$$E_i - E_F = kT \ln\left(\frac{N_A}{n_i}\right) \quad \text{(P-type)}$$

### From Carrier Concentration
$$E_F - E_i = kT \ln\left(\frac{n}{n_i}\right)$$

---

## Fermi Integral

### Definition
$$F_{1/2}(\eta) = \int_0^\infty \frac{\sqrt{\epsilon} d\epsilon}{1 + \exp(\epsilon - \eta)}$$

Where η = (EF - EC)/kT

### Key Results
| Regime | Carrier Density |
|--------|-----------------|
| Non-degenerate | n = Nc·exp(η) |
| Degenerate | n = Nc·(2/√π)·F_{1/2}(η) |

### Approximations
- η << -1: classical (Maxwell-Boltzmann)
- η ≈ 0: transition
- η >> 1: degenerate

---

## Temperature Dependence of EF

### Intrinsic
$$E_i(T) = E_c - \frac{E_g(T)}{2} + \frac{3}{4}kT\ln\left(\frac{m_p^*}{m_n^*}\right)$$

- Decreases with T (as Eg decreases)
- Slightly shifts if mn* ≠ mp*

### N-type (Extrinsic Range)
- EF insensitive to T (n ≈ ND)
- EF position from EC: EF = EC - kT·ln(NC/ND)

### At High T (Intrinsic Range)
- EF returns toward midgap
- Semiconductor becomes intrinsic

---

## Position of EF Relative to Bands

### Energy Diagram
```
Energy
  │  EC ────────  ← Conduction band
  │     • EF (N-type, near EC)
  │     • EF (intrinsic, midgap)
  │     • EF (P-type, near EV)
  │  EV ────────  ← Valence band
  │
```

### Table (Si at 300K)
| Doping (cm⁻³) | EF - EC (eV) |
|----------------|--------------|
| 10¹⁵ | -0.26 |
| 10¹⁶ | -0.21 |
| 10¹⁷ | -0.15 |
| 10¹⁸ | -0.09 |

---

## Mass Action Law Applications

### 1. Find Majority Carriers
n ≈ ND (if ND >> ni)

### 2. Find Minority Carriers
p = ni²/ND

### 3. Find EF
EF = Ei + kT·ln(ND/ni)

### 4. Check for Degeneracy
Compare (EC - EF) with 2kT

---

## Extended States

### Fermi Level Pinning
- Surface states pin EF at surface
- Due to dangling bonds/dangling states
- Important in metal-semiconductor contacts

### In Junctions
- EF is constant across junction (equilibrium)
- Bands bend to maintain constant EF
- At equilibrium: EF flat throughout

---

## Numerical Example

### Given: Si, ND = 10¹⁶ cm⁻³, 300K
1. ni = 1.5 × 10¹⁰ cm⁻³
2. n ≈ ND = 10¹⁶ cm⁻³
3. EF - Ei = kT·ln(ND/ni) = 0.026·ln(10¹⁶/1.5×10¹⁰) = 0.026 × 13.4 = 0.35 eV
4. EC - EF = 0.55 - 0.35 = 0.2 eV (from midgap EC-Ei = 0.55)

---

## ISRO Key Points
- EF = 50% occupation probability
- N-type: EF above Ei (toward EC)
- P-type: EF below Ei (toward EV)
- Degenerate: EF within band
- Non-degenerate: (EC - EF) > 2kT
- n = ni·exp((EF-EI)/kT)
- np = ni² always (equilibrium)
