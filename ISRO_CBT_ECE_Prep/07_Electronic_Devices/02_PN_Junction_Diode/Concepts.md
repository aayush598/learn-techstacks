# PN Junction Diode - Concepts

## PN Junction Formation

### Step-by-Step Process
1. Join P-type and N-type semiconductors
2. Majority carriers diffuse across junction
   - Electrons from N-side → P-side
   - Holes from P-side → N-side
3. Exposed donor ions (ND⁺) on N-side
4. Exposed acceptor ions (NA⁻) on P-side
5. Built-in electric field develops (N → P direction)
6. Equilibrium reached: diffusion = drift

### Depletion Region
- Region depleted of free carriers
- Contains only ionized dopant atoms
- Width: W = WN + WP
- Also called: space charge region, transition region, depletion layer

### Built-in Potential
$$V_{bi} = \frac{kT}{q} \ln\left(\frac{N_A N_D}{n_i^2}\right) = V_T \ln\left(\frac{N_A N_D}{n_i^2}\right)$$

At 300K:
$$V_{bi} = 0.026 \ln\left(\frac{N_A N_D}{n_i^2}\right)$$

Typical Values:
| Junction | Vbi (V) |
|----------|---------|
| Si abrupt | 0.6 - 0.8 |
| Ge abrupt | 0.2 - 0.3 |
| GaAs | 0.9 - 1.2 |

---

## Depletion Region Properties

### Charge Distribution (Abrupt Junction)
```
N-side: ρ = +qND (0 < x < WN)
P-side: ρ = -qNA (-WP < x < 0)
```

### Electric Field
- Maximum at junction: Emax = qNAWP/ε = qNDWN/ε
- Triangular profile
- Direction: N → P (opposes diffusion)

### Depletion Width
$$W = \sqrt{\frac{2\varepsilon}{q}\left(\frac{1}{N_A} + \frac{1}{N_D}\right)(V_{bi} - V)}$$

For one-sided junction (NA >> ND):
$$W \approx \sqrt{\frac{2\varepsilon(V_{bi} - V)}{qN_D}}$$

### Key Points
- W increases with reverse bias
- W decreases with forward bias
- W ∝ (1/ND) for one-sided junction
- W depends on √V for abrupt junction

---

## Forward Bias

### Applied Voltage
- Positive terminal to P-side
- Negative terminal to N-side
- Reduces barrier potential
- Narrows depletion width
- Majority carriers can cross junction

### Current Components
1. **Diffusion current** (dominant): majority carriers diffuse
2. **Recombination current**: carriers recombine in depletion region
3. **Space charge recombination**: at low forward bias

### V-I Characteristic
$$I = I_s\left[\exp\left(\frac{V}{nV_T}\right) - 1\right]$$

Where:
- Is = reverse saturation current
- n = ideality factor (1-2)
- VT = kT/q = 26 mV at 300K

### Forward Voltage Drops
| Material | Typical VF (V) |
|----------|----------------|
| Si | 0.6 - 0.7 |
| Ge | 0.2 - 0.3 |
| GaAs | 1.0 - 1.2 |
| LED (red) | 1.6 - 1.8 |
| LED (blue) | 3.0 - 3.5 |

---

## Reverse Bias

### Applied Voltage
- Negative terminal to P-side
- Positive terminal to N-side
- Increases barrier potential
- Widens depletion width
- Only minority carriers cross junction

### Reverse Saturation Current
$$I_s = qA\left(\frac{D_p}{L_p}p_n + \frac{D_n}{L_n}n_p\right) = qA\left(\frac{D_p p_{n0}}{L_p} + \frac{D_n n_{p0}}{L_n}\right)$$

Where:
- A = junction area
- Dp, Dn = diffusion constants
- Lp, Ln = diffusion lengths
- pn0, np0 = equilibrium minority carrier concentrations

### Key Properties
- Independent of reverse voltage (ideal)
- Depends on temperature: Is ∝ T³·exp(-Eg/kT)
- Doubles for every 10°C rise in Si
- Very small: nA to μA range

---

## Ideal Diode Equation (Shockley Equation)

### Complete V-I Relationship
$$I = I_s\left[\exp\left(\frac{V}{nV_T}\right) - 1\right]$$

### Analysis
| Condition | Approximation |
|-----------|---------------|
| V >> nVT | I ≈ Is·exp(V/nVT) |
| V << -nVT | I ≈ -Is |
| V = 0 | I = 0 |
| V = nVT | I ≈ 1.7Is |

