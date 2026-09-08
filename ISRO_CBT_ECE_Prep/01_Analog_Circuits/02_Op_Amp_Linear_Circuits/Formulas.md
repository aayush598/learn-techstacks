# Op-Amp Linear Circuits - Formulas

## Inverting Amplifier

### Voltage Gain
```
Av = Vout/Vin = -Rf/R1
```

### Output Voltage
```
Vout = -(Rf/R1) × Vin
```

### Input Impedance
```
Zin = R1
```

### Output Impedance
```
Zout = Zol/(1 + AOL×β)
where β = R1/(R1 + Rf)
```

### Bandwidth
```
fcl = GBP/|Av| = GBP × R1/Rf
```

## Non-Inverting Amplifier

### Voltage Gain
```
Av = Vout/Vin = 1 + Rf/R1 = 1/(β)
where β = R1/(R1 + Rf)
```

### Output Voltage
```
Vout = (1 + Rf/R1) × Vin
```

### Input Impedance
```
Zin = Zol × (1 + AOL×β) ≈ infinite
```

### Output Impedance
```
Zout = Zol/(1 + AOL×β)
```

## Unity Gain Buffer (Voltage Follower)

### Voltage Gain
```
Av = 1
```

### Input Impedance
```
Zin = Zol × (1 + AOL) ≈ infinite
```

### Output Impedance
```
Zout = Zol/(1 + AOL) ≈ 0
```

## Summing Amplifier (Inverting)

### Two-Input Summing
```
Vout = -(Rf/R1 × V1 + Rf/R2 × V2)
```

### General N-Input Summing
```
Vout = -∑(Rf/Rn × Vn) for n inputs
```

### Equal Weight Summing (R1 = R2 = ... = Rn = R)
```
Vout = -(Rf/R) × (V1 + V2 + ... + Vn)
```

### Averaging Circuit (Rf = R)
```
Vout = -(V1 + V2 + ... + Vn)/N when Rf = R and all input R equal
```

## Difference Amplifier

### General Output
```
Vout = V2 × (R4/(R3+R4)) × (1 + R2/R1) - V1 × (R2/R1)
```

### Balanced Difference (R2/R1 = R4/R3)
```
Vout = (R2/R1) × (V2 - V1)
```

### Unity Gain Difference (R1 = R2 = R3 = R4)
```
Vout = V2 - V1
```

### Common-Mode Rejection
```
CMRR = |Ad/Ac|
Ad = differential gain = R2/R1 (when balanced)
Ac = common-mode gain (ideally zero)
```

## T-Network Feedback

### Equivalent Feedback Resistance
```
Req = R2 + R4 + (R2 × R4/R3)
```

### Inverting Amplifier Gain with T-Network
```
Av = -Req/R1 = -(R2 + R4 + R2×R4/R3)/R1
```

### High Gain Approximation (R4 >> R2, R3 small)
```
Av ≈ -(R2 × R4)/(R1 × R3)
```

## Current-to-Voltage Converter (Transimpedance)

### Output Voltage
```
Vout = -If × Rf
```

### Transimpedance Gain
```
Gm = Vout/If = -Rf (in ohms)
```

### Bandwidth
```
fcl = GBP/(1 + Rf/Rs)
where Rs = source resistance
```

## Voltage-to-Current Converter

### Floating Load
```
Iout = Vin/R1
```

### Howland Current Pump
```
Iout = Vin/R (when bridge is balanced: R2/R1 = R4/R3)
```

### Load Voltage Range
```
VLmax = Vsat - Iout × R
VLmin = -Vsat + Iout × R
```

## Integrator

### Output Voltage
```
Vout = -(1/R1C) × ∫₀ᵗ Vin(τ) dτ + Vout(0)
```

### Frequency Response (S-domain)
```
Vout/Vin = -1/(sR1C)
```

### Unity Gain Frequency
```
f0 = 1/(2πR1C)
```

### Slew Rate Limitation
```
SR ≥ |dVout/dt|max
```

## Differentiator

### Output Voltage
```
Vout = -RfC × dVin/dt
```

### Frequency Response (S-domain)
```
Vout/Vin = -sRfC
```

### High-Frequency Gain Limit (with series resistor Rs)
```
Av(max) = -Rf/(Rs) (at high frequencies)
```

## General Op-Amp Formulas

### Closed-Loop Bandwidth
```
fcl = GBP/(1 + AOL×β) ≈ GBP×β for large AOL
```

### Gain-Bandwidth Product
```
GBP = Av × BW = constant (for voltage feedback op-amps)
```

### Slew Rate
```
SR = 2π × f × Vpeak (max output swing)
```

### Full-Power Bandwidth
```
fp = SR/(2π × Vpeak)
```

### Input Offset Voltage Effect
```
Vout(error) = Vos × (1 + Rf/R1) for inverting config
Vout(error) = Vos × (1 + Rf/R1) for non-inverting config
```

### Input Bias Current Effect
```
Vout(error) = Ib × Rf (inverting configuration, when R1 << Rf)
```

### Noise Gain
```
Av(noise) = 1 + Rf/R1 (same for inverting and non-inverting)
```

## ISRO Quick Reference Formulas

### Gain Magnitude Comparison
```
|Av(inverting)| = Rf/R1
|Av(non-inverting)| = 1 + Rf/R1
Non-inverting gain is always 1 more than inverting gain magnitude
```

### Input Resistance Matching
```
For inverting amp: Zin = R1
For non-inverting amp: Zin → ∞
Buffer provides highest input impedance
```

### Power Bandwidth
```
fp(max) = SR/(2π × Vom)
where Vom = maximum output voltage amplitude
```

### Cascaded Stages
```
Total Av = Av1 × Av2 × Av3 × ...
Total BW ≈ BW1/√(2^(1/n) - 1) for n identical stages
```

### Decibel Conversion
```
Av(dB) = 20 × log₁₀(|Av|)
Power gain(dB) = 10 × log₁₀(Gp)
```
