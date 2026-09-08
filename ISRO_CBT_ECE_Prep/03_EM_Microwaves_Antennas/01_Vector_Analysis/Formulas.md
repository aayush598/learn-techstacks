# Vector Analysis - Formulas

## Coordinate Transformations

### Cartesian ↔ Cylindrical
- x = ρ cos φ, y = ρ sin φ, z = z
- ρ = √(x² + y²), φ = tan⁻¹(y/x)
- Volume element: dV = ρ dρ dφ dz
- Differential length: dl = dρ âρ + ρ dφ âφ + dz âz

### Cartesian ↔ Spherical
- x = r sin θ cos φ
- y = r sin θ sin φ
- z = r cos θ
- r = √(x² + y² + z²)
- θ = tan⁻¹(√(x²+y²)/z)  [polar angle from z-axis]
- φ = tan⁻¹(y/x)
- Volume element: dV = r² sin θ dr dθ dφ

### Unit Vector Transformations (Cylindrical)
- âρ = cos φ âx + sin φ ây
- âφ = -sin φ âx + cos φ ây
- âx = cos φ âρ - sin φ âφ
- ây = sin φ âρ + cos φ âφ

### Unit Vector Transformations (Spherical)
- âr = sin θ cos φ âx + sin θ sin φ ây + cos θ âz
- âθ = cos θ cos φ âx + cos θ sin φ ây - sin θ âz
- âφ = -sin φ âx + cos φ ây

## Differential Elements (Cartesian)
- dl = dx âx + dy ây + dz âz
- dS (xy-plane) = dx dy, dS (yz) = dy dz, dS (xz) = dx dz
- dV = dx dy dz

## Del Operator ∇

### Cartesian
∇ = âx ∂/∂x + ây ∂/∂y + âz ∂/∂z

### Cylindrical
∇ = âρ ∂/∂ρ + âφ (1/ρ)∂/∂φ + âz ∂/∂z

### Spherical
∇ = âr ∂/∂r + âθ (1/r)∂/∂θ + âφ (1/(r sin θ))∂/∂φ

## Gradient (∇V) - Result: Scalar → Vector

### Cartesian
∇V = (∂V/∂x)âx + (∂V/∂y)ây + (∂V/∂z)âz

### Cylindrical
∇V = (∂V/∂ρ)âρ + (1/ρ)(∂V/∂φ)âφ + (∂V/∂z)âz

### Spherical
∇V = (∂V/∂r)âr + (1/r)(∂V/∂θ)âθ + (1/(r sin θ))(∂V/∂φ)âφ

### Property
- Direction of max increase
- Magnitude = max rate of change
- Curl(∇V) = 0

## Divergence (∇·A) - Result: Vector → Scalar

### Cartesian
∇·A = ∂Ax/∂x + ∂Ay/∂y + ∂Az/∂z

### Cylindrical
∇·A = (1/ρ) ∂(ρAρ)/∂ρ + (1/ρ)∂Aφ/∂φ + ∂Az/∂z

### Spherical
∇·A = (1/r²)∂(r²Ar)/∂r + (1/(r sin θ))∂(Aθ sin θ)/∂θ + (1/(r sin θ))∂Aφ/∂φ

## Curl (∇×A) - Result: Vector → Vector

### Cartesian
∇×A = âx(∂Az/∂y - ∂Ay/∂z) + ây(∂Ax/∂z - ∂Az/∂x) + âz(∂Ay/∂x - ∂Ax/∂y)

### Cylindrical
∇×A = âρ[(1/ρ)∂Az/∂φ - ∂Aφ/∂z] + âφ[∂Aρ/∂z - ∂Az/∂ρ]
     + âz[(1/ρ)∂(ρAφ)/∂ρ - (1/ρ)∂Aρ/∂φ]

### Spherical
∇×A = âr[(1/(r sin θ))(∂(Aφ sin θ)/∂θ - ∂Aθ/∂φ)]
     + âθ[(1/(r sin θ))∂Ar/∂φ - (1/r)∂(rAφ)/∂r]
     + âφ[(1/r)(∂(rAθ)/∂r - ∂Ar/∂θ)]

## Laplacian (∇²)

### Cartesian (scalar)
∇²V = ∂²V/∂x² + ∂²V/∂y² + ∂²V/∂z²

