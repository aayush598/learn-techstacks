# SMPS and Linear Regulators - Formulas

## 1. Linear Regulator Formulas

### Efficiency
```
η = Po/Pin = Vo × Io / (Vin × Iin)
η ≈ Vo/Vin (for low quiescent current)
η(%) = (Vo/Vin) × 100%
```

### Power Dissipation
```
Pd = (Vin - Vo) × Io + Vin × Iq
Pd ≈ (Vin - Vo) × Io (if Iq << Io)
```

### Junction Temperature
```
Tj = Ta + Pd × Rth(j-a)
Tj = Tc + Pd × Rth(j-c)
Tj(max) = 150°C (typical for IC regulators)
```

### Minimum Input Voltage
```
Vin(min) = Vo + Vdropout
For 78xx: Vin(min) = Vo + 2V
For LDO: Vin(min) = Vo + 0.3V (typical)
```

### Output Voltage (LM317)
```
Vo = 1.25 × (1 + R2/R1) + Iadj × R2
Vo ≈ 1.25 × (1 + R2/R1) (if Iadj × R2 << 1.25)

Typical Iadj = 50-100 μA
```

### Line Regulation
```
Line Reg = ΔVo / (ΔVin × Vo) × 100% (per V)
Or: Line Reg = ΔVo / ΔVin (mV/V)
```

### Load Regulation
```
Load Reg = (Vo(no-load) - Vo(full-load)) / Vo(full-load) × 100%
Or: Load Reg = ΔVo / ΔIo (mV/A)
```

## 2. SMPS Flyback Converter Formulas

### Output Voltage
```
Vo = Vin × (N2/N1) × D/(1-D)

Vo/Vin = (N2/N1) × D/(1-D)
D = 1 / (1 + (N1/N2) × (Vin/Vo))
```

### Magnetizing Inductance
```
Lm = Vin² × D² / (2 × Pin × fsw)   [for DCM]

Or:
Lm = Vin × D / (ΔIL × fsw)   [for CCM]
```

### Output Capacitor
```
C = Io × D / (ΔVo × fsw)
```

### Primary Switch Stress
```
VDS(max) = Vin + Vo × (N1/N2)   [reflected voltage]
```

### Output Diode Stress
```
VRRM = Vo + Vin × (N2/N1)
IF(avg) = Io
```

## 3. SMPS Forward Converter Formulas

### Output Voltage
```
Vo = Vin × (N2/N1) × D   [buck-derived]

Vo/Vin = (N2/N1) × D
D = Vo × N1 / (Vin × N2)
```

### Output Inductor
```
L = (Vo × (1-D)) / (ΔIL × fsw)
```

### Output Capacitor
```
C = ΔIL / (8 × fsw × ΔVo)   [with LC filter]
```

### Reset Winding
```
Nreset = Nprimary (typically)
Maximum duty cycle: Dmax = Nreset/(Nreset + Nprimary) = 0.5 (for Nreset = Nprimary)
```

## 4. SMPS Push-Pull Converter Formulas

### Output Voltage
```
Vo = Vin × (N2/N1) × D   [D per switch, 0 to 0.5]

Effective duty cycle: Deff = 2D (each switch)
Vo = Vin × (N2/N1) × Deff/2
```

### Switch Voltage Stress
```
VDS(max) = 2 × Vin   [voltage doubling due to center tap]
```

### Transformer Utilization
```
Higher than forward converter
No reset winding needed
```

## 5. SMPS Half-Bridge Converter Formulas

### Output Voltage
```
Vo = Vin × (N2/N1) × D   [D per switch]

Where Vin is full DC bus voltage
Switch voltage stress = Vin (not 2Vin)
```

### Capacitor Voltage
```
Vc1 = Vc2 = Vin/2 (balanced)
```

### Switch Stress
```
VDS(max) = Vin
```

### Dead Time
```
td > tOFF(switch) + propagation delay
Typical: td = 0.5-2 μs
```

## 6. SMPS Full-Bridge Converter Formulas

### Output Voltage
```
Vo = Vin × (N2/N1) × D   [phase-shifted control]

D = effective duty cycle (0 to 1)
```

