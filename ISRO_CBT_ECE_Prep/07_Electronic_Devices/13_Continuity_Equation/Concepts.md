# Continuity Equation - Concepts

## Physical Foundation

### Basic Principle
- Conservation of carriers
- Carriers can be created (generation) or destroyed (recombination)
- Carriers can flow in/out (current divergence)

### Rate Balance
```
Rate of change of carrier density =
    (Inflow - Outflow) + Generation - Recombination
```

---

## Derivation

### Consider a Volume Element
- Volume: A·dx
- Change in carriers = inflow - outflow + generated - recombined

### For Holes
$$\frac{\partial p}{\partial t} = -\frac{1}{q}\frac{\partial J_p}{\partial x} + G_p - R_p$$

### For Electrons
$$\frac{\partial n}{\partial t} = \frac{1}{q}\frac{\partial J_n}{\partial x} + G_n - R_n$$

---

## Full Continuity Equation

### With Drift, Diffusion, Generation, Recombination
$$\frac{\partial p}{\partial t} = D_p \frac{\partial^2 p}{\partial x^2} - \mu_p E \frac{\partial p}{\partial x} - \mu_p p \frac{\partial E}{\partial x} + G - \frac{\Delta p}{\tau_p}$$

### Assumptions
- Uniform temperature
- 1D transport
- Low-level injection (τ constant)

---

## Special Cases

### Case 1: Steady State (∂p/∂t = 0)
$$D_p \frac{\partial^2 \Delta p}{\partial x^2} = \frac{\Delta p}{\tau_p}$$

### Case 2: No Field (Pure Diffusion)
$$\frac{\partial \Delta p}{\partial t} = D_p \frac{\partial^2 \Delta p}{\partial x^2} - \frac{\Delta p}{\tau_p}$$

### Case 3: Uniform Illumination (G constant)
At steady state: Δp = G·τ

### Case 4: After Removing Source
$$\frac{d\Delta p}{dt} = -\frac{\Delta p}{\tau}$$
Solution: Δp(t) = Δp(0)·exp(-t/τ)

---

## Minority Carrier Diffusion Equation

### For Holes in N-type
$$D_p \frac{d^2 \Delta p}{dx^2} - \frac{\Delta p}{\tau_p} + G = 0$$

### General Solution
$$\Delta p(x) = A \exp\left(-\frac{x}{L_p}\right) + B \exp\left(\frac{x}{L_p}\right) + \tau_p G$$

Where Lp = √(Dpτp)

---

## Steady-State Solutions

### Semi-Infinite Sample (No Generation)
$$\Delta p(x) = \Delta p(0) \exp\left(-\frac{x}{L_p}\right)$$

### Finite Sample
$$\Delta p(x) = \Delta p(0) \frac{\sinh\left(\frac{W - x}{L_p}\right)}{\sinh\left(\frac{W}{L_p}\right)}$$

### Thin Sample (W << Lp)
$$\Delta p(x) \approx \Delta p(0)\left(1 - \frac{x}{W}\right)$$ (linear)

---

## Minority Carrier Diffusion Current

### At Injection Point
$$J_p(0) = \frac{q D_p \Delta p(0)}{L_p}$$

### For Finite Sample
$$J_p(0) = \frac{q D_p \Delta p(0)}{L_p}\coth\left(\frac{W}{L_p}\right)$$

---

## Surface Recombination

### Boundary Condition
At surface (x = W):
$$D_p \frac{d\Delta p}{dx}\bigg|_{x=W} = -s \Delta p(W)$$

Where s = surface recombination velocity

### Effect
- Surface recombination reduces effective lifetime
- Lowers excess carrier concentration at surface

---

## Recombination Lifetime

### Effective Lifetime
$$\frac{1}{\tau_{eff}} = \frac{1}{\tau_{bulk}} + \frac{1}{\tau_{surface}}$$

### Surface Lifetime
$$\tau_s = \frac{W}{2s}$$ (for thin sample)

### Diffusion Length Reduction
$$L_{eff} = \sqrt{D \tau_{eff}}$$

---

## ISRO Key Points
- Continuity: ∂p/∂t = -(1/q)∂Jp/∂x + G - R
- Steady state: diffusion = recombination
- Δp(x) = Δp(0)exp(-x/L)
- After source removal: Δp decays exponentially with τ
- Recombination: R = Δp/τ
- Generation: G uniform → Δp = Gτ
- Surface recombination velocity affects lifetime
