# SCR Thyristors - Formulas

## 1. SCR Triggering Conditions

### Two-Transistor Analogy Current
```
IA = (α2 × IG + Ico1 + Ico2) / (1 - (α1 + α2))

Where:
IA = anode current
IG = gate current
α1, α2 = common-base current gains
Ico1, Ico2 = collector leakage currents
```

### Latching Condition
```
α1 + α2 = 1 (or IA → ∞)

Practical triggering occurs when:
α1 + α2 ≈ 0.97-0.99
```

## 2. SCR V-I Characteristics Equations

### Forward Leakage Current
```
IFWO = Ico / (1 - (α1 + α2))

Where:
Ico = reverse saturation current of J2
α = f(IA) → increases with current
```

### On-State Voltage
```
VAK(on) = VTM = 1-2V (typically)
VAK = VT0 + RT × IA   [linear approximation]
VT0 ≈ 0.8-1.2V (offset)
RT ≈ 1-10 mΩ (dynamic resistance)
```

### Power Dissipation (SCR)
```
PT = VTM × IT(AV) + VRRM × IR(AV)
PT = VT0 × IT(AV) + RT × IT(RMS)²
```

## 3. Firing Angle Formulas (Phase Control)

### Single-Phase Half-Wave Rectifier with SCR
```
Vdc = (Vm/2π) × (1 + cos α)

Where:
Vm = peak supply voltage
α = firing angle (0° to 180°)

At α = 0°: Vdc = Vm/π (maximum)
At α = 90°: Vdc = Vm/(2π)
At α = 180°: Vdc = 0
```

### Single-Phase Full-Wave (Center Tap) with SCR
```
Vdc = (Vm/π) × (1 + cos α)

Range: 0 to 2Vm/π
```

### Three-Phase Half-Wave Rectifier
```
Vdc = (3√3 × Vm/2π) × (1 + cos(α + 30°)) / 2

Simplified: Vdc = (3Vml/2π) × cos α   [for α ≤ 30°]
```

### Three-Phase Full-Wave (Bridge) Rectifier
```
Vdc = (3Vml/π) × cos α   [for α ≤ 60°]

Where Vml = line-to-line peak voltage

Vdc = (3√2 × VL(rms)/π) × cos α
```

## 4. RMS and Average Current Formulas

### Single-Phase Half-Wave SCR Rectifier
```
IT(RMS) = Vm/(2RL) × √((1/π)(π - α + sin(2α)/2))

IT(AV) = Vm/(2πRL) × (1 + cos α)
```

### Form Factor
```
FF = IT(RMS) / IT(AV)

Higher FF → more heating per ampere of DC current
Typical: 1.5-3 depending on firing angle
```

### Ripple Factor
```
RF = √(FF² - 1)
RF = √(Vrms²/Vdc² - 1)
```

### Efficiency (Rectification Ratio)
```
η = Pdc / Pac = Vdc × Idc / Vrms × Irms
η = (Vdc/Vrms) × (Idc/Irms)
```

## 5. Latching and Holding Current

### Latching Current (IL)
```
IL = minimum anode current to maintain turn-on
IL ≈ 2-3 × IH (typically)
IL must be exceeded before gate pulse is removed
For inductive loads: IL × L/(V - VAK) > pulse width
```

### Holding Current (IH)
```
IH = minimum anode current to maintain conduction
IH = IL / (2 to 3)
IH < IL always
SCR turns off when IA < IH
```

### Current to Maintain Conduction
```
For DC circuit to keep SCR ON:
IA > IH (always required)
If IA < IH → SCR turns OFF (natural commutation)
```

## 6. dv/dt and di/dt Formulas

### dv/dt Limiting (Snubber)
```
dv/dt = V/Cs   [across snubber capacitor]

Cs required: Cs ≥ Vpeak / (dv/dt)max

Typical:
Cs = 0.01-1 μF
Rs = 10-100Ω
```

### di/dt Limiting (Series Inductor)
```
di/dt = V/Ls   [through series inductor]

Ls required: Ls ≥ Vpeak / (di/dt)max

Typical:
Ls = 10-100 μH for high-power SCRs
```

### Snubber Discharge Current
```
Is discharge = VAK / Rs   [peak through SCR at turn-on]

Rs must limit this to: Is ≤ (di/dt)max × Cs
```

## 7. SCR Gate Trigger Formulas

### Gate Trigger Power
```
PG = VG × IG   [during triggering]
PGT: average gate trigger power (from datasheet)
VGT: gate trigger voltage (0.7-1.5V)
IGT: gate trigger current (10-500 mA, varies by device)
```

### Gate Pulse Requirements
```
Minimum pulse width: tw ≥ IL × L / (V - VAK)
For inductive loads: wider pulses needed
Gate pulse rise time: tr < 1 μs (typical)
```

### RC Firing Circuit
```
Firing angle α = cos⁻¹(-1/(ωRC))   [for resistance firing]
Actually: α = cos⁻¹((2Vc/Vm) - 1)   [more accurate]

For RC firing:
Vc = Vm × sin(ωt) × (1/(ωRC))
α range: 0° to 180° (limited by component values)
```

## 8. SCR Thermal Formulas

### Junction Temperature
```
Tj = Tc + PT × Rth(j-c)
Tj = Ta + PT × Rth(j-a)
Tj(max) = 125°C or 150°C (depending on type)
```

### Power Dissipation vs Firing Angle
```
PT(α) = IT(AV)(α) × VTM + IR(AV) × VRRM

For resistive load:
PT(α) = (Vm²/2RL) × (1/(2π)) × (π - α + sin(2α)/2) × VTM/Vm
```

### Derating
```
IT(AV)(α) = IT(AV)(α=0°) × K(α)

Where K(α) = derating factor based on conduction angle
Full conduction (α=0°): K=1
Half conduction (α=90°): K≈0.5-0.6
```

## 9. SCR Surge Ratings

### I²t Rating
```
I²t = ITSM² × tp   [for fuse coordination]
tp = surge duration (typically 8.3 ms for 60 Hz)
For 50 Hz: tp = 10 ms (half-cycle)
```

### Surge Current
```
ITSM: non-repetitive peak forward on-state current
ITSM = (Vpeak - VTM) / Rs   [limited by circuit resistance]
Recovery time between surges: typically 1 minute
```

### Energy Rating
```
E = ∫[0 to tp] p(t) dt = ∫[0 to tp] vAK(t) × iA(t) dt
E ≈ VTM × ITSM × tp / 2   [for half-sine pulse]
```

## 10. Useful Relationships

### Conduction Angle
```
γ = 180° - α   [for single-phase half-wave]
For full-wave: γ = 180° - α
```

### Power Factor (with SCR)
```
PF = (Vdc/Vrms) × (Idc/Irms) × cos φ

More accurately:
PF = cos α × distortion factor
```

### Total Harmonic Distortion (THD)
```
THD = √(Vrms² - V1²) / V1 × 100%

V1 = fundamental component of output voltage
Vrms = total RMS output voltage
```

### Firing Angle for Specific Vdc
```
α = cos⁻¹((π × Vdc/Vm) - 1)   [half-wave]
α = cos⁻¹((π × Vdc/(2Vm)) - 1)   [full-wave center tap]
```
