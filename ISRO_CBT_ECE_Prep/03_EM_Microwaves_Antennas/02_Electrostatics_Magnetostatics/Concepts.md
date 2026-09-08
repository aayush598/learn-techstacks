# Electrostatics & Magnetostatics - Concepts

## Electrostatics Fundamentals

### Electric Charge & Coulomb's Law
- **Charge quantization**: Q = ne (n = integer, e = 1.6 × 10⁻¹⁹ C)
- **Conservation of charge**: Total charge in isolated system is constant
- **Coulomb's Law**: Force between two point charges ∝ q₁q₂/r²
- Force is attractive for unlike charges, repulsive for like charges
- Medium dependence: Force reduced by factor εᵣ in dielectric

### Electric Field Intensity (E)
- **Definition**: Force per unit positive test charge
- **Point charge**: E = Q/(4πε₀r²) âᵣ
- **Line charge**: E = ρₗ/(2πε₀ρ) âᵨ
- **Surface charge**: E = ρₛ/(2ε₀) âₙ
- **Volume charge**: E = ρᵥ/(3ε₀) r̂ (sphere)
- **Superposition principle**: E_total = Σ E_i (vector sum)

### Electric Flux & Gauss's Law
- **Electric flux**: ψ = ∮ E·dS (total flux through closed surface)
- **Gauss's Law**: ψ = Q_enclosed/ε₀
- Always valid but useful for symmetric charge distributions
- **Applications**: Infinite line, sheet, sphere, coaxial cable
- **Divergence form**: ∇·D = ρᵥ (point form of Gauss's law)

### Electric Potential & Energy
- **Potential difference**: V_AB = -∫ₐᴮ E·dl
- **Potential of point charge**: V = Q/(4πε₀r)
- **Relationship**: E = -∇V (gradient relationship)
- **Energy stored**: W = ½CV² = ½QV = ½Q²/C
- **Energy density**: w_e = ½ε|E|² = ½D·E

### Conductors in Electrostatic Equilibrium
- **E = 0** inside conductor
- All charge resides on surface
- E is perpendicular to surface (âₙ direction)
- **Surface charge density**: ρₛ = ε₀E_n
- **Equipotential surface**: V = constant inside and on surface

### Dielectric Materials
- **Polarization**: P = ε₀χₑE (induced dipole moment)
- **D = ε₀E + P = ε₀(1+χₑ)E = εE**
- **Relative permittivity**: εᵣ = 1 + χₑ = ε/ε₀
- **Boundary conditions**: D₁ₙ - D₂ₙ = ρₛ, E₁ₜ = E₂ₜ
- Lossless dielectrics: σ = 0, lossy: σ ≠ 0

### Capacitance
- **Definition**: C = Q/V
- **Parallel plate**: C = εA/d
- **Coaxial cable**: C = 2πεL/ln(b/a)
- **Spherical**: C = 4πε(ab)/(b-a)
- **Capacitors in parallel**: C_total = C₁ + C₂ + ...
- **Capacitors in series**: 1/C_total = 1/C₁ + 1/C₂ + ...

---

## Magnetostatics Fundamentals

### Magnetic Flux Density (B)
- **Biot-Savart Law**: dB = (μ₀/4π)(I dl × âᵣ)/r²
- **Infinite wire**: B = μ₀I/(2πρ) â𝜙
- **Solenoid**: B = μ₀nI (inside), n = turns/meter
- **Toroid**: B = μ₀NI/(2πρ) (inside)

### Ampere's Circuital Law
- **Integral form**: ∮ H·dl = I_enclosed
- **Differential form**: ∇ × H = J (point form)
- Equivalent to Biot-Savart for magnetostatics
- **Applications**: Infinite wire, solenoid, toroid, coaxial cable

### Magnetic Flux & Inductance
- **Magnetic flux**: Φ = ∫ B·dS
- **Inductance definition**: L = λ/I = NΦ/I
- **Solenoid**: L = μ₀N²A/l
- **Coaxial cable**: L = (μ₀l/2π)ln(b/a)
- **Series inductors**: L_total = L₁ + L₂ + ...
- **Parallel inductors**: 1/L_total = 1/L₁ + 1/L₂ + ...

### Magnetic Boundary Conditions
- **B normal**: B₁ₙ = B₂ₙ (continuous)
- **H tangential**: H₁ₜ - H₂ₜ = K (surface current)
- **Refractive index**: tan θ₁/tan θ₂ = μ₁/μ₂

### Magnetic Materials
- **Diamagnetic**: χₘ < 0 (weak repulsion)
- **Paramagnetic**: χₘ > 0 (weak attraction)
- **Ferromagnetic**: χₘ >> 0 (strong, nonlinear)
- **Hysteresis**: B-H curve shows energy loss per cycle
- **Remanence**: B remaining after H = 0
- **Coercivity**: H required to reduce B to 0

### Force on Current & Charge
- **Lorentz force**: F = qv × B
- **Force on wire**: F = I∫ dl × B
- **Hall effect**: V_H = BI/(nqb) (measures carrier density)

### Maxwell's Correction (Bridge to EM Waves)
- **Problem**: ∇ × H = J fails for time-varying fields
- **Displacement current**: J_d = ∂D/∂t
- **Ampere-Maxwell law**: ∇ × H = J + ∂D/∂t
- Enables prediction of EM wave propagation

---

## Key Relationships Summary
| Quantity | Electrostatics | Magnetostatics |
|----------|---------------|----------------|
| Field | E | B, H |
| Source | ρᵥ, ρₛ | J, K |
| Gauss's Law | ∇·D = ρᵥ | ∇·B = 0 |
| Curl Law | ∇×E = 0 | ∇×H = J |
| Energy | ½ε|E|² | ½μ|H|² |
| Boundary | E₁ₜ=E₂ₜ, D₁ₙ-D₂ₙ=ρₛ | H₁ₜ-H₂ₜ=K, B₁ₙ=B₂ₙ |
