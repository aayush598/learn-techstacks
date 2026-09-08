# ISRO Analog Circuits - Quick Solving Shortcuts

## Op-Amp Shortcuts
```
Virtual Ground: V+ = V- (no current into input terminals)
Inverting Gain: Av = -Rf/R1
Non-Inverting Gain: Av = 1 + Rf/R1
Summing Amp: Vo = -(Rf/R1)(V1+V2+...+Vn)
Difference Amp: Vo = (Rf/R1)(V2-V1) when Rf/R1 ratio matched
Slew Rate: SR = 2*pi*f*Vpeak_max
GBW = Gain * Bandwidth (constant for voltage feedback op-amps)
```

## Schmitt Trigger Shortcuts
```
UTP = +Vsat * R1/(R1+R2)
LTP = -Vsat * R1/(R1+R2)
Hysteresis = UTP - LTP = 2*Vsat*R1/(R1+R2)
```

## Power Amplifier Quick Formulas
```
Class A max eta = 25% (resistive), 50% (transformer)
Class B max eta = pi/4 = 78.5%
Class AB: between 25% and 78.5%
Class C: >80%
Class D: >90% (switching)
```

## Oscillator Quick Formulas
```
Wien Bridge: f = 1/(2*pi*RC), gain needed >= 3
RC Phase Shift: f = 1/(2*pi*RC*sqrt(6)), gain needed >= 29
Colpitts: f = 1/(2*pi*sqrt(L*Ceq)), Ceq = C1*C2/(C1+C2)
Hartley: f = 1/(2*pi*sqrt(C*Leq)), Leq = L1+L2+2M
```

## Diode Circuit Shortcuts
```
Ideal diode: Short (ON) or Open (OFF)
Si diode: 0.7V drop when ON
Ge diode: 0.3V drop when ON
Zener: Acts as voltage source Vz when reverse biased beyond Vz
Full-wave rectifier: Vdc = 2*Vm/pi = 0.636*Vm
Half-wave: Vdc = Vm/pi = 0.318*Vm
Ripple factor (FW with C filter): rf = 1/(4*sqrt(3)*f*C*Rl)
```

## Frequency Response Shortcuts
```
Gain-Bandwidth Product: GBW = Aol * BWol = Af * BWf
Miller capacitance: CM = C*(1-Av) for inverting
Upper cutoff: fH = 1/(2*pi* Rin*Cin) (dominant pole)
```

## Filter Quick Formulas
```
Butterworth: |H(jw)| = 1/sqrt(1+(w/wc)^(2n))
Sallen-Key LPF cutoff: fc = 1/(2*pi*sqrt(R1*R2*C1*C2))
For equal components: fc = 1/(2*pi*R*C)
```