### Cylindrical (scalar)
∇²V = (1/ρ)∂/∂ρ(ρ ∂V/∂ρ) + (1/ρ²)∂²V/∂φ² + ∂²V/∂z²

### Spherical (scalar)
∇²V = (1/r²)∂/∂r(r² ∂V/∂r) + (1/(r² sin θ))∂/∂θ(sin θ ∂V/∂θ)
     + (1/(r² sin² θ))∂²V/∂φ²

### Laplacian of Vector (Cartesian only - simple form)
∇²A = âx∇²Ax + ây∇²Ay + âz∇²Az

### For spherically symmetric (only r-dependence):
∇²V = (1/r²)∂/∂r(r² ∂V/∂r) = (1/r)∂²(rV)/∂r²

## Important Vector Identities

1. ∇·(∇×A) = 0
2. ∇×(∇V) = 0
3. ∇×(∇×A) = ∇(∇·A) - ∇²A
4. ∇·(fA) = f(∇·A) + A·(∇f)
5. ∇×(fA) = f(∇×A) + (∇f)×A
6. ∇·(A×B) = B·(∇×A) - A·(∇×B)
7. ∇(f·g) = f∇g + g∇f
8. A×(B×C) = B(A·C) - C(A·B)  [BAC-CAB rule]
9. A·(B×C) = B·(C×A) = C·(A×B)  [scalar triple product]

## Theorems

### Stokes Theorem
∮C A·dl = ∫∫S (∇×A)·dS

### Gauss Divergence Theorem
∮S A·dS = ∭V (∇·A) dV

### Green's Theorem (special case of Stokes)
∮(P dx + Q dy) = ∫∫(∂Q/∂x - ∂P/∂y) dx dy

## Application Formulas (EM links)

### Electric Field from Potential
E = -∇V

### Gauss's Law (Differential)
∇·D = ρv

### Gauss's Law (Integral)
∮S D·dS = Qenc

### Faraday's Law (Differential)
∇×E = -∂B/∂t

### Ampere's Law (Differential)
∇×H = J + ∂D/∂t

### Gauss's Law for Magnetism
∇·B = 0

### Continuity Equation (Charge Conservation)
∇·J = -∂ρv/∂t

### Wave Equations
∇²E = με ∂²E/∂t²
∇²H = με ∂²H/∂t²

### Helmholtz (Time-Harmonic) Wave Equations
∇²E + ω²μεE = 0
∇²H + ω²μεH = 0

### Poisson's / Laplace's Equations
∇²V = -ρv/ε (Poisson)
∇²V = 0 (Laplace, source-free)

## ISRO Speed Formulas / Shortcuts

### Quick Divergence in Spherical for radial fields
If A = (f(r))âr (only r-component):
∇·A = (1/r²) d(r² f(r))/dr

Example: A = (1/r²)âr → ∇·A = (1/r²)d(r²·(1/r²))/dr = (1/r²)·d(1)/dr = 0
(This is why ∇·(âr/r²) = 0 except at origin - the Coulomb field is divergence-free away from origin!)

### Quick Curl in Spherical for radial fields
If A = f(r)âr: ∇×A = 0 (radial fields have no curl)

### Common Results to Commit to Memory
- ∇·r = 3 (where r = position vector = xâx + yây + zâz)
- ∇×r = 0
- ∇r = âr (gradient of magnitude of russian r) - for r = |position vector|
- ∇(1/r) = -âr/r²
- ∇²(1/r) = 0 for r ≠ 0
- ∇·(âr/r²) = 0 for r ≠ 0

### Laplacian shortcut for spherically symmetric scalar V(r)
∇²V = (1/r²)(d/dr)(r² dV/dr)

## Notations Used in Exams
- Sometimes ∇² written as Δ (Laplacian)
- ∇×A sometimes written as curl A or rot A or A
- ∇·A sometimes written as div A
- ∇V in some ISRO questions written as grad V

## Quick Reference Table

| Operator | Input | Output | EM Significance |
|----------|-------|--------|----------------|
| Gradient ∇V | Scalar | Vector | E = -∇V |
| Divergence ∇·A | Vector | Scalar | ∇·D = ρv |
| Curl ∇×A | Vector | Vector | ∇×E = -∂B/∂t |
| Laplacian ∇²V | Scalar | Scalar | Wave/potential eqn |
