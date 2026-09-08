# Control Systems - Complete Formula Sheet

## Transfer Function
```
G(s) = Output(s)/Input(s) = C(s)/R(s)
Characteristic equation: 1 + G(s)H(s) = 0
```

## Block Diagram
```
Series: G1*G2
Parallel: G1+G2
Feedback: G/(1+GH) [negative], G/(1-GH) [positive]
```

## Routh-Hurwitz
```
For characteristic equation: a0*s^n + a1*s^(n-1) + ... + an = 0
Routh array: first column must have no sign changes for stability
Number of RHP poles = number of sign changes in first column
Special case: row of zeros -> use auxiliary equation
```

## Root Locus
```
Rules:
1. Starts at open-loop poles, ends at open-loop zeros
2. Branches on real axis to left of odd number of poles+zeros
3. Asymptotes: (2k+1)*180/(n-m) for k=0,1,...
4. Centroid: (sum poles - sum zeros)/(n-m)
5. Breakaway: dK/ds = 0 or dG/ds = 0
6. Imaginary axis crossing: use Routh on char eq
```

## Bode Plot
```
Magnitude (dB): 20*log10|G(jw)|
Phase: angle(G(jw))

Pole at origin: -20 dB/dec, -90 degrees
Zero at origin: +20 dB/dec, +90 degrees
Simple pole at w=p: corner freq p, slope -20 dB/dec after p
Simple zero at w=z: corner freq z, slope +20 dB/dec after z
Second order pole: -40 dB/dec after wn, phase -180 degrees
```

## Stability Margins
```
Gain margin: -|G(jw)| at phase crossover (where phase = -180)
Phase margin: 180 + angle(G(jw)) at gain crossover (where |G|=0dB)
Stable system: GM>0dB and PM>0 degrees
Typical good: GM>6dB, PM>30 degrees
```

## State Space
```
dx/dt = A*x + B*u (state equation)
y = C*x + D*u (output equation)
State transition: x(t) = e^(At)*x(0) + integral e^(A(t-tau))*B*u(tau)dtau
Transfer function: G(s) = C*(sI-A)^(-1)*B + D

Controllability: rank[B AB A^2B ... A^(n-1)B] = n
Observability: rank[C^T A^TC^T ... (A^T)^(n-1)C^T] = n
```

## Compensators
```
Lead: Gc = (1+sT)/(1+s*alpha*T), alpha<1
  Phase lead: phi_max = arcsin((1-alpha)/(1+alpha))
  Used to improve phase margin

Lag: Gc = (1+sT)/(1+s*beta*T), beta>1
  Gain improvement at low freq
  Used to improve steady-state accuracy

Lead-Lag: combination of both
```

## PID Control
```
Gc(s) = Kp + Ki/s + Kd*s
= Kp(1 + 1/(Ti*s) + Td*s)

Kp: proportional gain (reduces rise time, increases overshoot)
Ki: integral gain (eliminates steady-state error, increases overshoot)
Td: derivative gain (reduces overshoot, improves stability)

Ziegler-Nichols:
  P:   Kp = 0.5*Ku
  PI:  Kp = 0.45*Ku, Ti = Pu/1.2
  PID: Kp = 0.6*Ku, Ti = Pu/2, Td = Pu/8
  (Ku = ultimate gain, Pu = ultimate period)
```

## Time Domain
```
Type 0: Kv=0, Ka=0, ess=1/(1+Kp)
Type 1: Kv=K, Ka=0, ess=1/Kv
Type 2: Ka=K, ess=1/Ka

Kp = lim G(s) as s->0
Kv = lim s*G(s) as s->0
Ka = lim s^2*G(s) as s->0

Second order:
  wn: natural frequency, zeta: damping ratio
  Rise time: tr approximately 1.8/wn
  Settling time (2%): ts = 4/(zeta*wn)
  Peak time: tp = pi/(wn*sqrt(1-zeta^2))
  Overshoot: Mp = exp(-zeta*pi/sqrt(1-zeta^2))
```