### Phase-Shift for ZVS
```
φ = angle between leading and lagging legs
ZVS achieved for: φ > 0
Losses minimized at optimal φ
```

### Switch Stress
```
VDS(max) = Vin
```

## 7. SMPS Efficiency Formulas

### Total Losses
```
Ploss = Pcond + Pswitching + Pcore + Pdriver

Pcond = I² × Rds(on) × D
Psw = 0.5 × V × I × (tON + tOFF) × fsw
Pcore = core loss from datasheet (at fsw, Bmax)
Pdriver = Qg × Vgs × fsw
```

### Transformer Losses
```
Pcu = I² × Rac (copper loss)
Pcore = Kh × f × Bmax^n × Ve (Steinmetz equation)

Kh, n = core material constants
Ve = effective core volume
```

### Output Capacitor Loss
```
Pcap = I²rms × ESR
```

### Overall Efficiency
```
η = Po / (Po + Ploss)
Typical SMPS: 85-95%
```

## 8. 78xx Regulator Formulas

### Output Voltage
```
Vo = 78xx value (fixed)
Vo = 5V (7805), 12V (7812), 15V (7815)
```

### Power Dissipation
```
Pd = (Vin - Vo) × Io + Vin × Iq
```

### Maximum Load Current
```
Io(max) = (Tj(max) - Ta) / (Rth(j-a) × (Vin - Vo)) - Iq

For TO-220 with heatsink:
Rth(j-a) = Rth(j-c) + Rth(c-s) + Rth(s-a)
```

### Input Capacitor (Minimum)
```
Cin ≥ 0.33 μF (ceramic) for stability
Cin ≥ 1 μF (tantalum) for better performance
```

### Output Capacitor
```
Cout ≥ 0.1 μF (ceramic) for stability
Cout ≥ 10 μF (electrolytic) for load transient
```

## 9. LDO Formulas

### Output Voltage
```
Fixed LDO: Vo = rated value
Adjustable LDO: Vo = Vref × (1 + R2/R1) + Iadj × R2
Vref ≈ 1.25V (typical)
```

### Efficiency
```
η = Vo/Vin (ignoring Iq)
η = Vo/(Vo + Vdropout) (at minimum Vin)
```

### PSRR
```
PSRR = 20 × log10(ΔVin/ΔVo) dB

At 120 Hz: 60-80 dB (good)
At 1 MHz: 20-40 dB (reduced)
```

### Output Noise
```
Vn(rms) = 10-100 μVrms (typical)
Vn(peak-peak) = 50-500 μVpp
```

### Capacitor Requirements
```
ESR: 0.01-1 Ω (for stability)
Capacitance: 1-10 μF (ceramic preferred)
Some LDOs require minimum ESR for stability
```

## 10. Ripple Rejection Formulas

### PSRR vs Frequency
```
PSRR(f) ≈ PSRR(120Hz) × (f/f0)^n

Where:
f0 = pole frequency of regulator
n = roll-off rate (-20 dB/decade typical)
```

### Input Capacitor Effect
```
ΔVin(at regulator) = ΔVsource / (1 + jω × Rsource × Cin)

Larger Cin → lower ΔVin at regulator input
```

### Output Ripple (with LDO post-regulator)
```
ΔVo = ΔVin × 10^(-PSRR/20)

Example:
ΔVin = 100 mV, PSRR = 60 dB at ripple frequency
ΔVo = 100 × 10^(-3) = 0.1 mV = 100 μV
```

## 11. Protection Circuit Formulas

### Current Limiting
```
Ilimit = VBE / Rsense   [for basic current limit]
VBE ≈ 0.7V (for silicon transistor)

Example: Rsense = 0.7Ω → Ilimit = 1A
```

### Foldback Current Limiting
```
Isc = Ilim × Vo/(Vo + Vin × k)

Where k = feedback ratio
Provides lower short-circuit current
```

### Thermal Shutdown
```
Tshutdown ≈ 150-175°C (typical)
Hysteresis: 5-10°C (to prevent oscillation)
```

### OVP (Overvoltage Protection)
```
Vtrip = Vz + VBE (zener-based)
Or: Vtrip = Vref × (1 + R1/R2) (resistor divider)
```
