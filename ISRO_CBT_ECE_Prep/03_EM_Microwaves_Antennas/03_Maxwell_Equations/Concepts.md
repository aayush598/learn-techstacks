# Maxwell's Equations - Concepts

## Four Maxwell's Equations

### 1. Gauss's Law for Electric Fields (Differential)
```
div(D) = rho_v
Divergence of electric flux density = volume charge density
Integral: closed surface integral of D.dA = Q_enclosed
```

### 2. Gauss's Law for Magnetic Fields (Differential)
```
div(B) = 0
Divergence of magnetic flux density = zero
(No magnetic monopoles exist)
Integral: closed surface integral of B.dA = 0
```

### 3. Faraday's Law of Electromagnetic Induction
```
curl(E) = -dB/dt
Time-varying magnetic field creates electric field
Integral: line integral of E.dl = -d/dt(surface integral of B.dA)
```

### 4. Ampere-Maxwell Law
```
curl(H) = J + dD/dt
Magnetic field created by conduction current AND displacement current
Integral: line integral of H.dl = I_enclosed + d/dt(surface integral of D.dA)
```

---

## Displacement Current
- Term dD/dt added by Maxwell to Ampere's law
- Not actual current flow, but produces same magnetic field effect
- Essential for electromagnetic wave propagation
- Without it: inconsistent equations for time-varying fields

## Boundary Conditions
- At interface between two media:
  - Normal D: D1n - D2n = surface charge density
  - Tangential E: E1t = E2t (continuous)
  - Normal B: B1n = B2n (continuous)
  - Tangential H: H1t - H2t = surface current density

---

## ISRO Key Points
- Maxwell's equations unified electricity and magnetism
- dD/dt (displacement current) enables EM wave propagation
- Boundary conditions critical for plane wave problems
- In free space: J = 0, rho = 0 (simplified equations)
