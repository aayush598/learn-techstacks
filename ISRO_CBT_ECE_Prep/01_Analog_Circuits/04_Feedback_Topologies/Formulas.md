# Feedback Topologies - Formulas

## Universal Feedback Formula

```
Closed-loop gain: Af = A / (1 + A*beta)
where A = open-loop gain, beta = feedback fraction
T = A*beta = loop gain
D = 1 + A*beta = desensitivity factor
```

---

## Voltage Series Feedback
```
Af = A / (1 + A*beta)
Zif = Zi * (1 + A*beta)  [Input impedance increases]
Zof = Zo / (1 + A*beta)  [Output impedance decreases]
BWf = BW * (1 + A*beta)  [Bandwidth increases]
```

For non-inverting op-amp:
```
beta = R1 / (R1 + R2)
Af = 1 + R2/R1
```

## Voltage Shunt Feedback
```
Rmf = Rm / (1 + Rm*Gf)
Zif = Zi / (1 + Rm*Gf)  [Input impedance decreases]
Zof = Zo / (1 + Rm*Gf)  [Output impedance decreases]
```

## Current Series Feedback
```
Gmf = Gm / (1 + Gm*Rf)
Zif = Zi * (1 + Gm*Rf)  [Input impedance increases]
Zof = Zo * (1 + Gm*Rf)  [Output impedance increases]
```

## Current Shunt Feedback
```
Af = Ai / (1 + Ai*beta)
Zif = Zi / (1 + Ai*beta)  [Input impedance decreases]
Zof = Zo * (1 + Ai*beta)  [Output impedance increases]
```

---

## Key Relationships
```
Af * beta = A*beta / (1 + A*beta) < 1 (for negative feedback)
Af approaches 1/beta when A*beta >> 1 (ideal case)
Gain reduction = Bandwidth increase (constant GBW product)
```

---

## ISRO Quick Reference
- For op-amp: 1/beta = 1 + Rf/Rin (non-inverting)
- Feedback does NOT affect: input bias current, offset voltage (only reduces by D factor)
- Stability condition: Loop gain |A*beta| < 1 at 0 degrees phase
- If A*beta = -1 (positive feedback): Oscillation (Barkhausen criterion)
