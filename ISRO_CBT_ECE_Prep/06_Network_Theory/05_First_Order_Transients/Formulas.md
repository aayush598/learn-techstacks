# Network Theory - First Order Transients - Formulas

## RC Circuit (Charging)
```
Vc(t) = V(1 - e^(-t/RC))          [capacitor voltage]
i(t) = (V/R)*e^(-t/RC)            [current]
Power: P = V*i = (V^2/R)*e^(-t/RC)
Energy stored: E = (1/2)*C*Vc^2

Time constant: tau = RC
At t = tau: Vc = 0.632*V
At t = 2*tau: Vc = 0.865*V
At t = 3*tau: Vc = 0.950*V
At t = 4*tau: Vc = 0.982*V
At t = 5*tau: Vc = 0.993*V (considered fully charged)
```

## RC Circuit (Discharging)
```
Vc(t) = V0*e^(-t/RC)
i(t) = -(V0/R)*e^(-t/RC)

At t = tau: Vc = 0.368*V0
At t = 5*tau: Vc approximately 0 (considered fully discharged)
```

## RL Circuit (Energizing)
```
i(t) = (V/R)*(1 - e^(-Rt/L))      [inductor current]
VL(t) = V*e^(-Rt/L)                [inductor voltage]
vR(t) = V*(1 - e^(-Rt/L))         [resistor voltage]

Time constant: tau = L/R
At t = tau: i = 0.632*(V/R)
At t = 5*tau: i approximately V/R (steady state)
```

## RL Circuit (De-energizing)
```
i(t) = I0*e^(-Rt/L)               [decaying current]
VL(t) = -I0*R*e^(-Rt/L)           [opposing voltage]
Energy stored: E = (1/2)*L*i^2

At t = tau: i = 0.368*I0
At t = 5*tau: i approximately 0
```

## Universal Formula (First Order)
```
x(t) = x(inf) + [x(0+) - x(inf)]*e^(-t/tau)

where:
  x(0+) = initial value
  x(inf) = final (steady-state) value
  tau = time constant
```

## Quick Reference Table
| Circuit | tau | Charging | Discharging |
|---------|-----|----------|-------------|
| RC | R*C | V(1-e^(-t/tau)) | V*e^(-t/tau) |
| RL | L/R | I(1-e^(-t/tau)) | I*e^(-t/tau) |

## Energy Formulas
```
Capacitor: E = (1/2)*C*V^2 = (1/2)*Q^2/C = (1/2)*Q*V
Inductor:  E = (1/2)*L*I^2
```
