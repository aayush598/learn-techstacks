# Network Theory - First Order Transients - Concepts

## RC Circuit (Charging)
- When switch closes at t=0 with voltage source V through R to capacitor C
- Vc(t) = V(1 - e^(-t/RC))
- i(t) = (V/R)*e^(-t/RC)
- Time constant: tau = RC
- At t = tau: Vc = 0.632*V (63.2% charged)
- At t = 5*tau: Vc approximately V (fully charged, 99.3%)

## RC Circuit (Discharging)
- Capacitor with initial voltage V0 discharges through R
- Vc(t) = V0*e^(-t/RC)
- i(t) = -(V0/R)*e^(-t/RC) (negative = discharging)
- At t = tau: Vc = 0.368*V0 (36.8% remaining)

## RL Circuit (Energizing)
- When switch closes with voltage V through R and L
- i(t) = (V/R)*(1 - e^(-Rt/L))
- VL(t) = V*e^(-Rt/L)
- Time constant: tau = L/R
- At t = tau: i = 0.632*(V/R) (63.2% of final current)
- At t = 5*tau: i approximately V/R (steady state)

## RL Circuit (De-energizing)
- Current through L decays when source removed
- i(t) = I0*e^(-Rt/L) where I0 = initial current
- VL(t) = -L*(dI/dt) = I0*R*e^(-Rt/L)

## Key Initial Condition Rules
```
At t = 0-: Circuit in steady state before switching
At t = 0+: 
  Capacitor voltage = Vc(0-) (continuity)
  Inductor current = iL(0-) (continuity)
At t = infinity: 
  Capacitor = open circuit (DC steady state)
  Inductor = short circuit (DC steady state)
```

## ISRO Key Points
- tau = RC for RC circuits, tau = L/R for RL circuits
- 5*tau = settling time (99% complete)
- Capacitor acts as voltage source at t=0+
- Inductor acts as current source at t=0+
- At DC steady state: C = open, L = short
