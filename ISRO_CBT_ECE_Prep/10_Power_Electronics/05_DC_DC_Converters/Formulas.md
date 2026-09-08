# DC-DC Converters - Formulas

## 1. Buck Converter Formulas

### Output Voltage (CCM)
```
Vo = D × Vin
Vo/Vin = D
D = ton/T = ton × fsw
```

### Inductor Current
```
IL(avg) = Io = Vo/RL
ΔIL = (Vin - Vo) × ton / L = (Vin - Vo) × D / (Lfsw)
IL(peak) = Io + ΔIL/2
IL(min) = Io - ΔIL/2
```

### Output Voltage Ripple
```
ΔVo = ΔIL/(8fswC)   [with LC filter]
ΔVo = (1-D) × Vin/(8L × C × fsw²)
ΔVo(%) = ΔVo/Vo × 100%
```

### Component Stresses
```
Switch:
  Vpeak = Vin
  Ipeak = Io + ΔIL/2

Diode:
  Vpeak = Vin (when switch ON)
  Ipeak = Io + ΔIL/2 (when switch OFF)

Inductor:
  Lmin = (1-D) × Vin/(fsw × ΔIL)
  
Capacitor:
  Cmin = (1-D)/(8 × L × fsw² × (ΔVo/Vo))
```

### Critical Inductance (CCM/DCM boundary)
```
LC = (1-D) × R/(2fsw)

Or:
Io(critical) = (Vin × D × (1-D)²)/(2Lfsw)
```

## 2. Boost Converter Formulas

### Output Voltage (CCM)
```
Vo = Vin/(1-D)
Vo/Vin = 1/(1-D)
D = 1 - Vin/Vo
```

### Inductor Current
```
IL(avg) = Io/(1-D) = Io × Vo/Vin   [power balance]
ΔIL = Vin × D / (Lfsw)
IL(peak) = IL(avg) + ΔIL/2
```

### Output Voltage Ripple
```
ΔVo = Io × D / (C × fsw)
ΔVo(%) = D/(RL × C × fsw) × 100%
```

### Component Stresses
```
Switch:
  Vpeak = Vo
  Ipeak = IL(avg) + ΔIL/2

Diode:
  Vpeak = Vo (when switch ON)
  Ipeak = IL(avg) + ΔIL/2

Inductor:
  Lmin = Vin × D / (fsw × ΔIL)
```

### Critical Inductance
```
LC = D × (1-D)² × R/(2fsw)

Or:
Io(critical) = (Vin × D × (1-D)²)/(2Lfsw)
```

## 3. Buck-Boost Converter Formulas

### Output Voltage (CCM, magnitude)
```
Vo/Vin = D/(1-D)
Vo = Vin × D/(1-D)

D = Vo/(Vo + Vin)
```

### Inductor Current
```
IL(avg) = Io/(1-D)   [for inverting buck-boost]
ΔIL = Vin × D / (Lfsw)
```

### Output Voltage Ripple
```
ΔVo = Io × D / (C × fsw)
ΔVo(%) = D/(RL × C × fsw) × 100%
```

### Component Stresses
```
Switch:
  Vpeak = Vin + Vo (series combination)
  Ipeak = IL(avg) + ΔIL/2

Diode:
  Vpeak = Vin + Vo
  Ipeak = Io
```

### Critical Inductance
```
LC = (1-D)² × R/(2fsw)
```

## 4. Flyback Converter Formulas

### Output Voltage (CCM)
```
Vo = Vin × (N2/N1) × D/(1-D)

Vo/Vin = (N2/N1) × D/(1-D)

For isolation with N2/N1 = 1:
Vo/Vin = D/(1-D)  [same as buck-boost]
```

### Inductor (Magnetizing) Current
```
IL(avg) = Io × (N1/N2) / (1-D)   [referred to primary]
ΔIL = Vin × D / (Lm × fsw)
```

### Output Voltage Ripple
```
ΔVo = Io × D / (C × fsw)   [same as buck-boost]
```

