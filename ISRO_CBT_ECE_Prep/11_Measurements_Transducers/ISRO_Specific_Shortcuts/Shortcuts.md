# ISRO CBT ECE - Measurements & Transducers Shortcuts

## Quick Reference for 4 Questions (~5% weightage)

### 1. Voltmeter Loading (MOST LIKELY)
```
Loading Error(%) = Rth/(Rth + Rv) x 100
Rv = Sensitivity x V_range
Minimum Sens: S_min = Rs(1/error - 1)/V_range
```

### 2. Bridge Balance
```
Wheatstone: R1 x R4 = R2 x R3
Maxwell: Lx = R2 x R3 x C4
Schering: Cx = C2 x (R4/R3), D = w x C4 x R4
Wien freq: f = 1/(2pRC)
```

### 3. LVDT
```
Output: E_out = Sensitivity x displacement
Sensitivity: mV/mm (typ 40-100 mV/mm/V)
Null: E_out = 0 at center
Phase reversal: indicates direction
```

### 4. Strain Gauge
```
GF = (dR/R) / epsilon
Quarter bridge: Vout = Vs/4 x GF x epsilon
Dummy gauge: temperature compensation
```

### 5. Temperature
```
Pt100: R = 100(1 + 0.00385 x T)
NTC: R = R0 x exp[B(1/T - 1/T0)]
Thermocouple: V = S x dT
LM35: V = 10 mV/degC
```

### 6. PMMC
```
Shunt: Rsh = Rm/(n-1), n = I/Im
Multiplier: Rs = Rm(V/Vm - 1)
Sensitivity: S = 1/Ifs (ohm/V)
Scale: Linear (radial field)
```

### 7. ADC/DVM
```
Dual slope: n = (Vin/Vref) x N
Successive approx: t = n x Tclk
Resolution: Range/(10^n - 1)
3.5 digit max: 1999
```

### 8. CRO
```
Rise time: tr = 0.35/BW
Lissajous: fy/fx = Nh/Nv
Phase: phi = arcsin(a/b)
```

### 9. Flow Measurement
```
Venturi: Q = Cd x At x sqrt(2dP/(rho(1-beta^4)))
Pitot: v = sqrt(2 x dP/rho)
Orifice: lower Cd (0.6-0.65) than Venturi
```

### 10. DAQ
```
Nyquist: fs >= 2 x fmax
SNR = 6.02n + 1.76 dB
Anti-alias filter: BEFORE ADC
QE = +/- 1/2 LSB
```

## Speed Solving Tricks
1. **Loading error**: If Rv > 100 x Rs, error < 1% (skip calculation)
2. **Shunt**: n = I/Im, then Rsh = Rm/(n-1)
3. **Pt100**: Every 1 degC = 0.385 ohm change
4. **LVDT**: Sensitivity x displacement = output (direct multiply)
5. **Bridge balance**: Cross-multiply opposite arms
6. **Rise time x Bandwidth = 0.35** (always)
7. **SNR per bit = 6 dB** (quick approximation)
