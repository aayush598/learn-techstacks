# Network Theory - KCL, KVL and Basic Laws - Concepts

## Ohm's Law
```
V = I*R
P = V*I = I^2 R = V^2/R
Sign convention: current flows from higher to lower potential
```

## Kirchhoff's Current Law (KCL)
```
Sum of currents entering a node = Sum of currents leaving
Algebraic sum of currents at any node = 0
Based on: conservation of charge
Applies at node/junction
```

## Kirchhoff's Voltage Law (KVL)
```
Sum of voltages around any closed loop = 0
Algebraic sum of voltage rises = drops
Based on: conservation of energy
Applies around loop/mesh
```

## Sign Convention (Passive sign)
- Element absorbing power: current enters + terminal
- Element supplying power: current exits + terminal
- Passive element: P > 0 (absorbs)
- Active element (source): P < 0 (supplies)

## Power
```
Total power absorbed = Total power supplied (conservation)
Sum of power in circuit = 0
```

## Elements
```
Resistor: V = IR (linear)
Inductor: V = L di/dt
Capacitor: I = C dV/dt
Independent sources: fixed V or I regardless of load
Dependent sources:
  VCCS: output current proportional to control voltage
  VCVS: output voltage proportional to control voltage
  CCCS, CCVS: controlled by control current
```

## Series & Parallel
```
Series resistors: Req = R1+R2+...
  Same current, voltage divides
Parallel resistors: 1/Req = 1/R1 + 1/R2 +...
  Same voltage, current divides
Two parallel: Req = R1*R2/(R1+R2)
Voltage divider: Vk = Vtotal * Rk/(sum R)
Current divider: Ik = Itotal * Rtotal_par/Rk
```

## Source Combinations
```
Series voltage sources: add (same polarity), subtract (opposite)
Parallel voltage sources: NOT allowed unless equal voltage
Series current sources: NOT allowed unless equal
Parallel current sources: add
```

## Delta-Wye (Star) Transformation
```
Delta(Y): R_ab = Ra+Rb + (Ra Rb)/Rc
Y(Delta): Ra = R_ab R_ca/(R_ab+R_bc+R_ca)
```
Balanced: R_delta = 3*R_y, R_y = R_delta/3

## Linearity & Superposition
- KCL/KVL are linear
- Voltage/current obey superposition
- Response to sum of inputs = sum of responses

---

## ISRO Key Points
- KCL: sum in = sum out at node
- KVL: sum voltage = 0 around loop
- Balanced delta-y: 3x relation
- Two parallel: product/sum
- Conservation of power always