### Ideality Factor (n)
| Value | Mechanism |
|-------|-----------|
| n = 1 | Diffusion current (dominant) |
| n = 2 | Recombination current (dominant) |
| 1 < n < 2 | Both mechanisms present |

---

## Current Components in PN Junction

### Forward Bias
1. **Electron diffusion** from N to P
2. **Hole diffusion** from P to N
3. **Recombination** in depletion region
4. **Generation** in neutral regions (small)

### Reverse Bias
1. **Generation** of EHPs in depletion region
2. **Diffusion** of minority carriers to junction
3. Both contribute to Is

---

## Diffusion Length

### Definition
Average distance minority carrier travels before recombination

$$L = \sqrt{D\tau}$$

Where:
- D = diffusion coefficient
- τ = minority carrier lifetime

### For Electrons in P-side
$$L_n = \sqrt{D_n \tau_n}$$

### For Holes in N-side
$$L_p = \sqrt{D_p \tau_p}$$

### Typical Values (Si)
| Carrier | τ (μs) | D (cm²/s) | L (μm) |
|---------|--------|-----------|--------|
| Electrons | 1-100 | 35 | 10-60 |
| Holes | 1-100 | 12.5 | 6-35 |

---

## Junction Capacitance

### Depletion (Transition) Capacitance
$$C_j = \frac{\varepsilon A}{W} = A\sqrt{\frac{q\varepsilon}{2}\left(\frac{N_A N_D}{N_A + N_D}\right)\frac{1}{V_{bi} - V}}$$

- Dominant in reverse bias
- Varies as 1/√V for abrupt junction
- Used in varactor diodes

### Diffusion Capacitance
$$C_d = \frac{\tau I}{V_T}$$

- Dominant in forward bias
- Linearly proportional to current
- Due to stored minority carrier charge

---

## Switching Characteristics

### Forward Recovery Time
- Time for diode to reach steady-state forward voltage
- Typically very small (ns)

### Reverse Recovery Time (trr)
- Time for diode to switch from ON to OFF
- Components:
  1. Storage time (ts): time to remove stored charge
  2. Transition time (tt): time for depletion region to form
- trr = ts + tt
- Typical values: 1-100 ns for Si diodes

### Stored Charge
$$Q = \int_0^{I_F} \tau \, dI = \tau I_F$$

---

## Breakdown Mechanisms

### 1. Avalanche Breakdown
- Impact ionization by high-energy carriers
- Multiplication of carriers
- Dominant for VA > 6V
- Positive temperature coefficient
- VBR ∝ 1/ND^(3/4)

### 2. Zener Breakdown
- Direct ionization by electric field
- Tunneling of electrons
- Dominant for VA < 5V
- Negative temperature coefficient
- VBR ∝ 1/ND^(3/4)

### 3. Transition
- ~5-6V: both mechanisms contribute
- Temperature coefficient changes sign

---

## Temperature Effects

### On V-I Characteristic
- Forward voltage decreases ~2 mV/°C
- Reverse saturation current doubles per 10°C rise
- Curve shifts left with temperature increase

### On Breakdown Voltage
- Avalanche: VBR increases with temperature
- Zener: VBR decreases with temperature
- At ~5.6V: temperature coefficient ≈ 0

---

## Load Line Analysis

### DC Load Line
- Plot on V-I characteristic
- Equation: VDD = VR + IR·RL
- Intercepts: (VDD, 0) and (0, VDD/RL)
- Q-point is intersection with diode curve

### AC Load Line
- Slope = -1/rd (dynamic resistance)
- Passes through Q-point
- Used for small-signal analysis

---

## Small-Signal Model

### Dynamic Resistance
$$r_d = \frac{nV_T}{I_D} = \frac{nV_T}{I_Q}$$

At 300K (n=1):
$$r_d = \frac{26 \text{ mV}}{I_D}$$

### Values
| ID (mA) | rd (Ω) |
|---------|--------|
| 0.1 | 260 |
| 1 | 26 |
| 10 | 2.6 |
| 100 | 0.26 |

---

## ISRO Key Points
- Si diode: Vbi ≈ 0.7V, Ge: Vbi ≈ 0.3V
- Depletion width increases with reverse bias
- Diffusion capacitance dominates forward bias
- Transition capacitance dominates reverse bias
- trr is important for high-frequency switching
- Zener breakdown: negative temp coefficient, < 5V
- Avalanche breakdown: positive temp coefficient, > 6V
- At ~5.6V, temperature coefficient ≈ 0
