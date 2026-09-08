# Network Theory - Complete Formula Sheet

## KCL and KVL
```
KCL: Sum of currents entering a node = Sum of currents leaving
     (algebraic sum of currents at any node = 0)
KVL: Sum of voltage drops around any loop = 0
```

## Thevenin/Norton
```
Vth = Open circuit voltage
Rth = Vth/Isc (or turn off sources, find R looking in)
Norton: In = Vth/Rth, Rn = Rth
Maximum power: Pmax = Vth^2/(4*Rth) when RL = Rth
```

## Transient Analysis
```
RC: tau = RC
  Charging: Vc = V(1-e^(-t/tau))
  Discharging: Vc = V0*e^(-t/tau)

RL: tau = L/R
  Energizing: i = (V/R)(1-e^(-t/tau))
  De-energizing: i = I0*e^(-t/tau)

Universal: x(t) = x(inf) + [x(0+)-x(inf)]*e^(-t/tau)

Initial conditions:
  C: Vc(0+) = Vc(0-)
  L: iL(0+) = iL(0-)
  At DC steady state: C = open, L = short
```

## Second Order (RLC)
```
Series RLC:
  Characteristic eq: s^2 + (R/L)s + 1/(LC) = 0
  Alpha: alpha = R/(2L) [neper frequency]
  Omega_0: omega_0 = 1/sqrt(LC) [resonant freq]
  Overdamped: alpha > omega_0 (two real roots)
  Underdamped: alpha < omega_0 (complex roots)
  Critically damped: alpha = omega_0

Parallel RLC:
  Alpha: alpha = 1/(2RC)
  Omega_0: omega_0 = 1/sqrt(LC)
  Same damping conditions
```

## RLC Resonance
```
Series resonance:
  f0 = 1/(2*pi*sqrt(LC))
  Z_min = R
  Q = (1/R)*sqrt(L/C) = w0*L/R
  BW = f0/Q = R/(2*pi*L)

Parallel resonance:
  f0 = 1/(2*pi*sqrt(LC))
  Z_max = L/(R*C) = Q^2*R
  Q = R*sqrt(C/L) = R/(w0*L)
  BW = f0/Q = 1/(2*pi*R*C)
```

## Mason's Gain Formula
```
T = Sum(Tk * Delta_k) / Delta
Delta = 1 - (sum loop gains) + (sum 2 non-touching) - (sum 3 non-touching) + ...
Delta_k = Delta without loops touching path k
```

## Two-Port Networks
```
Z: V1=z11*I1+z12*I2, V2=z21*I1+z22*I2
Y: I1=y11*V1+y12*V2, I2=y21*V1+y22*V2
ABCD: V1=A*V2-B*I2, I1=C*V2-D*I2
h: V1=h11*I1+h12*V2, I2=h21*I1+h22*V2

Reciprocal: z12=z21, y12=y21, AD-BC=1, h12=-h21
Cascade: ABCD_total = ABCD_1 * ABCD_2
```

## Driving Point Impedance
```
Foster form I: Series combination of series LC circuits
Foster form II: Parallel combination of parallel LC circuits
Cauer form I: Continued fraction with L and C elements
Cauer form II: Continued fraction starting from lowest degree
```
