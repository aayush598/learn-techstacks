# Analog Circuits - Complete Formula Sheet

## Op-Amp Formulas
```
Inverting:         Av = -Rf/R1
Non-Inverting:     Av = 1 + Rf/R1
Summing:           Vo = -(Rf/R1)(V1+V2+...+Vn)
Difference:        Vo = (Rf/R1)(V2-V1)
Voltage Follower:  Av = 1
T-Network:         Av = -(R2+R3+R2*R3/R1)/R1

Slew Rate:         SR = 2*pi*f*Vpeak (V/s)
GBW Product:       GBW = |Av|*BW = constant
CMRR:              CMRR = Ad/Acd (dB = 20*log10(CMRR))
```

## Feedback Formulas
```
Closed-loop gain:  Af = A/(1+A*beta)
Desensitivity:     D = 1+A*beta
Zif = Zi*D (series input), Zif = Zi/D (shunt input)
Zof = Zo/D (voltage output), Zof = Zo*D (current output)
BWf = BW*D (bandwidth increases)
```

## Schmitt Trigger
```
UTP = +Vsat*R1/(R1+R2)
LTP = -Vsat*R1/(R1+R2)
VH = UTP - LTP = 2*Vsat*R1/(R1+R2)
```

## Power Amplifiers
```
Class A (resistive):  eta_max = 25%
Class A (transformer): eta_max = 50%
Class B:              eta_max = pi/4 = 78.5%
Class C:              eta_max > 80%
Class D:              eta_max > 90%
```

## Oscillators
```
Wien Bridge:     f = 1/(2*pi*R*C), gain >= 3
RC Phase Shift:  f = 1/(2*pi*R*C*sqrt(6)), gain >= 29
Colpitts:        f = 1/(2*pi*sqrt(L*Ceq)), Ceq = C1*C2/(C1+C2)
Hartley:         f = 1/(2*pi*sqrt(C*Leq)), Leq = L1+L2+2M
Crystal:         f approximately fs = 1/(2*pi*sqrt(L*C))
```

## Diode Circuits
```
Si diode drop: 0.7V, Ge: 0.3V
Zener: Vz = constant when reverse biased
Half-wave rectifier:   Vdc = Vm/pi = 0.318*Vm
Full-wave rectifier:   Vdc = 2*Vm/pi = 0.636*Vm
Bridge rectifier:      Vdc = 2*Vm/pi = 0.636*Vm
Ripple (C filter):     rf = 1/(4*sqrt(3)*f*C*Rl) [full-wave]
Peak inverse voltage:  PIV = 2*Vm (full-wave), Vm (half-wave)
```

## Filters
```
Active LPF cutoff:  fc = 1/(2*pi*R*C) (1st order)
Sallen-Key:        fc = 1/(2*pi*sqrt(R1*R2*C1*C2))
Butterworth:       |H(jw)| = 1/sqrt(1+(w/wc)^(2n))
3dB bandwidth:     BW = fc (cutoff frequency)
```

## BJT/MOSFET Quick
```
BJT: Ic = beta*Ib, Ie = (beta+1)*Ib
     alpha = beta/(beta+1), beta = alpha/(1-alpha)
     gm = Ic/Vt (Vt = 26mV at room temp)
     rpi = beta/gm = Vt/Ib
     ro = Va/Ic (Early effect)

MOSFET (saturation): Id = (1/2)*kn*(Vgs-Vt)^2*(1+lambda*Vds)
     gm = kn*(Vgs-Vt) = sqrt(2*kn*Id)
     rds = 1/(lambda*Id)
```
