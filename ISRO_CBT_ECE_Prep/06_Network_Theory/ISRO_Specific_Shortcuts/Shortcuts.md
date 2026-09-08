# Network Theory - Quick Solving Shortcuts

## Initial Conditions at t=0+
```
Capacitor: Vc(0+) = Vc(0-) (voltage cannot change instantaneously)
Inductor: iL(0+) = iL(0-) (current cannot change instantaneously)
Capacitor at t=0+: acts as VOLTAGE SOURCE (Vc(0-))
Inductor at t=0+: acts as CURRENT SOURCE (iL(0-))
Capacitor at t=infinity (DC): OPEN CIRCUIT
Inductor at t=infinity (DC): SHORT CIRCUIT
```

## Thevenin/Norton Quick Method
```
Vth = Open circuit voltage at terminals
Rth = Look-in resistance (sources set to zero)
  Voltage source -> short circuit
  Current source -> open circuit
Rth = Vth/Isc (alternative method)
Norton: In = Vth/Rth, Rn = Rth
```

## RLC Resonance Quick Formulas
```
Series resonance: f0 = 1/(2*pi*sqrt(LC))
  Z_min = R (minimum impedance)
  Q = (1/R)*sqrt(L/C) = w0*L/R = 1/(w0*R*C)
  BW = f0/Q = R/(2*pi*L)

Parallel resonance: f0 = 1/(2*pi*sqrt(LC))
  Z_max = R*Q^2 = L/(R*C) (maximum impedance)
  Q = R*sqrt(C/L) = R/(w0*L)
  BW = f0/Q = 1/(2*pi*R*C)
```

## Mason's Gain Formula
```
T = Sum(Tk * Delta_k) / Delta

Delta = 1 - (sum of all loop gains) + (sum of products of 2 non-touching loops)
       - (sum of products of 3 non-touching loops) + ...
Delta_k = Delta with loops touching forward path k removed
Tk = gain of kth forward path
```

## Maximum Power Transfer
```
For variable load RL:
  Maximum power when RL = Rth (Thevenin resistance)
  Pmax = Vth^2 / (4*Rth)

For variable source impedance (Zs):
  Maximum power when Zs = ZL* (conjugate matching)
  Zs = Rs - jXs when ZL = Rs + jXs
```

## Two-Port Network Quick Reference
```
Z-parameters: V = Z*I
Y-parameters: I = Y*V
ABCD: |V1|   |A  B| |V2|
      |I1| = |C  D| |-I2|
h-parameters: V1 = h11*I1 + h12*V2
               I2 = h21*I1 + h22*V2

For reciprocal: Z12=Z21, Y12=Y21, AD-BC=1, h12=-h21
```

## Superposition Quick Application
```
1. Turn off all sources except one
2. Voltage source -> short circuit
3. Current source -> open circuit
4. Solve for response from each source
5. Add all responses (algebraic sum)
```

## Quick Reference
| Concept | Quick Formula |
|---------|--------------|
| Time constant (RC) | tau = R*C |
| Time constant (RL) | tau = L/R |
| Series resonance | Z_min = R, Q = w0*L/R |
| Parallel resonance | Z_max = L/(R*C), Q = R/(w0*L) |
| Thevenin | Vth = V_OC, Rth = R looking in |
| Max power (resistive) | RL = Rth, Pmax = Vth^2/(4Rth) |
| Mason's gain | T = Sum(Tk*Delta_k)/Delta |