### Transformer Design
```
Lm = Vin² × D² / (2 × Pin × fsw)   [for DCM operation]

Or:
Lm = (Vin × D)² / (2 × Pin × fsw)
```

### Component Stresses
```
Primary switch:
  Vpeak = Vin + Vo × (N1/N2)   [reflected voltage]
  Ipeak = IL(avg) + ΔIL/2

Secondary diode:
  Vpeak = Vo + Vin × (N2/N1)
  Ipeak = Io
```

## 5. Cuk Converter Formulas

### Output Voltage (CCM)
```
Vo/Vin = D/(1-D)   [magnitude, inverted]

With isolation:
Vo = Vin × (N2/N1) × D/(1-D)
```

### Inductor Currents
```
IL1(avg) = Io/(1-D)   [input inductor]
IL2(avg) = Io           [output inductor]

ΔIL1 = Vin × D / (L1 × fsw)
ΔIL2 = Vo × (1-D) / (L2 × fsw)
```

### Output Voltage Ripple
```
ΔVo = Io × D / (C2 × fsw)   [output capacitor]
ΔVo(%) = D/(RL × C2 × fsw) × 100%
```

### Coupling Capacitor
```
ΔVc1 = Io × D / (C1 × fsw)   [voltage ripple]
Vc1(avg) = Vin + Vo   [voltage across C1]
```

## 6. CCM/DCM Boundary Formulas

### For Buck Converter
```
Io(critical) = (1-D) × Vin/(2Lfsw)

If Io > Io(critical) → CCM
If Io < Io(critical) → DCM
```

### For Boost Converter
```
Io(critical) = D × (1-D)² × Vin/(2Lfsw)

Maximum Io(critical) at D = 1/3
```

### For Buck-Boost Converter
```
Io(critical) = (1-D)² × Vin/(2Lfsw)

Or:
LC = (1-D)² × R/(2fsw)
```

### DCM Output Voltage (Buck)
```
Vo = Vin × D² / (D² + (8Lfsw)/(R))   [approximate]

For RL >> 8Lfsw:
Vo ≈ D × Vin   [approaches CCM formula]
```

## 7. Efficiency Formulas

### Conduction Losses
```
Pcond = I²Rds(on) × D   [MOSFET]
Pcond = Vf × Io × (1-D)   [diode]
Pcond = Io² × Rdc   [inductor DC resistance]
```

### Switching Losses
```
Psw = 0.5 × Vin × Ipeak × (tON + tOFF) × fsw
```

### Total Efficiency
```
η = Po/(Po + Ploss)
η = Po/(Po + Pcond + Psw + Pcore)

Typical efficiencies:
Buck: 90-95%
Boost: 90-95%
Flyback: 80-85%
Buck-Boost: 85-90%
```

## 8. Component Selection Formulas

### Inductor Selection
```
L = Vin × D × (1-D) / (ΔIL × fsw)   [Buck]
L = Vin × D / (ΔIL × fsw)           [Boost]
L = Vin × D / (ΔIL × fsw)           [Buck-Boost]

Rule of thumb: ΔIL = 0.2-0.4 × Io for good performance
```

### Capacitor Selection
```
C = Io × D / (ΔVo × fsw)            [Boost, Buck-Boost]
C = (1-D) / (8 × L × fsw² × ΔVo/Vo) [Buck]

ESR contribution: ΔVo(ESR) = ΔIL × ESR
Total ripple: ΔVo = √(ΔVo(cap)² + ΔVo(ESR)²)
```

### MOSFET Selection
```
VDS(max) ≥ Vin (Buck) or Vo (Boost) or Vin+Vo (Buck-Boost)
ID(max) ≥ Ipeak
Rds(on) selected for: Pcond = I²Rds(on) × D < Pbudget
```

### Diode Selection
```
For buck: VRRM ≥ Vin, IF ≥ Io
For boost: VRRM ≥ Vo, IF ≥ Io
For buck-boost: VRRM ≥ Vin+Vo, IF ≥ Io

Fast recovery diode preferred for CCM operation
Schottky for low voltage (<100V)
```
