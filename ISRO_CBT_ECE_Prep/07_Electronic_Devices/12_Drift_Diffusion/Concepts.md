# Drift & Diffusion - Concepts

## Carrier Transport Mechanisms

| Mechanism | Driving Force | Current Direction |
|-----------|--------------|-------------------|
| Drift | Electric field | Along field (holes), opposite (electrons) |
| Diffusion | Concentration gradient | High to low concentration |

### Total Current
$$J = J_{drift} + J_{diff} = q(n\mu_n + p\mu_p)E + qD_n\frac{dn}{dx} - qD_p\frac{dp}{dx}$$

---

## Drift Current

### Definition
- Motion of carriers under applied electric field
- Proportional to electric field (Ohmic region)
- All carriers contribute (majority + minority)

### Electron Drift Current
$$J_{n,drift} = q n \mu_n E$$

### Hole Drift Current
$$J_{p,drift} = q p \mu_p E$$

### Total Drift Current
$$J_{drift} = q(n\mu_n + p\mu_p)E = \sigma E$$

---

## Drift Velocity

### Definition
- Average velocity of carriers in field direction
- vd = μE (low field)
- Carrier mobility relates vd to E

### Scattering and Drift
- Carriers accelerate between collisions
- Collisions randomize velocity
- Net drift velocity small compared to thermal velocity
- vd << vth (at low fields)

---

## Diffusion Current

### Definition
- Motion due to concentration gradient
- Carriers move from high to low concentration
- Follows Fick's first law

### Electron Diffusion Current
$$J_{n,diff} = q D_n \frac{dn}{dx}$$

### Hole Diffusion Current
$$J_{p,diff} = -q D_p \frac{dp}{dx}$$

### Sign Convention
- Electrons diffuse down gradient → positive current in +x
- Holes diffuse down gradient → current in -x (negative)

---

## Einstein Relation

### Fundamental Relation
$$\frac{D}{\mu} = \frac{kT}{q} = V_T$$

### Significance
- Relates diffusion and drift
- Holds for non-degenerate semiconductors
- At 300K: D/μ = 26 mV

### Example (Si)
- Dn = 1350 × 0.026 = 35 cm²/s
- Dp = 480 × 0.026 = 12.5 cm²/s

---

## Continuity Equation

### General Form
$$\frac{\partial n}{\partial t} = \frac{1}{q}\frac{\partial J_n}{\partial x} + G - R$$

### Physical Meaning
Rate of change of carrier density = (net inflow) + (generation) - (recombination)

---

## Minority Carrier Diffusion

### Injected Minority Carriers
- When minority carriers are injected (e.g., at junction)
- They diffuse away from injection point
- Recombine with majority carriers
- Concentration decays exponentially

### Excess Carrier Concentration
$$\Delta p(x) = p(x) - p_{n0} = \Delta p(0) \exp\left(-\frac{x}{L_p}\right)$$

### Diffusion Length
$$L_p = \sqrt{D_p \tau_p}$$

---

## Diffusion Length

### Physical Meaning
- Average distance minority carrier travels before recombining
- Determines device dimensions

### Values (Si)
| Carrier | D (cm²/s) | τ (μs) | L (μm) |
|---------|-----------|--------|--------|
| Electrons | 35 | 1 | 59 |
| Holes | 12.5 | 1 | 35 |

### Relation
$$L = \sqrt{D\tau} = \sqrt{\mu V_T \tau}$$

---

## Low-Level vs High-Level Injection

### Low-Level Injection
- Δp << ND (minority carrier conc. << majority)
- Majority carrier conc. unchanged
- Simple linear recombination (τ constant)

### High-Level Injection
- Δp comparable to ND
- Majority carrier conc. increases
- τ increases (bimolecular)
- More complex analysis

---

## Generation-Recombination

### Recombination Mechanisms
1. **Shockley-Read-Hall (SRH)**: via traps (dominant in Si)
2. **Auger**: three-body process
3. **Radiative**: photon emission

### Recombination Rate
$$R = \frac{\Delta n}{\tau}$$

### Generation Rate
$$G = \frac{n_i}{\tau_g}$$

---

## ISRO Key Points
- Jdrift = σE (Ohmic)
- Jdiff = qDn(dn/dx) - qDp(dp/dx)
- D/μ = kT/q = VT = 26 mV
- L = √(Dτ)
- Total J = Jdrift + Jdiff
- Minority carrier injection → exponential decay
- Continuity equation relates J, G, R, t
