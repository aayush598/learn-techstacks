# Op-Amp Non-Linear Circuits - Formulas

## Basic Comparator

### Output State
```
Vout = +Vsat when V+ > V-
Vout = -Vsat when V+ < V-
```

### Inverting Comparator (Reference at V+)
```
Vout = +Vsat when Vin < Vref
Vout = -Vsat when Vin > Vref
```

### Non-Inverting Comparator (Reference at V-)
```
Vout = +Vsat when Vin > Vref
Vout = -Vsat when Vin < Vref
```

### Propagation Delay
```
tpd = time from input crossing to output switching
tpd typically 100ns to 1μs (general purpose)
```

## Zero-Crossing Detector

### Inverting Configuration
```
Vout = +Vsat when Vin < 0
Vout = -Vsat when Vin > 0
```

### Non-Inverting Configuration
```
Vout = +Vsat when Vin > 0
Vout = -Vsat when Vin < 0
```

### Frequency Measurement
```
f = 1/T where T = time between consecutive zero crossings
For sine wave: 2 zero crossings per cycle
```

## Schmitt Trigger (Inverting)

### Upper Threshold Point (UTP)
```
UTP = +Vsat × R1/(R1 + R2)
```

### Lower Threshold Point (LTP)
```
LTP = -Vsat × R1/(R1 + R2)
```

### Hysteresis Width
```
H = UTP - LTP = 2 × Vsat × R1/(R1 + R2)
```

### Input Must Satisfy
```
To switch from -Vsat to +Vsat: Vin > UTP
To switch from +Vsat to -Vsat: Vin < LTP
```

### Example Calculation
```
Given: Vsat = 10V, R1 = 10kΩ, R2 = 40kΩ
UTP = 10 × 10/(10+40) = 2V
LTP = -10 × 10/(10+40) = -2V
H = 2 - (-2) = 4V
```

## Schmitt Trigger (Non-Inverting)

### Threshold Points
```
UTP = Vsat × R2/(R1+R2) + Vref × R1/(R1+R2)
LTP = -Vsat × R2/(R1+R2) + Vref × R1/(R1+R2)
```

### Hysteresis Width
```
H = UTP - LTP = 2 × Vsat × R2/(R1+R2)
```

### Note: Different resistor roles
```
Non-inverting: H = 2 × Vsat × R2/(R1+R2)
Inverting: H = 2 × Vsat × R1/(R1+R2)
```

## Window Comparator

### Detection Conditions
```
Output LOW (within window): VrefLow < Vin < VrefHigh
Output HIGH (outside window): Vin < VrefLow OR Vin > VrefHigh
```

### Window Width
```
W = VrefHigh - VrefLow
```

### Center Voltage
```
Vcenter = (VrefHigh + VrefLow)/2
```

### With Logic Gate (AND)
```
Vout = (Comp1_output) AND (Comp2_output)
Comp1: Vin > VrefLow → Output HIGH
Comp2: Vin < VrefHigh → Output HIGH
Vout HIGH only when both conditions met
```

## Triangular Wave Generator

### Using Integrator + Schmitt Trigger
```
Slope of ramp = ±Vsat/(R×C)
Frequency = R2/(4×R1×R×C) for symmetric supply
Period T = 4×R1×R×C/R2
```

### Output Amplitude
```
Vpeak = ±Vsat × R1/(R1+R2) = ±UTP
```

## Square Wave Generator (Astable Multivibrator)

### Using Op-Amp as Comparator
```
Frequency = 1/(2×R×C×ln(1 + 2×R1/R2))
For R1 = R2: f = 1/(2×R×C×ln(3)) ≈ 1/(2.2×R×C)
```

### Duty Cycle
```
D = (R_a)/(R_a + R_b) × 100% for asymmetric timing
For symmetric: D = 50%
```

## Monostable Multivibrator (One-Shot)

### Pulse Width
```
tp = R×C×ln(2) ≈ 0.693×R×C
```

### Trigger Requirements
```
Trigger pulse width < tp (output pulse width)
Trigger must be applied to correct input
```

## Sample-and-Hold Parameters

### Acquisition Time
```
tac = Ron × C × ln(Vin/(Vin - Vhold_error))
For 0.1% accuracy: tac ≈ 7×Ron×C
```

### Hold Droop Rate
```
Droop = Ileak/C (V/second)
Where Ileak = capacitor leakage + op-amp input bias current
```

### Feedthrough
```
Vft = Vin × Cgd/(C + Cgd)
Where Cgd = gate-drain capacitance of switch
```

## Analog Switch Specifications

### On-Resistance
```
Ron = 50Ω to 1kΩ (typical for CMOS)
Ron平坦度 = variation over signal range
```

### Off-Isolation
```
OI = 20 × log₁₀(Vin/Vout_off) dB
Typical OI > 60 dB
```

### Charge Injection
```
Qinj = Cox × W × L × ΔVclock
Voltage error = Qinj/Csample
```

## Noise Immunity Calculations

### Required Hysteresis for Noise
```
H > 2 × Vnoise_peak for reliable operation
H > 3 × Vnoise_rms for 99.7% confidence
```

### Signal-to-Noise Considerations
```
SNR_required = 20 × log₁₀(Vsignal/Vnoise)
Hysteresis should be > noise amplitude
```

## ISRO Quick Reference Formulas

### Schmitt Trigger Threshold Summary
```
Inverting: UTP = +Vsat × R1/(R1+R2)
Inverting: LTP = -Vsat × R1/(R1+R2)
Non-inverting: UTP = Vsat × R2/(R1+R2) [with Vin=0]
Non-inverting: LTP = -Vsat × R2/(R1+R2) [with Vin=0]
```

### Window Comparator States
```
Vin < VrefLow: Output A HIGH, Output B LOW
VrefLow < Vin < VrefHigh: Both outputs HIGH
Vin > VrefHigh: Output A LOW, Output B HIGH
```

### Time Constant Relationships
```
RC time constant τ = R × C
Charging: V(t) = Vmax(1 - e^(-t/τ))
Discharging: V(t) = Vmax × e^(-t/τ)
```

### Comparator Response Time Effect
```
Maximum input frequency ≈ 0.35/tpd
Where tpd = propagation delay
```
