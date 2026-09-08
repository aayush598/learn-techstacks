# Strain Gauges - Concepts

## 1. Strain Gauge Overview
A strain gauge is a passive transducer that converts mechanical strain (deformation) into a change in electrical resistance.
Most commonly: metallic foil strain gauge bonded to a surface.

## 2. Gauge Factor (GF)
The fundamental parameter of a strain gauge.
```
GF = (ΔR/R) / ε

where:
ΔR/R = fractional change in resistance
ε = strain (dimensionless, mm/mm or με = microstrain)
```

### 2.1 Typical Values
- Metallic foil: GF = 2.0 to 2.1
- Semiconductor: GF = 100 to 200

### 2.2 Physical Basis
```
GF = 1 + 2ν + (Δρ/ρ)/ε

where:
ν = Poisson's ratio (~0.3 for metals)
Δρ/ρ = change in resistivity with strain

For metals: GF ≈ 1 + 2ν ≈ 2 (dominated by dimensional change)
For semiconductors: GF dominated by piezoresistive effect (Δρ/ρ)
```

## 3. Strain Measurement Circuit

### 3.1 Wheatstone Bridge
- Single gauge in one arm of Wheatstone bridge
- Small resistance change → small bridge unbalance → measurable voltage

### 3.2 Quarter Bridge
One active gauge, three fixed resistors.
```
V_out = (V_s/4) × (ΔR/R) = (V_s/4) × GF × ε
```

### 3.3 Half Bridge
Two active gauges (one in tension, one in compression).
Doubles sensitivity, provides temperature compensation.

### 3.4 Full Bridge
Four active gauges. Maximum sensitivity (4× quarter bridge).
Common in load cells and pressure transducers.

## 4. Temperature Compensation

### 4.1 Problem
Temperature changes cause:
- Resistance change in gauge (thermal expansion + TCR)
- Apparent strain even without mechanical strain

### 4.2 Dummy Gauge Method
- Place a second (dummy) gauge on unstrained material of same type
- Dummy gauge in adjacent bridge arm
- Temperature effects cancel: ΔR_temp/dummy = ΔR_temp/active
- Only mechanical strain produces output

### 4.3 Self-Temperature Compensation (STC)
- Gauges manufactured with specific alloy composition
- Coefficient of thermal expansion matched to specimen
- Reduces temperature error without dummy gauge

## 5. Bridge Configuration Effects
| Configuration | Gauge Arrangement | Output | Temp. Comp. |
|---------------|-------------------|--------|-------------|
| Quarter | 1 active | V_s/4 × GF × ε | No (needs dummy) |
| Half | 2 active (opposing) | V_s/2 × GF × ε | Yes |
| Full | 4 active | V_s × GF × ε | Yes |

## 6. Strain Gauge Materials
- Constantan (Cu-Ni): Most common, GF ≈ 2, good linearity
- Karma alloy: High temperature applications
- Nichrome: High temperature, high resistance
- Platinum: Very high temperature, precise

## 7. Gauge Resistance
- Standard nominal resistance: 120Ω, 350Ω, 1000Ω
- Higher resistance → less lead wire error, less heating
- 350Ω most common in precision applications

## 8. Bonding
- Adhesive bonding (cyanoacrylate, epoxy)
- Surface preparation critical
- Gauge must perfectly follow specimen strain
- Gauge length affects spatial resolution

## 9. Applications
- Structural health monitoring (bridges, buildings)
- Load cells (force/weight measurement)
- Pressure transducers
- Torque measurement
- Accelerometers
- Aerospace structural testing (ISRO relevant)

## 10. Key Parameters
| Parameter | Value |
|-----------|-------|
| Gauge factor | 2.0 (typical) |
| Nominal resistance | 120Ω or 350Ω |
| Strain range | ±0.1% (1000 με) |
| Temperature range | -200°C to +800°C |
| Linearity | ±0.5% |

## 11. ISRO Focus Areas
- Gauge factor calculation
- Bridge unbalance equation
- Dummy gauge temperature compensation
- Quarter bridge sensitivity
- GF physical meaning (ΔR/R)/ε
