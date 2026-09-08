# Noise in Communication Systems - Formulas

## Thermal Noise
```
Pn = k T B
Vn = sqrt(4 k T R B)
N0 (one-sided) = k T
N0/2 two-sided
k = 1.38e-23 J/K
kT0 = 4e-21 W/Hz @290K
kT0(dBm) = -174 dBm/Hz
```

## SNR and Eb/N0
```
SNR = Ps/Pn
SNR(dB) = 10 log10(Ps/Pn)
Eb/N0 = SNR * (B/Rb)  (B = bandwidth, Rb = bit rate)
Eb/N0(dB) = SNR(dB) + 10 log10(B/Rb)
```

## Noise Figure
```
F = SNRi/SNRo = (1) for ideal
NF(dB) = 10 log10 F
Te = (F-1) T0, T0 = 290 K
F = 1 + Te/T0
```

## Friis Cascade Formula
```
F_total = F1 + (F2-1)/G1 + (F3-1)/(G1 G2) + ...
All LINEAR (not dB)
If G1 >> F2: F_total ~ F1 (first stage dominant)
```

## Receiver Sensitivity
```
P_min = k T B F (SNR_min)
P_min(dBm) = -174 + 10 log10(B) + NF + SNR_min(dB)
Example: B=10kHz, NF=3dB, SNR=10dB
  P_min = -174 + 40 + 3 + 10 = -121 dBm
```

## Noise Addition
```
Two uncorrelated: N_total = N1 + N2 (power sum)
Equal noises: +3 dB
Noise voltages (uncorrelated): V_total = sqrt(V1^2+V2^2)
```

## Common PSD Values
```
Thermal @290K: -174 dBm/Hz
@300K: ~-174 dBm/Hz (close)
Antenna noise, sky noise: varies with frequency/elevation
```

## Quick Reference
| Value | Formula |
|-------|---------|
| Pn | kTB |
| Vn | sqrt(4kTRB) |
| N0 | kT |
| noise floor | -174 dBm/Hz |
| F | SNRi/SNRo |
| ND(dB) | 10log10 F |
| Te | (F-1)T0 |
| cascade | F1+(F2-1)/G1+... |
| Eb/N0 | SNR*(B/Rb) |
