# GTO, TRIAC, DIAC - Formulas

## 1. GTO Formulas

### Turn-Off Gain
```
βoff = IA / |IG(off)|

Typical βoff = 3-5
Higher βoff → less gate power needed for turn-off
βoff = IA / (IA × (1 - α1)) ≈ 1/(1 - α1)
```

### Gate Turn-Off Charge
```
QGO = Qds + Qdf + Qtail

Qds: stored charge during turn-on (major portion)
Qdf: charge during fall time
Qtail: charge during tail current
```

### Turn-Off Time
```
tq = ts + tf + ttail

ts: stored time (1-2 μs)
tf: fall time (0.5-2 μs)
ttail: tail current time (5-20 μs)
```

### Turn-Off Losses
```
PGOFF = QGO × VAK(avg) × fsw

More precisely:
EOFF = ∫[0 to tq] vAK(t) × iA(t) dt
Psw(off) = EOFF × fsw
```

### Gate Power Requirement
```
PG(total) = PG(on) + PG(off)

PG(on) = VGT × IGT × DON × T
PG(off) = |VG(off)| × |IG(off)| × (1-D) × T

Where:
DON = duty cycle during on-state
D = 1 - DON = fraction of off-state
```

### Anode Current Limiting
```
IA(max) = βoff × |IG(max)|

For βoff = 5 and IG = 500A:
IA(max) = 2500A
```

### Stored Charge Relationship
```
Qs = IA × τs   [stored charge]
τs = minority carrier lifetime in drift region
τs reduced by: gold doping, electron irradiation
```

## 2. TRIAC Formulas

### RMS Current (Phase Control)
```
IT(RMS) = Vm/(RL × √2) × √((1/π)(π - α + sin(2α)/2))

Where:
Vm = peak voltage
RL = load resistance
α = firing angle
```

### Average Current
```
IT(AV) = 0 (for full AC operation)

For half-cycle only:
IT(AV) = Vm/(2πRL) × (1 + cos α)
```

### Power Delivered to Load
```
PL = (Vm²/2RL) × (1/π) × (π - α + sin(2α)/2)

PL(α=0°) = Vm²/(2RL)  [maximum power]
PL(α=90°) = Vm²/(4RL)  [half power]
PL(α=180°) = 0  [no power]
```

### Power Dissipation in TRIAC
```
PT ≈ VTM × IT(RMS)²/IT(RMS)   [approximate]
PT = VTM × IT(AV)   [for resistive load, more accurate]

VTM = on-state voltage drop (1-2V)
```

### Gate Trigger Requirements
```
Quadrant I:   IGT = IGT1 (lowest, most sensitive)
Quadrant II:  IGT = IGT1/0.5 to IGT1/1
Quadrant III: IGT = IGT1
Quadrant IV:  IGT = IGT1/0.3 (highest, least sensitive)

VGT typically 0.7-1.5V for all quadrants
```

### dv/dt Limiting (Snubber)
```
Cs ≥ IT(RMS) × (dv/dt)max / Vpeak²   [approximate]

More accurately:
Cs required to limit dv/dt across TRIAC:
dv/dt = Vpeak/(RL × Cs)   [simplified]
```

### Phase Angle Calculation
```
α = cos⁻¹((π × Vdc/Vm) - 1)   [for half-wave]
α = cos⁻¹((π × Vdc/(2Vm)) - 1)   [for full-wave]

Where Vdc is desired average output voltage
```

## 3. DIAC Formulas

### Breakover Voltage
```
VBO = 20-60V (typically 32V)
VBO(positive) = VBO(negative)  [symmetric]
Tolerance: ±5% typical
```

### Switching Current
```
ITS = C × dV/dt at breakover   [approximately]
ITS determines minimum capacitor charge for triggering
```

### Capacitor Charge for TRIAC Triggering
```
Q = C × VBO(DIAC)

C × VBO = IT × t   [charge transfer to gate]

Where:
C = timing capacitor
VBO = DIAC breakover voltage
IT = gate trigger current of TRIAC
t = minimum pulse width
```

### Timing Capacitor Calculation
```
C = t / (R × ln(Vpeak/(Vpeak - VBO)))   [for RC charging]

Simplified:
C ≈ t / (R × ln(2))   [for Vpeak >> VBO]
C ≈ 1.44 × t / R   [approximate]
```

### Relaxation Oscillator Frequency
```
f ≈ 1 / (R × C × ln(1/(1-k)))

Where k = VBO/Vpeak (for Vpeak >> VBO)
k ≈ VBO/Vpeak
```

### TRIAC-DIAC Circuit Formulas
```
Firing angle α depends on RC time constant:
α = arccos(1 - VBO/Vm)   [simplified]

More accurately:
α = ω × RC × ln(Vm/(Vm - VBO))   [for RC circuit]
```

## 4. Comparison Formulas

### Conduction Loss Comparison
```
SCR:    Pcond = VTM × IT(AV)     [VTM ≈ 1-1.5V]
GTO:    Pcond = VTM × IT(AV)     [VTM ≈ 2-3V, higher than SCR]
TRIAC:  Pcond = VTM × IT(RMS)    [bidirectional]
DIAC:   Pcond = VBO(ON) × I      [VBO(ON) ≈ 1-2V]
```

### Switching Loss Comparison
```
SCR:    Psw ≈ 0 (natural commutation in AC)
GTO:    Psw = (EON + EOFF) × fsw  [EOFF significant]
TRIAC:  Psw = (EON + EOFF) × fsw  [bidirectional losses]
DIAC:   Psw ≈ 0 (used for triggering only)
```

### Gate Drive Power Comparison
```
SCR:    PG = VGT × IGT × DON     [low power]
GTO:    PG = PG(on) + PG(off)    [PG(off) can be significant]
TRIAC:  PG = VGT × IGT × DON     [low power]
DIAC:   PG = 0 (self-triggered)
```

## 5. Frequency Limitations

### GTO Maximum Frequency
```
fmax ≈ 1 / (2 × (tq + tg))

Where:
tq = turn-off time
tg = gate control time

For tq = 10 μs: fmax ≈ 50 kHz (theoretical)
Practical: 1-5 kHz for power GTOs
```

### TRIAC Maximum Frequency
```
fmax limited by:
1. Turn-on time: ton ≈ 1-5 μs
2. Turn-off time: toff ≈ 5-20 μs
3. dv/dt immunity

Practical: <1 kHz for power TRIACs
```

## 6. Useful Relationships

### Conduction Angle
```
γ = 180° - α   [for AC phase control]
Power delivered ∝ γ/180° approximately
```

### RMS vs Average for Phase Control
```
For resistive load:
Vrms = Vm × √((1/2π)(π - α + sin(2α)/2))
Vdc = Vm/(2π) × (1 + cos α)

Form Factor = Vrms/Vdc = varies with α
```

### Power Factor of TRIAC Circuit
```
PF = (Vdc/Vrms) × (Idc/Irms) × cos φ

For resistive load:
PF = √((π - α + sin(2α)/2) / (2π)) × (1 + cos α)/(π)
```

### Total Harmonic Distortion
```
THD = √(Vrms² - V1²) / V1 × 100%

For phase-controlled TRIAC:
THD increases with firing angle
At α = 90°: THD ≈ 48%
At α = 120°: THD ≈ 70%
```
