# Op-Amp Basics - Formulas

## 1. Ideal Op-Amp Rules (Foundation)

```
Rule 1: V+ = V-        (Virtual Short)
Rule 2: I+ = I- = 0    (Infinite Input Impedance)
Rule 3: V_out = A_OL(V+ - V-)  where A_OL → ∞
```

**When to use**: Any circuit with negative feedback where output is NOT saturated.

---

## 2. Input Bias Current Formulas

```
I_B = (I_B+ + I_B-) / 2        [Average bias current]
I_OS = |I_B+ - I_B-|           [Offset current]

Output offset due to I_B:
V_out(I_B) = I_B × R_comp × (1 + Rf/R1)

Where:
  R_comp = compensation resistor at non-inverting input
  R_comp ideally = R1 || Rf = (R1 × Rf)/(R1 + Rf)
```

**ISRO Quick Check**: If R_comp = R1 || Rf, then bias current effects cancel.

---

## 3. Input Offset Voltage Formulas

```
V_out(offset) due to V_OS:
V_out = V_OS × (1 + Rf/R1)     [Non-inverting configuration]

Temperature drift:
V_OS(T) = V_OS(T0) + TC_V_OS × (T - T0)

Where:
  TC_V_OS = temperature coefficient (μV/°C)
  T0 = reference temperature (25°C)
```

---

## 4. CMRR Formulas

```
CMRR = A_d / A_cm              [Linear ratio]
CMRR(dB) = 20 log₁₀(A_d/A_cm) [In decibels]

Output common-mode error:
V_out(cm) = V_cm / CMRR × (1 + Rf/R1)

Common-mode input range:
V_cm(max) = min(V+ supply, V_out_max) - V_OS
V_cm(min) = max(V- supply, V_out_min) + V_OS
```

**Quick Reference**:
| CMRR(dB) | Linear Ratio |
|----------|--------------|
| 60 dB | 1000 |
| 80 dB | 10,000 |
| 100 dB | 100,000 |

---

## 5. Slew Rate Formulas

```
SR = (dV_out/dt)_max           [V/μs]

For sinusoidal output V = V_p sin(2πft):
Required SR = 2π × f × V_p

Maximum frequency for given V_p:
f_max = SR / (2π × V_p)

Maximum output swing for given f:
V_p(max) = SR / (2π × f)

Full-Power Bandwidth:
FPBW = SR / (2π × V_p(max))
```

### Slew Rate Examples
```
741 op-amp: SR = 0.5 V/μs
At f = 100 kHz, max V_p = 0.5/(2π×10⁵) = 0.796 V
At V_p = 5V, max f = 0.5/(2π×5) = 15.9 kHz
```

---

## 6. Gain-Bandwidth Product Formulas

```
GBW = A_CL × BW = constant

Where:
  A_CL = closed-loop voltage gain
  BW = closed-loop bandwidth (-3dB)

Open-loop:
A_OL(f) = A_OL(0) / √(1 + (f/f_3dB)²)
A_OL(f) ≈ GBW/f  (when f >> f_3dB)

Closed-loop bandwidth:
BW_CL = GBW / A_CL

Unity gain frequency:
f_T = GBW (for 741, f_T = 1 MHz)
```

### GBW Quick Reference (741)
```
Gain = 1:    BW = 1 MHz
Gain = 10:   BW = 100 kHz
Gain = 100:  BW = 10 kHz
Gain = 1000: BW = 1 kHz
```

---

## 7. Noise Formulas

```
Total input noise voltage:
V_n(total) = √(V_n² + V_n_R²)

Thermal noise:
V_n_R = √(4kTRΔf)

Where:
  k = 1.38 × 10⁻²³ J/K
  T = temperature (Kelvin)
  R = resistance (Ω)
  Δf = bandwidth (Hz)
```

---

## 8. Power Supply Rejection Ratio

```
PSRR = ΔV_OS / ΔV_supply

In dB:
PSRR(dB) = 20 log₁₀(ΔV_supply/ΔV_OS)

Output error due to supply ripple:
V_out(ripple) = V_ripple/PSRR × (1 + Rf/R1)
```

---

## 9. Output Voltage Swing

```
For ±15V supply (741):
V_out(max) ≈ +13V to +14V
V_out(min) ≈ -13V to -14V

For single supply (0V to 5V):
V_out(max) ≈ 3.5V to 4V
V_out(min) ≈ 0.5V to 1V
```

---

## 10. Settling Time

```
t_s = time for output to settle within specified accuracy (ε)
after a step input

For first-order system:
t_s ≈ -ln(ε) / (2π × BW)

Typical values:
  0.1% settling: t_s ≈ 7/(2π×BW)
  0.01% settling: t_s ≈ 9/(2π×BW)
```

---

## 11. Channel Separation / Crosstalk

```
Channel separation (dB):
CS = 20 log₁₀(V_out(ch1)/V_in(ch2))

Typical: CS > 100 dB for good isolation
```

---

## 12. Key Parameter Relationships

```
GBW = A_OL(0) × f_3dB(open-loop)

SR = I_tail / C_comp
Where:
  I_tail = tail current of differential pair
  C_comp = compensation capacitor

Slew rate and bandwidth:
SR ≥ 2π × f × V_p(max)  [for undistorted output]

Output impedance with feedback:
Z_out(CL) = Z_out(OL) / (1 + A_OL × β)

Input impedance with feedback (series):
Z_in(CL) = Z_in(OL) × (1 + A_OL × β)
```

---

## 13. ISRO Formula Quick Sheet

### Most Used in ISRO
```
1. Virtual ground: V- = V+ = 0V (when V+ grounded)
2. GBW = Gain × Bandwidth = constant
3. SR = 2πfV_p
4. V_out(offset) = V_OS × (1 + Rf/R1)
5. CMRR(dB) = 20log(A_d/A_cm)
6. BW_CL = GBW / A_CL
7. R_comp = R1 || Rf (for bias current compensation)
```

### Units to Remember
```
SR: V/μs (not V/s!)
GBW: Hz
CMRR: dB or dimensionless
V_OS: μV or mV
I_B: nA or pA
```

### ISRO Common Traps
```
1. SR formula uses V_p (peak), not V_pp or V_rms
2. GBW is for CLOSED-LOOP, not open-loop at a frequency
3. Virtual ground fails at saturation
4. CMRR is for differential amplifier, not single input
5. R_comp goes to non-inverting input, NOT inverting
```
