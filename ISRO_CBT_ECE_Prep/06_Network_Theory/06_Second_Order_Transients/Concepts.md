# Network Theory - Second Order Transients - Concepts

## Series RLC
```
L d2i/dt2 + R di/dt + (1/C)i = source
Characteristic equation: s^2 + (R/L)s + 1/(LC) = 0
Damping factor (alpha): R/2L
Undamped natural freq (w0): 1/sqrt(LC)
```

## Response Types (Series RLC)
```
Damping ratio: zeta = alpha/w0 = R/(2L)*sqrt(LC) = R/(2*sqrt(L/C))

1. Overdamped (zeta > 1, R > 2 sqrt(L/C)):
   - Real distinct poles
   - i(t) = A1 e^(s1 t) + A2 e^(s2 t)

2. Critically damped (zeta = 1, R = 2 sqrt(L/C)):
   - Real repeated poles
   - i(t) = (A1 + A2 t) e^(-alpha t)

3. Underdamped (zeta < 1, R < 2 sqrt(L/C)):
   - Complex conjugate poles
   - i(t) = e^(-alpha t)[A1 cos(wd t) + A2 sin(wd t)]
   - wd = sqrt(w0^2 - alpha^2) (damped frequency)
```

## Key Frequencies
```
w0 = 1/sqrt(LC)  (undamped natural frequency)
alpha = R/(2L)   (damping coefficient)
wd = sqrt(w0^2 - alpha^2)  (damped natural freq)
alpha_d = wd/w0 = damped ratio
```

## Resistance Thresholds
```
Critical resistance: Rc = 2*sqrt(L/C)
  R > Rc: overdamped
  R = Rc: critically damped
  R < Rc: underdamped
```

## Energy and Q
```
Q at resonance = (1/R)*sqrt(L/C) = w0*L/R
Higher R -> lower Q -> more damping (in series)
```

## Parallel RLC
```
Damping: alpha = 1/(2RC)
w0 = 1/sqrt(LC)
Critical: Rc = sqrt(L/C)/2 = (1/2)*sqrt(L/C)
Higher R -> higher Q -> less damping (in parallel)
```

## Settling/Peak Time
```
For underdamped 2nd order:
  Peak time: tp = pi/wd
  Settling time: ts ~ 4/(zeta*w0) (2% criterion)
  Overshoot: Mp = e^(-pi zeta / sqrt(1-zeta^2))
Underdamped responses overshoot; overdamped don't
```

---

## ISRO Key Points
- R > 2 sqrt(L/C): overdamped (series)
- w0 = 1/sqrt(LC), alpha = R/2L
- Underdamped has ringing/overshoot
- Critical damping avoids overshoot (fastest settle without oscillation)
- Parallel RLC has different alpha (1/2RC)
