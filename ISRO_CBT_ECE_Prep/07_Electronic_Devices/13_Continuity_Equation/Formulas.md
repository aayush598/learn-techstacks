# Continuity Equation - Formulas

## General Continuity Equations

### For Holes
$$\frac{\partial p}{\partial t} = -\frac{1}{q}\frac{\partial J_p}{\partial x} + G_p - R_p$$

### For Electrons
$$\frac{\partial n}{\partial t} = \frac{1}{q}\frac{\partial J_n}{\partial x} + G_n - R_n$$

---

## Full Form (1D)

### With Drift + Diffusion
$$\frac{\partial p}{\partial t} = D_p \frac{\partial^2 p}{\partial x^2} - \mu_p E \frac{\partial p}{\partial x} - \mu_p p \frac{\partial E}{\partial x} + G - \frac{\Delta p}{\tau_p}$$

### For Electrons (similar)
$$\frac{\partial n}{\partial t} = D_n \frac{\partial^2 n}{\partial x^2} + \mu_n E \frac{\partial n}{\partial x} + \mu_n n \frac{\partial E}{\partial x} + G - \frac{\Delta n}{\tau_n}$$

---

## Special Cases

### 1. Steady State (∂/∂t = 0)
For holes, no field, no generation:
$$D_p \frac{d^2 \Delta p}{dx^2} - \frac{\Delta p}{\tau_p} = 0$$

### 2. With Generation (uniform G)
$$D_p \frac{d^2 \Delta p}{dx^2} - \frac{\Delta p}{\tau_p} + G = 0$$

### 3. Transient, No Field, No Generation (uniform)
$$\frac{d\Delta p}{dt} = -\frac{\Delta p}{\tau_p}$$

---

## Solutions

### Uniform Case (Transient)
$$\Delta p(t) = \Delta p(0) \exp\left(-\frac{t}{\tau_p}\right)$$

### Semi-Infinite (Steady, No Generation)
$$\Delta p(x) = \Delta p(0) \exp\left(-\frac{x}{L_p}\right)$$

### Generation + Decay
$$\Delta p(x) = \tau_p G \left[1 - \exp\left(-\frac{x}{L_p}\right)\right]$$

### Finite Sample
$$\Delta p(x) = \Delta p(0) \frac{\sinh\left(\frac{W - x}{L_p}\right)}{\sinh\left(\frac{W}{L_p}\right)}$$

### Thin Sample (W << Lp)
$$\Delta p(x) \approx \Delta p(0)\left(1 - \frac{x}{W}\right)$$

---

## Diffusion Length

### Definition
$$L_p = \sqrt{D_p \tau_p}$$

$$L_n = \sqrt{D_n \tau_n}$$

### Using Einstein Relation
$$L = \sqrt{\mu V_T \tau}$$

---

## Current from Injection

### Semi-Infinite
$$J_p(0) = \frac{q D_p \Delta p(0)}{L_p}$$

### Finite Sample
$$J_p(0) = \frac{q D_p \Delta p(0)}{L_p}\coth\left(\frac{W}{L_p}\right)$$

### Collector Current (BJT relation)
$$I_C = qA \frac{D_n n_{p0}}{L_n}\left[\exp\left(\frac{V_{BE}}{V_T}\right) - 1\right]$$

---

## Recombination

### Recombination Rate
$$R = \frac{\Delta n}{\tau}$$

### SRH (traps at Et)
$$R_{SRH} = \frac{np - n_i^2}{\tau_p(n + n_1) + \tau_n(p + p_1)}$$

Where:
$$n_1 = n_i \exp\left(\frac{E_t - E_i}{kT}\right)$$
$$p_1 = n_i \exp\left(\frac{E_i - E_t}{kT}\right)$$

---

## Generation

### Thermal Generation
$$G = \frac{n_i}{\tau_g} = \frac{np - n_i^2}{\tau}$$

### Optical Generation Rate
$$G = \frac{\alpha P_{opt}}{A h\nu} = \frac{\alpha I_0 \lambda}{hc}$$

---

## Surface Recombination

### Boundary Condition
$$D_p \frac{d\Delta p}{dx}\bigg|_{x=W} = -s \Delta p(W)$$

### Effective Lifetime
$$\frac{1}{\tau_{eff}} = \frac{1}{\tau_{bulk}} + \frac{1}{\tau_{surface}}$$

### Surface Lifetime
$$\tau_{surface} = \frac{W}{2s}$$

### Boundary Value (short surface lifetime)
$$\Delta p(W) \approx 0$$

---

## Time Constants

### RC-related Decay
$$\tau = RC$$

### Minority Carrier Lifetime
$$\tau = \frac{\Delta p}{R}$$

### Relationship to Diffusion Length
$$\tau = \frac{L^2}{D}$$

---

## ISRO Quick Reference

### Continuity Equation
1. ∂p/∂t = -(1/q)∂Jp/∂x + G - R
2. ∂n/∂t = (1/q)∂Jn/∂x + G - R

### Steady State
1. Dp·d²Δp/dx² - Δp/τ = 0
2. Δp(x) = Δp(0)exp(-x/L)

### Transient
1. dΔp/dt = -Δp/τ
2. Δp(t) = Δp(0)exp(-t/τ)

### Key Relations
1. L = √(Dτ)
2. R = Δp/τ
3. G = Δp/τ (steady)
4. J = qD·Δp(0)/L
