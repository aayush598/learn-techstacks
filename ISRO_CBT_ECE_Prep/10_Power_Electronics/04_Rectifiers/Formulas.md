# Rectifiers - Formulas

## 1. Half-Wave Rectifier Formulas

### With Diode (Resistive Load)
```
Vdc = Vm/π = 0.318 Vm   [average output voltage]
Vrms = Vm/2 = 0.5 Vm    [RMS output voltage]
Idc = Vm/(πRL)           [average load current]
Irms = Vm/(2RL)          [RMS load current]
```

### Performance Parameters
```
FF = Vrms/Vdc = (Vm/2)/(Vm/π) = π/2 = 1.57
RF = √(FF² - 1) = √(1.57² - 1) = 1.21 (121%)
η = (Vdc/Vrms)² = (2/π)² = 0.406 (40.6%)
TUF = 0.287
CF = Ipeak/Ilrms = 2
PIV = Vm (diode reverse voltage)
```

### With SCR (Phase Control)
```
Vdc = Vm/(2π) × (1 + cos α)
Vrms = Vm/2 × √((1/π)(π - α + sin(2α)/2))
Idc = Vdc/RL
Irms = Vrms/RL

At α = 0°: Vdc = Vm/π (maximum)
At α = 90°: Vdc = Vm/(2π)
At α = 180°: Vdc = 0
```

## 2. Full-Wave Center Tap Rectifier Formulas

### With Diodes (Resistive Load)
```
Vdc = 2Vm/π = 0.636 Vm
Vrms = Vm/√2 = 0.707 Vm
Idc = 2Vm/(πRL)
Irms = Vm/(√2 × RL)
```

### Performance Parameters
```
FF = Vrms/Vdc = (Vm/√2)/(2Vm/π) = π/(2√2) = 1.11
RF = √(1.11² - 1) = 0.482 (48.2%)
η = (2√2/π)² = 0.812 (81.2%)
TUF = 0.693
CF = √2 = 1.414
PIV = 2Vm (each diode)
```

### With SCRs (Phase Control)
```
Vdc = Vm/π × (1 + cos α)
Vrms = Vm/√2 × √((1/π)(π - α + sin(2α)/2))

At α = 0°: Vdc = 2Vm/π
At α = 90°: Vdc = Vm/π
At α = 180°: Vdc = 0
```

## 3. Single-Phase Full-Bridge Rectifier Formulas

### With Diodes (Resistive Load)
```
Vdc = 2Vm/π = 0.636 Vm
Vrms = Vm/√2 = 0.707 Vm
Idc = 2Vm/(πRL)
Irms = Vm/(√2 × RL)
```

### Performance Parameters
```
FF = 1.11
RF = 0.482 (48.2%)
η = 0.812 (81.2%)
TUF = 0.812
CF = √2 = 1.414
PIV = Vm (each diode)
```

### With SCRs (Fully Controlled Bridge)
```
Vdc = 2Vm/π × cos α    [for α = 0° to π, resistive load]
Vrms = Vm/√2 × √((1/π)(π - α + sin(2α)/2))

For inductive load (continuous conduction):
Vdc = 2Vm/π × cos α    [α = 0° to π]
At α = 0°: Vdc = 2Vm/π (maximum)
At α = 90°: Vdc = 0
At α > 90°: Vdc negative (inverter mode, without FD)
```

### With Semi-Converter Bridge
```
Vdc = Vm/π × (1 + cos α)
α range: 0° to 180°
Lower harmonics than fully controlled bridge
Vrms = Vm/√2 × √((1/2π)(2π - 2α + sin(2α)))
```

## 4. Three-Phase Rectifier Formulas

### Three-Phase Half-Wave
```
Vdc = (3√3 × Vm_phase)/(2π) × cos α   [with SCR]
Vdc = (3√3 × Vm_phase)/(2π)            [with diode, α=0°]
Vdc = (3 × Vml)/(2π) × cos α           [Vml = √3 × Vm_phase]

Vrms = Vm_phase × √((3/4π)(2π/3 + √3/2))

FF = 1.0198
RF = 0.183 (18.3%)
η = 0.9689 (96.89%)
TUF = 0.675
PIV = √3 × Vm_phase = Vml
```

