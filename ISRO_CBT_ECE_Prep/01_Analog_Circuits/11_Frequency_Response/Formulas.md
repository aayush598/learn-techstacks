# Frequency Response - Formulas

## Low-Frequency (coupling caps)
```
High-pass pole from input cap:
  f_L1 = 1/(2pi Cin Req_in)
  Req_in = R_s + (R1||R2||r_pi) (source + input resistance)
Output coupling cap:
  f_L2 = 1/(2pi Cout (RC + R_load))
Bypass cap (emitter):
  f_L3 = 1/(2pi Ce Re_eff)
Net fL ~ highest of individual lower poles
```

## High-Frequency (parasitic/Miller)
```
Miller input cap: C_M = Cbc*(1 + Av)  (CE)
f_H ~ 1/(2pi R_eq * C_total)   (single dominant pole approximation)
R_eq = R_s || R_base_input_resistance
Ctotal = C_M + Cin_parasitic
For CS: C_M = Cgd*(1+Av)
```

## Gain-Bandwidth
```
GBW = Av * f_H  (constant for single-pole)
Unity-gain frequency: f_T = GBW
f_H = f_T / Av
```

## -3dB & Decibel
```
-3 dB = 0.707 voltage ratio
20 dB/decade = 6 dB/octave = -20dB per factor-of-10 freq
```

## Multiple Equal Stages
```
Bandwidth of n identical stages:
  f_total = f_single * sqrt(2^(1/n) - 1)
n=2: factor 0.64, n=3: factor 0.51
```

## Op-Amp Closed loop
```
Non-inverting gain Av = 1 + Rf/R1
Closed-loop BW: f_H = GBW/Av
Smaller gain -> higher BW
```

## Dominant Pole approximation
```
If one pole dominates (others >>), 
  approximate as 1st-order: 
  Av(w) = Av0/(1 + jw/w_p)
```

## Phase Margin relation
```
PM = 180deg + Ph(gain crossover)
PM ~ 45-60 deg for stability
Related to damping: zeta ~ PM/100 (approx)
```

## Quick Reference
| Quantity | Formula |
|----------|---------|
| fL (coupling) | 1/(2pi R C) |
| Miller CM | Cbc(1+Av) |
| fH (dominant) | 1/(2pi Req C) |
| GBW | Av*fH |
| n-stage | f*sprt(2^(1/n)-1) |
| -3dB | 0.707 |
