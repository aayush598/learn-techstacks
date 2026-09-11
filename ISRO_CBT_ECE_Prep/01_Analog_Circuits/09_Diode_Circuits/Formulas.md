# Diode Circuits - Formulas

## Diode Equation
```
I = Is (e^(V/(nVT)) - 1)
VT = kT/q ≈ 26 mV (300K)
Approx: for VB > 4VT, I ≈ Is e^(V/nVT)
```

## Rectifiers
```
Half-wave: V_dc = Vm/pi = 0.318 Vm
Full-wave: V_dc = 2Vm/pi = 0.637 Vm
  (Vm = peak)
Peak with diode drop V_gamma:
  Half-wave: V_dc = (Vm - V_gamma)/pi
  Full-wave bridge: V_dc = (Vm - 2V_gamma) * 2/pi (two diodes in path)
```

## PIV (Peak Inverse Voltage)
```
Half-wave: PIV = Vm
Center-tap full wave: PIV = 2Vm
Bridge: PIV = Vm
```

## Ripple Factor
```
r = V_ripple(rms) / V_dc
Half-wave: r = 1.21
Full-wave: r = 0.48
(r = sqrt(Form factor^2 - 1))
```

## With Capacitor Filter (full wave)
```
V_r(pp) ≈ Idc/(f C)      (f = 2*line for full wave)
Ripple factor ≈ 1/(4 sqrt(3) f R C)  (full wave)
Higher RC -> lower ripple (longer discharge)
```

## Efficiency of Rectifier
```
Half-wave: eta = 40.6% (max)
Full-wave: eta = 81.2% (max)
eta = P_dc/(P_dc + P_ac_ripple)
```

## Clampers
```
Output DC shift = ±Vm (level shift)
Clamper adds/subtracts capacitor voltage to signal
```

## Zener Regulator
```
V_out = V_z (constant in breakdown)
I_z = (V_in - V_z)/R - I_L
Series R limits input current:
  R = (V_in - V_z)/I_z(max)
Line regulation: ΔVz/ΔVin
```

## Ideal vs Practical
```
Ideal diode V=0 forward, all current
Practical: Vf = V_gamma forward
Reverse: negligible except Zener (Vz) and maximum PIV
```

## Quick Reference
| Quantity | Half | Full |
|----------|------|------|
| Vdc | Vm/pi | 2Vm/pi |
| Ripple (no filter) | 1.21 | 0.48 |
| PIV (bridge/ct) | Vm / - | -/2Vm |
| Eta max | 40.6% | 81.2% |
| Output freq | f | 2f |