### Three-Phase Full-Bridge (6-Pulse)
```
Vdc = (3Vml/π) × cos α   [with SCR]
Vdc = (3Vml/π)            [with diode, α=0°]

Where Vml = √3 × Vm_phase = line-to-line peak voltage
Vml = √2 × VL(rms) = √2 × √3 × Vphase(rms)

Vrms = Vml × √((1/2) + (3√3)/(4π))   [approximately]
Vrms ≈ Vdc × 1.0009

FF = 1.0009
RF = 0.04 (4%)
η = 0.9998 (99.98%)
TUF = 0.955
PIV = Vml = √2 × VL(rms)
Output ripple frequency = 6 × supply frequency
```

### For 50 Hz supply:
```
Single-phase full-wave: ripple = 100 Hz
Three-phase half-wave: ripple = 150 Hz
Three-phase full-wave: ripple = 300 Hz
```

## 5. Freewheeling Diode Formulas

### Effect on Fully Controlled Bridge
```
Without FD: Vdc = (2Vm/π) × cos α
With FD:    Vdc = (Vm/π) × (1 + cos α)

At α = 60°:
Without FD: Vdc = (2Vm/π) × 0.5 = Vm/π
With FD:    Vdc = (Vm/π) × 1.5 = 1.5Vm/π

FD improves Vdc for α > 0°
```

### Conduction Angle of FD
```
δFD = α   [approximate for continuous conduction]
FD conducts when output voltage tries to go negative
FD current: IFD = IL × δFD/(2π)
```

### Power Factor Improvement
```
Without FD: PF = 0.9 × cos α (approximately)
With FD:    PF ≈ 0.95 (for same α)

FD reduces input current distortion
```

## 6. Filter Design Formulas

### Capacitor Filter (Full-Wave)
```
C = Iload / (2f × ΔV)

Where:
Iload = load current (A)
f = supply frequency (Hz)
ΔV = peak-to-peak ripple voltage (V)

Example: Iload = 1A, f = 50 Hz, ΔV = 2V
C = 1 / (2 × 50 × 2) = 5000 μF
```

### Ripple Voltage
```
ΔV = Iload / (2fC)        [full-wave with C filter]
ΔV = Vdc / (2f × C × RL)  [alternative form]
ΔVripple(%) = (ΔV/Vdc) × 100%
```

### Time Constant Requirement
```
τ = RL × C >> T = 1/(2f)

Rule of thumb: τ > 5T for good filtering
C > 5T/RL = 5/(2f × RL)
```

### Peak Diode Current (with C filter)
```
ID(peak) = Iload × (1 + 2π√(RL/(2f×C)))   [approximate]
ID(peak) >> Iload   [due to capacitor charging pulse]

For heavy filtering: ID(peak) = 3-5 × Iload
```

### LC Filter
```
For LC filter:
Vripple = Vdc × (1/(12√2 × f² × L × C))

L should be: L > RL/3 for good current smoothing
C can be smaller than C-only filter
```

## 7. Useful Relationships

### Voltage Conversion Ratios
```
Half-wave:          Vdc/Vm = 1/π = 0.318
Full-wave center:   Vdc/Vm = 2/π = 0.636
Full-wave bridge:   Vdc/Vm = 2/π = 0.636
Three-phase half:   Vdc/Vm_phase = 3√3/(2π) = 0.827
Three-phase full:   Vdc/Vm_phase = 3√3/π = 1.654
Three-phase full:   Vdc/Vml = 3/π = 0.955
```

### PIV Relationships
```
Half-wave:          PIV = Vm
Full-wave center:   PIV = 2Vm
Full-wave bridge:   PIV = Vm
Three-phase half:   PIV = √3 × Vm_phase = Vml
Three-phase full:   PIV = Vml = √2 × VL(rms)
```

### Firing Angle for Specific Vdc
```
Single-phase half (SCR):  α = cos⁻¹((2π × Vdc/Vm) - 1)
Single-phase full (SCR):  α = cos⁻¹((π × Vdc/(2Vm)) - 1)
Three-phase full (SCR):   α = cos⁻¹((π × Vdc/(3Vml)))
```

### Harmonic Content
```
Single-phase full-wave:
  Vn = 2Vm/(π(n²-1)) for n = 2,4,6,...
  V2 = 2Vm/(3π) (dominant harmonic)
  V4 = 2Vm/(15π)

Three-phase full-wave:
  Vn = 6Vm_phase/(π(n²-1)) for n = 6,12,18,...
  V6 = 6Vm_phase/(35π) (dominant harmonic)
```
