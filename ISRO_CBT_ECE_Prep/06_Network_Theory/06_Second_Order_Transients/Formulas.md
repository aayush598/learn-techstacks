# Network Theory - Second Order Transients - Formulas

## Series RLC
```
Characteristic: s^2 + 2 alpha s + w0^2 = 0
alpha = R/(2L), w0 = 1/sqrt(LC)
Roots: s = -alpha +- sqrt(alpha^2 - w0^2)
wd = sqrt(w0^2 - alpha^2)
```

## Response Types (Series)
```
Overdamped (alpha > w0):  i(t) = A1 e^s1t + A2 e^s2t
Critically (alpha = w0):  i(t) = (A1 + A2 t) e^-alpha t
Underdamped (alpha < w0): i(t) = e^-alpha t [A1 cos wd t + A2 sin wd t]
```

## Parallel RLC
```
alpha = 1/(2RC)  [different from series!]
w0 = 1/sqrt(LC)
Response same forms as series but different alpha
```

## Damping Ratio
```
zeta = alpha/w0
Overdamped: zeta > 1
Critically:  zeta = 1
Underdamped: zeta < 1
```

## Transient Performance (Underdamped)
```
Peak time: tp = pi/wd
Settling (2%): ts = 4/(zeta w0)
Overshoot: %MP = 100 e^(-pi zeta/sqrt(1-zeta^2))
Rise time: tr ~ 1.8/w0 (approx)
```

## Q and Damping
```
Series Q = w0 L/R = (1/R)sqrt(L/C)
Relation: zeta = 1/(2Q)
Higher Q -> lower damping -> more ringing
```

## Threshold Resistance (Series)
```
Critical: Rc = 2 sqrt(L/C)
R > Rc: overdamped; R < Rc: underdamped
```

## Quick Reference
| Quantity | Formula |
|----------|---------|
| w0 | 1/sqrt(LC) |
| alpha (series) | R/2L |
| alpha (parallel) | 1/2RC |
| wd | sqrt(w0^2 - alpha^2) |
| zeta | alpha/w0 |
| zeta vs Q | 1/(2Q) |
| Overshoot | exp(-pi zeta/sqrt(1-zeta^2)) |
| Settling 2% | 4/(zeta w0) |
| Rc (series) | 2 sqrt(L/C) |
