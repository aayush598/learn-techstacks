# Pressure and Flow Transducers - Concepts

## 1. Pressure Measurement

### 1.1 Bourdon Tube
- C-shaped hollow tube with elliptical cross-section
- One end fixed (pressure inlet), other end free (connected to pointer)
- Pressure causes tube to straighten → mechanical displacement
- Types: C-type,螺旋 (spiral), helical
- Range: 0-7000 bar
- Simple, reliable, low cost
- Used in industrial pressure gauges

### 1.2 Piezoelectric Transducer
- Produces charge when stressed (crystal: quartz, PZT)
- Charge q = d × F, where d = piezoelectric coefficient
- Output: q = d × P × A (charge proportional to pressure)
- ONLY for dynamic pressure (cannot measure static)
- Very fast response (μs range)
- Used for: blast pressure, combustion, vibration

### 1.3 Capacitive Pressure Sensor
- Parallel plate capacitor with one flexible diaphragm
- Pressure changes gap → capacitance changes
```
C = εA/d, ΔC due to pressure
```
- High sensitivity, good linearity
- Used in: MEMS pressure sensors, industrial transmitters

### 1.4 Strain Gauge Pressure Sensor
- Strain gauge bonded to diaphragm
- Pressure → diaphragm strain → resistance change
- Used in: load cells, industrial transmitters

## 2. Flow Measurement

### 2.1 Venturi Meter
- Converging section → throat → diverging section
- Based on Bernoulli's principle
- Pressure decreases at throat (higher velocity)
```
Q = C_d × A_t × √[2(P₁-P₂)/ρ(1-β⁴)]
β = d/D (throat to pipe diameter ratio)
```
- Low pressure loss (recovery in diverging section)
- Accuracy: ±0.5-1%
- β typically 0.3-0.75

### 2.2 Orifice Plate
- Plate with a hole, placed in pipe
- Creates pressure drop proportional to flow
```
Q = C_d × A_o × √[2(P₁-P₂)/ρ]
```
- Simple, low cost
- High pressure loss (no recovery)
- β typically 0.2-0.7
- C_d depends on β and Reynolds number

### 2.3 Pitot Tube
- Measures local velocity at a point
- Stagnation pressure at tip vs static pressure
```
v = √[2(P_stag - P_static)/ρ] = √[2ΔP/ρ]
```
- Used for: airspeed, flow profiling
- Not for average flow (point measurement only)

### 2.4 Rotameter (Variable Area)
- Float in tapered tube
- Flow lifts float until drag = weight
- Linear relationship: Q ∝ h (float height)
- Simple, direct reading

## 3. Bernoulli's Principle
```
P₁ + ½ρv₁² + ρgh₁ = P₂ + ½ρv₂² + ρgh₂

For horizontal flow (h₁ = h₂):
P₁ + ½ρv₁² = P₂ + ½ρv₂²
```

## 4. Continuity Equation
```
A₁v₁ = A₂v₂ = Q (volume flow rate)
```

## 5. Comparison of Flow Meters
| Type | Pressure Loss | Accuracy | Cost | Range |
|------|---------------|----------|------|-------|
| Venturi | Low | ±0.5-1% | High | Large |
| Orifice | High | ±1-2% | Low | Medium |
| Pitot | Very low | ±1-2% | Low | Point |
| Rotameter | Medium | ±2-5% | Low | Small |

## 6. Differential Pressure
All differential pressure flow meters (Venturi, orifice) measure ΔP.
Flow is proportional to √ΔP (square root relationship).

## 7. Reynolds Number
```
Re = ρvD/μ

Laminar: Re < 2300
Transition: 2300 < Re < 4000
Turbulent: Re > 4000

Flow meter accuracy depends on Re
```

## 8. ISRO Focus Areas
- Venturi meter discharge equation
- Pitot tube velocity measurement
- Piezoelectric transducer (dynamic only)
- Capacitive pressure sensor principle
- Orifice vs Venturi pressure loss
