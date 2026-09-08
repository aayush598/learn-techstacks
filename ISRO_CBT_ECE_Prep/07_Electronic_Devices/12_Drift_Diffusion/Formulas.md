# Drift & Diffusion - Formulas

## Drift Current

### Electron Drift
$$J_{n,drift} = q n \mu_n E$$

### Hole Drift
$$J_{p,drift} = q p \mu_p E$$

### Total Drift Current Density
$$J_{drift} = q(n\mu_n + p\mu_p)E = \sigma E$$

### Drift Velocity
$$v_d = \mu E$$

### Current (Drift) in Wire
$$I = q n v_d A$$

---

## Diffusion Current

### Electron Diffusion
$$J_{n,diff} = q D_n \frac{dn}{dx}$$

### Hole Diffusion
$$J_{p,diff} = -q D_p \frac{dp}{dx}$$

### General (3D)
$$J_{n,diff} = q D_n \nabla n$$
$$J_{p,diff} = -q D_p \nabla p$$

---

## Total Current

### Electron Current
$$J_n = q n \mu_n E + q D_n \frac{dn}{dx}$$

### Hole Current
$$J_p = q p \mu_p E - q D_p \frac{dp}{dx}$$

### Total Current
$$J = J_n + J_p$$

---

## Einstein Relation

### Fundamental
$$\frac{D}{\mu} = \frac{kT}{q} = V_T$$

### For Electrons
$$D_n = \mu_n V_T$$

### For Holes
$$D_p = \mu_p V_T$$

### At Temperature T
$$\frac{D}{\mu} = \frac{kT}{q} = 25.85 \left(\frac{T}{300}\right) \text{ mV}$$

---

## Minority Carrier Diffusion

### Excess Concentration
$$\Delta p(x) = p(x) - p_{n0}$$

### Exponential Decay
$$\Delta p(x) = \Delta p(0) \exp\left(-\frac{x}{L_p}\right)$$

### Diffusion Length
$$L_p = \sqrt{D_p \tau_p}$$

$$L_n = \sqrt{D_n \tau_n}$$

---

## Continuity Equation

### General (1D)
$$\frac{\partial p}{\partial t} = -\frac{1}{q}\frac{\partial J_p}{\partial x} + G_p - R_p$$

$$\frac{\partial n}{\partial t} = \frac{1}{q}\frac{\partial J_n}{\partial x} + G_n - R_n$$

### With Recombination (no generation, no field)
$$\frac{\partial \Delta p}{\partial t} = D_p \frac{\partial^2 \Delta p}{\partial x^2} - \frac{\Delta p}{\tau_p}$$

---

## Steady-State Solutions

### Long Semiconductor (x >> L)
$$\Delta p(x) = \Delta p(0) \exp\left(-\frac{x}{L_p}\right)$$

### Diffusion Current from Injection
$$J_{p,diff}(0) = \frac{q D_p \Delta p(0)}{L_p}$$

### Finite Bar
$$\Delta p(x) = \frac{\Delta p(0) \sinh\left(\frac{W - x}{L_p}\right)}{\sinh\left(\frac{W}{L_p}\right)}$$

### Thin bar solution (W << L)
$$\Delta p(x) \approx \Delta p(0)\left(1 - \frac{x}{W}\right)$$

---

## Recombination Rates

### SRH (Trap-assisted)
$$R_{SRH} = \frac{np - n_i^2}{\tau_p(n + n_1) + \tau_n(p + p_1)}$$

### Low-Level Injection (N-type)
$$R = \frac{\Delta p}{\tau_p}$$

### Auger Recombination
$$R_{Aug} = C_n n^2 p + C_p p^2 n$$

### Radiative
$$R_{rad} = B np$$

---

## Generation Rate

### Thermal Generation
$$G = \frac{n_i}{\tau_g}$$

### In Depletion Region
$$G = \frac{n_i}{2\tau}$$

### Optical Generation
$$G = \frac{\alpha P}{\hbar c} = \frac{\alpha P \lambda}{hc}$$

---

## PN Junction Current (Diffusion Based)

### Forward Current
$$I = I_s \left[\exp\left(\frac{V}{V_T}\right) - 1\right]$$

### Reverse Saturation Current
$$I_s = qA\left(\frac{D_p p_{n0}}{L_p} + \frac{D_n n_{p0}}{L_n}\right)$$

$$I_s = \frac{qA D_p n_i^2}{L_p N_D} + \frac{qA D_n n_i^2}{L_n N_A}$$

---

## ISRO Quick Reference

### Drift
1. Jdrift = σE
2. Jn = qnμnE
3. Jp = qpμpE

### Diffusion
1. Jn = qDn(dn/dx)
2. Jp = -qDp(dp/dx)

### Einstein
1. D/μ = VT = 26 mV
2. Dn = μnVT

### Continuity
1. ∂n/∂t = (1/q)∂Jn/∂x + G - R

### Minority Carriers
1. Δp(x) = Δp(0)exp(-x/Lp)
2. L = √(Dτ)
3. J = qDΔp(0)/L
