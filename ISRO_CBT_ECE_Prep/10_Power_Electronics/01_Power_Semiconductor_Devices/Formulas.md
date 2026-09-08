# Power Semiconductor Devices - Formulas

## 1. Power Diode Formulas

### Forward Voltage Drop
```
VF = VT × ln(IF/IS + 1)   [Shockley equation]
VT = kT/q = 26 mV at 300K
```

### Power Dissipation (Diode)
```
Pd = VF × IF(AV) + VRRM × IR(AV)
Pd ≈ VF × IF(AV)   [IR usually negligible]
```

### Reverse Recovery Time
```
trr = tA + tB
tA = time from zero crossing to peak reverse current
tB = time for reverse current to decay to 25% of IRR
```

### Reverse Recovery Charge
```
Qrr = ∫ i(t) dt  from t=0 to trr
Qrr ≈ 0.5 × IRR × trr  [triangular approximation]
```

### Softness Factor
```
S = tB / tA
S > 1: soft recovery (preferred)
S < 1: snap-off (avoid)
```

### Surge Current Rating
```
IFSM = √(2/C × ∫[0 to π/ω] i²(θ) dθ)   [for half-sine]
For single half-sine: I²t = (IFSM)² × tpulse / 2
```

## 2. Power MOSFET Formulas

### On-State Resistance
```
RDS(on) = Rch + Rdrift + Rsub + Rcontact
Rdrift ∝ BV^2.5 / μn × q × ND
```

### Drain Current (Saturation Region)
```
ID = (μn × Cox × W / 2L) × (VGS - Vth)²   [for VDS > VGS - Vth]
```

### Drain Current (Linear Region)
```
ID = μn × Cox × W/L × [(VGS - Vth) × VDS - VDS²/2]   [for VDS < VGS - Vth]
```

### Gate Charge
```
Qg = Qgs + Qgd + Qsw
Qgs = Cgs × ΔVgs
Qgd = Cgd × ΔVds
```

### Switching Losses
```
Psw = 0.5 × VDS × ID × (tON + tOFF) × fsw
Psw = EON × fsw + EOFF × fsw   [from datasheet energy curves]
```

### On-State Power Loss
```
Pcond = ID(RMS)² × RDS(on)   [for resistive load]
Pcond = ID(AV)² × RDS(on) + ID(RMS)² × RDS(on)  [general]
```

### Gate Drive Power
```
Pgate = Qg × VGS × fsw
```

### Body Diode Losses
```
Pbody = VF(body) × ID(body) × D × T   [D = duty, T = period]
```

### Voltage Rating Derating
```
Voperating ≤ 0.8 × VDS(max)   [20% margin for reliability]
```

## 3. IGBT Formulas

### On-State Voltage
```
VCE(sat) = VCE0 + IC × rCE   [linear approximation]
VCE0 ≈ 0.7-1.5V (offset voltage)
rCE = dynamic on-resistance
```

### Conduction Loss
```
Pcond = VCE(sat) × IC(AV)
Pcond = IC(RMS) × VCE(sat)   [for resistive load]
```

### Switching Losses
```
Psw = (EON + EOFF) × fsw
EON = ∫[0 to tON] vCE(t) × iC(t) dt
EOFF = ∫[0 to tOFF] vCE(t) × iC(t) dt
```

### Total Power Loss
```
Ptotal = Pcond + Psw + Pgate
Pgate ≈ Qg × VGE × fsw   [typically small]
```

### Current Rating Calculation
```
IC(max) = (Tj(max) - Ta) / [Rth(j-c) × (VCE(sat) + switching_loss_per_cycle)]
```

### Safe Operating Area
```
VCE × IC ≤ Pmax = (Tj(max) - Tc) / Rth(j-c)
```

## 4. Thermal Formulas

### Junction Temperature
```
Tj = Ta + Ptotal × Rth(j-a)
Tj = Tc + Ptotal × Rth(j-c)
Tj = Tj(max) - margin   [design target]
```

### Thermal Resistance
```
Rth(total) = Rth(j-c) + Rth(c-s) + Rth(s-a)   [series]
Rth(s-a) = 1 / (h × A)   [convection]
```

### Transient Thermal Impedance
```
Zth(j-c)(t) = Rth(j-c) × [1 - exp(-t/τth)]
τth = Rth × Cth   [thermal time constant]
```

### Heatsink Design
```
Rth(s-a) required = (Tj(max) - Ta) / Ptotal - Rth(j-c) - Rth(c-s)
Tc = Tj - Ptotal × Rth(j-c)
```

### Thermal Derating
```
Pallowed(Ta) = Pmax × (Tj(max) - Ta) / (Tj(max) - 25°C)
```

## 5. Device Selection Formulas

### MOSFET vs IGBT Crossover Frequency
```
f crossover: frequency where total losses are equal
Below crossover → IGBT preferred (lower conduction losses)
Above crossover → MOSFET preferred (lower switching losses)
Typical crossover: 20-100 kHz depending on voltage/current
```

### Conduction Loss Comparison
```
MOSFET: Pcond = ID² × RDS(on)
IGBT: Pcond = IC × VCE(sat)
Equal when: ID × RDS(on) = VCE(sat)
```

### Switching Loss Comparison
```
MOSFET: Psw = 0.5 × V × ID × (tON + tOFF) × fsw
IGBT: Psw = (EON + EOFF) × fsw
MOSFET advantage increases with frequency
```

## 6. Surge and Transient Ratings

### I²t Rating (Fusing Current)
```
I²t = (IFSM)² × t   [for fuse coordination]
For diode: I²t = IFSM² × t_p / 2   [half-sine]
```

### dv/dt Rating (MOSFET)
```
dv/dt (max) = 1 / (Rg × Cgd)   [approximately]
Exceeding causes spurious turn-on (Miller effect)
```

### di/dt Rating (IGBT)
```
di/dt (max) limited by:
1. Stray inductance: V = L × di/dt
2. Bond wire fusing
3. Current crowding
```

### Energy Rating
```
EAS = 0.5 × L × I² × (BV / (BV - VDD))   [MOSFET avalanche]
```

## 7. Useful Constants and Conversions

```
VT = kT/q = 25.85 mV at 300K (≈ 26 mV)
k = 1.381 × 10⁻²³ J/K (Boltzmann constant)
q = 1.602 × 10⁻¹⁹ C (electron charge)
1 mil = 25.4 μm
1 ohm-cm² = 10⁻⁴ ohm-m²
Tj(max) Si = 150°C typical, 175°C for automotive
Tj(max) SiC = 200°C+
Tj(max) GaN = 150-200°C
```

## 8. ISRO-Specific Formulas

```
Derating factor for space: 0.7-0.8 × rated values
Radiation TID effect on Vth: ΔVth ∝ Dose
SEE cross-section: σSEE = Nevents / Fluence
MTBF calculation: MTBF = 1 / (n × λ)   [n = number of devices, λ = failure rate]
```
